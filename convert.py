import json
import csv

def flatten_json(nested_json, parent_key='', sep='_'):
    items = []
    for k, v in nested_json.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def json_to_csv(json_str, csv_file_path):
    # Load the JSON data
    data = json.loads(json_str)
    
    # Flatten the JSON data
    flattened_data = [flatten_json(entry) for entry in data]
    
    # Open the CSV file for writing
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write the header row
        header = flattened_data[0].keys()
        writer.writerow(header)
        
        # Write the data rows
        for entry in flattened_data:
            writer.writerow(entry.values())

# Example nested JSON string
json_str = '''
[
    {
        "name": "John Doe",
        "age": 30,
        "address": {
            "city": "New York",
            "zip": "10001"
        }
    },
    {
        "name": "Jane Smith",
        "age": 25,
        "address": {
            "city": "Los Angeles",
            "zip": "90001"
        }
    }
]
'''

# Convert JSON to CSV
json_to_csv(json_str, 'output.csv')

print("Nested JSON data has been successfully converted to CSV and saved to 'output.csv'.")
