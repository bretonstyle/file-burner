import sys;
import os;
import time;
import threading;
import select;
import queue;
#from openai.api import OpenAI;


# Different modules for key detection on Windows vs Unix-based systems

def process_directory():
    """
    Process the directory by listing all the files in it.

    This function prompts the user to enter a directory path, then lists all the files in that directory.
    If no files are found or an error occurs, it displays an appropriate message.

    Parameters:
    None

    Returns:
    None
    """
    directory = input("Please enter the directory path: ")
    files = list_files_in_directory(directory)
    if files is not None:
        print(f"Files in directory {directory}:")
        for file in files:
            print(file)
    else:
        print("No files found or an error occurred.")

def list_files_in_directory(directory):
    """
    Lists all the files in the specified directory.

    Args:
        directory (str): The path to the directory.

    Returns:
        list: A list of file names in the directory.

    Raises:
        None

    """
    try:
        files = os.listdir(directory)
        return files
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


fire1 = """
^
(   )
(     )
(   )
^
"""

fire2 = """
    (
(   )
(     )
(       )
(         )
(       )
(     )
(   )
    ^
"""

def keypress(stop_queue):
    while True:
        if select.select([sys.stdin,],[],[],0.0)[0]:
            stop_queue.put('stop')
            break

def print_fire(stop_queue):
    fire = fire1
    while True:
        if not stop_queue.empty():
            break
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
        print(fire)
        time.sleep(.1)  # Wait for 1 second
        fire = fire2 if fire == fire1 else fire1

def main():

    process_directory()
    stop_queue = queue.Queue()

    fire_thread = threading.Thread(target=print_fire, args=(stop_queue,))
    fire_thread.start()

    keypress_thread = threading.Thread(target=keypress, args=(stop_queue,))
    keypress_thread.start()

    fire_thread.join()
    keypress_thread.join()

    


if __name__ == "__main__":
    main()