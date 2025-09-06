import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime

class ProductivityDashboard:
    def __init__(self, data):
        self.data = data
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        self.root.title("Productivity Dashboard")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Set color scheme
        self.root.configure(bg="#f0f0f0")
        
        # Configure styles
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        style.configure("Data.TLabel", font=("Arial", 10))
    
    def format_time(self, seconds):
        """Convert seconds to minutes:seconds format"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="📊 Productivity Report", 
                               style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Summary section
        self.create_summary_section(main_frame)
        
        # Apps section
        self.create_apps_section(main_frame)
        
        # Insights section
        self.create_insights_section(main_frame)
    
    def create_summary_section(self, parent):
        # Summary frame
        summary_frame = ttk.LabelFrame(parent, text="Summary", padding="10")
        summary_frame.pack(fill="x", pady=(0, 10))
        
        summary = self.data["summary"]
        
        # Create grid for summary data
        grid_frame = ttk.Frame(summary_frame)
        grid_frame.pack(fill="x")
        
        # Total time
        ttk.Label(grid_frame, text="Total Time:", style="Data.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 10))
        ttk.Label(grid_frame, text=self.format_time(summary["total_time"]), 
                 style="Data.TLabel").grid(row=0, column=1, sticky="w")
        
        # Productive time
        ttk.Label(grid_frame, text="Productive Time:", style="Data.TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 10))
        ttk.Label(grid_frame, text=self.format_time(summary["productive_time"]), 
                 style="Data.TLabel").grid(row=1, column=1, sticky="w")
        
        # Unproductive time
        ttk.Label(grid_frame, text="Unproductive Time:", style="Data.TLabel").grid(
            row=2, column=0, sticky="w", padx=(0, 10))
        ttk.Label(grid_frame, text=self.format_time(summary["unproductive_time"]), 
                 style="Data.TLabel").grid(row=2, column=1, sticky="w")
        
        # Productivity score
        ttk.Label(grid_frame, text="Productivity Score:", style="Data.TLabel").grid(
            row=3, column=0, sticky="w", padx=(0, 10))
        score_text = f"{summary['productivity_score']:.1f}%"
        score_color = "#2d8c2d" if summary["productivity_score"] >= 80 else "#d4861b" if summary["productivity_score"] >= 60 else "#c4342d"
        score_label = ttk.Label(grid_frame, text=score_text, style="Data.TLabel")
        score_label.grid(row=3, column=1, sticky="w")
    
    def create_apps_section(self, parent):
        # Apps frame
        apps_frame = ttk.LabelFrame(parent, text="App Usage", padding="10")
        apps_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Create treeview for apps
        tree = ttk.Treeview(apps_frame, columns=("Productive", "Unproductive"), 
                           show="tree headings", height=6)
        
        # Configure columns
        tree.heading("#0", text="App Name")
        tree.heading("Productive", text="Productive")
        tree.heading("Unproductive", text="Unproductive")
        
        tree.column("#0", width=150)
        tree.column("Productive", width=120)
        tree.column("Unproductive", width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(apps_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Populate tree with app data
        for app in self.data["apps"]:
            productive_time = self.format_time(app["productive"]["total_time_spent"])
            unproductive_time = self.format_time(app["unproductive"]["total_time_spent"])
            
            tree.insert("", "end", text=app["app_name"], 
                       values=(productive_time, unproductive_time))
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_insights_section(self, parent):
        # Insights frame
        insights_frame = ttk.LabelFrame(parent, text="Key Insights", padding="10")
        insights_frame.pack(fill="x")
        
        # Create text widget for insights
        text_widget = tk.Text(insights_frame, height=4, wrap="word", 
                             font=("Arial", 9), bg="#ffffff")
        
        # Add insights
        for i, insight in enumerate(self.data["insights"]):
            text_widget.insert("end", f"• {insight}\n\n")
        
        text_widget.config(state="disabled")  # Make read-only
        text_widget.pack(fill="x")
        
        # Keywords section
        keywords_frame = ttk.Frame(insights_frame)
        keywords_frame.pack(fill="x", pady=(10, 0))
        
        # Productive keywords
        prod_frame = ttk.Frame(keywords_frame)
        prod_frame.pack(fill="x", pady=(0, 5))
        ttk.Label(prod_frame, text="🟢 Productive Keywords:", 
                 style="Data.TLabel", foreground="#2d8c2d").pack(anchor="w")
        prod_text = ", ".join(self.data["productive_keywords"])
        ttk.Label(prod_frame, text=prod_text, style="Data.TLabel", 
                 wraplength=450).pack(anchor="w", padx=(20, 0))
        
        # Unproductive keywords
        unprod_frame = ttk.Frame(keywords_frame)
        unprod_frame.pack(fill="x")
        ttk.Label(unprod_frame, text="🔴 Unproductive Keywords:", 
                 style="Data.TLabel", foreground="#c4342d").pack(anchor="w")
        unprod_text = ", ".join(self.data["unproductive_keywords"])
        ttk.Label(unprod_frame, text=unprod_text, style="Data.TLabel", 
                 wraplength=450).pack(anchor="w", padx=(20, 0))
    
    def run(self):
        self.root.mainloop()

def load_and_display_dashboard(json_file_path=None, json_data=None):
    """
    Load productivity data and display dashboard
    
    Args:
        json_file_path (str): Path to JSON file
        json_data (dict): Direct JSON data (alternative to file)
    """
    if json_data:
        data = json_data
    elif json_file_path:
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{json_file_path}' not found.")
            return
        except json.JSONDecodeError:
            print("Error: Invalid JSON format.")
            return
    else:
        print("Error: Please provide either json_file_path or json_data")
        return
    
    # Create and run dashboard
    dashboard = ProductivityDashboard(data)
    dashboard.run()

# Example usage
if __name__ == "__main__":
    # Simply run with default path (./data/user_data.json)
    load_and_display_dashboard()
    
    # Or specify a different path if needed
    # load_and_display_dashboard("path/to/other/file.json")
    
    # Or use direct data if needed
    # load_and_display_dashboard(json_data=your_data_dict)