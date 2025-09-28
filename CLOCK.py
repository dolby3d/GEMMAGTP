import time, psutil, random, os

# --- SETTINGS ---
lines_per_frame = 15
chars_per_line = 60
feed_lines = 5
frames = 1000  # run for 1000 updates
hearts = ["♥","<3"]
story_lines = [
    "Live ASCII Dashboard",
    "Monitoring CPU, RAM, Network",
    "The heart pulses with system life"
]

# --- HELPERS ---
def bar(val, width=20):
    filled = int(width*min(val,100)/100)
    return '█'*filled + '.'*(width-filled)

def generate_feed_line():
    cpu=psutil.cpu_percent()
    ram=psutil.virtual_memory().percent
    net=psutil.net_io_counters()
    net_usage=min((net.bytes_sent+net.bytes_recv)/1024/50*100,100)
    events=["OK","WARN","ERROR","CONNECT","DISCONNECT","UPDATE","IDLE"]
    event=random.choice(events)
    line=f"C:{cpu:02.0f}% R:{ram:02.0f}% N:{net_usage:02.0f}% {event}"
    if len(line)<chars_per_line: line+=" "*(chars_per_line-len(line))
    return line

def generate_ascii_frame():
    now=time.localtime()
    clock=f"{now.tm_hour:02d}:{now.tm_min:02d}:{now.tm_sec:02d}"
    pulse=(int(time.time()*2)%2)
    heart=hearts[pulse]

    lines=[f"Clock: {clock} | Heart: {heart}"]
    cpu=psutil.cpu_percent()
    ram=psutil.virtual_memory().percent
    net=psutil.net_io_counters()
    net_usage=min((net.bytes_sent+net.bytes_recv)/1024/50*100,100)
    lines.append(f"C:{bar(cpu)} R:{bar(ram)} N:{bar(net_usage)}")

    # Story lines
    for r in range(2, lines_per_frame-feed_lines):
        story_idx=r-2
        if story_idx<len(story_lines):
            line=story_lines[story_idx]
            scroll_len=len(line)+chars_per_line
            offset=int(time.time())%scroll_len
            display=(" "*chars_per_line+line)[offset:offset+chars_per_line]
            flicker=[c if random.random()>0.05 else " " for c in display]
            lines.append("".join(flicker))
        else:
            lines.append(" "*chars_per_line)

    # Bottom live feed
    for _ in range(feed_lines):
        lines.append(generate_feed_line())

    return "\n".join(lines)

# --- MAIN LOOP ---
for frame_idx in range(frames):
    os.system('cls' if os.name=='nt' else 'clear')
    print(generate_ascii_frame())
    time.sleep(0.2)  # adjust refresh rate
