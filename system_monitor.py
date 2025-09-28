import time
import psutil
import datetime
import os

# ----------------- Helper Functions -----------------
def print_time():
    now = datetime.datetime.now()
    print(f"Time: {now.strftime('%H:%M:%S')}")

def print_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=0.1)
    print(f"CPU Usage: {cpu_percent:.1f}%")

def print_memory_usage():
    mem = psutil.virtual_memory()
    print(f"RAM Usage: {mem.percent:.1f}% ({mem.used // (1024**2)}MB/{mem.total // (1024**2)}MB)")

def build_memory_bar():
    mem = psutil.virtual_memory()
    total_blocks = 30
    filled_blocks = int(mem.percent / 100 * total_blocks)
    bar = "[" + "#" * filled_blocks + "-" * (total_blocks - filled_blocks) + "]"
    print(f"Memory Bar: {bar}")

def print_disk_usage():
    disk = psutil.disk_usage('/')
    print(f"Disk Usage: {disk.percent:.1f}% ({disk.used // (1024**3)}GB/{disk.total // (1024**3)}GB)")

def print_network_usage():
    net1 = psutil.net_io_counters()
    time.sleep(0.5)
    net2 = psutil.net_io_counters()
    sent = (net2.bytes_sent - net1.bytes_sent) / 1024
    recv = (net2.bytes_recv - net1.bytes_recv) / 1024
    print(f"Network: ↑{sent:.1f} KB/s ↓{recv:.1f} KB/s")

def print_fps():
    # Dummy FPS simulation (replace with actual FPS if needed)
    import random
    fps = random.randint(50, 144)
    print(f"FPS: {fps}")

def print_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                for entry in entries:
                    print(f"{name} Temp: {entry.current}°C")
        else:
            print("Temperature: N/A")
    except:
        print("Temperature: N/A")

def print_swap_usage():
    swap = psutil.swap_memory()
    print(f"Swap Usage: {swap.percent:.1f}% ({swap.used // (1024**2)}MB/{swap.total // (1024**2)}MB)")

# ----------------- Main Loop -----------------
try:
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
        print_time()
        print_cpu_usage()
        print_memory_usage()
        build_memory_bar()
        print_disk_usage()
        print_network_usage()
        print_fps()
        print_temperature()
        print_swap_usage()
        time.sleep(1)  # Update every second
except KeyboardInterrupt:
    print("Monitoring stopped.")
