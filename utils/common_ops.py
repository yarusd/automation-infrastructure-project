import csv
import os
import json
import re
import pytest

def load_config():
    """Loads the configuration from config.json and returns it as a dictionary."""
    # Get the absolute path of the current directory where common_ops.py is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the correct path for config.json
    CONFIG_PATH = os.path.join(BASE_DIR, "../config/config.json")

    print(f"DEBUG: Looking for config.json at {CONFIG_PATH}")

    # Load the configuration from config.json
    try:
        with open(CONFIG_PATH, "r") as config_file:
            config_data = json.load(config_file)
            
            # Auto-detect CI environment (GitHub Actions)
            # If 'CI' environment variable is present, force HEADLESS mode to True
            if os.getenv('CI'):
                config_data['HEADLESS'] = True
                
            return config_data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"ERROR: Could not find config.json at {CONFIG_PATH}") from e
    
def read_data_from_csv(file_path):
    """Reads data from a CSV file. """
    data = []
    # Fix: Convert Windows backslashes to forward slashes for Linux compatibility
    normalized_path = file_path.replace('\\', '/') 
    
    with open(normalized_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


def extract_digits_from_text(text: str) -> float:
    """
    Extracts the first numeric value from a string and returns it as float.
    """
    match = re.search(r"\d+(\.\d+)?", text)
    if not match:
        raise ValueError(f"No numeric value found in: {text}")
    return float(match.group())

def get_db_categories(conn):
    """
    Retrieves the complete list of joke categories from the system database.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    return [row[1] for row in cursor.fetchall()]


# ... existing functions: load_config, read_data_from_csv ...

def get_search_test_data(file_path):
    """
    Reads search data from CSV and applies xfail markers 
    to specific keywords known to have application bugs.
    """
    raw_data = read_data_from_csv(file_path)
    processed_data = []
    
    # List of keywords that trigger known functional bugs in the application
    # Bug: Search functionality is limited to movie names only (Actor/Genre fails)
    KNOWN_SEARCH_BUGS = ["Florence", "action"]
    
    for row in raw_data:
        if row["keyword"] in KNOWN_SEARCH_BUGS:
            # Wrap the row in a pytest.param to attach the xfail metadata
            param = pytest.param(
                row, 
                marks=pytest.mark.xfail(
                    reason=f"Application Bug: Search by {row['search_type']} is currently not supported"
                )
            )
        else:
            param = row
        processed_data.append(param)
        
    return processed_data