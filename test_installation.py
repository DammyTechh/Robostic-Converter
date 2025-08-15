#!/usr/bin/env python3
# Quick test script for Converter | Space
import sys

try:
    import customtkinter as ctk
    import docx
    import pptx
    import pypdf
    from PIL import Image
    import pdf2docx
    
    print("🎉 All core dependencies imported successfully!")
    print("✅ Converter | Space is ready to run!")
    print("\n🚀 Run 'python main.py' to start the application")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please run the installer again or install missing packages manually")
    sys.exit(1)
