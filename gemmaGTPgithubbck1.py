import os
import time
import psutil
import subprocess

# --- Configuration ---
history_cols = 64
history_rows = 7
left_padding = "  "
video_file = r"D:\VS\GEMMAGTP\ascii_video.txt"  # absolute path for ASCII frame
refresh_interval = 1.0  # 1 second per frame
push_interval = 60  # 60 seconds = 1 minute for git push

# Ensure folder exists
os.makedirs(os.path.dirname(video_file), exist_ok=True)

# ANSI colors
BRIGHT_BLUE = "\033[94m"
DIM_BLUE = "\033[34m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Small digits for clock
SMALL_DIGITS = {
    "0": [" ██ ","█  █","█  █","█  █","█  █"," ██ "],
    "1": ["  █ "," ██ ","  █ ","  █ ","  █ "," ███"],
    "2": [" ██ ","█  █","  █ "," ██ ","█   ","████"],
    "3": ["███ ","   █"," ██ ","   █","   █","███ "],
    "4": ["█  █","█  █","████","   █","   █","   █"],
    "5": ["████","█   ","███ ","   █","   █","███ "],
    "6": [" ██ ","█   ","███ ","█  █","█  █"," ██ "],
    "7": ["████","   █","  █ "," █  "," █  "," █  "],
    "8": [" ██ ","█  █"," ██ ","█  █","█  █"," ██ "],
    "9": [" ██ ","█  █"," ███","   █","   █"," ██ "],
    ":": ["    "," ██ ","    ","    "," ██ ","    "],
}

# --- Draw clock ---
def draw_small_clock(time_str):
    rows = [""] * 6
    for char in time_str:
        digit_rows = SMALL_DIGITS.get(char, ["    "]*6)
        for i in range(6):
            rows[i] += left_padding + digit_rows[i] + "  "
    return rows

# --- Update binary feed ---
def update_binary_feed(width, values):
    feed = []
    for val in values:
        ones_count = int(val * width)
        line = ["0"] * width
        for i in range(ones_count):
            line[-1-i] = "1"
        feed.append("".join(line))
    return feed

# --- Git push ---
def git_push():
    try:
        subprocess.run(["git", "add", "."], cwd=r"D:\VS\GEMMAGTP", check=True)
        subprocess.run(["git", "commit", "-m", "Update ASCII frame"], cwd=r"D:\VS\GEMMAGTP", check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=r"D:\VS\GEMMAGTP", check=True)
        print("Git push completed.")
    except subprocess.CalledProcessError as e:
        print("Git push failed:", e)

# --- Main loop ---
def run_music_terminal():
    prev_net = (0,0)
    prev_time = time.time()
    binary_feed = ["0"*history_cols for _ in range(history_rows)]
    last_push_time = time.time()  # track last git push

    try:
        while True:
            now = time.strftime("%H:%M:%S")
            clock_rows = draw_small_clock(now)

            # Metrics
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            net = psutil.net_io_counters()
            sent = (net.bytes_sent - prev_net[0])/1024
            recv = (net.bytes_recv - prev_net[1])/1024
            prev_net = (net.bytes_sent, net.bytes_recv)
            fps = 1/(time.time()-prev_time)
            prev_time = time.time()

            metrics = [
                f"CPU Usage: {cpu:>5}%",
                f"RAM Usage: {ram:>5}%",
                f"Disk Usage: {disk:>5}%",
                f"Network: ↑{sent:>7.1f}KB ↓{recv:>7.1f}KB",
                f"FPS: {fps:>6.1f}",
                f"Temp: N/A"
            ]

            # Binary feed
            values = [cpu/100, ram/100, disk/100, min(sent/1000,1), min(recv/1000,1), min(fps/120,1), 0.0]
            binary_feed = update_binary_feed(history_cols, values)
            for i in range(history_rows):
                binary_feed[i] = binary_feed[i][-1] + binary_feed[i][:-1]

            # Clear screen
            os.system('cls' if os.name=='nt' else 'clear')

            # Build ASCII frame
            ascii_output = [f"O View White Spaces  {now}\n"]
            for line in clock_rows:
                ascii_output.append(line.replace("█","o"))
            ascii_output.append("")
            ascii_output.extend(metrics)
            ascii_output.append("\n--- Binary Live Feed ---")
            ascii_output.extend(binary_feed)
            ascii_output.append("-"*history_cols + "\n")

            # Print to terminal
            for line in ascii_output:
                print(line)

            # Overwrite file with current frame only
            with open(video_file, "w", encoding="utf-8") as f:
                for line in ascii_output:
                    f.write(line + "\n")

            # Git push every push_interval seconds
            if time.time() - last_push_time >= push_interval:
                git_push()
                last_push_time = time.time()

            # Wait for next frame
            time.sleep(refresh_interval)

    except KeyboardInterrupt:
        print("\nMusic stopped.")

if __name__ == "__main__":
    run_music_terminal()
