# Zone-Controller Fixed Compute Core

This repository implements the exact fixed 8-job workload and the required scheduling,
synchronization, deadlock-avoidance, paging, and segmentation simulations.

## Fixed input

`jobs.py` contains the exact required `JOBS` list. Tasks 2–4 import `JOBS` from
`jobs.py`; they do not re-type the workload.

The two PCB fields are `job_id` (Process ID/PID) and `priority` (scheduling information).
`arrival_time`, `burst_time`, and `zone` are simulation-only metadata.

## Run

```bash
python task2_cpu_scheduling.py
python task3_round_robin.py
python task4_priority.py
python task5_peterson.py
python task6_bankers.py
python task7_memory_translation.py
```

## Measured scheduling results

### FCFS

| Job | Waiting | Turnaround |
|---|---:|---:|
| Z1-J01 | 0 | 8 |
| Z1-J02 | 7 | 11 |
| Z2-J01 | 10 | 19 |
| Z2-J02 | 18 | 23 |
| Z3-J01 | 22 | 24 |
| Z3-J02 | 23 | 29 |
| Z1-J03 | 28 | 31 |
| Z2-J03 | 29 | 36 |

Average waiting = **17.125**; average turnaround = **22.625**.

### Non-preemptive SJF

| Job | Waiting | Turnaround |
|---|---:|---:|
| Z1-J01 | 0 | 8 |
| Z1-J02 | 12 | 16 |
| Z2-J01 | 33 | 42 |
| Z2-J02 | 14 | 19 |
| Z3-J01 | 4 | 6 |
| Z3-J02 | 17 | 23 |
| Z1-J03 | 4 | 7 |
| Z2-J03 | 20 | 27 |

Average waiting = **13.000**; average turnaround = **18.500**.

### SRTF

| Job | Waiting | Turnaround |
|---|---:|---:|
| Z1-J01 | 20 | 28 |
| Z1-J02 | 0 | 4 |
| Z2-J01 | 33 | 42 |
| Z2-J02 | 7 | 12 |
| Z3-J01 | 1 | 3 |
| Z3-J02 | 10 | 16 |
| Z1-J03 | 1 | 4 |
| Z2-J03 | 20 | 27 |

Average waiting = **11.500**; average turnaround = **17.000**.

Thus the required ordering is:

**SRTF (11.500) < SJF (13.000) < FCFS (17.125)** average waiting time.

## Round Robin

Quantum 3 produced **17 dispatch slices and 16 context switches**.
Quantum 6 produced **11 dispatch slices and 10 context switches**.

Average waiting:
- q=3: **22.625**
- q=6: **20.375**

Average turnaround:
- q=3: **28.125**
- q=6: **25.875**

In a real OS, quantum 3 would cause more switching overhead than quantum 6 because
the measured switch count is 16 versus 10, and real context switches are not free.

## Priority scheduling

No aging waiting times:

| Job | Waiting |
|---|---:|
| Z1-J01 | 0 |
| Z1-J02 | 7 |
| Z2-J01 | 27 |
| Z2-J02 | 11 |
| Z3-J01 | 8 |
| Z3-J02 | 33 |
| Z1-J03 | 13 |
| Z2-J03 | 14 |

Longest wait: **Z3-J02 = 33 ticks**.

With aging:

| Job | Waiting |
|---|---:|
| Z1-J01 | 0 |
| Z1-J02 | 7 |
| Z2-J01 | 10 |
| Z2-J02 | 18 |
| Z3-J01 | 22 |
| Z3-J02 | 23 |
| Z1-J03 | 28 |
| Z2-J03 | 29 |

Longest wait: **Z2-J03 = 29 ticks**.

Aging reduces Z3-J02's wait from **33 to 23 ticks**, and the longest-waiting job changes
from Z3-J02 to Z2-J03.

## Peterson's Algorithm

The unsynchronized demonstration deliberately pauses between the counter read and write.
Because both threads can read 100 before either writes, a lost update is observable; the
possible incorrect results are 60 or 125 rather than the correct 85.

The Peterson-protected critical section uses the standard two-process `flag` and `turn`
variables around the read-modify-write. Five protected runs must all produce **85**.

## Banker's Algorithm

Need matrix:

```text
P0: [7, 4, 3]
P1: [1, 2, 2]
P2: [6, 0, 0]
P3: [0, 1, 1]
```

The initial state is safe. One valid safe sequence is:

**P1 -> P3 -> P0 -> P2**

Requests are checked independently against the original state.

- **P1 requests [1, 0, 2]: granted.** The resulting state remains safe, with a valid
  safe sequence **P1 -> P3 -> P0 -> P2**.
- **P0 requests [2, 0, 2]: denied.** The request does not exceed Available or P0's
  remaining Need, but the hypothetical allocation leaves no possible completion order,
  so granting it would leave the system in an **unsafe state**.

## Paging and segmentation

With page size 1024:

- 260 -> **5380**
- 1500 -> **2524**
- 3000 -> **10168**
- 5000 -> **page fault**

Segmentation:

- (0, 150) -> **1150**
- (1, 350) -> **segmentation fault**
- (2, 100) -> **600**

## Production choice

**Production choice: Priority scheduling.**

Reasons the other three families are less suitable for this workload, using the measured
numbers above:

1. **FCFS:** its average waiting time is **17.125**, and Z2-J03 waits **29 ticks**;
   the workload already supplies explicit priority values, so FCFS ignores information
   that can distinguish more urgent controller jobs.
2. **SJF/SRTF family:** SRTF has the best average waiting time at **11.500**, but the
   first-arriving Z1-J01 still waits **20 ticks** because later short jobs repeatedly
   preempt it; Priority scheduling can instead honor the workload's explicit priority
   field and aging reduces Z3-J02's wait from **33 to 23 ticks**.
3. **Round Robin:** quantum 3 needs **16 context switches**, versus **10** for quantum 6,
   while its average waiting time is **22.625** at q=3 and **20.375** at q=6, both worse
   than SRTF's **11.500**; the extra switching is unnecessary overhead for these
   priority-tagged controller jobs.

Priority scheduling is therefore the single selected production family, with aging
enabled to reduce starvation risk.
