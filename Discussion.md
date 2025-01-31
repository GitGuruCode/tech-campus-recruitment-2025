# Fast Log Search

This project provides a Python script to efficiently extract logs for a specific date from a large log file, using binary search for optimal performance.

---

## Solutions Considered

1. **Linear Search**  
   - This approach involves reading the file line by line and checking the date.  
   - **Problem**: It is inefficient for large files due to high I/O operations.

2. **Binary Search**  
   - The file is treated as a binary stream, and binary search is applied to locate the target date efficiently.  
   - **Advantage**: Reduces search time significantly for large log files.

---

## Final Solution Summary

The binary search approach was selected as it minimizes the number of reads required by targeting specific positions in the file. This method ensures fast and reliable log extraction, even for very large files.

---

## Steps to Run the Script

1. Ensure your folder structure matches the following:


2. **Run the script**:
- Navigate to the root folder (`tech-campus-recruitment-2025`) in the terminal.
- Use the command:
  ```bash
  python ./src/fast_search.py YYYY-MM-DD
  ```
  Example for July 29, 2015:
  ```bash
  python ./src/fast_search.py 2015-07-29
  ```

3. **Output**:
- The extracted logs will be saved in the `output` folder with the filename format:  
  `output_<YYYY-MM-DD>.txt`  
  Example: `output/output_2015-07-29.txt`.

---

## Features

- **Efficient**: Utilizes binary search to reduce file processing time.
- **Scalable**: Handles large log files seamlessly.
- **Customizable**: Modify paths or file handling for specific requirements.
