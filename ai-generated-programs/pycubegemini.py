import tkinter as tk
import math

class Cube3D:
    """
    Manages the 3D geometry, rotation, and projection of the Rubik's Cube model.
    The cube consists of 54 individual sticker objects (9 per face).
    """
    def __init__(self, size=3):
        self.size = size
        self.stickers = []
        self.initial_normals = {} # Stores the normal vector for each face (U, D, F, B, L, R)
        
        # Standard Rubik's cube colors (White, Yellow, Red, Orange, Blue, Green)
        # --- MODIFICATION: Swapping Red and Orange ---
        self.face_colors = {
            'U': 'white', 'D': 'yellow',
            'F': 'orange', 'B': 'red', # F is now Orange, B is now Red
            'L': 'blue', 'R': 'green'
        }
        # ---------------------------------------------

        self.init_geometry()
        self.rotation_x = 0.5  # Initial rotation for better viewing
        self.rotation_y = 0.5
        
        # Focal length for perspective projection (Camera position is at Z = FOCAL_DISTANCE)
        self.FOCAL_DISTANCE = 10.0

        # Initializing the current color of each sticker to its face's color
        for sticker in self.stickers:
            sticker['color'] = self.face_colors[sticker['face']]

    def init_geometry(self, s=1.0, g=0.01):
        """
        Creates the 54 sticker faces and their initial 3D vertex coordinates.
        The overall cube will have a side length of 3.0, centered at (0, 0, 0).
        s: Size of a single small cube (1x1x1 unit)
        g: Gap/border size between stickers (used to shrink the sticker)
        """
        
        # Sticker side length (small cube size minus the gap)
        sticker_side_length = s - g 
        h = sticker_side_length / 2 # Half side length of the colored sticker

        # Define 6 face directions (normals)
        face_map = {
            'U': (0, 1, 0), 'D': (0, -1, 0),  # Up, Down (Y-axis)
            'F': (0, 0, 1), 'B': (0, 0, -1),  # Front, Back (Z-axis)
            'L': (-1, 0, 0), 'R': (1, 0, 0)   # Left, Right (X-axis)
        }

        # Store initial normal vectors for backface culling
        self.initial_normals = {
            'U': (0, 1, 0), 'D': (0, -1, 0),
            'F': (0, 0, 1), 'B': (0, 0, -1),
            'L': (-1, 0, 0), 'R': (1, 0, 0)
        }

        # The centers of the small cubes on a face (since s=1.0)
        # For a 3x3 cube centered at 0, the centers are at -1.0, 0.0, and 1.0
        coords = [-1.0, 0.0, 1.0] 
        # The position of the cube face boundary (1.5 for a 3x3 cube)
        face_pos = self.size * s / 2

        # Iterate over all 6 faces
        for face_name, (nx, ny, nz) in face_map.items():
            for i in range(self.size):
                for j in range(self.size):
                    
                    # ox, oy are the center offsets of the small cube face in the plane (e.g., in the YZ plane for the R face)
                    ox = coords[j] 
                    oy = coords[i] 
                    oz = 0 # Local Z is 0 for the sticker plane

                    # Define 4 vertices (in local coordinates)
                    # Vertices are relative to the center of the small cube face (ox, oy)
                    local_verts = [
                        (ox - h, oy - h, oz),
                        (ox + h, oy - h, oz),
                        (ox + h, oy + h, oz),
                        (ox - h, oy + h, oz)
                    ]

                    world_verts = []
                    for vx, vy, vz in local_verts:
                        # Map local face coords (vx, vy) to the final world coords (x, y, z)
                        if face_name in ('F', 'B'):
                            # F/B (Z-normal): X=vx, Y=vy, Z=face_pos * nz
                            final_x = vx
                            final_y = vy
                            final_z = face_pos * nz 
                            center_x, center_y, center_z = ox, oy, final_z
                        elif face_name in ('U', 'D'):
                            # U/D (Y-normal): X=vx, Y=face_pos * ny, Z=vy
                            final_x = vx
                            final_y = face_pos * ny
                            final_z = vy
                            center_x, center_y, center_z = ox, final_y, oy
                        elif face_name in ('L', 'R'):
                            # L/R (X-normal): X=face_pos * nx, Y=vy, Z=vx
                            final_x = face_pos * nx
                            final_y = vy
                            final_z = vx
                            center_x, center_y, center_z = final_x, oy, ox
                            
                        world_verts.append((final_x, final_y, final_z))

                    self.stickers.append({
                        'face': face_name,
                        'verts': world_verts,
                        'center': (center_x, center_y, center_z),
                        'color': self.face_colors[face_name], 
                        'normal': self.initial_normals[face_name]
                    })

    def rotate_point(self, p):
        """Applies 3D rotation (Y-axis then X-axis) to a single 3D point (x, y, z)."""
        x, y, z = p
        
        # --- Y-Axis Rotation (Orbit Horizontal) ---
        cos_y = math.cos(self.rotation_y)
        sin_y = math.sin(self.rotation_y)
        x_y = x * cos_y + z * sin_y
        z_y = z * cos_y - x * sin_y
        y_y = y # Y remains unchanged

        # --- X-Axis Rotation (Orbit Vertical) ---
        cos_x = math.cos(self.rotation_x)
        sin_x = math.sin(self.rotation_x)
        x_final = x_y
        y_final = y_y * cos_x - z_y * sin_x
        z_final = y_y * sin_x + z_y * cos_x

        return (x_final, y_final, z_final)

    def project(self, p, canvas_center_x, canvas_center_y, scale=500):
        """
        Projects a 3D point (x, y, z) to 2D screen coordinates (x_s, y_s).
        Uses standard perspective projection: Px = F * (x / (F - z)).
        F is the focal distance.
        """
        x, y, z = p
        
        # **PERSPECTIVE FIX**
        # F - z is the distance from the point to the camera plane.
        # We assume the camera is at (0, 0, self.FOCAL_DISTANCE) looking towards the origin.
        z_distance = self.FOCAL_DISTANCE - z
        
        # Avoid division by zero, although given our geometry it should be safe.
        if z_distance <= 0:
            # If point is behind the camera or on the camera plane, return center
            return (canvas_center_x, canvas_center_y) 
            
        z_factor = self.FOCAL_DISTANCE / z_distance
        
        # Scale (x, y) coordinates by the z_factor and apply general scale
        x_s = x * scale * z_factor + canvas_center_x
        y_s = -y * scale * z_factor + canvas_center_y # Y is inverted on screen
        
        return (x_s, y_s)

    def get_drawn_stickers(self):
        """
        Calculates all sticker positions after rotation and culls backfaces.
        Returns a list of dicts: [{'verts_2d': [...], 'color': '...', 'center_2d': ...]}]
        """
        drawn_stickers = []
        
        # Vector pointing from the rotated center of the cube to the camera position (0, 0, FOCAL_DISTANCE)
        camera_pos = (0, 0, self.FOCAL_DISTANCE) 

        for i, sticker in enumerate(self.stickers):
            # 1. Rotate the initial normal vector
            rotated_normal = self.rotate_point(sticker['normal'])
            rotated_center = self.rotate_point(sticker['center'])
            
            # 2. Backface Culling (Dot product test):
            # If the normal vector points away from the camera, hide it.
            # Vector from face center to camera: Vc = Camera - RotatedCenter
            
            vec_to_camera = (
                camera_pos[0] - rotated_center[0], 
                camera_pos[1] - rotated_center[1], 
                camera_pos[2] - rotated_center[2]
            )
            
            # Dot product: Vc . RotatedNormal
            dot_product = (
                vec_to_camera[0] * rotated_normal[0] +
                vec_to_camera[1] * rotated_normal[1] +
                vec_to_camera[2] * rotated_normal[2]
            )
            
            # Only draw faces where the normal points toward the camera (dot product > 0)
            if dot_product < 0:
                continue # Skip drawing this face (it's hidden)

            # 3. Rotate vertices
            verts_3d_rotated = []
            for vert in sticker['verts']:
                verts_3d_rotated.append(self.rotate_point(vert))

            # Add to the list of visible stickers, keeping 3D data for projection later
            drawn_stickers.append({
                'sticker_index': i,
                'verts_3d': verts_3d_rotated,
                'center_3d': rotated_center,
                'color': sticker['color']
            })
            
        return drawn_stickers


