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
        self.executed = False

def read_processes_from_file(file_path):
    processes = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():
                try:
                    pid, arrival_time, burst_time = map(int, line.strip().split())
                    process = Process(pid, arrival_time, burst_time)
                    processes.append(process)
                except ValueError:
                    continue
    return processes

def rr_scheduler(processes, time_quantum):
    current_time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        for process in remaining_processes:
            if process.remaining_time > 0:
                current_time = max(current_time, process.arrival_time)
                process.start_time = current_time
                if process.remaining_time > time_quantum:
                    current_time += time_quantum
                    process.remaining_time -= time_quantum
                else:
                    current_time += process.remaining_time
                    process.remaining_time = 0
                    process.finish_time = current_time
                    process.turnaround_time = process.finish_time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.burst_time
                    remaining_processes.remove(process)
                    break

def display_results(processes):
    total_waiting_time = 0
    total_turnaround_time = 0
    total_cpu_time = sum(process.burst_time for process in processes)

    print("Process ID\tFinish Time\tWaiting Time\tTurnaround Time")
    for process in processes:
        print(f"{process.pid}\t\t\t\t{process.finish_time}\t\t\t{process.waiting_time}\t\t\t\t\t{process.turnaround_time}")
        total_waiting_time += process.waiting_time
        total_turnaround_time += process.turnaround_time

    if processes:
        cpu_utilization = (total_cpu_time / processes[-1].finish_time) * 100
        print(f"\nTotal CPU Utilization: {cpu_utilization:.2f}%")

    if processes:
        print(f"Average Waiting Time: {total_waiting_time / len(processes):.2f}")
        print(f"Average Turnaround Time: {total_turnaround_time / len(processes):.2f}")

    plt.figure(figsize=(10, len(processes) * 0.5))
    for i, process in enumerate(processes):
        plt.barh(y=i, width=process.burst_time, left=process.start_time, align='center',
                 color="Purple", label=f'P{process.pid} (Burst: {process.burst_time})')
        plt.text(process.start_time + process.burst_time / 2, i,
                 f'P{process.pid}', color='white', va='center', ha='center')

    plt.xlabel('Time')
    plt.ylabel('Processes')
    plt.title('Gantt Chart')
    plt.yticks(range(len(processes)), [f'P{process.pid}' for process in processes])
    plt.grid(True)
    plt.show()


def main():
    file_path = "RR.txt"
    processes = read_processes_from_file(file_path)

    time_quantum = 4
    rr_processes = processes.copy()
    rr_scheduler(rr_processes, time_quantum)
    print("\nRR Scheduling Results:")
    display_results(rr_processes)

if __name__ == "__main__":
    main()
