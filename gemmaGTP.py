def run_monitoring():
    prev_net = None
    fps_start = time.time()
    frame_count = 0

    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            frame_count += 1
            fps_start, frame_count, fps = update_fps(fps_start, frame_count)
            
            prev_net = print_system_table(prev_net, fps)

            # Key triggers
            if keyboard.is_pressed('i'):
                print("\n--- Basic Info ---")
                print_system_table(prev_net, fps)
                time.sleep(0.5)

            if keyboard.is_pressed('i1'):
                print("\n=== Detailed Diagnostics ===")
                print("Per-core CPU Usage:", psutil.cpu_percent(percpu=True))
                print("Virtual Memory:", psutil.virtual_memory())
                print("Swap Memory:", psutil.swap_memory())
                print("Disk Usage:", psutil.disk_usage('/'))
                print("Network Stats:", psutil.net_io_counters())
                if hasattr(psutil, "sensors_temperatures"):
                    temps = psutil.sensors_temperatures()
                    print("Temperatures:", temps if temps else "N/A")
                print("============================\n")
                time.sleep(0.5)

            if keyboard.is_pressed('h'):
                print("\n=== Shortcuts Help ===")
                print("s  → Load script")
                print("m  → Start monitoring")
                print("i  → Show basic info (table)")
                print("i1 → Show detailed diagnostics")
                print("h  → Show this help message")
                print("q  → Quit monitoring")
                print("=======================\n")
                time.sleep(1)

            if keyboard.is_pressed('q'):
                print("GEMMA:> EXITING SYSTEM MONITOR...")
                break

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nGEMMA:> MONITORING STOPPED.")
