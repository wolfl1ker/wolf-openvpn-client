import os
import subprocess
import shutil
import sys
import urllib.request
from pathlib import Path

# Requirements:
# sudo apt-get install python3
APP_DIR = "/opt/wolfopenvpnclient"
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"
DESKTOP_FILE_PATH = "/usr/share/applications/wolfopenvpnclient.desktop"


def install_pip():
    try:
        get_pip_script = urllib.request.urlopen(GET_PIP_URL).read()
        script_path = Path(sys.executable).parent / "get-pip.py"

        with open(script_path, "wb") as script_file:
            script_file.write(get_pip_script)

        subprocess.run([sys.executable, str(script_path), "--default-pip"], check=True)
        script_path.unlink()
        print("pip installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing pip: {e}")
        sys.exit(1)


def is_package_installed(package_name):
    try:
        subprocess.run([sys.executable, "-m", "pip", "show", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def install_package(package_name):
    if not is_package_installed(package_name):
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
            print(f"{package_name} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package_name}: {e}")
            sys.exit(1)


def install_application():
    global APP_DIR
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(APP_DIR):
        os.makedirs(APP_DIR)
    else:
        print(f"The directory {APP_DIR} already exists.")
        return

    shutil.copytree(os.path.join(script_dir, "src"), os.path.join(APP_DIR, "src"))
    print("Application installed successfully.")


def create_desktop_file():
    global APP_DIR, DESKTOP_FILE_PATH
    desktop_file_content = f"""[Desktop Entry]
Type=Application
Encoding=UTF-8
Name=Wolf OpenVPN Client
Comment=Wolf OpenVPN Client
Exec=sh -c '{sys.executable} {APP_DIR}/src/main.py'
Path={APP_DIR}
Icon={APP_DIR}/src/Resources/icon.png
Terminal=false
Categories=Network;VPN;
Keywords=vpn;openvpn;wolfopenvpn;
"""
    with open(DESKTOP_FILE_PATH, "w") as desktop_file:
        desktop_file.write(desktop_file_content)
    print(f"Desktop file created at {DESKTOP_FILE_PATH}.")


if __name__ == "__main__":
    if shutil.which("pip") is None:
        install_pip()
    install_package("PySide6")
    install_application()
    create_desktop_file()
    print("Installation complete.")
