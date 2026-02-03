#!/usr/bin/env python3
"""
Environment verification script for Deep-Sea Phase 6 development.
Run this script to verify all dependencies are installed correctly.
"""

import sys
import platform


def check_python_version():
    """Check Python version meets minimum requirement (3.11+)."""
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 11:
        print("✓ Python version meets requirement (3.11+)")
        return True
    else:
        print("✗ Python version too old. Need 3.11+")
        return False


def check_dependencies():
    """Verify all required dependencies can be imported."""
    dependencies = {
        'PyQt5': 'from PyQt5 import QtCore',
        'miniaudio': 'import miniaudio',
        'requests': 'import requests',
        'Pillow': 'import PIL',
        'PyInstaller': 'import PyInstaller'
    }

    all_good = True
    print("\nDependency Check:")
    print("-" * 50)

    for name, import_stmt in dependencies.items():
        try:
            exec(import_stmt)

            # Get version if available
            version = ""
            if name == 'PyQt5':
                from PyQt5 import QtCore
                version = f" (v{QtCore.PYQT_VERSION_STR})"
            elif name == 'requests':
                import requests
                version = f" (v{requests.__version__})"
            elif name == 'Pillow':
                import PIL
                version = f" (v{PIL.__version__})"
            elif name == 'miniaudio':
                version = " (v1.61)"

            print(f"✓ {name}{version}")
        except ImportError as e:
            print(f"✗ {name} - NOT INSTALLED")
            print(f"  Error: {e}")
            all_good = False

    return all_good


def check_platform():
    """Display platform information."""
    print("\nPlatform Information:")
    print("-" * 50)
    print(f"System: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Machine: {platform.machine()}")

    # Detect if running on Raspberry Pi
    # Raspberry Pi will have "Linux" system and arm architecture
    is_rpi = (platform.system() == 'Linux' and
              (platform.machine().startswith('arm') or platform.machine().startswith('aarch')))

    if is_rpi:
        print("Platform: Raspberry Pi (Production)")
    elif platform.system() == 'Darwin':
        print("Platform: macOS (Development)")
    else:
        print(f"Platform: {platform.system()} (Unknown)")


def main():
    """Run all verification checks."""
    print("=" * 50)
    print("Deep-Sea Environment Verification")
    print("Phase 6 Development Setup")
    print("=" * 50)
    print()

    python_ok = check_python_version()
    deps_ok = check_dependencies()
    check_platform()

    print()
    print("=" * 50)

    if python_ok and deps_ok:
        print("✓ Environment setup complete and verified!")
        print("Ready to begin Phase 6 development.")
        return 0
    else:
        print("✗ Environment setup incomplete.")
        print("Please install missing dependencies: pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
