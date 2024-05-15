import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = 0
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

def read_processes_from_file(file_path):
    processes = []
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            if line.strip():
                try:
                    pid, arrival_time, burst_time = map(int, line.strip().split())
                    process = Process(pid, arrival_time, burst_time)
                    processes.append(process)
                except ValueError:
                    continue
    return processes

def srt_scheduler(processes):
    current_time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        ready_processes = [process for process in remaining_processes if process.arrival_time <= current_time]
        if ready_processes:
            shortest_process = min(ready_processes, key=lambda x: x.remaining_time)
            shortest_process.remaining_time -= 1
            current_time += 1
            if shortest_process.remaining_time == 0:
                shortest_process.finish_time = current_time
                shortest_process.turnaround_time = shortest_process.finish_time - shortest_process.arrival_time
                shortest_process.waiting_time = shortest_process.turnaround_time - shortest_process.burst_time
                remaining_processes.remove(shortest_process)
        else:
            current_time += 1
    for process in processes:
        process.remaining_time = process.burst_time

def display_results(processes):
    total_waiting_time = sum(process.waiting_time for process in processes)
    total_turnaround_time = sum(process.turnaround_time for process in processes)
    total_cpu_time = sum(process.burst_time for process in processes)
    cpu_utilization = (total_cpu_time / processes[-1].finish_time) * 100

    print("Process ID\tFinish Time\tWaiting Time\tTurnaround Time")
    for process in processes:
        print(f"{process.pid}\t\t{process.finish_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}")

    print(f"\nTotal CPU Utilization: {cpu_utilization:.2f}%")
    print(f"Average Waiting Time: {total_waiting_time / len(processes):.2f}")
    print(f"Average Turnaround Time: {total_turnaround_time / len(processes):.2f}")

    plt.figure(figsize=(10, len(processes) * 0.5))
    for i, process in enumerate(processes):
        plt.barh(y=i, width=process.burst_time, left=process.start_time, align='center',
                 color="Pink",label=f'P{process.pid} (Burst: {process.burst_time})')
        plt.text(process.start_time + process.burst_time / 2, i,
                 f'P{process.pid}', color='white', va='center', ha='center')

    plt.xlabel('Time')
    plt.ylabel('Processes')
    plt.title('Gantt Chart')
    plt.yticks(range(len(processes)), [f'P{process.pid}' for process in processes])
    plt.grid(True)
    plt.show()

def main():
    file_path = "SRT.txt"
    processes = read_processes_from_file(file_path)

    srt_scheduler(processes)
    print("\nSRT Scheduling Results:")
    display_results(processes)

if __name__ == "__main__":
    main()
