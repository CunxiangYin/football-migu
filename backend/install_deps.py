#!/usr/bin/env python
"""Install missing dependencies at runtime."""

import subprocess
import sys

def install_package(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import requests, install if missing
try:
    import requests
except ImportError:
    print("Installing requests...")
    install_package("requests")
    import requests

print("All dependencies installed successfully!")