from ftpretty import ftpretty
import os

local_dist = os.path.join(".", "dist")
remote_dist = "/public_html/MacroTracker/"
assets = remote_dist + "assests/"

def uploadDir(f, local_directory, remote_directory):
    for file in os.listdir(local_directory):
        local_file_path = os.path.join(local_directory, file)
        if os.path.isfile(local_file_path):
            print(f"Uploading file: {local_file_path} to {remote_directory}")
            f.put(local_file_path, remote_directory)
        elif os.path.isdir(local_file_path):
            new_remote_directory = f'{remote_directory}{file}/'
            print(f"Child directory remotely: {new_remote_directory}, and locally: {local_file_path}")
            uploadDir(f, local_file_path, new_remote_directory)

f = ftpretty(
    host=os.environ["HOST"],
    user=os.environ["USERNAME"],
    password=os.environ["PASSWORD"],
    secure=True,
    port=21
)

f.delete(assets)
uploadDir(f, local_dist, remote_dist)
f.close()
