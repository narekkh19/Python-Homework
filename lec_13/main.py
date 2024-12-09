import random
import string
import time
from collections import Counter
from threading import Thread, Lock
from multiprocessing import Process, Manager

def generate_large_file(filename, num_lines=1_000_000, words_per_line=10):
    with open(filename, 'w') as file:
        for _ in range(num_lines):
            line = ' '.join(''.join(random.choices(string.ascii_lowercase, k=5)) for _ in range(words_per_line))
            file.write(line + '\n')

def count_words(filename):
    with open(filename, 'r') as file:
        word_count = Counter()
        for line in file:
            word_count.update(line.split())
    return word_count

def worker_thread(chunk, lock, result):
    local_count = Counter(chunk.split())
    with lock:
        result.update(local_count)

def count_words_multithreading(filename, num_threads=4):
    with open(filename, 'r') as file:
        lines = file.readlines()

    chunk_size = len(lines) // num_threads
    threads = []
    result = Counter()
    lock = Lock()

    for i in range(num_threads):
        chunk = ' '.join(lines[i * chunk_size:(i + 1) * chunk_size])
        thread = Thread(target=worker_thread, args=(chunk, lock, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result

def worker_process(chunk, return_dict, index):
    local_count = Counter(chunk.split())
    return_dict[index] = local_count

def count_words_multiprocessing(filename, num_processes=4):
    with open(filename, 'r') as file:
        lines = file.readlines()

    chunk_size = len(lines) // num_processes
    processes = []
    manager = Manager()
    return_dict = manager.dict()

    for i in range(num_processes):
        chunk = ' '.join(lines[i * chunk_size:(i + 1) * chunk_size])
        process = Process(target=worker_process, args=(chunk, return_dict, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    final_count = Counter()
    for count in return_dict.values():
        final_count.update(count)

    return final_count

if __name__ == '__main__':
    FILENAME = 'large_text.txt'
    generate_large_file(FILENAME)

    start_time = time.time()
    sequential_result = count_words(FILENAME)
    sequential_time = time.time() - start_time

    start_time = time.time()
    multithreading_result = count_words_multithreading(FILENAME)
    multithreading_time = time.time() - start_time

    start_time = time.time()
    multiprocessing_result = count_words_multiprocessing(FILENAME)
    multiprocessing_time = time.time() - start_time

    print(f"Sequential Time: {sequential_time:.2f} seconds")
    print(f"Multithreading Time: {multithreading_time:.2f} seconds")
    print(f"Multiprocessing Time: {multiprocessing_time:.2f} seconds")
    print(f"Speedup with Multithreading: {sequential_time / multithreading_time:.2f}")
    print(f"Speedup with Multiprocessing: {sequential_time / multiprocessing_time:.2f}")
