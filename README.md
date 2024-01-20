# CPU Scheduling Algorithms

## Priority Scheduling with Aging (PSWA)

### Description
Priority Scheduling with Aging (PSWA) is an advanced form of priority scheduling where each process is assigned a priority. Processes with higher priorities are executed first. Aging is used to prevent starvation of lower priority processes. In aging, as time progresses, the priority of a process increases (i.e., the priority number decreases in case of a lower number indicating higher priority), ensuring that every process eventually gets executed.

### Pros
- Efficient for systems where priority-based tasks are common.
- Aging ensures that no process is left waiting indefinitely.

### Cons
- Requires priority assignment which can be complex.
- Can lead to priority inversion if not managed properly.

## Shortest Job First (SJF)

### Description
Shortest Job First (SJF) is a scheduling algorithm where the process with the shortest execution time is selected for execution next. SJF can be preemptive or non-preemptive. In the preemptive version, if a new process arrives with a shorter burst time than the remaining time of the current process, the current process is preempted.

### Pros
- Minimizes average waiting time for processes.
- Highly efficient if job times are known in advance.

### Cons
- Can lead to starvation of longer processes.
- Requires prior knowledge of the CPU burst time.

## First-Come, First-Served (FCFS)

### Description
First-Come, First-Served (FCFS) is the simplest scheduling algorithm. In this approach, the process that arrives first is executed first and the next process starts only after the previous one finishes. This is a non-preemptive, queue-based scheduling algorithm.

### Pros
- Simple and easy to implement.
- Fair in the sense that it serves processes in the order they arrive.
# Page Replacement Algorithms

## First-In, First-Out (FIFO)

### Description
First-In, First-Out (FIFO) is one of the simplest page replacement algorithms. In FIFO, the operating system keeps track of all pages in the memory in a queue, with the oldest page at the front. When a page needs to be replaced, the oldest page is selected and removed to make room for the new page.

### Pros
- Simple to understand and easy to implement.
- Fair in the sense that each page has the same lifespan in memory.

### Cons
- Can suffer from the "Belady's anomaly" where increasing the number of page frames results in an increase in the number of page faults.
- Not always optimal as it may remove pages that are frequently used.

## Optimal (OPT)

### Description
Optimal (OPT), also known as the "min" algorithm, is a theoretical algorithm used for benchmarking. It replaces the page that will not be used for the longest period of time in the future.

### Pros
- Provides the best possible performance in terms of the least number of page faults.
- Ideal for comparative analysis and understanding the lower bound of page faults.

### Cons
- Not feasible in practical systems as it requires future knowledge of page requests.
- Mainly used for theoretical and comparison purposes.

## Least Recently Used (LRU)

### Description
Least Recently Used (LRU) is a page replacement algorithm that removes the page that has been least recently used. It assumes that pages used recently will be used again soon, so it keeps recently used pages in memory.

### Pros
- More efficient in practice than FIFO.
- Adapts well to various types of workloads.

### Cons
- More complex to implement than FIFO.
- Can be expensive in terms of time and hardware to track page usage.

## Least Frequently Used (LFU)

### Description
Least Frequently Used (LFU) is a page replacement algorithm that tracks how often a page is used. When a page needs to be replaced, LFU removes the page with the smallest count of uses.

### Pros
- Good for situations where some pages are accessed very frequently.
- Tends to keep frequently used pages in memory.

### Cons
- Can lead to the problem where a page used heavily in the past but not recently can remain in memory.
- Requires additional overhead to track the frequency of access for each page.


### Cons
- Can lead to a phenomenon called the “convoy effect” where short processes get stuck behind long ones.
- Not optimal for systems where process execution time varies significantly.
