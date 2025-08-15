#!/usr/bin/env python3
"""
Enhanced Installation script for Converter | Space by Dammytech
This script will install all required dependencies with enhanced error handling
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            timeout=300  # 5 minutes timeout
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"

def install_package(package, optional=False):
    """Install a single package using pip"""
    print(f"📦 Installing {package}...")
    success, output = run_command(f"{sys.executable} -m pip install {package}")
    
    if success:
        print(f"✅ {package} installed successfully!")
        return True
    else:
        if optional:
            print(f"⚠️  Optional package {package} failed to install: {output}")
        else:
            print(f"❌ Failed to install {package}: {output}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version < (3, 7, 0):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def upgrade_pip():
    """Upgrade pip to latest version"""
    print("\n📊 Upgrading pip...")
    success, output = run_command(f"{sys.executable} -m pip install --upgrade pip")
    if success:
        print("✅ pip upgraded successfully")
    else:
        print(f"⚠️  pip upgrade failed: {output}")
    return success

def install_core_dependencies():
    """Install core dependencies"""
    print("\n🔧 Installing core dependencies...")
    
    core_packages = [
        "customtkinter==5.2.0",
        "python-docx==0.8.11", 
        "python-pptx==0.6.21",
        "PyPDF2==3.0.1",
        "pdf2docx==0.5.6",
        "Pillow==10.0.0",
        "img2pdf==0.4.4",
        "reportlab==4.0.4"
    ]
    
    failed_core = []
    
    for package in core_packages:
        if not install_package(package):
            failed_core.append(package)
    
    return failed_core

def install_platform_specific():
    """Install platform-specific packages"""
    failed_platform = []
    
    if platform.system() == "Windows":
        print("\n🪟 Installing Windows-specific packages...")
        windows_packages = ["pywin32==306"]
        
        for package in windows_packages:
            if not install_package(package, optional=True):
                failed_platform.append(package)
    
    return failed_platform

def install_optional_packages():
    """Install optional enhancement packages"""
    print("\n✨ Installing optional enhancement packages...")
    
    optional_packages = [
        "tkinterdnd2==0.3.0",
        "pathlib2"
    ]
    
    failed_optional = []
    
    for package in optional_packages:
        if not install_package(package, optional=True):
            failed_optional.append(package)
    
    return failed_optional

def verify_installation():
    """Verify that key packages can be imported"""
    print("\n🔍 Verifying installation...")
    
    test_imports = [
        ("customtkinter", "CustomTkinter GUI framework"),
        ("docx", "python-docx for Word processing"),
        ("pptx", "python-pptx for PowerPoint processing"), 
        ("pypdf", "PyPDF2 for PDF processing"),
        ("PIL", "Pillow for image processing"),
        ("pdf2docx", "pdf2docx converter")
    ]
    
    failed_imports = []
    
    for module, description in test_imports:
        try:
            __import__(module)
            print(f"✅ {description} - OK")
        except ImportError as e:
            print(f"❌ {description} - FAILED: {e}")
            failed_imports.append((module, description))
    
    return failed_imports

def create_test_script():
    """Create a simple test script"""
    test_script = """#!/usr/bin/env python3
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
    print("\\n🚀 Run 'python main.py' to start the application")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please run the installer again or install missing packages manually")
    sys.exit(1)
"""
    
    try:
        with open("test_installation.py", "w", encoding="utf-8") as f:
            f.write(test_script)
        print("📝 Created test_installation.py - run this to verify your setup")
        return True
    except Exception as e:
        print(f"⚠️  Could not create test script: {e}")
        return False

def main():
    """Main installation function"""
    print("🚀 Converter | Space by Dammytech - Enhanced Installation Script")
    print("=" * 70)
    print("🌐 Website: https://dammytech.netlify.app")
    print("📧 Support: petersdamilare5@gmail.com")
    print("=" * 70)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Upgrade pip
    upgrade_pip()
    
    # Install dependencies
    failed_core = install_core_dependencies()
    failed_platform = install_platform_specific()
    failed_optional = install_optional_packages()
    
    # Verify installation
    failed_imports = verify_installation()
    
    # Create test script
    create_test_script()
    
    # Final report
    print("\n" + "=" * 70)
    print("📋 INSTALLATION REPORT")
    print("=" * 70)
    
    if not failed_core and not failed_imports:
        print("🎉 Installation completed successfully!")
        print("\n✅ Core Features Available:")
        print("   • PDF ↔ Word conversion")
        print("   • Word ↔ PowerPoint conversion") 
        print("   • Image → PDF conversion")
        print("   • Advanced PDF Editor")
        print("   • Modern 3D GUI interface")
        
        if not failed_platform:
            print("\n✅ Platform-specific features available")
        
        if not failed_optional:
            print("✅ All optional enhancements available")
        
        print("\n🚀 READY TO USE!")
        print("   Run: python main.py")
        
    else:
        print("⚠️  Installation completed with some issues:")
        
        if failed_core:
            print("\n❌ Failed core packages (CRITICAL):")
            for package in failed_core:
                print(f"   • {package}")
                
        if failed_imports:
            print("\n❌ Import verification failed:")
            for module, desc in failed_imports:
                print(f"   • {module} - {desc}")
        
        print("\n🛠️  MANUAL INSTALLATION REQUIRED:")
        print("   pip install " + " ".join(failed_core))
        
        if failed_platform:
            print("\n⚠️  Platform-specific packages failed (optional):")
            for package in failed_platform:
                print(f"   • {package}")
    
    print("\n📞 SUPPORT:")
    print("   🌐 Website: https://dammytech.netlify.app")
    print("   📧 Email: petersdamilare5@gmail.com")
    print("   📝 Include installation log when reporting issues")
    
    print("\n🔗 Quick Links:")
    print("   • Test installation: python test_installation.py")
    print("   • Start application: python main.py") 
    print("   • View logs: converter.log")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()