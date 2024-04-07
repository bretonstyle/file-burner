import sys;
import os;
import time;
import threading;
import select;
import queue;
import asciifire;
import subprocess;
import json;
import openai;
import logging;
import argparse;

# Create the logger and log to a file  
logging.basicConfig(filename='main.log', level=logging.INFO)

# Create the parser
parser = argparse.ArgumentParser(description='Process a config file.')
parser.add_argument('-c', '--config', default='config.json', help='The path to the config file.')
args = parser.parse_args()

# Pull the config file path from the arguments
config_file = args.config

# If the config file does not exist, use environment variable
if not os.path.exists(config_file):
    openai_key = os.environ['OPENAI_KEY']
    logging.info("File not found. Using OpenAI key from environment variable.")

else:
    # Pull OpenAI key from config.json
    with open(config_file) as f:
        data = json.load(f)
        openai_key = data['openai_key']
        logging.info("Using OpenAI key from config file.")

#Initialize OpenAI client
client = openai.OpenAI(api_key=openai_key);

def test_openai():
    #TODO: Add try/catch block to handle OpenAI exceptions
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Write me a Haiku, in the form of a pirate"},
    ],
    temperature=0,
    )
    print(response.choices[0].message.content)



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

def keypress(stop_queue):
    while True:
        if select.select([sys.stdin,],[],[],0.0)[0]:
            stop_queue.put('stop')
            break

def main():
    #process_directory()
    #subprocess.call(["python3", "asciifire.py"])
    test_openai()

if __name__ == "__main__":
    main()