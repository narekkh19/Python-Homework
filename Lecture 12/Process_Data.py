import random
import time

def generate_random_data(file_name):
    with open(file_name, 'w') as file:
        for _ in range(100):
            line = ' '.join(str(random.randint(1, 100)) for _ in range(20))
            file.write(line + '\n')

def parse_file_content(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    parsed_lines = [list(map(int, line.split())) for line in lines]
    return parsed_lines

def filter_above_threshold(lines, threshold=40):
    filtered_lines = [list(filter(lambda x: x > threshold, line)) for line in lines]
    return filtered_lines

def save_data_to_file(file_name, data):
    with open(file_name, 'w') as file:
        for line in data:
            file.write(' '.join(map(str, line)) + '\n')

def yield_file_data(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            yield list(map(int, line.split()))

def time_tracker(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} completed in {end_time - start_time:.2f} seconds.")
        return result
    return wrapper

@time_tracker
def process_data():
    file_name = 'random_numbers.txt'
    generate_random_data(file_name)
    data = parse_file_content(file_name)
    filtered_data = filter_above_threshold(data)
    save_data_to_file(file_name, filtered_data)
    print("Contents of filtered file (using generator):")
    for line in yield_file_data(file_name):
        print(line)

if __name__ == '__main__':
    process_data()
