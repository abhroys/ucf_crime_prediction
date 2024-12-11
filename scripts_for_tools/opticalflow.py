import os
import cv2
import numpy as np

def compute_optical_flow_per_class(input_dir, output_dir):
    """
    Compute optical flow for all frames in the input directory and save in the output directory.
    Args:
        input_dir (str): Path to the input class folder (e.g., Train/Abuse).
        output_dir (str): Path to the output class folder for optical flow.
    """
    os.makedirs(output_dir, exist_ok=True)
    frame_files = sorted([f for f in os.listdir(input_dir) if f.endswith(".png")])
    
    prev_frame = cv2.imread(os.path.join(input_dir, frame_files[0]))
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    for i in range(1, len(frame_files)):
        curr_frame = cv2.imread(os.path.join(input_dir, frame_files[i]))
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

        # Compute optical flow
        flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        # Convert to HSV for visualization
        hsv = np.zeros_like(prev_frame)
        hsv[..., 1] = 255
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        flow_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # Save optical flow image
        flow_filename = f"flow_{i:04d}.png"
        cv2.imwrite(os.path.join(output_dir, flow_filename), flow_image)

        prev_gray = curr_gray

def generate_optical_flow_for_dataset(root_dir, output_root_dir, categories):
    """
    Generate optical flow for the entire dataset organized by categories.
    Args:
        root_dir (str): Root directory of the dataset (e.g., Train or Test).
        output_root_dir (str): Root directory to save optical flow frames.
        categories (list): List of class names (subfolder names).
    """
    for category in categories:
        input_dir = os.path.join(root_dir, category)
        output_dir = os.path.join(output_root_dir, category)
        print(f"Processing class: {category}")
        compute_optical_flow_per_class(input_dir, output_dir)
        print(f"Optical flow generated for class: {category}")

# Example usage
categories = [ "RoadAccidents", ]

# Generate optical flow for Train and Test sets
generate_optical_flow_for_dataset("Train", "Train/OpticalFlow", categories)
generate_optical_flow_for_dataset("Test", "Test/OpticalFlow", categories)
