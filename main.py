import os;
import json;
import openai;
import logging;
import argparse;
import asciifire;

# Create the logger and log to a file  
logging.basicConfig(filename='main.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.info("File Burner Initialized")

##############################################
def get_options():
##############################################
    # Process command line options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b',
        '--block',
        action='store_true',
        help='Enable blocking getch mode'
    )
    parser.add_argument(
        '-s',
        '--cycle',
        action='store_true',
        help='Cycle ascii colors'
    )
    parser.add_argument(
        '-t',
        '--cycletime',
        type=int,
        help='Cycle time interval'
    )
    parser.add_argument(
        '-d',
        '--delay',
        type=int,
        default=18750,
        help='Delay time in seconds. Will be divided by 1000000'
    )
    parser.add_argument(
        '-c',
        '--color',
        type=str,
        default='RED',
        help='Specify ascii color'
    )
    parser.add_argument(
        '-p',
        '--properties',
        type=str,
        default='config.json',
        help='Specify config file'
    )

    options = parser.parse_args()

    # If the human specifies a cycle_time, they must want to cycle.
    if options.cycletime:
        options.cycle = True

    # Set default cycle time.
    if not options.cycletime:
        options.cycletime = 15

    # Valid colors.
    options.validcolors = { 'RED':1, 'BLUE':2, 'GREEN':3, 'YELLOW':4, 'WHITE': 5 }
    if options.color != 'RED':
        options.color = options.color.upper()
        if not options.validcolors.get(options.color):
            # Human specified bad color.. using RED.
            options.color = 'RED'

    return (options)

# Pull the config file path from the arguments
options = get_options()
config_file = options.properties

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

def test_openai(prompt):
    #TODO: Add try/catch block to handle OpenAI exceptions
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an edgy computer who likes to swear."},
        {"role": "user", "content": prompt},
    ],
    temperature=0,
    )
    print(response.choices[0].message.content)


def craft_prompt(num=20):
    is_spicy = input("Do you want spicy, swear-laden insults? (y/n): ")
    if is_spicy == 'y':
        return f"""Retrieve a list of {num} swear-laden insults, 60 or less characters long, 
        directed at files on a computer, no repeats. Number the list. Call them file. Don't acknowledge the prompt. Only the list."""
    else:
        return f"""Retrieve a list of {num} work-safe insults, 60 or less characters long, 
        directed at files on a computer, no repeats. Number the list. Call them file. Don't acknowledge the prompt. Only the list."""


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
        print(f"Files in directory:     {directory}:")
        logging.info(f"Files in directory:     {directory}:")
        for file in files:
            print(file)
            logging.info(file)
        return files
    else:
        print("No files found or an error occurred.")
        logging.info("No files found or an error occurred.")
    

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
        logging.error(f"An error occurred: {e}")
        print (f"An error occurred, aborting...")
        return None

if __name__ == "__main__":
    list_of_files = process_directory()
    prompt = craft_prompt(len(list_of_files))
    test_openai(prompt)
    fire = asciifire.Fire(options)
    fire.run()
    