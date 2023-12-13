# Wolf OpenVPN Client

OpenVPN3 Client for linux based systems, built on Python3 using PySide6

![System](https://img.shields.io/badge/system-Linux-blue)
![OpenVPN](https://img.shields.io/badge/OpenVPN-3.x-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![PySide6](https://img.shields.io/badge/PySide-6.6.x-green)

![Version](https://img.shields.io/badge/version-1.0-brightgreen)
![Status](https://img.shields.io/badge/status-stable-brightgreen)
![Language](https://img.shields.io/badge/language-Python-red)

## Content

- [Wolf OpenVPN Client](#wolf-openvpn-client)
    - [Table of Contents](#content)
    - [Features](#features)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Known Issues](#known-issues)
    - [License](#license)

## Features

- GUI for OpenVPN client for linux ([site](https://openvpn.net/openvpn-client-for-linux/))
- Multiple connection profiles based on .ovpn configuration files, with easy selection
- Saving configuration files within the application
- Providing connection statistics

## Installation

Required:
- [OpenVPN3 console client](https://openvpn.net/openvpn-client-for-linux/)
- Python3, pip
- _optional_ PySide6.4 or PySide6.6
- Troubleshooting / __Linux Mint__: libxcb-cursor0

```bash
# Example installation
git clone https://github.com/wolfl1ker/wolf-openvpn-client.git
cd wolf-openvpn-client
sudo python3 install.py
cd .. && rm -rf wolf-openvpn-client
```

## Usage

Via the app icon in applications menu

![step0.png](tutorial%2Fstep0.png)

To add new connection-profile: File->Profiles

![step1.png](tutorial%2Fstep1.png)

The Add button opens the "Add Profile" dialog, where a display name and 
configuration file can be chosen. To delete a saved profile, choose the 
profile for deletion and click on the Delete button.

![step2.png](tutorial%2Fstep2.png)

To connect: select the profile for connection and click connect button.

To disconnect: click on disconnect button.

On exit, the application will ask if you want to disconnect.

![step3.png](tutorial%2Fstep3.png)

## Known Issues

- Known Issues from PySide: https://wiki.qt.io/Qt_6.4_Known_Issues#Wayland
- Holding the left mouse button (LMB) on the Menu bar and moving the cursor to another Menu bar can crash Gnome.

## License

Provided via [LICENSE](LICENSE) file 

