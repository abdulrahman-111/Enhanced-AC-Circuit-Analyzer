import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from matplotlib.figure import Figure
import cmath
from collections import defaultdict

class EnhancedACCircuitAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced AC Circuit Analyzer")
        self.root.geometry("1200x800")
        
        # Circuit data storage
        self.components = []  # List of (type, value, node1, node2)
        self.voltage_sources = []  # List of (type, peak, freq, phase, node1, node2)
        self.current_sources = []  # List of (type, peak, freq, phase, node1, node2)
        self.nodes = set()  # Set of node identifiers
        self.next_node_id = 0
        
        # Initialize GUI elements first
        self.create_widgets()
        
        # Then initialize with ground node
        self.add_node("GND")
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Input controls
        left_panel = ttk.Frame(main_frame, width=300, padding="10")
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        # Right panel - Circuit visualization and results
        right_panel = ttk.Frame(main_frame, padding="10")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Notebook for different input tabs
        self.notebook = ttk.Notebook(left_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Initialize all menu variables before creating tabs
        self.component_type = tk.StringVar(value="Resistor")
        self.component_value = tk.DoubleVar(value=1000.0)
        self.node1_var = tk.StringVar()
        self.node2_var = tk.StringVar()
        self.source_type = tk.StringVar(value="Sine")
        self.source_peak = tk.DoubleVar(value=10.0)
        self.source_freq = tk.DoubleVar(value=60.0)
        self.source_phase = tk.DoubleVar(value=0.0)
        self.source_node1_var = tk.StringVar()
        self.source_node2_var = tk.StringVar(value="GND")
        self.current_source_type = tk.StringVar(value="Sine")
        self.current_source_peak = tk.DoubleVar(value=0.1)
        self.current_source_freq = tk.DoubleVar(value=60.0)
        self.current_source_phase = tk.DoubleVar(value=0.0)
        self.current_source_node1_var = tk.StringVar()
        self.current_source_node2_var = tk.StringVar(value="GND")
        self.new_node_name = tk.StringVar()
        
        # Now create tabs
        self.create_component_tab()
        self.create_voltage_source_tab()
        self.create_current_source_tab()
        self.create_node_tab()
        
        # Analysis controls
        self.create_analysis_controls(left_panel)
        
        # Circuit visualization
        self.create_circuit_visualization(right_panel)
        
        # Results display
        self.create_results_display(right_panel)
    
    def create_component_tab(self):
        component_tab = ttk.Frame(self.notebook)
        self.notebook.add(component_tab, text="Components")
        
        # Component type selection
        ttk.Label(component_tab, text="Component Type:").grid(row=0, column=0, sticky=tk.W)
        component_types = ["Resistor", "Capacitor", "Inductor"]
        self.type_menu = ttk.Combobox(component_tab, textvariable=self.component_type, 
                                     values=component_types, state="readonly")
        self.type_menu.grid(row=0, column=1, pady=5, sticky=tk.EW)
        
        # Component value input
        ttk.Label(component_tab, text="Value:").grid(row=1, column=0, sticky=tk.W)
        self.value_entry = ttk.Entry(component_tab, textvariable=self.component_value)
        self.value_entry.grid(row=1, column=1, pady=5, sticky=tk.EW)
        ttk.Label(component_tab, text="Ω for R, μF for C, mH for L").grid(row=2, column=0, columnspan=2, sticky=tk.W)
        
        # Node connections
        ttk.Label(component_tab, text="Node 1:").grid(row=3, column=0, sticky=tk.W)
        self.node1_menu = ttk.Combobox(component_tab, textvariable=self.node1_var, state="readonly")
        self.node1_menu.grid(row=3, column=1, pady=5, sticky=tk.EW)
        
        ttk.Label(component_tab, text="Node 2:").grid(row=4, column=0, sticky=tk.W)
        self.node2_menu = ttk.Combobox(component_tab, textvariable=self.node2_var, state="readonly")
        self.node2_menu.grid(row=4, column=1, pady=5, sticky=tk.EW)
        
        # Add component button
        ttk.Button(component_tab, text="Add Component", command=self.add_component).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Component list
        ttk.Label(component_tab, text="Current Components:").grid(row=6, column=0, columnspan=2, pady=(10,5), sticky=tk.W)
        self.component_listbox = tk.Listbox(component_tab, height=8)
        self.component_listbox.grid(row=7, column=0, columnspan=2, sticky=tk.EW)
        
        # Update node menus
        self.update_node_menus()
    
    def create_voltage_source_tab(self):
        source_tab = ttk.Frame(self.notebook)
        self.notebook.add(source_tab, text="Voltage Sources")
        
        # Source type selection
        ttk.Label(source_tab, text="Waveform:").grid(row=0, column=0, sticky=tk.W)
        source_types = ["Sine", "Square", "Triangle"]
        self.source_type_menu = ttk.Combobox(source_tab, textvariable=self.source_type, 
                                           values=source_types, state="readonly")
        self.source_type_menu.grid(row=0, column=1, pady=5, sticky=tk.EW)
        
        # Peak voltage
        ttk.Label(source_tab, text="Peak Voltage (V):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(source_tab, textvariable=self.source_peak).grid(row=1, column=1, pady=5, sticky=tk.EW)
        
        # Frequency
        ttk.Label(source_tab, text="Frequency (Hz):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(source_tab, textvariable=self.source_freq).grid(row=2, column=1, pady=5, sticky=tk.EW)
        
        # Phase
        ttk.Label(source_tab, text="Phase (degrees):").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(source_tab, textvariable=self.source_phase).grid(row=3, column=1, pady=5, sticky=tk.EW)
        
        # Node connections
        ttk.Label(source_tab, text="Positive Node:").grid(row=4, column=0, sticky=tk.W)
        self.source_node1_menu = ttk.Combobox(source_tab, textvariable=self.source_node1_var, state="readonly")
        self.source_node1_menu.grid(row=4, column=1, pady=5, sticky=tk.EW)
        
        ttk.Label(source_tab, text="Negative Node:").grid(row=5, column=0, sticky=tk.W)
        self.source_node2_menu = ttk.Combobox(source_tab, textvariable=self.source_node2_var, state="readonly")
        self.source_node2_menu.grid(row=5, column=1, pady=5, sticky=tk.EW)
        
        # Add source button
        ttk.Button(source_tab, text="Add Voltage Source", command=self.add_voltage_source).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Source list
        ttk.Label(source_tab, text="Current Sources:").grid(row=7, column=0, columnspan=2, pady=(10,5), sticky=tk.W)
        self.source_listbox = tk.Listbox(source_tab, height=8)
        self.source_listbox.grid(row=8, column=0, columnspan=2, sticky=tk.EW)
        
        # Update node menus
        self.update_node_menus()
    
    def create_current_source_tab(self):
        source_tab = ttk.Frame(self.notebook)
        self.notebook.add(source_tab, text="Current Sources")
        
        # Source type selection
        ttk.Label(source_tab, text="Waveform:").grid(row=0, column=0, sticky=tk.W)
        source_types = ["Sine", "Square", "Triangle"]
        self.current_source_type_menu = ttk.Combobox(source_tab, textvariable=self.current_source_type, 
                                           values=source_types, state="readonly")
        self.current_source_type_menu.grid(row=0, column=1, pady=5, sticky=tk.EW)
        
        # Peak current
        ttk.Label(source_tab, text="Peak Current (A):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(source_tab, textvariable=self.current_source_peak).grid(row=1, column=1, pady=5, sticky=tk.EW)
        
        # Frequency
        ttk.Label(source_tab, text="Frequency (Hz):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(source_tab, textvariable=self.current_source_freq).grid(row=2, column=1, pady=5, sticky=tk.EW)
        
        # Phase
        ttk.Label(source_tab, text="Phase (degrees):").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(source_tab, textvariable=self.current_source_phase).grid(row=3, column=1, pady=5, sticky=tk.EW)
        
        # Node connections
        ttk.Label(source_tab, text="From Node:").grid(row=4, column=0, sticky=tk.W)
        self.current_source_node1_menu = ttk.Combobox(source_tab, textvariable=self.current_source_node1_var, state="readonly")
        self.current_source_node1_menu.grid(row=4, column=1, pady=5, sticky=tk.EW)
        
        ttk.Label(source_tab, text="To Node:").grid(row=5, column=0, sticky=tk.W)
        self.current_source_node2_menu = ttk.Combobox(source_tab, textvariable=self.current_source_node2_var, state="readonly")
        self.current_source_node2_menu.grid(row=5, column=1, pady=5, sticky=tk.EW)
        
        # Add source button
        ttk.Button(source_tab, text="Add Current Source", command=self.add_current_source).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Source list
        ttk.Label(source_tab, text="Current Sources:").grid(row=7, column=0, columnspan=2, pady=(10,5), sticky=tk.W)
        self.current_source_listbox = tk.Listbox(source_tab, height=8)
        self.current_source_listbox.grid(row=8, column=0, columnspan=2, sticky=tk.EW)
        
        # Update node menus
        self.update_node_menus()
    
    def create_node_tab(self):
        node_tab = ttk.Frame(self.notebook)
        self.notebook.add(node_tab, text="Nodes")
        
        # New node name
        ttk.Label(node_tab, text="New Node Name:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(node_tab, textvariable=self.new_node_name).grid(row=0, column=1, pady=5, sticky=tk.EW)
        
        # Add node button
        ttk.Button(node_tab, text="Add Node", command=self.add_node_ui).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Current nodes list
        ttk.Label(node_tab, text="Current Nodes:").grid(row=2, column=0, columnspan=2, pady=(10,5), sticky=tk.W)
        self.node_listbox = tk.Listbox(node_tab, height=10)
        self.node_listbox.grid(row=3, column=0, columnspan=2, sticky=tk.EW)
        
        # Update node list
        self.update_node_list()
    
    def create_analysis_controls(self, parent):
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Analyze button
        ttk.Button(control_frame, text="Analyze Circuit", command=self.analyze_circuit).pack(side=tk.LEFT, padx=5)
        
        # Clear button
        ttk.Button(control_frame, text="Clear Circuit", command=self.clear_circuit).pack(side=tk.LEFT, padx=5)
        
        # Detect series/parallel button
        ttk.Button(control_frame, text="Detect Series/Parallel", command=self.detect_series_parallel).pack(side=tk.LEFT, padx=5)
    
    def create_circuit_visualization(self, parent):
        # Circuit diagram frame
        circuit_frame = ttk.Frame(parent)
        circuit_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(circuit_frame, text="Circuit Diagram:").pack(anchor=tk.W)
        
        # Create matplotlib figure
        self.circuit_fig = Figure(figsize=(8, 4), dpi=100)
        self.circuit_ax = self.circuit_fig.add_subplot(111)
        self.circuit_ax.set_axis_off()
        
        # Create canvas for embedding in Tkinter
        self.circuit_canvas = FigureCanvasTkAgg(self.circuit_fig, master=circuit_frame)
        self.circuit_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Draw initial empty circuit
        self.draw_circuit()
    
    def create_results_display(self, parent):
        # Results frame
        results_frame = ttk.Frame(parent)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(results_frame, text="Analysis Results:").pack(anchor=tk.W)
        
        # Results text area
        self.results_text = tk.Text(results_frame, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
    
    def update_node_menus(self):
        nodes = sorted(self.nodes)
        
        # Only update if the widgets exist
        if hasattr(self, 'node1_menu'):
            self.node1_menu['values'] = nodes
            self.node2_menu['values'] = nodes
        
        if hasattr(self, 'source_node1_menu'):
            self.source_node1_menu['values'] = nodes
            self.source_node2_menu['values'] = nodes
        
        if hasattr(self, 'current_source_node1_menu'):
            self.current_source_node1_menu['values'] = nodes
            self.current_source_node2_menu['values'] = nodes
        
        # Set default values if not set
        if nodes and not self.node1_var.get():
            self.node1_var.set(nodes[0])
            self.node2_var.set("GND")
    
    def update_node_list(self):
        self.node_listbox.delete(0, tk.END)
        for node in sorted(self.nodes):
            self.node_listbox.insert(tk.END, node)
    
    def update_component_list(self):
        self.component_listbox.delete(0, tk.END)
        for i, (c_type, value, node1, node2) in enumerate(self.components):
            display_value = value
            unit = "Ω"
            
            if c_type == "Capacitor":
                display_value = value * 1e6  # F to μF
                unit = "μF"
            elif c_type == "Inductor":
                display_value = value * 1e3  # H to mH
                unit = "mH"
                
            self.component_listbox.insert(tk.END, f"{c_type} {display_value:.2f}{unit} between {node1} and {node2}")
    
    def update_source_list(self):
        self.source_listbox.delete(0, tk.END)
        for i, (s_type, peak, freq, phase, node1, node2) in enumerate(self.voltage_sources):
            self.source_listbox.insert(tk.END, f"{s_type} {peak:.2f}V {freq:.2f}Hz {phase:.2f}° between {node1} and {node2}")
    
    def update_current_source_list(self):
        self.current_source_listbox.delete(0, tk.END)
        for i, (s_type, peak, freq, phase, node1, node2) in enumerate(self.current_sources):
            self.current_source_listbox.insert(tk.END, f"{s_type} {peak:.2f}A {freq:.2f}Hz {phase:.2f}° from {node1} to {node2}")
    
    def add_node(self, name=None):
        if name is None:
            name = f"N{self.next_node_id}"
            self.next_node_id += 1
        
        if name not in self.nodes:
            self.nodes.add(name)
            self.update_node_menus()
            self.update_node_list()
            return name
        return None
    
    def add_node_ui(self):
        name = self.new_node_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a node name")
            return
        
        if name in self.nodes:
            messagebox.showerror("Error", f"Node '{name}' already exists")
            return
        
        self.add_node(name)
        self.new_node_name.set("")
    
    def add_component(self):
        c_type = self.component_type.get()
        value = self.component_value.get()
        node1 = self.node1_var.get()
        node2 = self.node2_var.get()
        
        if not node1 or not node2:
            messagebox.showerror("Error", "Please select both nodes")
            return
            
        if node1 == node2:
            messagebox.showerror("Error", "Nodes must be different")
            return
            
        if value <= 0:
            messagebox.showerror("Error", "Component value must be positive")
            return
            
        # Convert units to base units (Ohms, Farads, Henrys)
        if c_type == "Capacitor":
            value = value * 1e-6  # μF to F
        elif c_type == "Inductor":
            value = value * 1e-3  # mH to H
            
        self.components.append((c_type, value, node1, node2))
        
        # Update lists
        self.update_component_list()
        self.draw_circuit()
    
    def add_voltage_source(self):
        s_type = self.source_type.get()
        peak = self.source_peak.get()
        freq = self.source_freq.get()
        phase = self.source_phase.get()
        node1 = self.source_node1_var.get()
        node2 = self.source_node2_var.get()
        
        if not node1 or not node2:
            messagebox.showerror("Error", "Please select both nodes")
            return
            
        if node1 == node2:
            messagebox.showerror("Error", "Nodes must be different")
            return
            
        if peak <= 0:
            messagebox.showerror("Error", "Peak voltage must be positive")
            return
            
        if freq <= 0:
            messagebox.showerror("Error", "Frequency must be positive")
            return
            
        self.voltage_sources.append((s_type, peak, freq, phase, node1, node2))
        
        # Update lists
        self.update_source_list()
        self.draw_circuit()
    
    def add_current_source(self):
        s_type = self.current_source_type.get()
        peak = self.current_source_peak.get()
        freq = self.current_source_freq.get()
        phase = self.current_source_phase.get()
        node1 = self.current_source_node1_var.get()
        node2 = self.current_source_node2_var.get()
        
        if not node1 or not node2:
            messagebox.showerror("Error", "Please select both nodes")
            return
            
        if node1 == node2:
            messagebox.showerror("Error", "Nodes must be different")
            return
            
        if peak <= 0:
            messagebox.showerror("Error", "Peak current must be positive")
            return
            
        if freq <= 0:
            messagebox.showerror("Error", "Frequency must be positive")
            return
            
        self.current_sources.append((s_type, peak, freq, phase, node1, node2))
        
        # Update lists
        self.update_current_source_list()
        self.draw_circuit()
    
    def draw_circuit(self):
        self.circuit_ax.clear()
        self.circuit_ax.set_axis_off()
        
        if not self.components and not self.voltage_sources and not self.current_sources:
            self.circuit_ax.text(0.5, 0.5, "No components or sources added", ha='center', va='center')
            self.circuit_canvas.draw()
            return
        
        # Create a simple grid layout for nodes
        node_positions = {}
        num_nodes = len(self.nodes)
        
        # Position nodes in a circle
        center = (0.5, 0.5)
        radius = 0.4
        for i, node in enumerate(sorted(self.nodes)):
            angle = 2 * np.pi * i / num_nodes
            x = center[0] + radius * np.cos(angle)
            y = center[1] + radius * np.sin(angle)
            node_positions[node] = (x, y)
            
            # Draw node label
            self.circuit_ax.text(x, y, node, ha='center', va='center', 
                               bbox=dict(facecolor='white', edgecolor='black', boxstyle='circle,pad=0.2'))
        
        # Draw components
        for c_type, value, node1, node2 in self.components:
            x1, y1 = node_positions[node1]
            x2, y2 = node_positions[node2]
            
            # Draw connection line
            self.circuit_ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1)
            
            # Position component at midpoint
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Draw component symbol
            if c_type == "Resistor":
                self.draw_resistor(mid_x, mid_y, x1, y1, x2, y2)
            elif c_type == "Capacitor":
                self.draw_capacitor(mid_x, mid_y, x1, y1, x2, y2)
            elif c_type == "Inductor":
                self.draw_inductor(mid_x, mid_y, x1, y1, x2, y2)
            
            # Label component
            display_value = value
            unit = "Ω"
            if c_type == "Capacitor":
                display_value = value * 1e6
                unit = "μF"
            elif c_type == "Inductor":
                display_value = value * 1e3
                unit = "mH"
            
            # Calculate angle for text rotation
            angle = np.degrees(np.arctan2(y2-y1, x2-x1))
            
            # Position label perpendicular to the component
            label_x = mid_x + 0.03 * np.sin(np.arctan2(y2-y1, x2-x1))
            label_y = mid_y - 0.03 * np.cos(np.arctan2(y2-y1, x2-x1))
            
            self.circuit_ax.text(label_x, label_y, f"{display_value:.2f}{unit}", 
                               ha='center', va='center', rotation=angle)
        
        # Draw voltage sources
        for s_type, peak, freq, phase, node1, node2 in self.voltage_sources:
            x1, y1 = node_positions[node1]
            x2, y2 = node_positions[node2]
            
            # Draw source symbol
            self.draw_voltage_source(x1, y1, x2, y2, s_type, peak, freq, phase)
        
        # Draw current sources
        for s_type, peak, freq, phase, node1, node2 in self.current_sources:
            x1, y1 = node_positions[node1]
            x2, y2 = node_positions[node2]
            
            # Draw source symbol
            self.draw_current_source(x1, y1, x2, y2, s_type, peak, freq, phase)
        
        self.circuit_canvas.draw()
    
    def draw_resistor(self, x, y, x1, y1, x2, y2):
        # Calculate angle of the line
        angle = np.arctan2(y2-y1, x2-x1)
        
        # Create a rectangle perpendicular to the line
        length = 0.1
        width = 0.015
        
        # Rectangle coordinates
        dx = length * np.cos(angle) / 2
        dy = length * np.sin(angle) / 2
        perp_dx = width * np.sin(angle)
        perp_dy = -width * np.cos(angle)
        
        # Rectangle vertices
        vertices = [
            [x - dx + perp_dx, y - dy + perp_dy],
            [x + dx + perp_dx, y + dy + perp_dy],
            [x + dx - perp_dx, y + dy - perp_dy],
            [x - dx - perp_dx, y - dy - perp_dy]
        ]
        
        self.circuit_ax.add_patch(patches.Polygon(vertices, fill=True, color='red'))
    
    def draw_capacitor(self, x, y, x1, y1, x2, y2):
        # Calculate angle of the line
        angle = np.arctan2(y2-y1, x2-x1)
        
        # Capacitor plate length
        plate_length = 0.05
        
        # Plate 1
        dx = plate_length * np.sin(angle)
        dy = -plate_length * np.cos(angle)
        self.circuit_ax.plot([x - dx, x + dx], [y - dy, y + dy], 'k-',color='blue', linewidth=2)
        
        # Plate 2 (offset slightly)
        offset = 0.02 * np.cos(angle), 0.02 * np.sin(angle)
        self.circuit_ax.plot([x - dx + offset[0], x + dx + offset[0]], 
                           [y - dy + offset[1], y + dy + offset[1]], 'k-', color='blue',linewidth=2)
    
    def draw_inductor(self, x, y, x1, y1, x2, y2):
        # Calculate angle of the line
        angle = np.arctan2(y2-y1, x2-x1)
        
        # Inductor parameters
        coil_radius = 0.03
        num_coils = 5
        spacing = 0.02
        
        # Draw coils
        for i in range(num_coils):
            coil_x = x + (i - (num_coils-1)/2) * spacing * np.cos(angle)
            coil_y = y + (i - (num_coils-1)/2) * spacing * np.sin(angle)
            circle = patches.Circle((coil_x, coil_y), coil_radius, fill=False,color='green', linewidth=1)
            self.circuit_ax.add_patch(circle)
    
    def draw_voltage_source(self, x1, y1, x2, y2, s_type, peak, freq, phase):
        # Midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Calculate angle
        angle = np.arctan2(y2-y1, x2-x1)
        
        # Draw circle
        radius = 0.05
        self.circuit_ax.add_patch(patches.Circle((mid_x, mid_y), radius,color='purple' ,fill=False))
        
        # Draw plus and minus signs
        plus_size = radius * 0.5
        self.circuit_ax.plot([mid_x - plus_size, mid_x + plus_size], [mid_y, mid_y], 'k-', linewidth=1)
        self.circuit_ax.plot([mid_x, mid_x], [mid_y - plus_size, mid_y + plus_size], 'k-', linewidth=1)
        
        # Draw arrow indicating polarity
        arrow_length = radius * 1.5
        arrow_dx = arrow_length * np.cos(angle)
        arrow_dy = arrow_length * np.sin(angle)
        
        # Draw arrow from node1 to node2 (positive to negative)
        self.circuit_ax.arrow(mid_x, mid_y, arrow_dx, arrow_dy, head_width=0.02, 
                            head_length=0.03, fc='k', ec='k')
        
        # Label source
        label_x = mid_x + 0.08 * np.sin(angle)
        label_y = mid_y - 0.08 * np.cos(angle)
        self.circuit_ax.text(label_x, label_y, f"{peak:.1f}V\n{freq:.1f}Hz\n{phase:.0f}°", 
                           ha='center', va='center', fontsize=8)
    
    def draw_current_source(self, x1, y1, x2, y2, s_type, peak, freq, phase):
        # Midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Calculate angle
        angle = np.arctan2(y2-y1, x2-x1)
        
        # Draw circle
        radius = 0.05
        self.circuit_ax.add_patch(patches.Circle((mid_x, mid_y), radius,color='purple', fill=False))
        
        # Draw arrow inside circle indicating current direction
        arrow_length = radius * 0.8
        arrow_dx = arrow_length * np.cos(angle)
        arrow_dy = arrow_length * np.sin(angle)
        
        # Draw arrow from node1 to node2
        self.circuit_ax.arrow(mid_x - arrow_dx/2, mid_y - arrow_dy/2, 
                            arrow_dx, arrow_dy, 
                            head_width=0.02, head_length=0.03, fc='k', ec='k')
        
        # Label source
        label_x = mid_x + 0.08 * np.sin(angle)
        label_y = mid_y - 0.08 * np.cos(angle)
        self.circuit_ax.text(label_x, label_y, f"{peak:.1f}A\n{freq:.1f}Hz\n{phase:.0f}°", 
                           ha='center', va='center', fontsize=8)
    
    def analyze_circuit(self):
        if not self.components and not self.voltage_sources and not self.current_sources:
            messagebox.showerror("Error", "No components or sources to analyze")
            return
        
        # Prepare results text
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "=== AC Circuit Analysis Results ===\n\n")
        
        try:
            # Get all nodes and create index mapping (excluding ground)
            all_nodes = sorted(self.nodes)
            node_index = {node: i for i, node in enumerate(all_nodes) if node != "GND"}
            num_nodes = len(node_index)
            
            if num_nodes == 0:
                self.results_text.insert(tk.END, "No nodes to analyze (only ground exists)\n")
                return
            
            # Get reference frequency from first voltage source or current source
            freq = 60.0  # default
            if self.voltage_sources:
                freq = self.voltage_sources[0][2]
            elif self.current_sources:
                freq = self.current_sources[0][2]
            
            omega = 2 * np.pi * freq
            
            # Initialize Modified Nodal Analysis (MNA) matrices
            # G matrix: conductance matrix (n x n)
            # B matrix: connection matrix for voltage sources (n x m)
            # C matrix: connection matrix for voltage sources (m x n) (C = B^T)
            # D matrix: zero matrix (m x m)
            # I vector: current sources (n x 1)
            # E vector: voltage sources (m x 1)
            
            # Count voltage sources
            num_v_sources = len(self.voltage_sources)
            
            # Total matrix size: (n + m) x (n + m)
            total_size = num_nodes + num_v_sources
            G = np.zeros((total_size, total_size), dtype=complex)
            rhs = np.zeros(total_size, dtype=complex)
            
            # Fill G matrix for components
            for c_type, value, node1, node2 in self.components:
                # Calculate admittance
                if c_type == "Resistor":
                    y = 1 / value
                elif c_type == "Capacitor":
                    y = 1j * omega * value
                elif c_type == "Inductor":
                    y = 1 / (1j * omega * value)
                
                # Update conductance matrix
                if node1 != "GND" and node2 != "GND":
                    i = node_index[node1]
                    j = node_index[node2]
                    G[i, i] += y
                    G[j, j] += y
                    G[i, j] -= y
                    G[j, i] -= y
                elif node1 != "GND":
                    i = node_index[node1]
                    G[i, i] += y
                elif node2 != "GND":
                    j = node_index[node2]
                    G[j, j] += y
            
            # Process voltage sources (add to B, C, D matrices)
            for vs_idx, (s_type, peak, freq, phase, node1, node2) in enumerate(self.voltage_sources):
                v_complex = peak * cmath.exp(1j * np.radians(phase))
                m = num_nodes + vs_idx  # row/col for this source
                
                if node1 != "GND":
                    i = node_index[node1]
                    G[i, m] = 1
                    G[m, i] = 1
                
                if node2 != "GND":
                    j = node_index[node2]
                    G[j, m] = -1
                    G[m, j] = -1
                
                rhs[m] = v_complex
            
            # Process current sources (add to I vector)
            for s_type, peak, freq, phase, node1, node2 in self.current_sources:
                i_complex = peak * cmath.exp(1j * np.radians(phase))
                
                if node1 != "GND" and node2 != "GND":
                    i = node_index[node1]
                    j = node_index[node2]
                    rhs[i] -= i_complex
                    rhs[j] += i_complex
                elif node1 != "GND":
                    i = node_index[node1]
                    rhs[i] -= i_complex
                elif node2 != "GND":
                    j = node_index[node2]
                    rhs[j] += i_complex
            
            # Solve the system
            try:
                solution = np.linalg.solve(G, rhs)
            except np.linalg.LinAlgError:
                self.results_text.insert(tk.END, "Matrix is singular - check your circuit connections\n")
                return
            
            # Extract node voltages
            node_voltages = {node: 0 for node in all_nodes}
            node_voltages["GND"] = 0
            for node, idx in node_index.items():
                node_voltages[node] = solution[idx]
            
            # Extract voltage source currents
            source_currents = {}
            for vs_idx, (s_type, peak, freq, phase, node1, node2) in enumerate(self.voltage_sources):
                m = num_nodes + vs_idx
                source_currents[(node1, node2)] = solution[m]
            
            # Display results
            self.results_text.insert(tk.END, f"Analysis Frequency: {freq:.2f} Hz\n\n")
            
            self.results_text.insert(tk.END, "=== Node Voltages ===\n")
            for node in sorted(node_voltages.keys()):
                v = node_voltages[node]
                self.results_text.insert(tk.END, 
                    f"{node}: {abs(v):.4f}V ∠{np.degrees(cmath.phase(v)):.2f}°\n")
            
            self.results_text.insert(tk.END, "\n=== Component Currents ===\n")
            for c_type, value, node1, node2 in self.components:
                v1 = node_voltages[node1]
                v2 = node_voltages[node2]
                v_diff = v1 - v2
                
                # Calculate impedance
                if c_type == "Resistor":
                    z = value
                elif c_type == "Capacitor":
                    z = 1 / (1j * omega * value)
                elif c_type == "Inductor":
                    z = 1j * omega * value
                
                # Calculate current
                current = v_diff / z
                
                display_value = value
                unit = "Ω"
                if c_type == "Capacitor":
                    display_value = value * 1e6
                    unit = "μF"
                elif c_type == "Inductor":
                    display_value = value * 1e3
                    unit = "mH"
                
                self.results_text.insert(tk.END, 
                    f"{c_type} {display_value:.2f}{unit} between {node1} and {node2}: "
                    f"{abs(current):.4f}A ∠{np.degrees(cmath.phase(current)):.2f}°\n")
            
            if self.voltage_sources:
                self.results_text.insert(tk.END, "\n=== Voltage Source Currents ===\n")
                for vs_idx, (s_type, peak, freq, phase, node1, node2) in enumerate(self.voltage_sources):
                    current = source_currents[(node1, node2)]
                    self.results_text.insert(tk.END, 
                        f"Source {peak:.2f}V {freq:.2f}Hz ∠{phase:.2f}° between {node1} and {node2}: "
                        f"{abs(current):.4f}A ∠{np.degrees(cmath.phase(current)):.2f}°\n")
            
            if self.current_sources:
                self.results_text.insert(tk.END, "\n=== Current Source Voltages ===\n")
                for s_type, peak, freq, phase, node1, node2 in self.current_sources:
                    v1 = node_voltages[node1]
                    v2 = node_voltages[node2]
                    v_diff = v1 - v2
                    self.results_text.insert(tk.END, 
                        f"Source {peak:.2f}A {freq:.2f}Hz ∠{phase:.2f}° between {node1} and {node2}: "
                        f"{abs(v_diff):.4f}V ∠{np.degrees(cmath.phase(v_diff)):.2f}°\n")
            
            # Calculate and display equivalent impedances for series/parallel components
            self.calculate_equivalent_impedances(freq)
            
        except Exception as e:
            self.results_text.insert(tk.END, f"\nError in analysis: {str(e)}\n")
    
    def detect_series_parallel(self):
        """Detect series and parallel connections in the circuit"""
        if not self.components:
            messagebox.showinfo("Info", "No components to analyze")
            return
            
        self.results_text.insert(tk.END, "\n=== Series/Parallel Analysis ===\n")
        
        # Build adjacency list for components
        component_graph = defaultdict(list)
        for idx, (_, _, node1, node2) in enumerate(self.components):
            component_graph[node1].append((node2, idx))
            component_graph[node2].append((node1, idx))
        
        # Find all nodes with exactly two components connected (potential series connection points)
        series_nodes = [node for node in component_graph if len(component_graph[node]) == 2 and node != "GND"]
        
        if series_nodes:
            self.results_text.insert(tk.END, "\nPotential Series Connections:\n")
            for node in series_nodes:
                comp1_idx = component_graph[node][0][1]
                comp2_idx = component_graph[node][1][1]
                c1_type, c1_val, n11, n12 = self.components[comp1_idx]
                c2_type, c2_val, n21, n22 = self.components[comp2_idx]
                
                self.results_text.insert(tk.END, 
                    f"Components {c1_type} {n11}-{n12} and {c2_type} {n21}-{n22} may be in series at node {node}\n")
        else:
            self.results_text.insert(tk.END, "\nNo obvious series connections found\n")
        
        # Find parallel components (same node pairs)
        parallel_groups = defaultdict(list)
        for idx, (c_type, value, node1, node2) in enumerate(self.components):
            key = tuple(sorted((node1, node2)))
            parallel_groups[key].append((idx, c_type, value))
        
        parallel_exists = False
        for nodes, components in parallel_groups.items():
            if len(components) > 1:
                if not parallel_exists:
                    self.results_text.insert(tk.END, "\nParallel Components Found:\n")
                    parallel_exists = True
                
                self.results_text.insert(tk.END, f"Between nodes {nodes[0]} and {nodes[1]}:\n")
                for idx, c_type, value in components:
                    display_value = value
                    unit = "Ω"
                    if c_type == "Capacitor":
                        display_value = value * 1e6
                        unit = "μF"
                    elif c_type == "Inductor":
                        display_value = value * 1e3
                        unit = "mH"
                    self.results_text.insert(tk.END, f"  - {c_type} {display_value:.2f}{unit}\n")
        
        if not parallel_exists:
            self.results_text.insert(tk.END, "\nNo parallel components found\n")
    
    def calculate_equivalent_impedances(self, freq):
        """Calculate equivalent impedances for series and parallel components"""
        if not self.components:
            return
            
        omega = 2 * np.pi * freq
        
        # Group components by their node pairs
        component_groups = defaultdict(list)
        for c_type, value, node1, node2 in self.components:
            key = tuple(sorted((node1, node2)))
            component_groups[key].append((c_type, value))
        
        # Check for parallel components
        parallel_exists = False
        for nodes, components in component_groups.items():
            if len(components) > 1:
                if not parallel_exists:
                    self.results_text.insert(tk.END, "\n=== Equivalent Parallel Impedances ===\n")
                    parallel_exists = True
                
                # Calculate parallel impedance
                total_admittance = 0
                for c_type, value in components:
                    if c_type == "Resistor":
                        z = value
                    elif c_type == "Capacitor":
                        z = 1 / (1j * omega * value)
                    elif c_type == "Inductor":
                        z = 1j * omega * value
                    total_admittance += 1 / z
                
                z_eq = 1 / total_admittance
                
                self.results_text.insert(tk.END, 
                    f"Between {nodes[0]} and {nodes[1]}: {len(components)} components in parallel\n")
                self.results_text.insert(tk.END, 
                    f"Equivalent impedance: {abs(z_eq):.4f}Ω ∠{np.degrees(cmath.phase(z_eq)):.2f}°\n")
        
        # Check for series components by finding chains
        # This is more complex and would require graph traversal
        # For now, we'll just look for two components sharing one node (simple series)
        component_connections = defaultdict(list)
        for idx, (_, _, node1, node2) in enumerate(self.components):
            component_connections[node1].append(idx)
            component_connections[node2].append(idx)
        
        series_exists = False
        for node, indices in component_connections.items():
            if len(indices) == 2 and node != "GND":
                if not series_exists:
                    self.results_text.insert(tk.END, "\n=== Equivalent Series Impedances ===\n")
                    series_exists = True
                
                idx1, idx2 = indices
                c1_type, c1_val, n11, n12 = self.components[idx1]
                c2_type, c2_val, n21, n22 = self.components[idx2]
                
                # Calculate series impedance
                z1 = 0
                if c1_type == "Resistor":
                    z1 = c1_val
                elif c1_type == "Capacitor":
                    z1 = 1 / (1j * omega * c1_val)
                elif c1_type == "Inductor":
                    z1 = 1j * omega * c1_val
                
                z2 = 0
                if c2_type == "Resistor":
                    z2 = c2_val
                elif c2_type == "Capacitor":
                    z2 = 1 / (1j * omega * c2_val)
                elif c2_type == "Inductor":
                    z2 = 1j * omega * c2_val
                
                z_eq = z1 + z2
                
                self.results_text.insert(tk.END, 
                    f"Series connection at node {node}: {c1_type} and {c2_type}\n")
                self.results_text.insert(tk.END, 
                    f"Equivalent impedance: {abs(z_eq):.4f}Ω ∠{np.degrees(cmath.phase(z_eq)):.2f}°\n")
    
    def clear_circuit(self):
        self.components = []
        self.voltage_sources = []
        self.current_sources = []
        self.nodes = {"GND"}  # Keep only ground
        self.next_node_id = 0
        
        # Update all displays
        self.update_component_list()
        self.update_source_list()
        self.update_current_source_list()
        self.update_node_menus()
        self.update_node_list()
        self.draw_circuit()
        self.results_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedACCircuitAnalyzer(root)
    root.mainloop()