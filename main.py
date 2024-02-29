import sys;
import os;

def process_directory():
    directory = input("Please enter the directory path: ")
    files = list_files_in_directory(directory)
    if files is not None:
        print(f"Files in directory {directory}:")
        for file in files:
            print(file)
    else:
        print("No files found or an error occurred.")

def list_files_in_directory(directory):
    try:
        files = os.listdir(directory)
        return files
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def main():
    process_directory()

if __name__ == "__main__":
    main()