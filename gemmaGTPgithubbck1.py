import os
import time
import psutil

# --- Configuration ---
history_cols = 64
history_rows = 7
left_padding = "  "

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

# --- Print binary feed with gradient ---
def print_binary_feed(feed):
    for line in feed:
        output = ""
        for i, char in enumerate(line):
            pos_ratio = i / len(line)
            if char == "1":
                if pos_ratio > 0.66:
                    output += BRIGHT_BLUE + "1" + RESET
                elif pos_ratio > 0.33:
                    output += BRIGHT_BLUE + "1" + RESET
                else:
                    output += DIM_BLUE + "1" + RESET
            else:
                output += "0"
        print(output)

# --- Main loop ---
def run_music_terminal():
    prev_net = (0,0)
    prev_time = time.time()
    binary_feed = ["0"*history_cols for _ in range(history_rows)]
    
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

            # Song title
            print(f"{CYAN}O View White Spaces{RESET}\n")

            # Clock
            for line in clock_rows:
                print(f"{BRIGHT_BLUE}{line}{RESET}")
            print()

            # Metrics
            for metric in metrics:
                print(f"{GREEN}{metric}{RESET}")

            # Binary feed
            print(f"\n{CYAN}--- Binary Live Feed ---{RESET}")
            print_binary_feed(binary_feed)
            print(f"{CYAN}{'-'*history_cols}{RESET}")

            # Beat rhythm (0.5s per update)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nMusic stopped.")

if __name__ == "__main__":
    run_music_terminal()
