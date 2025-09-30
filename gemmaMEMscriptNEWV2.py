import psutil
import requests
from datetime import datetime

# ---------------- Helper Functions ----------------

def print_time():
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[Time]: {now}")

def print_cpu_usage():
    usage = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {usage}%")

def print_memory_usage():
    mem = psutil.virtual_memory()
    print(f"RAM Usage: {mem.percent}% ┤{'█' * int(mem.percent // 5)}{'─' * (20 - int(mem.percent // 5))}┤")
    swap = psutil.swap_memory()
    print(f"Swap Usage: {swap.percent}% ┤{'█' * int(swap.percent // 5)}{'─' * (20 - int(swap.percent // 5))}┤")

def print_disk_usage():
    disk = psutil.disk_usage('/')
    print(f"Disk Usage: {disk.percent}%")

def print_network_usage():
    net = psutil.net_io_counters()
    print(f"Network: ↑ {net.bytes_sent/1024:.1f}KB ↓ {net.bytes_recv/1024:.1f}KB")

def print_fps(fps=0.9):
    print(f"FPS: {fps}")

def print_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            temp = list(temps.values())[0][0].current
            print(f"Temp: {temp}°C")
        else:
            print("Temp: N/A")
    except:
        print("Temp: N/A")

def fetch_ascii_feed():
    url = "https://raw.githubusercontent.com/dolby3d/GEMMAGTP/refs/heads/main/ascii_video.txt"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            print(content)
        else:
            print("Failed to fetch ASCII feed.")
    except Exception as e:
        print(f"Error fetching ASCII feed: {e}")

# ---------------- Main Triggers ----------------

def ls():
    print_time()
    print_cpu_usage()
    print_memory_usage()
    print_disk_usage()
    print_network_usage()
    print_fps()
    print_temperature()
    print("-" * 64)

def mem():
    print_memory_usage()

def save():
    # For simplicity, just store a snapshot
    global saved_data
    saved_data = {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "swap": psutil.swap_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }
    print("Data saved.")

def print_data():
    if 'saved_data' in globals():
        for key, value in saved_data.items():
            print(f"{key.upper()}: {value}%")
    else:
        print("No saved data available.")

def script_report():
    print("""
Script: System & ASCII Live Monitor
Triggers:
  s     → ls() : Display system metrics snapshot
  r     → Fetch and display ASCII live feed from GitHub
  R     → Show script report summary
  mem   → Show memory summary
  save  → Save current data
  print → Print saved data
  q     → Quit/stop the script
Data Sources:
  ascii_video.txt → https://raw.githubusercontent.com/dolby3d/GEMMAGTP/refs/heads/main/ascii_video.txt
  Local system metrics via helper functions
""")

# ---------------- Main Loop ----------------

def main():
    print("Password required to access script interface.")
    password = input("Enter password: ")
    if password != "yourpassword":  # Replace with actual password
        print("Incorrect password. Exiting.")
        return

    print("Access granted. Script interface active.")
    while True:
        trigger = input("Enter trigger: ").lower()
        if trigger == 's':
            ls()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'r':
            fetch_ascii_feed()
        elif trigger == 'R':
            script_report()
        elif trigger == 'mem':
            mem()
        elif trigger == 'save':
            save()
        elif trigger == 'print':
            print_data()
        elif trigger == 'q':
            print("Exiting script.")
            break
        else:
            print("Unknown trigger. Press s, r, R, mem, save, print, or q.")

if __name__ == "__main__":
    main()
