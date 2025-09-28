import time, psutil, threading, atexit
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# ---------- ASCII Clock ----------
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
    ":": ["     ", "  █  ", "     ", "  █  ", "     "]
}

hearts = [" <3 ", " <♥ ", " <💖 ", " <💘 "]

# ---------- GIF Export ----------
gif_images = []
font_path = "C:/Windows/Fonts/consola.ttf"  # monospace font
font_size = 18
font = ImageFont.truetype(font_path, font_size)
frame_width_px = 800
frame_height_px = 400

def ascii_clock():
    t = datetime.now().strftime("%H:%M:%S")
    lines = [""]*5
    for c in t:
        for i in range(5):
            lines[i] += digits.get(c, ["     "]*5)[i] + "  "
    double_lines = []
    for l in lines:
        double_lines.append(l)
        double_lines.append(l)
    return double_lines

def heartbeat(index):
    return hearts[index % len(hearts)]

def capture_gif_frame(frame_text):
    img = Image.new("RGB", (frame_width_px, frame_height_px), "black")
    draw = ImageDraw.Draw(img)
    y = 0
    for line in frame_text.splitlines():
        draw.text((0, y), line, font=font, fill="white")
        y += font_size
    gif_images.append(img)

# ---------- Save GIF on exit ----------
def save_gif_on_exit():
    if gif_images:
        gif_images[0].save(
            'ascii_dashboard.gif',
            save_all=True,
            append_images=gif_images[1:],
            duration=100,  # GIF speed in ms
            loop=0
        )
        print("\nGIF saved as ascii_dashboard.gif!")

atexit.register(save_gif_on_exit)

# ---------- FPS Counter ----------
class FPSCounter:
    def __init__(self):
        self.last_time = time.perf_counter()
        self.frames = 0
        self.fps = 0
    def update(self):
        self.frames += 1
        now = time.perf_counter()
        dt = now - self.last_time
        if dt >= 1.0:
            self.fps = self.frames / dt
            self.frames = 0
            self.last_time = now
        return self.fps

# ---------- Disk Bars ----------
def disk_bars():
    lines = []
    for d in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(d.mountpoint)
            filled = int(20*usage.percent/100)
            bar = '█'*filled + '-'*(20-filled)
            lines.append(f"{d.device}: [{bar}] {usage.percent:3.0f}%")
        except:
            continue
    return lines

# ---------- GPU Stats ----------
try:
    import pynvml
    pynvml.nvmlInit()
    gpu_available = True
except:
    gpu_available = False

def gpu_stats():
    if not gpu_available:
        return ["GPU: detected/unavailable"]
    lines = []
    for i in range(pynvml.nvmlDeviceGetCount()):
        h = pynvml.nvmlDeviceGetHandleByIndex(i)
        name = pynvml.nvmlDeviceGetName(h).decode()
        util = pynvml.nvmlDeviceGetUtilizationRates(h)
        mem = pynvml.nvmlDeviceGetMemoryInfo(h)
        mem_percent = mem.used / mem.total * 100
        lines.append(f"GPU{i} ({name}): {util.gpu:3d}% | Mem: {mem_percent:3.0f}%")
    return lines

# ---------- Terminal Animation ----------
fps_counter = FPSCounter()
heart_index = 0

try:
    while True:
        print("\033[H\033[J", end="")  # clear screen

        clk = ascii_clock()
        hb = heartbeat(heart_index)

        # Print big clock + heartbeat centered
        for l in clk:
            total_len = len(l) + len(hb)
            padding = max(0, (80 - total_len)//2)
            print(" "*padding + l + hb)

        print("-"*80)

        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent
        net = psutil.net_io_counters()
        net_usage = (net.bytes_sent + net.bytes_recv)/1024

        stats_line = f"CPU:{cpu_percent:3.0f}% RAM:{ram_percent:3.0f}% NET:{net_usage:6.1f} KB"
        fps_line = f"FPS: {fps_counter.update():5.1f}"

        disk_lines = disk_bars()
        gpu_lines = gpu_stats()

        bottom_lines = [stats_line.ljust(40)+fps_line.rjust(40)]
        bottom_lines += disk_lines + gpu_lines
        bottom_lines += ["[Gemma -> append box -> colors updated]"]

        for line in bottom_lines:
            print(line.ljust(80))

        # Capture GIF
        full_frame_text = "\n".join(clk + bottom_lines)
        capture_gif_frame(full_frame_text)

        heart_index += 1
        time.sleep(0.05)  # ~20 FPS live
except KeyboardInterrupt:
    print("\nDashboard stopped. Saving GIF...")
