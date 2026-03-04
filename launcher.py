import os
import sys
import threading
import subprocess
import time
import tkinter as tk
from tkinter import messagebox
from django.core.management import execute_from_command_line

# Define the port
PORT = 8001
URL = f"http://127.0.0.1:{PORT}"

class InvigilationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Invigilation System")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Status Label
        self.status_label = tk.Label(root, text="Running...", fg="green", font=("Segoe UI", 12, "bold"))
        self.status_label.pack(pady=20)
        
        # Info Label
        self.info_label = tk.Label(root, text="Close this window to stop the app.", font=("Segoe UI", 9))
        self.info_label.pack(pady=5)
        
        # Start Django in a customized thread
        self.server_thread = threading.Thread(target=self.run_django)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Open App Mode after a short delay
        self.root.after(2000, self.open_app_mode)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def run_django(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_invigilation.settings')
        sys.argv = ['manage.py', 'runserver', f'127.0.0.1:{PORT}', '--noreload']
        try:
            execute_from_command_line(sys.argv)
        except SystemExit:
            pass
        except Exception as e:
            print(f"Error starting server: {e}")

    def open_app_mode(self):
        # Try to launch Edge in App Mode (Windows default)
        try:
            # Common paths for Edge
            edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            if not os.path.exists(edge_path):
                edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
            
            if os.path.exists(edge_path):
                subprocess.Popen([edge_path, f"--app={URL}"])
            else:
                # Fallback to system default if Edge not found (unlikely on Windows)
                import webbrowser
                webbrowser.open(URL)
        except Exception as e:
            print(f"Failed to launch Edge: {e}")
            import webbrowser
            webbrowser.open(URL)

if __name__ == '__main__':
    root = tk.Tk()
    app = InvigilationApp(root)
    
    # Handle window close
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to close the application?"):
            root.destroy()
            sys.exit(0)
            
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
