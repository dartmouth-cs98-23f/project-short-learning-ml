from collections import deque
import statistics

def clipper(topics, timestamps, window_size, mean_or_median, change_threshold):
    if len(topics) != len(timestamps):
        raise ValueError("unequal number of topics and timestamps")

    n = len(topics)
    list_of_start_and_end_times = []

    window_topics = deque(maxlen=window_size)
    window_timestamps = deque()

    for i in range(n):
        window_topics.append(topics[i])
        window_timestamps.append(timestamps[i])

        if len(window_topics) == window_size or i == n - 1 or timestamps[i] == 0:
            if mean_or_median == 'mean':
                comp = statistics.mean(topics[i:i+window_size])
            else:
                comp = statistics.median(topics[i:i+window_size])

            if i == 0:
                curr_comp = comp

            # print(i, curr_comp, comp, window_topics)
                
            if (abs(curr_comp - comp) > change_threshold) or i == n - 1:
                curr_comp = comp
                list_of_start_and_end_times.append((window_timestamps[0], window_timestamps[-2]))
                end = window_timestamps[-1]
                window_timestamps = deque()
                window_timestamps.append(end)

    return list_of_start_and_end_times

# topics = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 2, 2, 1, 1, 1, 1, 1]
# timestamps = [i for i in range(len(topics))]

# change_threshold = 0.7
# window_size = 3
# result = clipper(topics, timestamps, window_size, 'mean', change_threshold)

# print("Points in time where the trend changes:")
# for start, end in result:
#     print(f"Start: {start}, End: {end}")
