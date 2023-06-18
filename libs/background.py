import os
import torch

def remove_background(input_path, output_path):
    full_output_path = os.path.join(output_path, 'no_background.mp4')
    print("full_output_path: ", full_output_path)
    
    # Load the model.
    print("Loading model...")
    model = torch.hub.load("PeterL1n/RobustVideoMatting", "mobilenetv3") # or "resnet50"

    # Converter API.
    print("Loading converter...")
    convert_video = torch.hub.load("PeterL1n/RobustVideoMatting", "converter")

    print("Converting video...")
    convert_video(
        model,                                  # The model, can be on any device (cpu or cuda).
        input_source=input_path,                # A video file or an image sequence directory.
        output_type='video',                    # Choose "video" or "png_sequence"
        output_composition=full_output_path,    # File path if video; directory path if png sequence.
        output_video_mbps=4,                    # Output video mbps. Not needed for png sequence.
        downsample_ratio=None,                  # A hyperparameter to adjust or use None for auto.
        seq_chunk=12,                           # Process n frames at once for better parallelism.
    )
    
    print("Done removing background from video.")
    return full_output_path
