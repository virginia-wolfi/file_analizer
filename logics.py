import heapq
import time


class EmptyFileError(Exception):
    pass


def analyze_file(file_path: str) -> dict[str, any]:
    """
    Process a file containing numbers to find various statistics and sequences.

    Args:
    - file_path (str): Path to the file containing numbers.

    Returns:
    - dict: A dictionary containing the following keys:
        - 'min_value' (int): Minimum value found in the file.
        - 'max_value' (int): Maximum value found in the file.
        - 'average' (float): Average of all numbers in the file.
        - 'median' (float): Median of all numbers in the file.
        - 'max_inc_seq' (list): Longest increasing sequence of numbers.
        - 'max_dec_seq' (list): Longest decreasing sequence of numbers.

     Raises:
    - EmptyFileError: If the file does not contain any numbers.
    """
    # Variables to track the longest increasing and decreasing sequences
    max_inc_seq_len = 0
    max_dec_seq_len = 0

    # Variables to track the median using two heaps
    min_heap = []
    max_heap = []

    # Open the file and read the first line to initialize variable
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        if not first_line:
            raise EmptyFileError("The file is empty.")

        # Initialize with the first number as the barrier element
        barrier_element = int(first_line)
        min_val = barrier_element
        max_val = barrier_element
        total_sum = barrier_element
        count = 1
        prev_num = barrier_element
        current_inc_seq = [barrier_element]
        current_dec_seq = [barrier_element]
        max_inc_seq = [barrier_element]
        max_dec_seq = [barrier_element]

        # Initialize heaps with the barrier element
        heapq.heappush(max_heap, -barrier_element)  # max_heap stores the negative values for max-heap behavior

        # Process each subsequent number in the file
        for line in file:
            num = int(line.strip())

            # Update min, max, sum, and count
            min_val = min(min_val, num)
            max_val = max(max_val, num)
            total_sum += num
            count += 1

            # Maintain heaps for median calculation
            if num <= -max_heap[0]:
                heapq.heappush(max_heap, -num)
            else:
                heapq.heappush(min_heap, num)

            # Balance heaps
            if len(max_heap) > len(min_heap) + 1:
                heapq.heappush(min_heap, -heapq.heappop(max_heap))
            elif len(min_heap) > len(max_heap):
                heapq.heappush(max_heap, -heapq.heappop(min_heap))

            # Update sequences
            if num > prev_num:
                current_inc_seq.append(num)
                current_dec_seq = [num]
            elif num < prev_num:
                current_dec_seq.append(num)
                current_inc_seq = [num]
            else:
                current_inc_seq = [num]
                current_dec_seq = [num]

            # Update longest sequences
            if len(current_inc_seq) > max_inc_seq_len:
                max_inc_seq_len = len(current_inc_seq)
                max_inc_seq = current_inc_seq.copy()

            if len(current_dec_seq) > max_dec_seq_len:
                max_dec_seq_len = len(current_dec_seq)
                max_dec_seq = current_dec_seq.copy()

            prev_num = num

    # Calculate average
    average = total_sum / count

    # Calculate median from heaps
    if len(max_heap) > len(min_heap):
        median = -max_heap[0]
    else:
        median = (-max_heap[0] + min_heap[0]) / 2

    # Return results as a dictionary
    return {
        'max_value': max_val,
        'min_value': min_val,
        'median': median,
        'average': average,
        'max_inc_seq': max_inc_seq,
        'max_dec_seq': max_dec_seq
    }


# Prompt user for file path input
def main():
    file_path = input("Enter the path to the file: ").strip()
    start_time = time.time()
    try:
        result = analyze_file(file_path)
        print(f"Max: {result['max_value']}\n"
              f"Min: {result['min_value']}\n"
              f"Median: {result['median']}\n"
              f"Average: {result['average']:.2f}\n"
              f"Longest Increasing Sequence: {str(result['max_inc_seq'])[1:-1]}\n"
              f"Longest Decreasing Sequence: {str(result['max_dec_seq'])[1:-1]}\n")
    except EmptyFileError as e:
        print(f"Error: {e}")
    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time:.2f} seconds')


if __name__ == "__main__":
    main()
