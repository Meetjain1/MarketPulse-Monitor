import streamlit as st
import os
import sys

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(__file__))

# Import the main app function
from app import main

# Just run the main function from app.py
if __name__ == "__main__":
    main()
