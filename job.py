#Everything you build here is the fixed compute core that Part 2's blueprint describes deploying.
# You may not swap in a different job list or a different set of algorithms once this Part is 
# graded — Part 2 must describe deploying this exact engine.
#
#Tasks
#
#Create the fixed job list. Save this exact list of 8 sensor-processing jobs as jobs.py in 
#your repository — do not add, remove, reorder, or change any value, since every acceptance 
#criterion below depends on this exact, fixed input:
#
#JOBS = [
#    {"job_id": "Z1-J01", "zone": "Zone-A", "arrival_time": 0, "burst_time": 8, "priority": 3},
#    {"job_id": "Z1-J02", "zone": "Zone-A", "arrival_time": 1, "burst_time": 4, "priority": 1},
#    {"job_id": "Z2-J01", "zone": "Zone-B", "arrival_time": 2, "burst_time": 9, "priority": 4},
#    {"job_id": "Z2-J02", "zone": "Zone-B", "arrival_time": 3, "burst_time": 5, "priority": 2},
#    {"job_id": "Z3-J01", "zone": "Zone-C", "arrival_time": 4, "burst_time": 2, "priority": 1},
#    {"job_id": "Z3-J02", "zone": "Zone-C", "arrival_time": 5, "burst_time": 6, "priority": 5},
#    {"job_id": "Z1-J03", "zone": "Zone-A", "arrival_time": 6, "burst_time": 3, "priority": 2},
#    {"job_id": "Z2-J03", "zone": "Zone-B", "arrival_time": 8, "burst_time": 7, "priority": 3},
#]
#Two of these fields map directly onto named Process Control Block fields: 
# job_id is the Process ID, and priority is the scheduling information 
# (lower number = higher priority, consistent with Task 4). arrival_time, burst_time, and 
# zone are scheduling-simulation metadata used by the algorithms below, not PCB fields 
# themselves. Add a short comment or docstring in jobs.py stating exactly this: 
# which two fields are PCB fields (and which PCB field each is), and that the 
# other three are simulation-only metadata.
#
#Implement and compare FCFS, non-preemptive SJF, and SRTF. For each algorithm, 
# compute every job's waiting time and turnaround time (using JOBS from Task 1 unmodified), 
# print a per-job table, and report the average waiting time and average turnaround time. 
# If two ready jobs are tied on the scheduling criterion, break the tie by earlier arrival_time,
#  then by lower job_id (this fixed list has no such ties, but state the rule in your code 
# anyway).
#
#Implement Round Robin at two time-quantum values. Run Round Robin with quantum 3 and 
# again with quantum 6 on the same JOBS list. Use zero context-switch time cost 
# (switching is instantaneous in this simulation), and when a job's quantum expires 
# at exactly the same tick a new job arrives, add the newly-arrived job to the ready queue 
# before re-adding the expired job to the back of the queue. Report average waiting and 
# turnaround time for each run and the number of times a different job started running 
# (i.e. the number of context switches) in each run. Then write one sentence stating which 
# quantum value the theory would predict causes more overhead in a real OS 
# (where switching is not free) and why, referencing your own switch-count numbers 
# as the observable proxy for that overhead.
#
#Implement Priority scheduling with and without aging. Run non-preemptive priority scheduling 
#twice on the same JOBS list. In both runs, at every dispatch decision, pick the ready job 
#with the lowest effective-priority number; break any tie in effective priority by earlier 
#arrival_time, then by lower job_id. In the no-aging run, effective priority always equals the 
#job's fixed priority. In the aging run, a ready-but-not-yet-run job's effective priority 
#is max(1, priority - (ticks waited since becoming ready) // 3) at the moment of each dispatch 
#decision. Report each job's waiting time for both runs and identify the single job with the 
#longest wait in each run.
#
#Demonstrate and fix a race condition with Peterson's Algorithm. Model a shared "Zone-B 
# compute-credit counter" starting at 100. Two threads run concurrently: one subtracts 40 
#(a completed job consuming credits), the other adds 25 (an SLA-breach reimbursement) — 
#the arithmetically correct final value is 85. First, run this without any synchronization 
#at least 5 times, forcing an interleaving (e.g. a short time.sleep between reading and writing 
#the counter) so the race condition is observable, and record each run's final value. 
#Then implement Peterson's Algorithm using its standard flag and turn shared variables to guard
# entry to the critical section, around the same read-modify-write, and re-run at least 5 times.
#
#Implement Banker's Algorithm and check two resource requests. Use this exact scenario — 4 zone-controller processes, 3 resource types (R0 = compute slots, R1 = network channels, R2 = storage buffers):
#
#AVAILABLE = [3, 3, 2]
#MAX_NEED = {"P0": [7, 5, 3], "P1": [3, 2, 2], "P2": [9, 0, 2], "P3": [2, 2, 2]}
#ALLOCATION = {"P0": [0, 1, 0], "P1": [2, 0, 0], "P2": [3, 0, 2], "P3": [2, 1, 1]}
#Compute the Need matrix, run the safety algorithm on the initial state, and print whether it is safe (it is) and one valid safe sequence. Then evaluate these two requests independently against the original state above (do not carry one request's hypothetical changes into the other): (a) P1 requests [1, 0, 2] — your program must grant this (the resulting state is safe); (b) P0 requests [2, 0, 2] — your program must deny this and print that granting it would leave the system in an unsafe state, even though the request does not exceed Available or P0's Need.
#
#Implement a paging and segmentation address translator. Using this exact page table (page size 1024 bytes) and segment table:
#
#PAGE_SIZE = 1024
#PAGE_TABLE = {0: 5, 1: 2, 2: 9, 3: 1}
#SEGMENT_TABLE = {0: (1000, 400), 1: (2200, 300), 2: (500, 150)}  # {segment: (base, limit)}
#Translate these four paged logical addresses: 260, 1500, 3000, 5000 (page number = address // 1024, offset = address % 1024; the last one references a page not in PAGE_TABLE and must be reported as a page fault, not a crash). Then translate these three segmented logical addresses (given as (segment, offset) pairs): (0, 150), (1, 350), (2, 100) (physical address = base + offset when offset < limit; (1, 350) must be reported as a segmentation fault, not a crash, since 350 >= 300).
#
#Justify your deployment choice. In your README.md, using your own measured numbers from Tasks 2–4, state which single algorithm family you would actually run in production for these zone-controller jobs — FCFS, the SJF/SRTF family, Round Robin, or Priority scheduling — and, for each of the other three families, give one specific, numbers-cited reason it is less suitable for this workload.
#
#Acceptance criteria (your submission is complete when…)
#
#jobs.py contains the exact 8-job list from Task 1, unmodified, and is imported (not re-typed) by every script in Tasks 2–4.
#FCFS, SJF, and SRTF each report the correct waiting/turnaround table for JOBS, and SRTF's average waiting time is lower than SJF's, which is lower than FCFS's (the correct ordering for this exact job list).
#Under the stated boundary convention, the quantum-3 run has exactly 16 context switches (job changes) across 17 dispatch slices, and the quantum-6 run has exactly 10 context switches across 11 dispatch slices, for this exact job list; the written sentence correctly states that a real OS would pay more real switching overhead at quantum 3 than at quantum 6, citing these two switch counts as the evidence.
#The no-aging priority run's single longest-waiting job is Z3-J02; the aging run's single longest-waiting job is a different job than Z3-J02, and Z3-J02's own wait time is strictly lower with aging than without.
#The unsynchronized counter demo does not reliably produce 85 on every run (at least one of the 5 runs differs from 85), and the Peterson's-Algorithm-protected version produces exactly 85 on all 5 runs.
#Banker's Algorithm reports the initial state as safe with a valid safe sequence, grants P1's request [1, 0, 2], and denies P0's request [2, 0, 2] with an explicit unsafe-state explanation (not merely an availability-check failure).
#The paging translator returns physical addresses 5380, 2524, and 10168 for addresses 260, 1500, and 3000 respectively, and reports a page fault (not an exception or wrong value) for 5000. The segmentation translator returns physical addresses 1150 and 600 for (0, 150) and (2, 100), and reports a segmentation fault for (1, 350).
#Task 8's justification names exactly one algorithm family as the production choice and gives a distinct, numbers-cited reason for each of the other three families being less suitable (four reasons total, each citing at least one of the student's own measured numbers from Tasks 2–4).




