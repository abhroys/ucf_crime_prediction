import os

# Specify the folder path
normal_videos_folder = r"D:\abhay\dataset_DL\ufc_crime_dataset\Test\NormalVideos"  # Update with the correct folder path

# Define the filename to keep up to
keep_up_to = "Normal_Videos_923_x264_18220.png"  # Add the .png extension

# List all files in the folder
try:
    all_files = sorted(os.listdir(normal_videos_folder))
except FileNotFoundError:
    print(f"Error: The folder '{normal_videos_folder}' does not exist.")
    exit()

# Debug: Check if the specified file exists
if keep_up_to not in all_files:
    print(f"Error: File '{keep_up_to}' not found in the folder.")
    print("Files in the folder:")
    print(all_files[:10])  # Print first 10 files for debugging
    exit()

# Get the index of the file to keep up to
keep_up_to_index = all_files.index(keep_up_to)

# Collect files to delete (those beyond the specified file)
files_to_delete = all_files[keep_up_to_index + 1:]

# Delete the files
deleted_files_count = 0
for file in files_to_delete:
    file_path = os.path.join(normal_videos_folder, file)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted: {file}")
        deleted_files_count += 1

print(f"Total files deleted: {deleted_files_count}")
