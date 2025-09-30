# secure_monitor_final.py
import psutil
import time
import requests
from datetime import datetime
import keyboard
import getpass
import functools
import sys
import os
import hashlib

# =========================
# Configuration
# =========================
USERNAME = "dolby"
# Default password: gemma123 (hashed)
PASSWORD_HASH = hashlib.sha256("gemma123".encode()).hexdigest()
ASCII_URL = "https://raw.githubusercontent.com/dolby3d/GEMMAGTP/refs/heads/main/ascii_video.txt"

logged_in = False

# =========================
# Password Utilities
# =========================
def verify_password(input_password):
    return hashlib.sha256(input_password.encode()).hexdigest() == PASSWORD_HASH

def login():
    global logged_in
    print("=== LOGIN REQUIRED ===")
    user = input("Username: ")
    pwd = getpass.getpass("Password: ")
    if user == USERNAME and verify_password(pwd):
        logged_in = True
        print("✅ Login successful. Hotkeys are now active.")
    else:
        print("❌ Invalid username or password.")

@functools.wraps
def require_login(prompt_on_call=True):
    """Decorator to protect functions, requires login."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            global logged_in
            if logged_in:
                return func(*args, **kwargs)
            if not sys.stdin.isatty():
                print(f"❌ Action '{func.__name__}' blocked. Login required.")
                return None
            if prompt_on_call:
                login()
                if logged_in:
                    return func(*args, **kwargs)
                else:
                    print(f"❌ Action '{func.__name__}' blocked due to failed login.")
            else:
                print(f"❌ Action '{func.__name__}' blocked. Login required.")
        return wrapper
    return decorator

# =========================
# System Metrics (Protected)
# =========================
@require_login()
def print_time():
    print(f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@require_login()
def print_cpu_usage():
    usage = psutil.cpu_percent(percpu=True)
    total = psutil.cpu_percent()
    for i, u in enumerate(usage):
        print(f"Core {i+1}: {u}%")
    print(f"Total CPU Usage: {total}%")

@require_login()
def build_memory_bar(used, total, length=20):
    if total == 0: return "[--------------------] 0%"
    filled = int(length * used // total)
    bar = '█'*filled + '-'*(length-filled)
    percent = round((used/total)*100)
    return f"[{bar}] {percent}%"

@require_login()
def print_memory_usage():
    mem = psutil.virtual_memory()
    bar = build_memory_bar(mem.used, mem.total)
    print(f"🧠 RAM Usage: {mem.used/(1024**3):.1f} GB / {mem.total/(1024**3):.1f} GB")
    print(f"Memory Bar: {bar}")

@require_login()
def print_disk_usage():
    disk = psutil.disk_usage('/')
    bar = build_memory_bar(disk.used, disk.total)
    print(f"💾 Disk Usage: {disk.used/(1024**3):.1f} GB / {disk.total/(1024**3):.1f} GB")
    print(f"Disk Bar: {bar}")

@require_login()
def print_network_usage(interval=1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()
    up = (net2.bytes_sent - net1.bytes_sent)/(1024**2)
    down = (net2.bytes_recv - net1.bytes_recv)/(1024**2)
    print(f"📶 Upload: {up:.2f} MB/s, Download: {down:.2f} MB/s")

@require_login()
def print_fps(fps=60):
    print(f"🎮 FPS: {fps}")

@require_login()
def print_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            print(f"🌡 CPU Temp: {temps['coretemp'][0].current}°C")
        else:
            for k,v in temps.items():
                if v:
                    print(f"🌡 {k}: {v[0].current}°C")
                    return
            print("🌡 CPU Temp: N/A")
    except Exception:
        print("🌡 CPU Temp: N/A")

@require_login()
def print_swap_usage():
    swap = psutil.swap_memory()
    bar = build_memory_bar(swap.used, swap.total)
    print(f"🔄 Swap Usage: {swap.used/(1024**3):.1f} GB / {swap.total/(1024**3):.1f} GB")
    print(f"Swap Bar: {bar}")

# =========================
# High-Level Actions
# =========================
@require_login()
def ls():
    print_time()
    print_cpu_usage()
    print_memory_usage()
    print_disk_usage()
    print_network_usage()
    print_fps()
    print_temperature()
    print_swap_usage()

@require_login()
def fetch_ascii_video():
    try:
        r = requests.get(ASCII_URL, timeout=10)
        if r.status_code==200:
            print(r.text)
        else:
            print(f"Failed to fetch ASCII video ({r.status_code})")
    except Exception as e:
        print(f"Error: {e}")

@require_login()
def show_help():
    print("""
