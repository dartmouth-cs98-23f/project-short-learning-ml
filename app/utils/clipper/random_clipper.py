from datetime import timedelta
import random
import pandas as pd
import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))

data_dir = '../data/'
transcripts_dir = 'transcripts/'

def random_clipper(filename):
    video_path =  data_dir+transcripts_dir+filename
    df = pd.read_csv(video_path)
    last = df['second'].iloc[-1]
    diff = last - df['second'][0]
    duration = timedelta(seconds=diff) 
    clips = int(diff//40)
    return extract_random_clip_times(duration, num_clips=clips)    

def extract_random_clip_times(total_video_length, clip_duration=30, num_clips=5):
    clip_times = []
    used_times = set()

    for _ in range(num_clips):
        start_time_seconds = random.uniform(0, total_video_length.total_seconds() - clip_duration)
        start_time = timedelta(seconds=start_time_seconds)
        end_time = start_time + timedelta(seconds=clip_duration)

        print(start_time, end_time)
        print(used_times)
        print('----------------------------------------------------------------')

        # Ensure non-overlapping by checking against used times
        while any(start_time <= existing_end and existing_start <= end_time
                  for existing_start, existing_end in used_times):
            start_time_seconds = random.uniform(0, total_video_length.total_seconds() - clip_duration)
            start_time = timedelta(seconds=start_time_seconds)
            end_time = start_time + timedelta(seconds=clip_duration)

        used_times.add((start_time, end_time))
        clip_times.append((str(start_time), str(end_time)))

    return clip_times

# Example usage:
# total_video_length = timedelta(seconds=300) 
# num_clips = 5 
# clip_times = extract_random_clip_times(total_video_length, num_clips=num_clips)

# for i, (start_time, end_time) in enumerate(clip_times, start=1):
#     print(f"Clip {i}: Start Time: {start_time}, End Time: {end_time}")

res = random_clipper('playlist_SecondPunicWar_CrossingTheAlps_Hannibal_Crosses_the_Alps_-_The_Invasion_of_Italy_-_The_Great_Carthaginian_General_-_Part_23.csv')

for i, (start_time, end_time) in enumerate(res, start=1):
    print(f"Clip {i}: Start Time: {start_time}, End Time: {end_time}")