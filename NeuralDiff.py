#!/usr/bin/env python3

import argparse
import sys
import time
from tqdm import tqdm  # Provides an easy progress bar

# Define color codes using universal ANSI sequences
PURPLE = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"

# ASCII Art logo with the app name "NeuraDiff"
def print_logo():
    print(f"{PURPLE}")
    print("⠀⠀⠀⠀⠀⠀⠀⢀⣤⣴⠿⠿⠿⠿⠿⠿⠷⠶⢤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⢀⡠⠖⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⢦⡀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⣄⠀⠀⠀⠀⠀")
    print("⠸⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢣⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀NeuraDiff - File Comparison Tool⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀")
    print(f"{RESET}")
    time.sleep(1)  # Pause to display the logo

# Progress bar simulation for "scanning" files
def simulate_loading(description):
    print(f"{CYAN}{description}{RESET}")
    for _ in tqdm(range(100), bar_format="{l_bar}{bar} | {n_fmt}%"):
        time.sleep(0.02)  # Simulate scanning delay
    print()  # Print newline after progress bar

# Function to compare files
def compare_files(files, output_file):
    # Display progress bar for each file to simulate scanning
    for file in files:
        simulate_loading(f"Scanning {file} for unique and duplicate lines...")

    # Initialize sets to track unique lines and duplicates
    all_lines = set()
    duplicates = set()

    # Process each file and identify duplicates
    for file in files:
        try:
            with open(file, 'r') as f:
                # Filter out lines that are empty or contain only whitespace
                file_lines = set(line.strip() for line in f if line.strip())
                duplicates |= all_lines & file_lines  # Find any duplicates
                all_lines |= file_lines               # Add all lines to the total set
        except FileNotFoundError:
            print(f"{PURPLE}Error: {file} not found.{RESET}")
            sys.exit(1)

    # Unique lines are all lines minus the duplicates
    unique_lines = all_lines - duplicates

    # Write unique lines to the output file with a progress bar
    simulate_loading(f"Saving unique lines to {output_file}...")
    with open(output_file, 'w') as out:
        for line in unique_lines:
            out.write(line + '\n')

    # Print duplicates and unique lines with colors
    print("\nComparison Result:")
    for line in all_lines:
        if line in duplicates:
            print(f"{BLUE}[{GREEN}+{BLUE}]----| {RESET}{BOLD}{line}{BLUE} |----[{GREEN}+{BLUE}]{BLUE}[{BOLD} {RED}DUPLICATE {RESET}{BLUE}]{RESET}")
        else:
            print(f"{BLUE}[{GREEN}+{BLUE}]----| {RESET}{BOLD}{line}{BLUE} |----[{GREEN}+{BLUE}]{BLUE}[{BOLD} {GREEN}UNIQUE {RESET}{BLUE}]{RESET}")

if __name__ == "__main__":
    # Argument parser for command line arguments
    parser = argparse.ArgumentParser(
        description="Compare multiple files and mark duplicates and unique lines."
    )
    parser.add_argument("-f", nargs='+', required=True, metavar="file",
                        help="Specify the files to compare (two or more files).")
    parser.add_argument("-o", required=True, metavar="output",
                        help="Specify the output file name for unique lines.")
    args = parser.parse_args()

    # Display the logo
    print_logo()

    # Validate arguments
    if len(args.f) < 2:
        print(f"{PURPLE}Error: At least two files are required for comparison.{RESET}")
        print("Use -h for help on usage.")
        sys.exit(1)

    # Call the comparison function
    compare_files(args.f, args.o)

