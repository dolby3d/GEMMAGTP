import time, psutil, random

# --- SETTINGS ---
fps_target = 30
frame_interval = (1/fps_target) * 1.33  # 1/3 slower
frames = 0
start = time.time()
net_start = psutil.net_io_counters()

cpu = ram = swap = net_usage = sent = recv = 0
last_update = start
fps_smooth = 0.0

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

# --- HELPERS ---
def bar(val,width=20):
    filled = int(width*min(val,100)/100)
    return '█'*filled + '.'*(width-filled)

def smooth_clock():
    t = time.localtime()
    sec = time.time() % 60
    return f"{t.tm_hour:02d}:{t.tm_min:02d}:{int(sec):02d}.{int((sec-int(sec))*10)}"

def format_line(text, width=80):
    return text[:width].ljust(width)

# --- MAIN LOOP ---
try:
    while True:
        now = time.time()
        # Update heavy stats every 1s
        if now - last_update >= 1.0:
            last_update = now
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            swap = psutil.swap_memory().percent
            net = psutil.net_io_counters()
            sent = (net.bytes_sent - net_start.bytes_sent)/1024
            recv = (net.bytes_recv - net_start.bytes_recv)/1024
            net_start = net
            net_usage = min((sent+recv)/50*100,100)

        # Smooth heart pulse
        pulse = (frames % fps_target)/fps_target
        heart = hearts[0] if pulse < 0.5 else hearts[1]

        # Smooth clock
        clock = smooth_clock()

        # Smoothed FPS
        elapsed = now - start
        raw_fps = frames/elapsed if elapsed>0 else 0
        fps_smooth = fps_smooth*0.8 + raw_fps*0.2

        # Clear screen
        print("\033[2J\033[H", end='')

        # Build 20-line frame
        for r in range(20):
            if r == 0:
                # Top line: clock + heart + FPS
                print(format_line(f"Clock: {clock} | Heart: {heart} | FPS: {fps_smooth:.1f}"))
            elif r == 1:
                stats = f"C:{cpu:.0f}% R:{ram:.0f}% S:{swap:.0f}% N:{net_usage:.0f}%"
                print(format_line(stats))
            elif 2 <= r < 12:
                story_idx = r - 2
                line = story_lines[story_idx]
                total_len = len(line) + 80
                # Left -> right scroll
                offset = total_len - (frames % total_len)
                display = (" " * 80 + line)[offset:offset+80]

                # Tiny flicker effect
                flicker = [c if random.random() > 0.05 else " " for c in display]
                print(format_line("".join(flicker)))
            else:
                # Bottom lines: random flicker for full-screen effect
                empty = "".join(" " if random.random() > 0.95 else "." for _ in range(80))
                print(format_line(empty))

        frames += 1
        time.sleep(frame_interval)

except KeyboardInterrupt:
    print("\033[0m")
    print("Full-screen TV-style dashboard stopped.")
