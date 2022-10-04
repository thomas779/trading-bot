import time
import threading

start = time.perf_counter()

def do_something():
    print("sleeping 1 second...")
    time.sleep(1)
    print("done sleeping...")

t1 = threading.Thread(target=do_something)
t2 = threading.Thread(target=do_something)

t1.start()
t2.start()

finish = time.perf_counter()

print(f'finish in {round(finish-start, 2)} second(s)')
