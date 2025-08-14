# Streamlit Cloud Deployment Guide

This document provides instructions for deploying the MarketPulse Monitor application on Streamlit Cloud.

## Prerequisites

- A GitHub account
- Your MarketPulse Monitor code pushed to a GitHub repository
- A Streamlit Cloud account (sign up at https://streamlit.io/cloud if you don't have one)

## Deployment Steps

1. **Prepare your repository**
   - Make sure all the necessary files are committed and pushed to your GitHub repository
   - The main files needed are:
     - `app.py` - Main application file
     - `requirements.txt` - Dependencies
     - Supporting modules: `db.py`, `price_compare.py`, `email_alert.py`

2. **Log in to Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Sign in with your GitHub account

3. **Deploy your app**
   - Click on "New app" button
   - Select your repository from the list
   - Choose the branch (usually "main")
   - Set the Main file path to `app.py`
   - Optionally customize the app URL
   - Click "Deploy!"

4. **Monitor deployment**
   - Streamlit Cloud will install dependencies and start your app
   - You can view logs during the deployment process
   - Once deployment is complete, your app will be available at the assigned URL

## Troubleshooting

If you encounter deployment issues:

1. **Dependency conflicts**
   - Ensure your `requirements.txt` specifies compatible versions
   - Consider using older, more stable versions of packages

2. **Python version issues**
   - Streamlit Cloud uses Python 3.9 by default
   - You can specify a different version using a `runtime.txt` file

3. **File access errors**
   - Use absolute paths with `os.path.dirname(__file__)` instead of `os.getcwd()`
   - Avoid writing to the app directory during runtime

4. **Memory or performance issues**
   - Optimize data loading and processing
   - Consider using caching with `@st.cache_data` for expensive operations

## Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit Forums](https://discuss.streamlit.io/)
