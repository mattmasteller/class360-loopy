import os
import shutil

def get_file_size_in_mb(file_path):
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / 1024 / 1024
    file_size_mb = round(file_size_mb, 1)
    return file_size_mb

def create_html(input_path, video_path, num_loops=5):
    print("Creating HTML file...")
    
    output_path = os.path.dirname(video_path)
    
    shutil.copy(input_path, output_path)
    
    html = "<html>\n<head>\n"
    html += "<style>\nbody {display: flex; flex-direction: column; align-items: center;}\n</style>\n"
    html += "</head>\n<body>\n"

    # Add the input video
    html += f'<h2>{os.path.basename(input_path)} ({get_file_size_in_mb(input_path)} MB)</h2>\n'
    html += '<video width="800" height="450" controls>\n'
    html += f'<source src="{os.path.basename(input_path)}" type="video/mp4">\n'
    html += "Your browser does not support the video tag.\n"
    html += "</video>\n<br/>\n"
    
    # Add the no background video
    no_background_path = f"{output_path}/no_background.mp4"
    html += f'<h2>{os.path.basename(no_background_path)} ({get_file_size_in_mb(no_background_path)} MB)</h2>\n'
    html += '<video width="800" height="450" controls>\n'
    html += f'<source src="no_background.mp4" type="video/mp4">\n'
    html += "Your browser does not support the video tag.\n"
    html += "</video>\n<br/>\n"

    # Add the output loop videos
    for i in range(num_loops):
        loop_path = f"{output_path}/loop_{i}.webm"
        if os.path.exists(loop_path):
            html += f'<h2>{os.path.basename(loop_path)} ({get_file_size_in_mb(loop_path)} MB)</h2>\n'
            html += '<video width="800" height="450" loop autoplay muted playsinline>\n'
            html += f'<source src="loop_{i}.webm" type="video/webm">\n'
            html += "Your browser does not support the video tag.\n"
            html += "</video>\n<br/>\n"
        
    html += "</body>\n</html>"
    
    with open(f"{output_path}/index.html", "w") as file:
        file.write(html)
