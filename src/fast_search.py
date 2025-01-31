import os
import sys
from datetime import datetime, timedelta

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def find_next_newline(f, pos):
    f.seek(pos)
    chunk_size = 4096
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            return None
        newline_pos = chunk.find(b'\n')
        if newline_pos != -1:
            return pos + newline_pos
        pos += len(chunk)
        if len(chunk) < chunk_size:
            return None

def get_line_date(f, pos):
    newline_pos = find_next_newline(f, pos)
    if newline_pos is None:
        return None
    next_line_start = newline_pos + 1
    file_size = os.fstat(f.fileno()).st_size
    if next_line_start >= file_size:
        return None
    f.seek(next_line_start)
    line = f.readline()
    if not line:
        return None
    try:
        line_str = line.decode('utf-8', errors='ignore').strip()
        parts = line_str.split()
        if not parts:
            return None
        return parts[0]
    except UnicodeDecodeError:
        return None

def binary_search_date(f, target_date_str):
    target_date = parse_date(target_date_str)
    low = 0
    high = os.fstat(f.fileno()).st_size
    start_pos = None

    while low < high:
        mid = (low + high) // 2
        current_date_str = get_line_date(f, mid)
        if current_date_str is None:
            high = mid
            continue
        try:
            current_date = parse_date(current_date_str)
        except ValueError:
            high = mid
            continue
        if current_date < target_date:
            low = mid + 1
        else:
            high = mid

    if low >= os.fstat(f.fileno()).st_size:
        return None

    newline_pos = find_next_newline(f, low)
    if newline_pos is None:
        return None
    line_start = newline_pos + 1
    file_size = os.fstat(f.fileno()).st_size
    if line_start >= file_size:
        return None
    f.seek(line_start)
    line = f.readline()
    if not line:
        return None
    try:
        line_str = line.decode('utf-8', errors='ignore').strip()
        parts = line_str.split()
        if not parts:
            return None
        current_date_str = parts[0]
        if current_date_str == target_date_str:
            return line_start
        else:
            return None
    except UnicodeDecodeError:
        return None

def find_date_position(filename, target_date_str):
    with open(filename, 'rb') as f:
        start_pos = binary_search_date(f, target_date_str)
        if start_pos is None:
            return None, None
        next_date = parse_date(target_date_str) + timedelta(days=1)
        next_date_str = next_date.strftime("%Y-%m-%d")
        end_pos = binary_search_date(f, next_date_str)
        file_size = os.path.getsize(filename)
        if end_pos is None:
            end_pos = file_size
        return start_pos, end_pos

def extract_logs(input_filename, target_date_str, output_filename):
    start_pos, end_pos = find_date_position(input_filename, target_date_str)
    if start_pos is None:
        with open(output_filename, 'w') as f_out:
            f_out.write('')
        return
    with open(input_filename, 'rb') as f_in:
        f_in.seek(start_pos)
        with open(output_filename, 'wb') as f_out:
            while True:
                current_pos = f_in.tell()
                if current_pos >= end_pos:
                    break
                line = f_in.readline()
                if not line:
                    break
                f_out.write(line)

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_logs.py YYYY-MM-DD")
        sys.exit(1)
    date_arg = sys.argv[1]
    try:
        parse_date(date_arg)
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        sys.exit(1)
    input_filename = 'test_logs.log'
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, f'output_{date_arg}.txt')
    extract_logs(input_filename, date_arg, output_filename)

if __name__ == '__main__':
    main()