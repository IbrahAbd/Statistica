import os

def clean_images(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            # Check if the file ends with _0.jpg
            if not filename.endswith("_0.jpg"):
                # If it doesn't match, delete the file
                os.remove(os.path.join(folder_path, filename))
                print(f"Deleted: {filename}")

if __name__ == "__main__":
    folder_path = "E:\github\Statistica\Images"
    clean_images(folder_path)
