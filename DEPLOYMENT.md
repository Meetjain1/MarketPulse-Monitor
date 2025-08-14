# Deployment Guide for MarketPulse Monitor

## Overview
This guide covers deploying the MarketPulse Monitor dashboard to Streamlit Cloud.

## Prerequisites
- Python 3.9, 3.10, or 3.11 (3.11 recommended)
- All dependencies listed in requirements.txt
- Git repository access

## Files Required for Deployment

### 1. requirements.txt
Contains all Python dependencies with version constraints:
```
streamlit>=1.28.0,<2.0.0
pandas>=2.0.0,<3.0.0
plotly>=5.14.1,<6.0.0
numpy>=1.26.0,<2.0.0
pillow>=10.0.0,<11.0.0
openpyxl>=3.1.0,<4.0.0
xlrd>=2.0.1,<3.0.0
```

### 2. runtime.txt
Specifies Python version:
```
python-3.11.18
```

### 3. packages.txt
System-level dependencies:
```
libgl1-mesa-glx
```

### 4. Procfile
Deployment configuration:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

## Deployment Steps

1. **Push Changes to Git**
   ```bash
   git add .
   git commit -m "Fix deployment compatibility issues"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Connect your GitHub repository
   - Set main file to: `app.py`
   - Deploy

## Troubleshooting Common Issues

### Issue: "distutils was removed from the standard library in Python 3.12"
**Solution**: Use Python 3.11 or lower (specified in runtime.txt)

### Issue: Package version incompatibility
**Solution**: All packages in requirements.txt are now compatible with Python 3.11

### Issue: Build failures
**Solution**: 
- Ensure all dependencies are properly specified
- Use compatible Python version
- Check for missing system packages

### Issue: Import errors
**Solution**: Run test_imports.py locally to verify all imports work

## Local Testing

Before deploying, test locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Test imports
python test_imports.py

# Run app locally
streamlit run app.py
```

## Environment Variables

No environment variables are required for basic functionality.

## Monitoring Deployment

Check Streamlit Cloud logs for:
- Package installation status
- Python version compatibility
- Import errors
- Runtime errors

## Support

If issues persist:
1. Check Streamlit Cloud logs
2. Verify Python version compatibility
3. Test locally with same Python version
4. Review requirements.txt for conflicts