JOBS = [
    {"job_id": "Z1-J01", "zone": "Zone-A", "arrival_time": 0, "burst_time": 8, "priority": 3},
    {"job_id": "Z1-J02", "zone": "Zone-A", "arrival_time": 1, "burst_time": 4, "priority": 1},
    {"job_id": "Z2-J01", "zone": "Zone-B", "arrival_time": 2, "burst_time": 9, "priority": 4},
    {"job_id": "Z2-J02", "zone": "Zone-B", "arrival_time": 3, "burst_time": 5, "priority": 2},
    {"job_id": "Z3-J01", "zone": "Zone-C", "arrival_time": 4, "burst_time": 2, "priority": 1},
    {"job_id": "Z3-J02", "zone": "Zone-C", "arrival_time": 5, "burst_time": 6, "priority": 5},
    {"job_id": "Z1-J03", "zone": "Zone-A", "arrival_time": 6, "burst_time": 3, "priority": 2},
    {"job_id": "Z2-J03", "zone": "Zone-B", "arrival_time": 8, "burst_time": 7, "priority": 3},
]


def fcfs(jobs):
    queue = []
    time = 0
    avg_waiting_time = 0 
    t_wait = 0
    for job in jobs:
        while time <= job["arrival_time"]:
            print(f'job id:{job["job_id"]} is aquaing the cpu till its burst time : {job["burst_time"]}')
            time += 1
    
    for job in jobs:
        print(f'job-id: {job["job_id"]} awaiting time is {t_wait}') 
        t_wait += job["burst_time"]
    avg_waiting_time = t_wait//len(jobs)
    print(f'average waiting time for fcfs is : {avg_waiting_time}')    
            
            
