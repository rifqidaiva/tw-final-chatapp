import os


def ensure_dir(directory):
    """
    Ensure that the specified directory exists. If it doesn't, create it.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory {directory} created.")
    else:
        print(f"Directory {directory} already exists.")
