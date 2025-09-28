import time
import psutil
import keyboard  # For detecting key presses

# --- Helper Functions ---
def print_time():
    print(f"Time: {time.strftime('%H:%M:%S')}")

def print_cpu_usage():
    usage = psutil.cpu_percent()
    bar = build_bar(usage)
    print(f"CPU Usage: {usage}% {bar}")

def print_memory_usage():
    mem = psutil.virtual_memory()
    bar = build_bar(mem.percent)
    print(f"RAM Usage: {mem.percent}% {bar}")

def print_disk_usage():
    disk = psutil.disk_usage('/')
    bar = build_bar(disk.percent)
    print(f"Disk Usage: {disk.percent}% {bar}")

def print_network_usage(prev):
    net = psutil.net_io_counters()
    up = (net.bytes_sent - prev[0]) / 1024
    down = (net.bytes_recv - prev[1]) / 1024
    print(f"Network: ↑{up:.1f} KB/s ↓{down:.1f} KB/s")
    return (net.bytes_sent, net.bytes_recv)

def print_fps(fps):
    print(f"FPS: {fps}")

def print_temperature():
    # Optional: CPU temp if available
    temps = psutil.sensors_temperatures()
    if "coretemp" in temps:
        temp = temps["coretemp"][0].current
        print(f"CPU Temp: {temp}°C")

def print_swap_usage():
    swap = psutil.swap_memory()
    bar = build_bar(swap.percent)
    print(f"Swap Usage: {swap.percent}% {bar}")

def build_bar(percent, length=20):
    filled = int(length * percent / 100)
    return '█' * filled + '-' * (length - filled)

# --- Main Script ---
def run_monitor():
    prev_net = (0, 0)
    fps = 60  # Example FPS, you can calculate dynamically
    while True:
        print("\033c", end="")  # Clear terminal
        print_time()
        print_cpu_usage()
        print_memory_usage()
        print_disk_usage()
        prev_net = print_network_usage(prev_net)
        print_fps(fps)
        print_temperature()
        print_swap_usage()
        time.sleep(1)

# --- Trigger with 's' key ---
def load_script():
    print("System Monitor Triggered! Press Ctrl+C to stop.")
    run_monitor()

keyboard.add_hotkey('s', load_script)

# Keep script running to detect key press
print("Press 's' to start system monitor...")
keyboard.wait()
