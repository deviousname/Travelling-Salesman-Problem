import random
import math
import tkinter as tk
from tkinter import ttk



class TSPGUI:
    def __init__(self, width=512, height=512, amount_of_cities=16):
        self.width = width
        self.height = height
        self.amount_of_cities = amount_of_cities
        self.points = []
        self.path = []

        # Initialize the main Tkinter window and set its title
        self.root = tk.Tk()
        self.root.title("Travelling Salesman Problem")
        self.root.geometry(f"{self.width}x{self.height}")

        # Create the main frame for the application
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        # Make the mainframe expand with the window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create the canvas for visualizing the path
        self.canvas = tk.Canvas(self.mainframe, bg="white")
        self.canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        # Make the canvas expand with the window
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        # Create a separate frame for the buttons and Spinbox
        self.buttons_frame = ttk.Frame(self.mainframe)
        self.buttons_frame.grid(column=0, row=1, sticky=(tk.W, tk.E))

        # Make the buttons_frame not expand vertically
        self.mainframe.rowconfigure(1, weight=0)

        # Create the "Generate New Path" button
        self.generate_button = ttk.Button(
            self.buttons_frame, text="Generate New Path", command=self.generate_and_draw
        )
        self.generate_button.grid(column=0, row=0, padx=5, pady=5)

        # Create the "Amount of Cities" label and Spinbox
        self.amount_of_cities_label = ttk.Label(
            self.buttons_frame, text="Amount of Cities:"
        )
        self.amount_of_cities_label.grid(column=1, row=0, padx=5, pady=5)

        self.amount_of_cities_var = tk.IntVar()
        self.amount_of_cities_var.set(self.amount_of_cities)
        self.amount_of_cities_spinbox = ttk.Spinbox(
            self.buttons_frame,
            from_=3,
            to=1000,
            textvariable=self.amount_of_cities_var,
            command=self.generate_and_draw,
        )
        self.amount_of_cities_spinbox.grid(column=2, row=0, padx=5, pady=5)

        # Bind the on_resize function to the Configure event
        self.root.bind("<Configure>", self.on_resize)

        # Generate the initial path and start the main Tkinter event loop
        self.generate_and_draw()
        self.root.mainloop()

    def distance(self, p1, p2):
        """Calculate the Euclidean distance between two points."""
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def generate_points(self, n):
        """Generate n random points within the specified width and height."""
        points = []
        for i in range(n):
            points.append((random.randint(0, self.width), random.randint(0, self.height)))
        return points

    def generate_path(self, points):
        """Create a random path that visits all points."""
        path = []
        for i in range(len(points)):
            path.append(i)
        random.shuffle(path)
        return path

    def path_length(self, path, points):
        """Calculate the total length of a path."""
        length = 0
        for i in range(len(path) - 1):
            length += self.distance(points[path[i]], points[path[i + 1]])
        length += self.distance(points[path[0]], points[path[-1]])
        return length

    def swap(self, path, i, j):
        """Swap two elements of a path."""
        temp = path[i]
        path[i] = path[j]
        path[j] = temp

    def two_opt(self, path, points):
        """Perform the 2-opt optimization on a given path."""
        best_path = path[:]
        best_length = self.path_length(path, points)
        for i in range(len(path) - 1):
            for j in range(i + 1, len(path)):
                self.swap(path, i, j)
                length = self.path_length(path, points)
                if length < best_length:
                    best_path = path[:]
                    best_length = length
                self.swap(path, i, j)
        return best_path

    def draw_path(self, points, path):
        """Draw the path on the canvas."""
        self.canvas.delete("all")
        for i in range(len(path) - 1):
            self.canvas.create_line(points[path[i]], points[path[i + 1]])
        self.canvas.create_line(points[path[0]], points[path[-1]])

    def generate_and_draw(self):
        """Generate a new path and draw it on the canvas."""
        self.amount_of_cities = self.amount_of_cities_var.get()
        self.points = self.generate_points(self.amount_of_cities)
        self.path = self.generate_path(self.points)
        self.path = self.two_opt(self.path, self.points)
        self.draw_path(self.points, self.path)

    def on_resize(self, event):
        """Handle window resizing."""
        self.width = self.mainframe.winfo_width()
        self.height = self.mainframe.winfo_height() - self.generate_button.winfo_height()
        self.canvas.config(width=self.width, height=self.height)
        self.draw_path(self.points, self.path)

if __name__ == "__main__":
    app = TSPGUI()
