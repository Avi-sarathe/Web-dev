#!/usr/bin/env python3
"""
High-speed solution runner and test case checker.
Usage:
    python3 tester.py <solution_file> [input_file] [expected_output_file]
Example:
    python3 tester.py solution.cpp input.txt expected.txt
    python3 tester.py solution.py
"""

import sys
import os
import subprocess
import time

def run_test(solution_path, input_str=None, expected_output=None):
    ext = os.path.splitext(solution_path)[1]
    cmd = []
    cleanup_bin = None

    if ext == ".cpp":
        bin_path = "./temp_runner_bin"
        compile_cmd = ["clang++", "-O3", "-std=c++17", solution_path, "-o", bin_path]
        comp_start = time.perf_counter()
        comp_res = subprocess.run(compile_cmd, capture_output=True, text=True)
        comp_time = (time.perf_counter() - comp_start) * 1000

        if comp_res.returncode != 0:
            print("❌ Compilation Error:")
            print(comp_res.stderr)
            return
        print(f"🔨 Compiled in: {comp_time:.1f} ms")
        cmd = [bin_path]
        cleanup_bin = bin_path
    elif ext == ".py":
        cmd = [sys.executable, solution_path]
    else:
        print(f"Unsupported file type: {ext}")
        return

    try:
        start_time = time.perf_counter()
        exec_res = subprocess.run(
            cmd,
            input=input_str if input_str is not None else "",
            capture_output=True,
            text=True,
            timeout=5.0
        )
        duration_ms = (time.perf_counter() - start_time) * 1000

        actual_output = exec_res.stdout.strip()

        print(f"\n⏱️ Execution time: {duration_ms:.2f} ms")

        if exec_res.returncode != 0:
            print(f"❌ Runtime Error (exit code {exec_res.returncode}):")
            print(exec_res.stderr)
            return

        print("--- Output ---")
        print(actual_output)

        if expected_output is not None:
            expected_clean = expected_output.strip()
            print("\n--- Verification ---")
            if actual_output == expected_clean:
                print("✅ PASSED: Output matches expected exactly!")
            else:
                print("❌ FAILED: Output mismatch!")
                print("Expected:")
                print(expected_clean)
    except subprocess.TimeoutExpired:
        print("❌ Time Limit Exceeded (TLE) > 5.0 seconds")
    finally:
        if cleanup_bin and os.path.exists(cleanup_bin):
            os.remove(cleanup_bin)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tester.py <solution_file> [input_file] [expected_output_file]")
        return

    solution = sys.argv[1]
    input_str = ""
    expected = None

    if len(sys.argv) >= 3 and os.path.exists(sys.argv[2]):
        with open(sys.argv[2], "r") as f:
            input_str = f.read()

    if len(sys.argv) >= 4 and os.path.exists(sys.argv[3]):
        with open(sys.argv[3], "r") as f:
            expected = f.read()

    run_test(solution, input_str if input_str else None, expected)

if __name__ == "__main__":
    main()
