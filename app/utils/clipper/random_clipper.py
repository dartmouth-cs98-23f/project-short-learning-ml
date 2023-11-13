from datetime import timedelta
import random
import pandas as pd
import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))

def clipper(filename):
    df = pd.read_csv(filename)
    duration = df['second'].iloc[-1]
    clips = int(duration//40)
    return extract_random_clip_times(duration, num_clips=clips)    

def extract_random_clip_times(total_video_length, clip_duration=30, num_clips=5):
    clip_times = []
    used_times = set()

    for _ in range(num_clips):
        start_time = random.uniform(0, total_video_length - clip_duration)
        end_time = start_time + clip_duration

        # print(start_time, end_time)
        # print(used_times)
        # print('----------------------------------------------------------------')

        # Ensure non-overlapping by checking against used times
        while any(existing_start <= start_time <= existing_end or existing_start <= end_time <= existing_end
                  for existing_start, existing_end in used_times):
            start_time = random.uniform(0, total_video_length - clip_duration)
            end_time = start_time + clip_duration

        used_times.add((start_time, end_time))
        clip_times.append((timedelta(seconds=start_time), timedelta(seconds=end_time)))

    return clip_times