fcfs(jobs=JOBS)
#job id:Z1-J01 is aquaing the cpu till its burst time : 8
#job id:Z1-J02 is aquaing the cpu till its burst time : 4
#job id:Z2-J01 is aquaing the cpu till its burst time : 9
#job id:Z2-J02 is aquaing the cpu till its burst time : 5
#job id:Z3-J01 is aquaing the cpu till its burst time : 2
#job id:Z3-J02 is aquaing the cpu till its burst time : 6
#job id:Z1-J03 is aquaing the cpu till its burst time : 3
#job id:Z2-J03 is aquaing the cpu till its burst time : 7
#job id:Z2-J03 is aquaing the cpu till its burst time : 7
#job-id: Z1-J01 awaiting time is 0
#job-id: Z1-J02 awaiting time is 8
#job-id: Z2-J01 awaiting time is 12
#job-id: Z2-J02 awaiting time is 21
#job-id: Z3-J01 awaiting time is 26
#job-id: Z3-J02 awaiting time is 28
#job-id: Z1-J03 awaiting time is 34
#job-id: Z2-J03 awaiting time is 37
#average waiting time for fcfs is : 5

print('--------------------------------')
def sjf(jobs):
    sorted_bustTime = []
    twait = 0
    avg_waiting_time = 0
    for job in jobs:
        sorted_bustTime.append(job["burst_time"])
    sorted_bustTime.sort()
    for i in range(len(sorted_bustTime)):
        for job in jobs:
            if job["burst_time"] == sorted_bustTime[i]:
                print(f'job id {job["job_id"]} is aquaing the cpu till its burst time : {job["burst_time"]} awaiting time is {twait}')
                twait += sorted_bustTime[i]
    for i in range(len(sorted_bustTime)):
        avg_waiting_time += sorted_bustTime[i]
    avg_waiting_time = avg_waiting_time//len(sorted_bustTime)    
    print(f'average waiting time sjf is :{avg_waiting_time}')
        




sjf(jobs=JOBS)
#job id Z3-J01 is aquaing the cpu till its burst time : 2 awaiting time is 0
#job id Z1-J03 is aquaing the cpu till its burst time : 3 awaiting time is 2
#job id Z1-J02 is aquaing the cpu till its burst time : 4 awaiting time is 5
#job id Z2-J02 is aquaing the cpu till its burst time : 5 awaiting time is 9
#job id Z3-J02 is aquaing the cpu till its burst time : 6 awaiting time is 14
#job id Z2-J03 is aquaing the cpu till its burst time : 7 awaiting time is 20
#job id Z1-J01 is aquaing the cpu till its burst time : 8 awaiting time is 27
#job id Z2-J01 is aquaing the cpu till its burst time : 9 awaiting time is 35
#average waiting time sjf is :5      
print('-------------------------------------')

