from flask import Flask, request, send_file
import json
import csv
import io

app = Flask(__name__)

def flatten_json(nested_json, parent_key='', sep='_'):
    items = []
    for k, v in nested_json.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def json_to_csv(json_str):
    # Load the JSON data
    data = json.loads(json_str)
    
    # Flatten the JSON data
    flattened_data = [flatten_json(entry) for entry in data]
    
    # Create a CSV file in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write the header row
    header = flattened_data[0].keys()
    writer.writerow(header)
    
    # Write the data rows
    for entry in flattened_data:
        writer.writerow(entry.values())
    
    output.seek(0)
    return output

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JSON to CSV Converter</title>
    </head>
    <body>
        <h1>JSON to CSV Converter</h1>
        <form action="/convert" method="post">
            <label for="jsonInput">Enter JSON:</label><br>
            <textarea id="jsonInput" name="jsonInput" rows="10" cols="50"></textarea><br><br>
            <input type="submit" value="Convert to CSV">
        </form>
    </body>
    </html>
    '''

@app.route('/convert', methods=['POST'])
def convert():
    json_str = request.form['jsonInput']
    csv_file = json_to_csv(json_str)
    return send_file(csv_file, mimetype='text/csv', attachment_filename='output.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
