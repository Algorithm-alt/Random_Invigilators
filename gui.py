import os
import sys
import time
import threading
import webview
from django.core.management import execute_from_command_line

def run_django():
    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_invigilation.settings')
    
    # Run server on port 8001 with noreload to avoid thread issues
    sys.argv = ['manage.py', 'runserver', '127.0.0.1:8001', '--noreload']
    execute_from_command_line(sys.argv)

def start_app():
    # Create the window pointing to the local server
    webview.create_window('School Invigilation System', 'http://127.0.0.1:8001')
    webview.start()

if __name__ == '__main__':
    # Start Django in a separate thread
    t = threading.Thread(target=run_django)
    t.daemon = True
    t.start()
    
    # Give the server a moment to start
    time.sleep(1)
    
    # Start the GUI
    start_app()