def SRTF(jobs):
    time = 0
    sorted_bustTime = []
    twait = 0
    avg_waiting_time = 0
    for job in jobs:
        sorted_bustTime.append(job["burst_time"])
    sorted_bustTime.sort()
    for job in jobs:
        if time == job["arrival_time"]:
          
          print(f'job id {job["job_id"]} is aquaing the cpu till its burst time : {job["burst_time"]} awaiting time is {twait}')
          sorted_bustTime.remove(job["burst_time"])
          twait += job["burst_time"]
    for i in range(len(sorted_bustTime)):
        for job in jobs:
            if job["burst_time"] == sorted_bustTime[i]:
                print(f'job id {job["job_id"]} is aquaing the cpu till its burst time : {job["burst_time"]} awaiting time is {twait}')
                twait += sorted_bustTime[i]
    for job in jobs:
        avg_waiting_time += job["burst_time"]
    avg_waiting_time  = avg_waiting_time//len(jobs)
    print(f'average waiting time SRTF is :{avg_waiting_time}')

SRTF(jobs=JOBS)
#job id Z1-J01 is aquaing the cpu till its burst time : 8 awaiting time is 0
#job id Z3-J01 is aquaing the cpu till its burst time : 2 awaiting time is 8
#job id Z1-J03 is aquaing the cpu till its burst time : 3 awaiting time is 10
#job id Z1-J02 is aquaing the cpu till its burst time : 4 awaiting time is 13
#job id Z2-J02 is aquaing the cpu till its burst time : 5 awaiting time is 17
#job id Z3-J02 is aquaing the cpu till its burst time : 6 awaiting time is 22
#job id Z2-J03 is aquaing the cpu till its burst time : 7 awaiting time is 28
#job id Z2-J01 is aquaing the cpu till its burst time : 9 awaiting time is 35
#average waiting time SRTF is :5

print('--------------------------------------------------------------------')



print("-------------------------------------------------------------------")

def round_robin(jobs,quantum):
    que = {}   #ready queue
    twait = 0
    joblist = []
    
    for job in jobs:
        
        if job["burst_time"] > quantum:
            print(f'job id: {job["job_id"]} is aquiring the cpu for time interval {quantum} and wait time is {twait}')
            twait += quantum
            que[job["job_id"]] = job["burst_time"] - quantum
        else:
            print(f'job id: {job["job_id"]} is aquiring the cpu for time interval {job["burst_time"]} and wait time is {twait}')
            twait += job["burst_time"]
            for job in que:
                while que[job] > 0:
                    if que[job] > quantum:
                        print(f'job id: {job} is aquiring the cpu for time interval {quantum} and wait time is {twait}')
                        twait += quantum
                        que[job] -= quantum
                    else:
                        print(f'job id: {job} is aquiring the cpu for time interval {que[job]} and wait time is {twait}')
                        twait += que[job]
                        que[job] = 0
    
    



round_robin(jobs=JOBS,quantum=3)
#job id: Z1-J01 is aquiring the cpu for time interval 3 and wait time is 0   
#job id: Z1-J02 is aquiring the cpu for time interval 3 and wait time is 3   context switch
#job id: Z2-J01 is aquiring the cpu for time interval 3 and wait time is 6   context switch
#job id: Z2-J02 is aquiring the cpu for time interval 3 and wait time is 9   context switch
#job id: Z3-J01 is aquiring the cpu for time interval 2 and wait time is 12  context switch
#job id: Z1-J01 is aquiring the cpu for time interval 3 and wait time is 14  context switch
#job id: Z1-J01 is aquiring the cpu for time interval 2 and wait time is 17  context switch
#job id: Z1-J02 is aquiring the cpu for time interval 1 and wait time is 19  context switch
#job id: Z2-J01 is aquiring the cpu for time interval 3 and wait time is 20  context switch
#job id: Z2-J01 is aquiring the cpu for time interval 3 and wait time is 23  context switch
#job id: Z2-J02 is aquiring the cpu for time interval 2 and wait time is 26  context switch
#job id: Z3-J02 is aquiring the cpu for time interval 3 and wait time is 28  context switch
#job id: Z1-J03 is aquiring the cpu for time interval 3 and wait time is 31  context switch
#job id: Z3-J02 is aquiring the cpu for time interval 3 and wait time is 34  context switch
#job id: Z2-J03 is aquiring the cpu for time interval 3 and wait time is 37  context switch
print("-------------------------------------")
round_robin(jobs=JOBS,quantum=6)

