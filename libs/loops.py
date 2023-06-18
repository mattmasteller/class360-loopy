import cv2
import os
from PIL import Image
import imagehash
from scipy.spatial import distance
import imageio
import numpy as np
from skimage.transform import resize

def extract_frames(video_path):
    frames = []
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    video.release()
    return frames, fps

def calculate_hash(frame):
    return imagehash.phash(Image.fromarray(frame))

def hamming_distance(hash1, hash2):
    return distance.hamming(list(hash1.hash.flatten()), list(hash2.hash.flatten()))

def write_output(frames, start, end, format, output_path, fps):
    if format == "gif":
        writer = imageio.get_writer(output_path, format=format, mode='I', duration=1.0/fps)
    else: # for 'mp4' and 'webm'
        writer = imageio.get_writer(output_path, format=format, fps=fps, codec="vp9" if format=="webm" else None, mode='I', macro_block_size=None, bitrate='8000k')
    for i in range(start, end+1):
        frame = frames[i]
        height, width, _ = frame.shape
        if height % 16 != 0 or width % 16 != 0:
            new_height = (height // 16) * 16
            new_width = (width // 16) * 16
            frame = resize(frame, (new_height, new_width), mode='reflect', preserve_range=True)
        writer.append_data(frame.astype(np.uint8))
    writer.close()

def is_frame_too_dark(frame, threshold=30):
    return np.mean(frame) < threshold

def create_loops(video_path, num_loops=5, window_size=50, min_loop_length=10):
    output_path = os.path.dirname(video_path)
    
    print("Extracting frames...")
    frames, fps = extract_frames(video_path)
    frame_hashes = [calculate_hash(frame) for frame in frames]
    
    candidates = []
    print("Finding loop candidates...")
    for i in range(len(frames) - window_size):
        if is_frame_too_dark(frames[i]):
            continue
        for j in range(i + min_loop_length, i + window_size):
            if is_frame_too_dark(frames[j]):
                continue
            dist = hamming_distance(frame_hashes[i], frame_hashes[j])
            if dist < 0.1:
                mid_frame = frames[int((i + j) / 2)]
                mid_hash = calculate_hash(mid_frame)
                mid_dist = hamming_distance(frame_hashes[0], mid_hash)
                if mid_dist > 0.1:
                    candidates.append((i, j, dist))
    
    candidates.sort(key=lambda x: x[2])

    for i in range(min(num_loops, len(candidates))):
        start, end, _ = candidates[i]
        print(f'Creating loop {i} from frames {start} to {end}...')
        write_output(frames, start, end, 'webm', f'{output_path}/loop_{i}.webm', fps)
        
    return len(candidates)
