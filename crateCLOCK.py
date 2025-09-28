import time, psutil, random
from PIL import Image, ImageDraw, ImageFont

# --- SETTINGS ---
num_frames = 100           # total frames for GIF
frame_width_px = 800
frame_height_px = 400
font_size = 15
lines_per_frame = 20
chars_per_line = 80
frame_duration_ms = 100

hearts = ["♥","<3"]
story_lines = [
    "Once upon a time in a digital world,",
    "there was a tiny heart that pulsed endlessly.",
    "It watched the CPU and RAM dance in rhythm,",
    "monitoring FPS like a guardian of speed.",
    "Data streamed like rivers of light,",
    "packets flowing up and down with grace.",
    "Every line of code told a story,",
    "every frame a snapshot of life.",
    "The heart beat faster when the network surged,",
    "and slowed when everything was calm."
]

# --- HELPER FUNCTIONS ---
def bar(val,width=20):
    filled = int(width*min(val,100)/100)
    return '█'*filled + '.'*(width-filled)

def generate_ascii_frame(frame_idx):
    # Clock & heart
    now = time.localtime()
    clock = f"{now.tm_hour:02d}:{now.tm_min:02d}:{now.tm_sec:02d}"
    pulse = (frame_idx % 10)/10
    heart = hearts[0] if pulse < 0.5 else hearts[1]
    
    # Stats
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    swap = psutil.swap_memory().percent
    net = psutil.net_io_counters()
    net_usage = min((net.bytes_sent+net.bytes_recv)/1024/50*100,100)
    
    lines = []
    for r in range(lines_per_frame):
        if r == 0:
            lines.append(f"Clock: {clock} | Heart: {heart} | FPS: 0.0")
        elif r == 1:
            lines.append(f"C:{cpu:.0f}% R:{ram:.0f}% S:{swap:.0f}% N:{net_usage:.0f}%")
        elif 2 <= r < 12:
            story_idx = r-2
            if story_idx < len(story_lines):
                line = story_lines[story_idx]
                # Endless scroll
                scroll_len = len(line) + chars_per_line
                offset = frame_idx % scroll_len
                display = (" " * chars_per_line + line)[offset:offset+chars_per_line]
                flicker = [c if random.random()>0.05 else " " for c in display]
                lines.append("".join(flicker))
            else:
                lines.append(" " * chars_per_line)
        else:
            # Bottom lines: flicker effect
            empty = "".join(" " if random.random()>0.95 else "." for _ in range(chars_per_line))
            lines.append(empty)
    return "\n".join(lines)

# --- GENERATE FRAMES ---
ascii_frames = [generate_ascii_frame(i) for i in range(num_frames)]

# --- CONVERT TO IMAGES ---
font = ImageFont.load_default()
images = []
for frame_text in ascii_frames:
    img = Image.new('RGB', (frame_width_px, frame_height_px), color='black')
    draw = ImageDraw.Draw(img)
    y = 0
    for line in frame_text.splitlines():
        draw.text((0, y), line, font=font, fill='white')
        y += font_size
    images.append(img)

# --- SAVE GIF ---
images[0].save(
    'ascii_dashboard.gif',
    save_all=True,
    append_images=images[1:],
    duration=frame_duration_ms,
    loop=0
)

print("ASCII dashboard GIF saved as ascii_dashboard.gif!")
