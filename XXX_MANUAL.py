GEMMA Monitoring Script Report

Saved location in memory: Session context
Permanent copy: GEMMA/gemma_permanent.py
Log file: GEMMA/gemma_log.txt
Rules enforced:

RULE00: Only user dolby can change the script

RULE01: User dolby — never change script, only fix; exceptions: say/type y or yes

Key triggers:

Key	Action
s	Load script
m	Start monitoring
i	Show basic system info
i1	Show detailed diagnostics
h	Show shortcuts help
q	Quit monitoring

Features:

Full-screen dashboard with CPU, RAM, Swap, network stats

FPS calculation and smooth display

GEMMA folder auto-created for permanent copy & logs

Script copy persists immediately at start

Keyboard triggers active while monitoring

Logs script start and maintains RULE messages

Notes:

Only q exits monitoring; other keys just display info

Script auto-saves a permanent copy without user intervention

Logging is stored in GEMMA/gemma_log.txt

Enforces lowercase dolby for user checks








+------------------+-----------------------+
| Metric           | Value                 |
+------------------+-----------------------+
| Time             | 12:34:56              |
| CPU Usage        | 23.5% ██████          |
| Memory Usage     | 48.7% ██████████      |
| Total Memory (GB)| 15.92                 |
| Used Memory (GB) | 7.74                  |
| Free Memory (GB) | 8.18                  |
| Disk Usage       | 67.3% ███████████     |
| Bytes Sent (MB)  | 123.45                |
| Bytes Received(MB)| 543.21               |
| Swap Used        | 12.1%                 |
| Total Swap (GB)  | 4.00                  |
| Used Swap (GB)   | 0.48                  |
| CPU Temp Core 0  | 45.0°C                |
| CPU Temp Core 1  | 44.0°C                |
+------------------+-----------------------+