#!/bin/bash

echo "========================================"
echo "LinkedIn Job Scraper Installation"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Python found. Starting installation..."
echo

# Make the script executable
chmod +x install_linkedin_scraper.py

# Run the installation script
python3 install_linkedin_scraper.py

if [ $? -eq 0 ]; then
    echo
    echo "Installation completed successfully!"
    echo
    echo "To start the application, run: streamlit run main.py"
    echo
else
    echo
    echo "Installation failed! Please check the error messages above."
    exit 1
fi
