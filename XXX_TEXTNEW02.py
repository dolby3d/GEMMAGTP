
save_script()


Key	Target	Action / Description
s	Root / Dashboard	Reload root Gemma Dashboard (main script)
ls	Root / Dashboard	Safe reload permanent gemma_monitor.py
i	Root / Dashboard	Show basic system info (CPU, RAM, Disk, FPS)
i1	Root / Dashboard	Show detailed diagnostics (per-core CPU, memory, disk, network, temps)
h	Root / Dashboard	Print help / all key commands & script info
q	Root / Dashboard	Quit monitoring
g	ASCII_GPU child	Trigger GPU ASCII Capture
v	ASCII_Video child	Trigger ASCII Video Player
p	Python_Sim child	Trigger Python Simulation
(future)	CompactSummary child	Trigger unified memory summary (if implemented)




🔹 GEMMA DASHBOARD CHEAT SHEET

Script Info

Name: gemma_monitor.py

Folder: gemma_dashboard/

Permanent copy: Protected and auto-reloadable (s or ls)

Key Triggers & Actions

Key	Target	Action / Description
s	Root / Dashboard	Reload root Gemma Dashboard (main script)
ls	Root / Dashboard	Safe reload permanent gemma_monitor.py
i	Root / Dashboard	Show basic system info (CPU, RAM, Disk, FPS)
i1	Root / Dashboard	Show detailed diagnostics (per-core CPU, memory, disk, network, temps)
h	Root / Dashboard	Print help / all key commands & script info
q	Root / Dashboard	Quit monitoring
g	ASCII_GPU child	Trigger GPU ASCII Capture
v	ASCII_Video child	Trigger ASCII Video Player
p	Python_Sim child	Trigger Python Simulation
(future)	CompactSummary child	Trigger unified memory summary (if implemented)

Active Child Memory Places

Child Name	Description	Status
ASCII_GPU	GPU ASCII Capture	Active
ASCII_Video	ASCII Video Player	Active
Python_Sim	Interactive Python Simulation	Active
CompactSummary	Unified Memory Summary	Active

Notes / Safety

Root Dashboard is always primary; handles all commands first.

ls = emergency reload to restore permanent root script.

Auto-reload (s) refreshes root safely without affecting child memory places.

Logs every key press in gemma_log.txt.