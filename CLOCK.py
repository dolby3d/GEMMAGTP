import time
import psutil
import os
import subprocess

# --- Configuration ---
repo_path = "C:/path/to/your/repo"  # Change this to your local repo path
branch = "main"

# --- Logging function ---
def log_system(filename):
    prev_net = (0, 0)
    prev_time = time.time()
    with open(filename, "a") as f:
        try:
            while True:
                # Collect system metrics
                cpu = psutil.cpu_percent()
                mem = psutil.virtual_memory().percent
                disk = psutil.disk_usage('/').percent
                net = psutil.net_io_counters()
                sent = (net.bytes_sent - prev_net[0]) / 1024
                recv = (net.bytes_recv - prev_net[1]) / 1024
                prev_net = (net.bytes_sent, net.bytes_recv)
                fps = 1 / (time.time() - prev_time)
                prev_time = time.time()
                
                # Build output
                output = [
                    f"Time: {time.strftime('%H:%M:%S')}",
                    f"CPU Usage: {cpu}%",
                    f"RAM Usage: {mem}%",
                    f"Disk Usage: {disk}%",
                    f"Network: ↑{sent:.1f}KB ↓{recv:.1f}KB",
                    f"FPS: {fps:.1f}",
                ]
                
                # Print to terminal
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n".join(output))
                
                # Save to file
                f.write("\n".join(output) + "\n" + "-"*40 + "\n")
                
                # Wait 1 second
                time.sleep(1)
                
                # Commit & push every 60 seconds
                if int(time.time()) % 60 == 0:
                    push_to_github(filename)
                    
        except KeyboardInterrupt:
            print("Monitoring stopped.")

# --- Git push function ---
def push_to_github(filename):
    try:
        subprocess.run(["git", "-C", repo_path, "add", filename], check=True)
        subprocess.run(["git", "-C", repo_path, "commit", "-m", f"Update {filename}"], check=True)
        subprocess.run(["git", "-C", repo_path, "push", "origin", branch], check=True)
        print(f"Pushed {filename} to GitHub!")
    except subprocess.CalledProcessError:
        print("Git push failed. Check your repository or network.")

# --- Main ---
if __name__ == "__main__":
    log_filename = f"system_log_{time.strftime('%Y-%m-%d')}.txt"
    log_system(log_filename)
