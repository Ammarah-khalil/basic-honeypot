import socket
import threading
import tkinter as tk
import requests
from datetime import datetime

# ------------------- HONEYPOT CONFIG ------------------- #
PORTS = [22, 80, 21]  # SSH, HTTP, FTP
LOG_FILE = "honeypot.log"

# ------------------- GUI CONFIG ------------------- #
BG_COLOR = "#0d1117"
FG_COLOR = "#ffffff"
FONT_MAIN = ("Consolas", 11)
FONT_HEADER = ("Consolas", 14, "bold")

# ------------------- Honeypot Class ------------------- #
class Honeypot:
    def __init__(self, log_callback):
        self.log_callback = log_callback
        self.running = True

    def geoip_lookup(self, ip):
        try:
            r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=2)
            data = r.json()
            return data.get("country", "Unknown")
        except:
            return "Unknown"

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", port))
        server.listen(5)
        self.log_callback(f"[+] Listening on port {port}")
        while self.running:
            client, addr = server.accept()
            ip = addr[0]
            country = self.geoip_lookup(ip)
            event = f"[!] Connection from {ip} ({country}) on port {port} at {datetime.now()}"
            self.log_callback(event)
            with open(LOG_FILE, "a") as f:
                f.write(event + "\n")

            # Send fake banner
            if port == 22:
                client.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n")
            elif port == 80:
                client.send(b"HTTP/1.1 200 OK\r\nServer: Apache\r\n\r\n")
            elif port == 21:
                client.send(b"220 FTP server ready.\r\n")
            client.close()

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()

# ------------------- GUI Class ------------------- #
class HoneypotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Honeypot")
        self.root.geometry("800x550")
        self.root.configure(bg=BG_COLOR)

        self.text_box = tk.Text(root, bg=BG_COLOR, fg=FG_COLOR, font=FONT_MAIN)
        self.text_box.pack(fill="both", expand=True, padx=10, pady=10)

        self.clear_btn = tk.Button(root, text="Clear Logs", bg="#111a2b", fg="white",
                                   font=("Consolas", 12), command=self.clear_logs)
        self.clear_btn.pack(pady=5)

        self.honeypot = Honeypot(self.log_event)
        self.honeypot.start()

    def log_event(self, msg):
        self.text_box.insert(tk.END, msg + "\n")
        self.text_box.see(tk.END)

    def clear_logs(self):
        self.text_box.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = HoneypotGUI(root)
    root.mainloop()
