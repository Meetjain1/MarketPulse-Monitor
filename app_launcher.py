import sys
import os
import subprocess

# Check if running on Streamlit Cloud
if "STREAMLIT_SHARING" in os.environ or "STREAMLIT_SERVER_URL" in os.environ:
    # Print Python version for debugging
    print(f"Python version: {sys.version}")
    
    # Install compatible versions if on Python 3.13+
    if sys.version_info.major == 3 and sys.version_info.minor >= 13:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", 
                                 "numpy==1.26.3", 
                                 "pandas==2.0.3",
                                 "pillow==10.2.0"])
            print("Successfully installed compatible package versions")
        except Exception as e:
            print(f"Error installing compatible packages: {e}")

# Continue with the normal import process
import streamlit as st
import pandas as pd
import io
import os
from datetime import datetime
import plotly.express as px
import numpy as np

# Import our own special code files - they do all the hard work!
import db
import price_compare
import email_alert

# Set up our database when the app first starts
# This is like setting the table before dinner!
db.init_db()
