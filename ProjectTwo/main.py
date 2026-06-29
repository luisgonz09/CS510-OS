"""
    Class:   CS-510
    Author:  Luis D. Gonzalez Sanchez
    Date:    June 21, 2026

    Description:  Python-based OS performance and optimization simulator.
                  This application displays disk, CPU, and memory statistics,
                  demonstrates concurrency through threading, and handles a
                  system exception without aborting the application.
"""

import os
import psutil
import sys
import threading
from datetime import datetime


def printBlankLines(lines: int):
    """Prints blank lines to make the program output easier to read."""
    for i in range(lines):
        print("")


def printMsg1(num):
    """Displays the cube calculation and current thread information."""
    current_thread = threading.current_thread()
    print("Thread 1 is executing.")
    print("Thread 1 Name: {}".format(current_thread.name))
    print("Thread 1 ID: {}".format(threading.get_ident()))
    print("Thread 1 cubed: {}".format(num * num * num))


def printMsg2(num):
    """Displays the square calculation and current thread information."""
    current_thread = threading.current_thread()
    print("Thread 2 is executing.")
    print("Thread 2 Name: {}".format(current_thread.name))
    print("Thread 2 ID: {}".format(threading.get_ident()))
    print("Thread 2 squared: {}".format(num * num))


def format_bytes(size: float) -> str:
    """Converts a byte value into a readable size format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return "{:.2f} {}".format(size, unit)
        size /= 1024
    return "{:.2f} PB".format(size)


"""
   This function displays disk usage information and file statistics.
"""
def getFileDiskUsageStatistics() -> None:
    print("Getting Disk Statistics")
    print("=============================")
    file_name = "./projecttwo.txt"

    try:
        if not os.path.exists(file_name):
            with open(file_name, "w", encoding="utf-8") as file:
                file.write("CS 510 Project Two sample file.\n")
                file.write("This file is used to display file statistics.\n")

        disk_usage = psutil.disk_usage("/")
        file_stats = os.stat(file_name)

        print("Disk Resource Usage")
        print("Total Disk Space: {}".format(format_bytes(disk_usage.total)))
        print("Used Disk Space: {}".format(format_bytes(disk_usage.used)))
        print("Free Disk Space: {}".format(format_bytes(disk_usage.free)))
        print("Disk Usage Percentage: {}%".format(disk_usage.percent))
        print("")
        print("File Information")
        print("File Name: {}".format(file_name))
        print("File Size: {}".format(format_bytes(file_stats.st_size)))
        print("File Permissions: {}".format(oct(file_stats.st_mode)))
        print("Created Time: {}".format(datetime.fromtimestamp(file_stats.st_ctime)))
        print("Last Modified Time: {}".format(datetime.fromtimestamp(file_stats.st_mtime)))
        print("Last Accessed Time: {}".format(datetime.fromtimestamp(file_stats.st_atime)))
    except OSError as error:
        print("A disk or file system error occurred: {}".format(error))

    printBlankLines(2)


"""
   This function retrieves standard and virtual memory statistics.
"""
def getMemoryStatistics() -> None:
    print("Getting Memory Statistics")
    print("=============================")

    try:
        virtual_memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()

        print("Physical Memory")
        print("Total Memory: {}".format(format_bytes(virtual_memory.total)))
        print("Available Memory: {}".format(format_bytes(virtual_memory.available)))
        print("Used Memory: {}".format(format_bytes(virtual_memory.used)))
        print("Memory Usage Percentage: {}%".format(virtual_memory.percent))
        print("")
        print("Virtual Memory / Swap")
        print("Total Swap: {}".format(format_bytes(swap_memory.total)))
        print("Used Swap: {}".format(format_bytes(swap_memory.used)))
        print("Free Swap: {}".format(format_bytes(swap_memory.free)))
        print("Swap Usage Percentage: {}%".format(swap_memory.percent))
    except Exception as error:
        print("A memory statistics error occurred: {}".format(error))

    printBlankLines(2)


"""
   This function retrieves CPU statistics, including process information.
"""
def getCpuStatistics() -> None:
    print("Getting CPU Statistics")
    print("=============================")

    try:
        print("CPU Resource Usage")
        print("Physical CPU Cores: {}".format(psutil.cpu_count(logical=False)))
        print("Logical CPU Cores: {}".format(psutil.cpu_count(logical=True)))
        print("Current CPU Usage: {}%".format(psutil.cpu_percent(interval=1)))
        print("")

        cpu_frequency = psutil.cpu_freq()
        if cpu_frequency is not None:
            print("CPU Frequency")
            print("Current Frequency: {:.2f} MHz".format(cpu_frequency.current))
            print("Minimum Frequency: {:.2f} MHz".format(cpu_frequency.min))
            print("Maximum Frequency: {:.2f} MHz".format(cpu_frequency.max))
            print("")

        print("Process Information")
        print("Total Running Processes: {}".format(len(psutil.pids())))
        print("Top Processes by CPU Usage:")
        processes = []
        for process in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                processes.append(process.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        top_processes = sorted(
            processes,
            key=lambda item: item.get("cpu_percent") or 0,
            reverse=True
        )[:5]

        print("{:<10} {:<25} {:<12} {:<12}".format("PID", "Name", "CPU %", "Memory %"))
        for process in top_processes:
            print("{:<10} {:<25} {:<12} {:.2f}".format(
                process.get("pid", "N/A"),
                str(process.get("name", "N/A"))[:24],
                process.get("cpu_percent", 0.0),
                process.get("memory_percent", 0.0) or 0.0
            ))
    except Exception as error:
        print("A CPU statistics error occurred: {}".format(error))

    printBlankLines(2)


"""
   This function demonstrates multi-threading capabilities.
"""
def showThreadingExample() -> None:
    print("Demonstrating Threading")
    print("=============================")

    thread_one = threading.Thread(target=printMsg1, args=(3,), name="CubeThread")
    thread_two = threading.Thread(target=printMsg2, args=(4,), name="SquareThread")

    print("Creating Thread 1: {}".format(thread_one.name))
    print("Creating Thread 2: {}".format(thread_two.name))

    print("Starting Thread 1")
    thread_one.start()
    print("Starting Thread 2")
    thread_two.start()

    thread_one.join()
    print("Thread 1 has completed and was destroyed.")

    thread_two.join()
    print("Thread 2 has completed and was destroyed.")

    print("Done With Threading!")

    printBlankLines(2)


"""
   This function demonstrates system error handling.
"""
def showErrorHandling() -> None:
    print("Demonstrating Error Handling")
    print("=============================")
    try:
        print("Attempting to divide 10 by 0.")
        res = 10 / 0

    except ZeroDivisionError as error:
        print("Error caused: Divide by zero error.")
        print("System message: {}".format(error))
        print("You can't divide by zero!")

    except MemoryError:
        print("Memory Error!")

    else:
        print("Result is", res)

    finally:
        print("Execution complete.")

    printBlankLines(2)


"""
   Main function, does not require modification.

   This calls the specific functions.
"""
def main() -> int:
    print("Starting Program")
    print("=============================")

    getFileDiskUsageStatistics()

    getCpuStatistics()

    getMemoryStatistics()

    showThreadingExample()

    showErrorHandling()

    return 0


if __name__ == '__main__':
    sys.exit(main())
