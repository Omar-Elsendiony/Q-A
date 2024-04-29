import os
import shutil

def deleteFolder(folder_path):
    # Get a list of all folders in the directory
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    # Find the folder that starts with 'FauxPy'
    fauxpy_folder = next((f for f in folders if f.startswith('FauxPy')), None)

    # Delete the folder if it exists
    if fauxpy_folder:
        shutil.rmtree(os.path.join(folder_path, fauxpy_folder))
        print(f"The folder '{fauxpy_folder}' has been deleted.")
    else:
        print("No folder starting with 'FauxPy' found.")





