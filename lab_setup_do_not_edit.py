import sys
import os
import importlib
from IPython import get_ipython

def _aggressive_reloader(info):
    """
    INTERNAL TOOL: Scans for local modules and reloads them.
    """
    current_dir = os.getcwd()
    modules_to_reload = []
    
    # Scan loaded modules
    for name, module in sys.modules.items():
        if not hasattr(module, '__file__') or module.__file__ is None:
            continue
        
        module_path = os.path.abspath(module.__file__)
        
        # Only reload modules located in the current directory
        if module_path.startswith(current_dir):
            # prevent reloading this script itself to avoid loops
            if "lab_setup_do_not_edit" in name:
                continue
            modules_to_reload.append(module)

    # Reload (twice for dependencies)
    for _ in range(2):
        for module in modules_to_reload:
            try:
                importlib.reload(module)
            except Exception:
                pass 

def _activate_autoreload():
    ip = get_ipython()
    
    if ip is None:
        # We are not in Colab/Jupyter, do nothing
        return

    # Remove existing hooks to prevent duplicates
    try:
        ip.events.unregister('pre_run_cell', _aggressive_reloader)
    except ValueError:
        pass

    # Register the new hook
    ip.events.register('pre_run_cell', _aggressive_reloader)
    
    # Print a clean message for the student
    print("✅ Environment ready! Code will update automatically.")

# This runs immediately when the student imports the file
_activate_autoreload()
