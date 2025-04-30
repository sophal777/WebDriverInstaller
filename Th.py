import threading
import time

# Function that will be run by each thread
def fb(N, browser_choice, app_all):
    print(f"Thread {N} using {browser_choice} and performing {app_all}")

# Function that is called every time a loop is successful
def every_Loop():
    print("[*] every_Loop function is called!")
    # Add your actual logic here for every loop
    # For example, perform some task or validation

def start():
    browser_choice = "Chrome"  # Example browser choice
    app_all = "Facebook"  # Example app choice
    thread_count = 5  # Example number of threads
    loop_count = 3  # Example number of loops
    verify_open = 2  # Example number of successful loops before calling every_Loop()

    break_count = 0
    success_count = 0

    while break_count < loop_count:
        break_count += 1
        print(f"[+] Starting loop {break_count}/{loop_count}")

        threads = []
        for N in range(thread_count):
            t = threading.Thread(target=fb, args=(N, browser_choice, app_all))
            t.start()
            threads.append(t)
            time.sleep(1)  # Delay between starting threads

        for t in threads:
            t.join()

        success_count += 1
        if success_count >= verify_open:
            print("[*] Calling every_Loop() function")
            every_Loop()  # Call the every_Loop function
            success_count = 0  # Reset after calling every_Loop()

        print(f"[*] Waiting 5 seconds before next loop...")
        time.sleep(5)

    print("[✓] All loops completed.")

# Call the start function
start()
