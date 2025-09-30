import psutil

for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        if proc.info['cmdline']:
            print(proc.info['pid'], proc.info['cmdline'])
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue