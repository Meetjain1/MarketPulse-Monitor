from setuptools import setup, find_packages

setup(
    name="marketpulse-monitor",
    version="1.0.0",
    description="E-commerce Price Monitoring Dashboard",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0,<2.0.0",
        "pandas>=2.0.0,<3.0.0",
        "plotly>=5.14.1,<6.0.0",
        "numpy>=1.26.0,<2.0.0",
        "pillow>=10.0.0,<11.0.0",
        "openpyxl>=3.1.0,<4.0.0",
        "xlrd>=2.0.1,<3.0.0",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
