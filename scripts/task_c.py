import time
import subprocess
import csv
import matplotlib.pyplot as plt


n = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

# run more times for each n to get average time
repeat = 10

def measure_time(command):
    """
    Measure average running time of a command.
    """
    total_time = 0.0
    for _ in range(repeat):
        start = time.perf_counter()
        subprocess.run(command,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        end = time.perf_counter()
        total_time += (end - start)
    return total_time / repeat


def main():
    matcher_times = []
    verifier_times = []

    for i in n:
        input_file = f"data/taskC/n{i}.in"
        output_file = f"results/taskC/n{i}.out"

       # measure matcher
        matcher_cmd = ["python3", "src/matcher.py", input_file]
        matcher_time = measure_time(matcher_cmd)
        matcher_times.append(matcher_time)

        # Generate stable output once for verifier
        with open(output_file, "w") as f:
            subprocess.run(matcher_cmd, stdout=f)

        # measure verifier
        verifier_cmd = ["python3", "src/verifier.py", input_file, output_file]
        verifier_time = measure_time(verifier_cmd)
        verifier_times.append(verifier_time)

        print(f"n={i}: matcher={matcher_time:.6f}s, verifier={verifier_time:.6f}s")

    # save results to CSV
    with open("results/taskC_times.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "matcher_time", "verifier_time"])
        for i in range(len(n)):
            writer.writerow([n[i], matcher_times[i], verifier_times[i]])

    # plort matcher
    plt.figure()
    plt.plot(n, matcher_times, marker="o")
    plt.xlabel("n")
    plt.ylabel("Time (seconds)")
    plt.title("Matcher Runtime")
    plt.savefig("results/taskC_matcher.png")

    # plot verifier
    plt.figure()
    plt.plot(n, verifier_times, marker="o")
    plt.xlabel("n")
    plt.ylabel("Time (seconds)")
    plt.title("Verifier Runtime")
    plt.savefig("results/taskC_verifier.png")

    print("Task C finished. Results saved in results/")

if __name__ == "__main__":
    main()
