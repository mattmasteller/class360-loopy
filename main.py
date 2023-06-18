import argparse
import datetime # for timestamping
import os
from libs.background import remove_background
from libs.loops import create_loops
from libs.test_html import create_html

def main():
    parser = argparse.ArgumentParser(description='Create smoothly looping .webm videos.')
    parser.add_argument('--file', type=str, help='Path to the input .mp4 video file. Defaults to input.mp4.')
    parser.add_argument('--loops', type=int, help='Number of loop candidates to create. Defaults to 5.')
    
    # Parse arguments
    args = parser.parse_args()
    input_path = args.file if args.file else 'example.mp4'
    num_loops = args.loops if args.loops else 5
    
    # Create output directory
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    output_path = f'out-{timestamp}'
    os.mkdir(output_path)
    
    # Process video
    video_path = remove_background(input_path, output_path)
    num_candidates = create_loops(video_path=video_path, num_loops=num_loops)
    create_html(input_path=input_path, video_path=video_path, num_loops=min(num_loops, num_candidates))

if __name__ == "__main__":
    main()