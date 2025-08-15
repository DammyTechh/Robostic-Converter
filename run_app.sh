#!/bin/bash

echo ""
echo "========================================"
echo "   Converter | Space by Dammytech"
echo "========================================"
echo ""
echo "Starting the application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed"
        echo "Please install Python 3.7+ from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "ERROR: main.py not found!"
    echo "Please make sure you're in the correct directory"
    exit 1
fi

# Try to run the application
$PYTHON_CMD main.py

# If there's an error, show message
if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "ERROR: Application failed to start"
    echo "========================================"
    echo ""
    echo "This might be due to missing dependencies."
    echo "Run: $PYTHON_CMD install_dependencies.py"
    echo ""
    echo "Contact support: petersdamilare5@gmail.com"
    echo "Website: https://dammytech.netlify.app"
    echo ""
fi

read -p "Press Enter to continue..."