=== HOTKEY HELP MENU ===
s   → Display full system snapshot
r   → Fetch & display ASCII video
R   → Display script report
mem → Display memory summary
save / save_script / save script → Save current script
pass → Change password (dolby only)
q   → Quit system monitor
h   → Show this help menu
========================
""")

# =========================
# Save Functions
# =========================
def _write_script_to_disk(path="monitor_saved.py"):
    try:
        this_file = os.path.abspath(__file__)
        with open(this_file,'r',encoding='utf-8') as f:
            content = f.read()
        with open(path,'w',encoding='utf-8') as f_out:
            f_out.write(content)
        return True
    except Exception as e:
        print(f"Error saving script: {e}")
        return False

@require_login()
def save(path="monitor_saved.py"):
    if _write_script_to_disk(path):
        print(f"✅ Script saved to {path}")
    else:
        print("❌ Save failed.")

@require_login()
def save_script(path="monitor_saved.py"):
    return save(path)

@require_login()
def save_script_alias(path="monitor_saved.py"):
    return save(path)

# =========================
# Password Management
# =========================
@require_login()
def change_password():
    global PASSWORD_HASH
    if USERNAME != "dolby":
        print("❌ Only 'dolby' can change password.")
        return
    current = getpass.getpass("Enter current password: ")
    if not verify_password(current):
        print("❌ Incorrect current password.")
        return
    new_pwd = getpass.getpass("Enter new password: ")
    confirm = getpass.getpass("Confirm new password: ")
    if new_pwd != confirm:
        print("❌ Passwords do not match.")
        return
    PASSWORD_HASH = hashlib.sha256(new_pwd.encode()).hexdigest()
    print("✅ Password changed successfully.")

# =========================
# Command Processor
# =========================
def process_command(command):
    cmd = command.lower().strip()
    if cmd in ["save", "save_script", "save script"]:
        save()
    elif cmd=="pass":
        change_password()
    elif cmd=="s":
        ls()
    elif cmd=="r":
        fetch_ascii_video()
    elif cmd=="R":
        show_help()
    elif cmd=="mem":
        print_memory_usage()
    elif cmd=="h":
        show_help()
    elif cmd=="q":
        if _confirm_quit():
            print("Quitting monitor... ✅")
            sys.exit(0)
    else:
        print(f"❌ Unknown command '{cmd}'")

# =========================
# Quit Confirm
# =========================
@require_login(prompt_on_call=False)
def _confirm_quit():
    ans = input("Confirm quit? (y/N): ").lower()
    return ans=='y'

# =========================
# Monitor Loop
# =========================
def monitor_loop():
    print("System monitor starting. Login required.")
    print("Press 'h' for help after login.")
    try:
        while True:
            # Hotkeys
            if keyboard.is_pressed('s'):
                ls(); time.sleep(0.25)
            elif keyboard.is_pressed('r'):
                fetch_ascii_video(); time.sleep(0.25)
            elif keyboard.is_pressed('R'):
                show_help(); time.sleep(0.25)
            elif keyboard.is_pressed('mem'):
                print_memory_usage(); time.sleep(0.25)
            elif keyboard.is_pressed('h'):
                show_help(); time.sleep(0.25)
            elif keyboard.is_pressed('q'):
                if _confirm_quit():
                    print("Quitting monitor... ✅"); break
                time.sleep(0.25)
            elif sys.stdin.isatty():
                if keyboard.is_pressed('enter'):
                    command = input("Command: ").strip()
                    process_command(command)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nMonitor interrupted by user.")

# =========================
# Import Guard
# =========================
def _import_guard():
    if __name__ != "__main__":
        if sys.stdin.isatty():
            print("Note: secure_monitor imported. All functions require login.")
_import_guard()

# =========================
# Run Directly
# =========================
if __name__ == "__main__":
    monitor_loop()
