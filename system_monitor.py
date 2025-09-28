# Assuming your monitoring functions are already defined in memory

import time

try:
    while True:
        print("\033c", end="")  # Clear terminal each update
        print_time()
        print_cpu_usage()
        print_memory_usage()
        print_disk_usage()
        print_network_usage()
        build_memory_bar()
        print_fps()
        print_temperature()
        print_swap_usage()
        time.sleep(1)  # Update every second
except KeyboardInterrupt:
    print("Monitoring stopped.")
