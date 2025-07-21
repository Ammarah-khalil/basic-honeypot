 Advanced Honeypot with GUI

This project is a **low-interaction honeypot** built in Python. It monitors multiple ports (SSH, HTTP, and FTP) and logs all connection attempts in real-time. The project features a **dark-blue GUI** for a hacker-style look.

---
Features
- **Monitors ports 22 (SSH), 80 (HTTP), and 21 (FTP)**.
- Displays **real-time connection logs** with timestamp and IP address.
- **Fake service banners** to simulate real services:
  - SSH: `SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5`
  - HTTP: `HTTP/1.1 200 OK`
  - FTP: `220 FTP server ready.`
- **GeoIP Lookup**: Shows the attacker’s country using the `ipinfo.io` API.
- **Dark-blue GUI** with a **Clear Log** button.
- Logs are saved to `honeypot.log` for further analysis.

---

Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Ammarah-khalil/honeypot.git
cd honeypot
pip install requests
