import os

# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the CSV file
csv_file_path = os.path.join(script_dir, 'your_data.csv')

# Now you can use csv_file_path to access the CSV file
