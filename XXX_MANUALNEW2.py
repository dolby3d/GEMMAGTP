eatures in This Final Script

Hashed password for secure login (SHA-256).

Full login protection for all functions (ls, fetch_ascii_video, print_*, save, save_script, change_password).

Password change command (pass) — only dolby can change it.

Hotkeys: s, r, R, mem, h, q (all login-protected).

Save commands (save, save_script, save script) are login-protected.

Help menu (h) lists all commands.

Quit confirmation requires login and optional confirmation.

Command input supports textual commands during the monitor loop.




🔹 GEMMA DASHBOARD MANUAL
Script Info

Script Name: gemma_monitor.py

Location: gemma_dashboard/

Permanent Copy: Always saved here

Password Rule02: Password never displayed

Save/Load Password: gemma123dolby123 (only entered at prompt)

Mini Real-Time Dashboard

Displayed at top; updates every second:

CPU Usage

RAM Usage

Disk Usage

FPS

Child Memory Places Status: Active/Inactive

Keys Always Visible: s(ls) i i1 h q g v p

Key Commands
Key	Function
s	Reload root dashboard (mini panel + cheat sheet reprinted)
ls	Reload permanent Gemma Dashboard (password-protected)
i	Show basic info (CPU, RAM, Disk, FPS)
i1	Show detailed diagnostics (per-core CPU, memory, swap, disk, network, temps)
h	Show cheat sheet + child memory statuses (on-demand help)
q	Quit monitoring safely
g	Trigger ASCII GPU Capture child
v	Trigger ASCII Video Player child
p	Trigger Python Sim child
Child Memory Places
Child Name	Description	Status
ASCII_GPU	GPU ASCII Capture	Active
ASCII_Video	ASCII Video Player	Active
Python_Sim	Interactive Python Simulation	Active
CompactSummary	Unified Memory Summary	Active

Python Sim provides a mini interactive Python environment with helpers like print_time(), build_bar(), update_fps(), GPU ASCII capture, snapshots, etc.

Password-Protected Operations

Load Permanent Script (ls)

Prompts for password

Correct → reloads root dashboard

Incorrect → aborts load, logs attempt

Save Script (save_script())

Prompts for password

Correct → saves permanent copy

Incorrect → aborts save, logs attempt

Rule02 enforced: Password never shown anywhere

Logging

All key presses, reloads, child triggers, save/load attempts are logged in:

gemma_dashboard/gemma_log.txt


Logs include timestamps, action descriptions, and never reveal the password

Workflow Example

Run dashboard → mini panel + cheat sheet displayed

Press i → basic info

Press i1 → detailed diagnostics

Press h → cheat sheet on-demand

Trigger children: g, v, p → corresponding actions

Reload via s or ls (with correct password)

Save script via save_script() (password-protected)

Exit safely via q