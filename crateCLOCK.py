import time
from datetime import datetime
import os

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# ASCII digits 0-9, colon, and dash
digits = {
    "0": [" ███ ", "█   █", "█   █", "█   █", " ███ "],
    "1": ["  █  ", " ██  ", "  █  ", "  █  ", " ███ "],
    "2": [" ███ ", "    █", " ███ ", "█    ", "█████"],
    "3": ["████ ", "    █", " ███ ", "    █", "████ "],
    "4": ["█  █ ", "█  █ ", "█████", "   █ ", "   █ "],
    "5": ["█████", "█    ", "████ ", "    █", "████ "],
    "6": [" ███ ", "█    ", "████ ", "█   █", " ███ "],
    "7": ["█████", "    █", "   █ ", "  █  ", "  █  "],
    "8": [" ███ ", "█   █", " ███ ", "█   █", " ███ "],
    "9": [" ███ ", "█   █", " ████", "    █", " ███ "],
    ":": ["     ", "  █  ", "     ", "  █  ", "     "],
    "-": ["     ", "     ", "█████", "     ", "     "]
}

def print_ascii_text(text, color=RESET):
    lines = [""] * 5
    for char in text:
        for i in range(5):
            lines[i] += digits.get(char, ["     "]*5)[i] + "  "
    for line in lines:
        print(color + line + RESET)

def print_seconds_bar(seconds):
    bar_length = 60
    filled_length = int(bar_length * seconds / 60)
    bar = GREEN + "█" * filled_length + RESET + "-" * (bar_length - filled_length)
    print(f"\nSeconds: [{bar}] {seconds:02d}/60")

try:
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        now = datetime.now()
        hours = now.strftime("%H")
        minutes = now.strftime("%M")
        seconds = now.second
        current_time = f"{hours}:{minutes}:{seconds:02d}"
        current_date = now.strftime("%Y-%m-%d")

        print("🕒 Time:")
        print_ascii_text(current_time, CYAN)
        print_seconds_bar(seconds)

        print("\n📅 Date:")
        print_ascii_text(current_date.replace("-", "-"), YELLOW)

        time.sleep(1)
except KeyboardInterrupt:
    print("\nDashboard stopped.")
