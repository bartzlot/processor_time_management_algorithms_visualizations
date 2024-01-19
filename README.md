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

### Cons
- Can lead to a phenomenon called the “convoy effect” where short processes get stuck behind long ones.
- Not optimal for systems where process execution time varies significantly.
