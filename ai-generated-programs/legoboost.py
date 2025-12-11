import time
import threading
import tkinter as tk
from pylgbst import get_connection_auto
from pylgbst.hub import MoveHub
from pylgbst.peripherals import VisionSensor

# Color Mapping: Lego ID -> (Hex Color, Name)
# Note: Colors may vary slightly based on environment/calibration
COLOR_MAP = {
    0: ("#000000", "Black"),
    1: ("#FF69B4", "Pink"),
    2: ("#800080", "Purple"),
    3: ("#0000FF", "Blue"),
    4: ("#00FFFF", "Cyan"),
    5: ("#90EE90", "Light Green"),
    6: ("#008000", "Green"),
    7: ("#FFFF00", "Yellow"),
    8: ("#FFA500", "Orange"),
    9: ("#FF0000", "Red"),
    10: ("#FFFFFF", "White")
}

class LegoColorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lego Boost Color Reader")
        self.root.geometry("400x400")
        
        # Initial UI State
        self.current_bg = "#CCCCCC" # Gray
        self.current_text = "Searching for Hub...\nPress GREEN BUTTON on Hub"
        
        self.label = tk.Label(
            self.root, 
            text=self.current_text, 
            font=("Arial", 24, "bold"),
            bg=self.current_bg,
            fg="black",
            wraplength=350
        )
        self.label.pack(expand=True, fill="both")
        
        self.hub = None
        self.sensor = None
        self.running = True

        # Start the connection process in a separate thread to keep UI responsive
        self.conn_thread = threading.Thread(target=self.connect_to_hub, daemon=True)
        self.conn_thread.start()

        # Build protocol to handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start the regular UI update loop
        self.update_ui_loop()
        
        self.root.mainloop()

    def update_ui_loop(self):
        """Periodically update the UI from the main thread"""
        if not self.running:
            return
            
        self.label.config(bg=self.current_bg, text=self.current_text)
        
        # Decide text color based on background brightness for readability
        # Simple heuristic: if background is black/blue/red/purple, use white text
        bg_hex = self.current_bg
        if bg_hex in ["#000000", "#0000FF", "#800080", "#FF0000", "#008000"]:
            self.label.config(fg="white")
        else:
            self.label.config(fg="black")
            
        self.root.after(100, self.update_ui_loop)

    def on_color_change(self, color_id, distance=None):
        """Callback from pylgbst when sensor data changes"""
        print(f"Sensor Detected ID: {color_id}")
        
        if color_id in COLOR_MAP:
            hex_color, name = COLOR_MAP[color_id]
            self.current_bg = hex_color
            self.current_text = name
        elif color_id is None or color_id == 255:
            # Sometimes 255 or None is sent for "no object/unknown"
            self.current_bg = "#CCCCCC"
            self.current_text = "No Object"
        else:
            self.current_bg = "#CCCCCC"
            self.current_text = f"Unknown ID: {color_id}"

    def connect_to_hub(self):
        try:
            print("Scanning for Lego Move Hub...")
            connection = get_connection_auto()
            self.hub = MoveHub(connection)
            print("Hub Connected!")
            
            # Update UI to show we are looking for the sensor
            self.current_text = "Hub Connected!\nLooking for Color Sensor..."
            self.current_bg = "#DDDDDD"
            
            # Find the Vision Sensor (usually Port C or D)
            # We check attached devices
            target_port = None
            for port in [self.hub.port_C, self.hub.port_D]:
                if isinstance(port, VisionSensor):
                    target_port = port
                    break
            
            if target_port:
                print("Vision Sensor found/verified.")
                self.sensor = target_port
                # Subscribe to color updates
                # callback takes arguments: (color, distance=None) depending on mode
                self.sensor.subscribe(self.on_color_change, mode=VisionSensor.COLOR_INDEX)
                self.current_text = "Sensor Ready!\nShow me a color."
            else:
                self.current_text = "Error:\nNo Color Sensor found on Port C or D"
                
            # Keep thread alive to maintain connection
            while self.running and connection.is_alive():
                time.sleep(1)
                
        except Exception as e:
            print(f"Connection Error: {e}")
            self.current_text = f"Error:\n{str(e)}"

    def on_close(self):
        self.running = False
        if self.hub:
            try:
                # Attempt to disconnect cleanly
                self.hub.connection.disconnect()
            except:
                pass
        self.root.destroy()

if __name__ == "__main__":
    app = LegoColorApp()
