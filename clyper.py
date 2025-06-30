import os
import json
import sys
import pyperclip
import datetime

# Path of the script 
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIRECTORY, "clyper_data.json")

# Load existing data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as file:
        try:
            DATA = json.load(file)
        except json.JSONDecodeError:
            DATA = {}
else:
    DATA = {}

def check_unwanted_chars(text):
    return any(c in text for c in ['`', '"', "'"])

def check_unwanted_chars_in_key(key):
    return any(c in key for c in ['`', '"', "'", ""])


def remove_unwanted_chars(text):
    return text.translate(str.maketrans('', '', '`"\''))

def remove_unwanted_chars_key(key):
    cleaned_key = ''.join(key.split())
    return cleaned_key.translate(str.maketrans('', '', '`"\''))


def print_warning(text):
    cleaned_text = remove_unwanted_chars(text)
    print("⚠️  WARNING!")
    print("Detected unwanted character(s) in your input which could cause errors.")
    print(f"Changed your input from:\n  {text}\nto:\n  {cleaned_text}")
    user_ans = input(f"Press 'y' to continue with cleaned input or 'n' to cancel: ").strip().lower()
    return user_ans

def take_user_validation(text):
    user_input = print_warning(text)
    return user_input == 'y'

# Adds data into the JSON file  
def add_data():
    text = input("Input text for your command: ").strip()
    if not text:
        print('❌ Text cannot be empty.')
        return 

    if check_unwanted_chars(text):
        if not take_user_validation(text):
            print("❌ Entry cancelled.")
            return
        text = remove_unwanted_chars(text)

    key = input("Add a key for your text: ").strip()
    if not key:
        print('❌ Key cannot be empty.')
        return

    if check_unwanted_chars_in_key(key):
        if not take_user_validation(key):
            print("❌ Entry cancelled.")
            return
        key = remove_unwanted_chars_key(key)

    info = input("Add some info about your command (optional): ").strip()
    info = remove_unwanted_chars(info)

    # Record date (not used yet, but good for future)
    entry_date = str(datetime.date.today())

    # Check if key already exists
    if key in DATA:
        overwrite = input(f'⚠️ Key "{key}" already exists. Overwrite? (y/n): ').strip().lower()
        if overwrite != 'y':
            print("❌ Cancelled.")
            return

    DATA[key] = {
        'text': text,
        'info': info,
        'date': entry_date
    }

    with open(DATA_FILE, 'w') as file:
        json.dump(DATA, file, indent=2)

    print(f'✅ Entry for key "{key}" added successfully.')


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  pclip [key]       - copy saved text for key to clipboard")
        print("  pclip add         - add a new key-text pair")
        print("  pclip list        - list all saved keys")
        sys.exit()

    command = sys.argv[1].lower()

    if command in ["add", "a"]:
        add_data()
    # elif command == "list":
    #     list_data()
    # else:
    #     copy_to_clipboard(command)

if __name__ == "__main__":
    main()