#job id: Z1-J01 is aquiring the cpu for time interval 6 and wait time is 0
#job id: Z1-J02 is aquiring the cpu for time interval 4 and wait time is 6   context switch
#job id: Z1-J01 is aquiring the cpu for time interval 2 and wait time is 10  context switch
#job id: Z2-J01 is aquiring the cpu for time interval 6 and wait time is 12  context switch
#job id: Z2-J02 is aquiring the cpu for time interval 5 and wait time is 18  context switch
#job id: Z2-J01 is aquiring the cpu for time interval 3 and wait time is 23  context switch
#job id: Z3-J01 is aquiring the cpu for time interval 2 and wait time is 26  context switch
#job id: Z3-J02 is aquiring the cpu for time interval 6 and wait time is 28  context switch
#job id: Z1-J03 is aquiring the cpu for time interval 3 and wait time is 34  context switch
#job id: Z2-J03 is aquiring the cpu for time interval 6 and wait time is 37  context switch


print("------------------------------------------------------------")

AVAILABLE = [3, 3, 2]
MAX_NEED = {"P0": [7, 5, 3], "P1": [3, 2, 2], "P2": [9, 0, 2], "P3": [2, 2, 2]}
ALLOCATION = {"P0": [0, 1, 0], "P1": [2, 0, 0], "P2": [3, 0, 2], "P3": [2, 1, 1]}
#Compute the Need matrix, run the safety algorithm on the initial state, and print whether it is safe (it is) and one valid safe sequence. Then evaluate these two requests independently against the original state above (do not carry one request's hypothetical changes into the other): (a) P1 requests [1, 0, 2] — your program must grant this (the resulting state is safe); (b) P0 requests [2, 0, 2] — your program must deny this and print that granting it would leave the system in an unsafe state, even though the request does not exceed Available or P0's Need.

 # {segment: (base, limit)}





                      
for process in ALLOCATION:
    i = 0 
    while i < len(ALLOCATION[process]):
        if AVAILABLE[i] < ALLOCATION[process][i]:
            print(f'process:{process} is not safe!')
        print(f'process:{process} is safe')    
        i += 1
first = set()
for process in ALLOCATION:
    for process in MAX_NEED:
        
        if MAX_NEED[process][0] <= ALLOCATION[process][0]:
            first.add(process)
print(f'first allocated process is :{first}')
                

#process:P0 is safe
#process:P0 is safe
#process:P0 is safe
#process:P1 is safe
#process:P1 is safe
#process:P1 is safe
#process:P2 is safe
#process:P2 is safe
#process:P2 is safe
#process:P3 is safe
#process:P3 is safe
#process:P3 is safe
#first allocated process is :{'P3'}

print('----------------------------------------------------------------------')


PAGE_SIZE = 1024
PAGE_TABLE = {0: 5, 1: 2, 2: 9, 3: 1}
SEGMENT_TABLE = {0: (1000, 400), 1: (2200, 300), 2: (500, 150)} 


PAGE_SIZE = 1024

PAGE_TABLE = {0: 5, 1: 2, 2: 9, 3: 1}

SEGMENT_TABLE = {
    0: (1000, 400),
    1: (2200, 300),
    2: (500, 150)
}


# -------------------------------
# Paging Address Translation
# -------------------------------
def translate_page(logical_address):
    page_number = logical_address // PAGE_SIZE
    offset = logical_address % PAGE_SIZE

    if page_number not in PAGE_TABLE:
        return f"Page fault: page {page_number} is not present in page table."

    frame_number = PAGE_TABLE[page_number]
    physical_address = frame_number * PAGE_SIZE + offset

    return physical_address


# -------------------------------
# Segmentation Address Translation
# -------------------------------
def translate_segment(segment, offset):
    if segment not in SEGMENT_TABLE:
        return f"Segmentation fault: segment {segment} does not exist."

    base, limit = SEGMENT_TABLE[segment]

    if offset >= limit:
        return (
            f"Segmentation fault: offset {offset} >= "
            f"segment limit {limit}"
        )

    physical_address = base + offset
    return physical_address


# -------------------------------
# Test Paging
# -------------------------------
print("PAGING TRANSLATION")
print("-------------------")

paged_addresses = [260, 1500, 3000, 5000]

for address in paged_addresses:
    result = translate_page(address)
    print(f"Logical address {address} -> {result}")


# -------------------------------
# Test Segmentation
# -------------------------------
print("\nSEGMENTATION TRANSLATION")
print("------------------------")

segmented_addresses = [
    (0, 150),
    (1, 350),
    (2, 100)
]

for segment, offset in segmented_addresses:
    result = translate_segment(segment, offset)
    print(f"(Segment {segment}, Offset {offset}) -> {result}")















        
    