class RubiksCubeApp:
    """The Tkinter application class to handle UI and drawing."""
    def __init__(self, master):
        self.master = master
        master.title("Tkinter 3D Rubik's Cube Viewer")

        self.cube = Cube3D(size=3)
        self.current_color = self.cube.face_colors['U'] # Default to white

        # --- Canvas Setup ---
        self.canvas_width = 600
        self.canvas_height = 600
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='#222222')
        self.canvas.pack(pady=10, padx=10, side=tk.LEFT)

        # --- Control Panel Setup ---
        control_frame = tk.Frame(master, padx=10, pady=10)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(control_frame, text="Current Color:", font=('Arial', 12)).pack(pady=(0, 5))
        self.color_display = tk.Label(control_frame, bg=self.current_color, width=10, height=2, relief=tk.RAISED)
        self.color_display.pack(pady=(0, 15))

        tk.Label(control_frame, text="Color Palette:", font=('Arial', 12, 'bold')).pack(pady=(0, 5))
        
        # --- Color Palette Buttons ---
        self.palette_frame = tk.Frame(control_frame)
        self.palette_frame.pack()
        
        colors = ['white', 'yellow', 'red', 'orange', 'blue', 'green']
        self.color_buttons = {}
        for i, color in enumerate(colors):
            btn = tk.Button(self.palette_frame, text=color.capitalize(), bg=color, width=10, 
                            command=lambda c=color: self.set_color(c))
            btn.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            self.color_buttons[color] = btn

        # --- Solve Button ---
        self.solve_button = tk.Button(control_frame, text="Solve / Check Colors", command=self.solve_cube, 
                                      font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white', relief=tk.RAISED)
        self.solve_button.pack(pady=(20, 10), fill=tk.X)

        # --- Output Display ---
        tk.Label(control_frame, text="Current Face Colors:", font=('Arial', 10)).pack(pady=(5, 0))
        self.output_text = tk.Text(control_frame, height=10, width=30, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.pack()


        # Bind mouse events for camera control and coloring
        self.canvas.bind('<Button-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        
        self.last_x, self.last_y = 0, 0
        self.is_dragging = False # Flag to distinguish drag from click
        
        # Scale for projecting 3D coordinates to 2D canvas pixels
        self.projection_scale = 75 

        self.draw_cube()

    def set_color(self, color):
        """Sets the currently selected color."""
        self.current_color = color
        self.color_display.config(bg=color)
        
    def on_press(self, event):
        """Records the initial click position."""
        self.last_x, self.last_y = event.x, event.y
        self.is_dragging = False

    def on_drag(self, event):
        """Handles mouse drag to rotate the cube."""
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        
        # Only start dragging if movement is significant
        if abs(dx) > 1 or abs(dy) > 1:
            self.is_dragging = True
            
            # Dragging right (positive dx) results in positive rotation_y change
            # Default sensitivity was 200.0
            self.cube.rotation_y += dx / 200.0  # Horizontal drag changes Y-rotation
            # Dragging down (positive dy) results in positive rotation_x change
            self.cube.rotation_x += dy / 200.0  # Vertical drag changes X-rotation
            
            # Clamp X rotation to prevent flipping the view upside down (from vertical orbit)
            self.cube.rotation_x = max(-math.pi / 2.1, min(math.pi / 2.1, self.cube.rotation_x))

            self.last_x, self.last_y = event.x, event.y
            self.draw_cube()

    def on_release(self, event):
        """Handles mouse release, performing a color change if it wasn't a drag."""
        if not self.is_dragging:
            self.handle_click(event.x, event.y)
        self.is_dragging = False
        
    def handle_click(self, click_x, click_y):
        """
        Attempts to identify which sticker was clicked based on proximity to the
        projected center of all visible stickers. Prevents recoloring of center pieces.
        """
        min_dist_sq = float('inf')
        closest_sticker_index = -1
        
        # Redraw the cube to get the latest projected sticker data
        drawn_stickers_info = self.draw_cube()

        for info in drawn_stickers_info:
            center_2d_x, center_2d_y = info['center_2d']
            
            # Calculate distance squared to avoid costly square root
            dist_sq = (click_x - center_2d_x)**2 + (click_y - center_2d_y)**2
            
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_sticker_index = info['sticker_index']
                
        # Indices of the 6 center stickers (U, D, F, B, L, R) based on the order of creation (index 4 for each 9-sticker face)
        CENTER_INDICES = {4, 13, 22, 31, 40, 49}

        # Only change color if the click was close enough, AND it is NOT a center piece
        if closest_sticker_index != -1 and min_dist_sq < 900: # 30*30 = 900 threshold
            if closest_sticker_index not in CENTER_INDICES:
                self.cube.stickers[closest_sticker_index]['color'] = self.current_color
                self.draw_cube()
                
    def solve_cube(self):
        """
        Retrieves the current color of all 54 stickers and formats the state 
        into a single 54-character string using URFDLB order and single-letter codes.
        """
        # 1. Define the required order and color mapping
        # URFDLB order is the standard for solved string notation
        ORDERED_FACES = ['U', 'R', 'F', 'D', 'L', 'B']
        
        # Mapping from full color name to single character (first letter of the color)
        COLOR_CODE_MAP = {
            'white': 'W', 'yellow': 'Y', 'red': 'R', 
            'orange': 'O', 'blue': 'B', 'green': 'G'
        }
        
        # Group stickers by their original face
        face_groups = {face: [] for face in self.cube.face_colors.keys()}
        for sticker in self.cube.stickers:
            face_groups[sticker['face']].append(sticker['color'])

        # 2. Build the final 54-character string
        final_string = ""
        for face_name in ORDERED_FACES:
            # Get the 9 colors for the current face
            colors = face_groups[face_name] 
            # Convert colors to single-character code and concatenate
            face_string = "".join([COLOR_CODE_MAP[color] for color in colors])
            final_string += face_string

        # 3. Update the output display with the new string format
        output_str = f"Cube State String (U=White, R=Green, F=Orange, D=Yellow, L=Blue, B=Red):\n{final_string}"
            
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, output_str)
        self.output_text.config(state=tk.DISABLED)


    def draw_cube(self):
        """
        Clears the canvas, calculates the new 2D positions, and draws the visible stickers.
        Returns the list of drawn stickers info for hit detection.
        """
        self.canvas.delete("all")
        center_x = self.canvas_width / 2
        center_y = self.canvas_height / 2
        
        # Get the list of visible stickers with their 3D rotated coordinates
        visible_stickers = self.cube.get_drawn_stickers()
        
        # List to store 2D projection data for hit detection
        drawn_stickers_info = []

        # Sort stickers by their average Z depth (furthest drawn first)
        visible_stickers.sort(key=lambda s: s['center_3d'][2], reverse=True)

        for sticker_info in visible_stickers:
            verts_3d = sticker_info['verts_3d']
            color = sticker_info['color']
            
            # Project all 4 vertices to 2D
            verts_2d_coords = []
            for v in verts_3d:
                x_s, y_s = self.cube.project(v, center_x, center_y, scale=self.projection_scale)
                verts_2d_coords.extend([x_s, y_s])
            
            # Calculate 2D center for hit detection
            center_x_2d, center_y_2d = self.cube.project(sticker_info['center_3d'], center_x, center_y, scale=self.projection_scale)

            # Draw the polygon on the canvas
            self.canvas.create_polygon(
                verts_2d_coords,
                fill=color,
                outline='black',
                width=2
            )
            
            # Store the 2D center and original index for the hit test
            drawn_stickers_info.append({
                'sticker_index': sticker_info['sticker_index'],
                'center_2d': (center_x_2d, center_y_2d)
            })
            
        return drawn_stickers_info


if __name__ == "__main__":
    # Tkinter boilerplate setup
    root = tk.Tk()
    app = RubiksCubeApp(root)
    root.mainloop()