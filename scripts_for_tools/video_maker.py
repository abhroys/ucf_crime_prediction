import cv2
import os
from collections import defaultdict

def group_frames_by_video(frame_folder):
    """
    Groups frames by video based on their filename prefixes.

    Args:
        frame_folder (str): Path to the folder containing frames.

    Returns:
        dict: A dictionary where keys are video identifiers and values are lists of frame paths.
    """
    frame_files = sorted(
        [f for f in os.listdir(frame_folder) if f.endswith('.png') or f.endswith('.jpg')]
    )
    
    grouped_frames = defaultdict(list)
    for frame_file in frame_files:
        # Extract video identifier (e.g., 'video1' from 'video1_frame001.png')
        video_id = '_'.join(frame_file.split('_')[:-1])  # Adjust based on naming convention
        grouped_frames[video_id].append(os.path.join(frame_folder, frame_file))
    
    return grouped_frames

def frames_to_video(frame_paths, output_video, fps=30):
    """
    Combines a list of frames into a video.

    Args:
        frame_paths (list): List of frame file paths.
        output_video (str): Path to save the output video.
        fps (int): Frames per second for the video.
    """
    if not frame_paths:
        print("No frames provided for video creation!")
        return

    # Read the first frame to determine video size
    first_frame = cv2.imread(frame_paths[0])
    height, width, layers = first_frame.shape
    size = (width, height)

    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for .avi format
    out = cv2.VideoWriter(output_video, fourcc, fps, size)

    print(f"Creating video '{output_video}' with {len(frame_paths)} frames...")
    for frame_path in frame_paths:
        frame = cv2.imread(frame_path)
        out.write(frame)

    out.release()
    print(f"Video saved to {output_video}")

def process_all_videos(frame_folder, output_folder, fps=30):
    """
    Processes all video frames in a folder and creates separate videos.

    Args:
        frame_folder (str): Path to the folder containing frames.
        output_folder (str): Path to save the output videos.
        fps (int): Frames per second for the videos.
    """
    grouped_frames = group_frames_by_video(frame_folder)
    os.makedirs(output_folder, exist_ok=True)

    for video_id, frame_paths in grouped_frames.items():
        output_video = os.path.join(output_folder, f"{video_id}.avi")
        frames_to_video(frame_paths, output_video, fps)

# Example usage
frame_folder = "Train\RoadAccidents"  # Replace with your folder containing frames
output_folder = "output_folder_video_train\Shoplifting"      # Replace with desired output folder
fps = 30                                    # Frames per second

process_all_videos(frame_folder, output_folder, fps)
