import tkinter as tk
from tkinter import messagebox
import threading
import logging
import time
import asyncio
import bleak
from bleak import BleakScanner

# Monkeypatch bleak.discover if it's missing (for newer bleak versions)
if not hasattr(bleak, "discover"):
    bleak.discover = BleakScanner.discover

from pylgbst.hub import MoveHub
from pylgbst import get_connection_auto
from pylgbst.peripherals import EncodedMotor, VisionSensor

# Configure logging
logging.basicConfig(level=logging.INFO)

class LegoBoostController:
    def __init__(self, root):
        self.root = root
        self.root.title("LEGO Boost Controller")
        self.root.geometry("400x400")

        self.hub = None
        self.connection_thread = None
        self.is_connecting = False
        self.conn_timeout_id = None
        self.connection_aborted = False
        self.attempt_id = 0

        # Status Label
        self.status_label = tk.Label(root, text="Status: Disconnected", fg="red", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        # Connect Button
        self.connect_btn = tk.Button(root, text="Connect to Hub", command=self.start_connection, height=2, width=20)
        self.connect_btn.pack(pady=5)

        # Controls Frame
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(pady=20)

        # Directional Buttons
        self.btn_forward = tk.Button(self.controls_frame, text="Forward", command=lambda: self.move(1), width=10, height=2)
        self.btn_forward.grid(row=0, column=1, padx=5, pady=5)

        self.btn_left = tk.Button(self.controls_frame, text="Left", command=lambda: self.turn("left"), width=10, height=2)
        self.btn_left.grid(row=1, column=0, padx=5, pady=5)

        self.btn_stop = tk.Button(self.controls_frame, text="STOP", command=self.stop, width=10, height=2, bg="red", fg="white")
        self.btn_stop.grid(row=1, column=1, padx=5, pady=5)

        self.btn_right = tk.Button(self.controls_frame, text="Right", command=lambda: self.turn("right"), width=10, height=2)
        self.btn_right.grid(row=1, column=2, padx=5, pady=5)

        self.btn_backward = tk.Button(self.controls_frame, text="Backward", command=lambda: self.move(-1), width=10, height=2)
        self.btn_backward.grid(row=2, column=1, padx=5, pady=5)

        # Disable controls initially
        self.toggle_controls(tk.DISABLED)

        # Sensor Output
        self.sensor_label = tk.Label(root, text="Color Sensor: -", font=("Helvetica", 12))
        self.sensor_label.pack(pady=20)

    def toggle_controls(self, state):
        for widget in self.controls_frame.winfo_children():
            widget.configure(state=state)

    def start_connection(self):
        if self.hub:
            self.disconnect()
            return

        self.is_connecting = True
        self.connection_aborted = False
        self.attempt_id += 1
        current_attempt = self.attempt_id
        
        # Schedule timeout (15 seconds)
        if self.conn_timeout_id:
            self.root.after_cancel(self.conn_timeout_id)
        self.conn_timeout_id = self.root.after(15000, lambda: self.connection_timeout(current_attempt))
        
        self.connect_btn.config(state=tk.DISABLED, text="Connecting...")
        self.status_label.config(text="Status: Searching for Hub...", fg="orange")
        
        self.connection_thread = threading.Thread(target=lambda: self.connect_hub(current_attempt))
        self.connection_thread.daemon = True
        self.connection_thread.start()

    def connection_timeout(self, attempt_id):
        # Only act if this timeout matches the current attempt
        if self.attempt_id != attempt_id:
            return

        if self.is_connecting:
            self.is_connecting = False
            self.connection_aborted = True
            self.status_label.config(text="Status: Didn't connect. Try again", fg="maroon")
            self.connect_btn.config(state=tk.NORMAL, text="Connect to Hub")
            logging.info(f"Connection attempt {attempt_id} timed out.")

    def connect_hub(self, attempt_id):
        try:
            # Attempt to connect to MoveHub
            # We must provide a name or MAC, otherwise pylgbst raises an AssertionError
            connection = get_connection_auto(hub_name="Move Hub")
            
            # Check if this attempt is still valid (not timed out, not superseded)
            if self.attempt_id != attempt_id or self.connection_aborted:
                logging.info(f"Connection attempt {attempt_id} aborted or superseded. Disconnecting.")
                connection.disconnect()
                return

            self.hub = MoveHub(connection)
            
            # Reset UI in main thread
            self.root.after(0, lambda: self.on_connect_success(attempt_id))
            
            # Subscribe to color sensor if available
            self.setup_sensor()

        except Exception as e:
            if self.attempt_id == attempt_id and not self.connection_aborted:
                logging.error(f"Failed to connect: {e}")
                self.root.after(0, lambda: self.on_connect_fail(str(e), attempt_id))

    def cancel_timeout(self):
        if self.conn_timeout_id:
            self.root.after_cancel(self.conn_timeout_id)
            self.conn_timeout_id = None

    def setup_sensor(self):
        # Look for VisionSensor (Color & Distance Sensor)
        sensor = None
        if isinstance(self.hub.port_C, VisionSensor):
            sensor = self.hub.port_C
        elif isinstance(self.hub.port_D, VisionSensor):
            sensor = self.hub.port_D
            
        if sensor:
            logging.info("Color sensor found")
            sensor.subscribe(self.on_color_change)
        else:
            logging.info("No color sensor found on Port C or D")
            self.root.after(0, lambda: self.sensor_label.config(text="Color Sensor: Not Found"))

    def on_color_change(self, color, distance=None):
        # Update UI with color value
        # Colors: 0: Black, 3: Blue, 5: Green, 7: Yellow, 9: Red, 10: White (approx mapping)
        color_names = {
            0: "Black", 3: "Blue", 5: "Green", 7: "Yellow", 9: "Red", 10: "White"
        }
        name = color_names.get(color, f"Unknown ({color})")
        text = f"Color Sensor: {name}"
        if distance is not None:
            text += f" | Dist: {distance}"
        
        self.root.after(0, lambda: self.sensor_label.config(text=text))

    def on_connect_success(self, attempt_id):
        if self.attempt_id != attempt_id: return
        self.cancel_timeout()
        self.status_label.config(text="Status: Connected", fg="green")
        self.connect_btn.config(state=tk.NORMAL, text="Disconnect")
        self.toggle_controls(tk.NORMAL)
        self.is_connecting = False

    def on_connect_fail(self, error_msg, attempt_id):
        if self.attempt_id != attempt_id: return
        self.cancel_timeout()
        self.status_label.config(text="Status: Connection Failed", fg="red")
        self.connect_btn.config(state=tk.NORMAL, text="Connect to Hub")
        messagebox.showerror("Connection Error", f"Could not connect to Hub:\n{error_msg}")
        self.is_connecting = False
        self.hub = None

    def disconnect(self):
        if self.hub:
            try:
                self.hub.disconnect()
            except:
                pass
            self.hub = None
        
        self.status_label.config(text="Status: Disconnected", fg="red")
        self.connect_btn.config(state=tk.NORMAL, text="Connect to Hub")
        self.toggle_controls(tk.DISABLED)
        self.sensor_label.config(text="Color Sensor: -")

    def move(self, direction):
        if not self.hub: return
        # Move both motors A and B
        # speed is -1 to 1. Direction 1 = forward, -1 = backward
        speed = 0.5 * direction
        self.hub.motor_AB.start_speed(speed)

    def turn(self, side):
        if not self.hub: return
        # Turn by running motors in opposite directions
        if side == "left":
            self.hub.motor_A.start_speed(-0.3)
            self.hub.motor_B.start_speed(0.3)
        else:
            self.hub.motor_A.start_speed(0.3)
            self.hub.motor_B.start_speed(-0.3)

    def stop(self):
        if not self.hub: return
        self.hub.motor_AB.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LegoBoostController(root)
    
    def on_close():
        app.disconnect()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
