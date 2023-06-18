# Video Background Removal and Looping

This repository contains a proof of concept project for removing the video background and creating smooth WEBM loops from a source MP4 video. We define a smooth loop as a sequence of video frames, such that the first and last frames have a high similarity. 

## Process Overview - Video Background Removal

We utilize an advanced PyTorch machine learning model for the removal of video backgrounds. This model was developed by a research team from ByteDance (makers of TikTok).

More information can be found here:

- [GitHub Repository](https://github.com/PeterL1n/RobustVideoMatting)
- [Research Paper (PDF)](https://arxiv.org/pdf/2108.11515.pdf)
- [Showreel Video on YouTube](https://www.youtube.com/watch?v=Jvzltozpbpk)

## Process Overview - Looping

- Split the source MP4 video into individual frames.
- Generate perceptual hashes for each frame.
- Compare each frame to its neighboring frames using the hamming distance of the hashes, while taking care to prevent edge cases such as an all-black set of frames.
- Ensure that there is sufficient change in the video by comparing the middle frame between 2 potential candidate frames to the start of the loop.
- If the two candidates are similar and pass the edge tests, they are marked as potential output.
- Select the top 5 candidate loops, sorted by best match, and encode them into .webm formats.

## Getting Started

### Prerequisites

To use the source code, you must first install FFMPEG, PyTorch, and other required dependencies specified in the [requirements.txt](https://github.com/mattmasteller/class360-loopy/blob/main/requirements.txt) file.

### Install FFMPEG

See [this guide](https://www.wikihow.com/Install-FFmpeg-on-Windows) for Windows, or [this guide](https://www.ffmpeg.org/download.html) for Linux, or [this guide](https://www.ffmpeg.org/download.html#build-mac) for Mac.

### Installation

To clone the repository, run:

```bash
git clone https://github.com/mattmasteller/class360-loopy
```

Then install the dependencies by running:

```bash
pip install -r requirements.txt
```

### Running the Code

After completing the installation steps, you can run the code by executing:

```bash
python main.py --file example.mp4 --loops 5
```

Replace `example.mp4` with the path to your input file. Replace `5` with the number of loop candidates you want to generate.

### Viewing the Output

The output files will be saved in a folder named `out-[timestamp]` in the same directory as the input file. The output folder will contain the following files:

- `no_background.mp4` - The input video with the background removed.
- `loop_0.webm` - The first loop candidate.
- `loop_1.webm` - The second loop candidate.
- `loop_n.webm` - Etc.
- `example.mp4` (i.e. the input file name) - The input video. This is a copy of the input file, not the original file.
- `index.html` - A web page for viewing the output.

## Contributing

We welcome all contributors to this open-source project. Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. This means you are free to share and adapt the material under the following terms: you must give appropriate credit, you may not use the material for commercial purposes, and if you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original. See the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

We'd like to express our gratitude to the ByteDance research team for their excellent work on video matting which is utilized in this project.
