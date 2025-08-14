# This file contains compatibility helpers for different Python versions

import sys

def is_python_3_9_or_higher():
    """Check if Python version is 3.9 or higher"""
    major = sys.version_info.major
    minor = sys.version_info.minor
    return (major == 3 and minor >= 9) or major > 3
