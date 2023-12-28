from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

def fetch_json(url):
    # Get the current time in milliseconds
    current_time_ms = int(round(time.time() * 1000))

    # Update the URL with the current time
    updated_url = url.format(current_time_ms)

    # Send a GET request to the URL
    response = requests.get(updated_url)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json()['result']
    else:
        return None

@app.route('/get_indices', methods=['GET'])
def get_indices():
    indices_url = "https://nepalipaisa.com/api/GetIndexLive?_={}"
    indices_data = fetch_json(indices_url)

    if indices_data is not None:
        return jsonify(indices_data)
    else:
        return jsonify({"error": "Error fetching data"})

@app.route('/get_sub_indices', methods=['GET'])
def get_subindices():
    subindices_url = "https://nepalipaisa.com/api/GetSubIndexLive?_={}"
    subindices_data = fetch_json(subindices_url)

    if subindices_data is not None:
        return jsonify(subindices_data)
    else:
        return jsonify({"error": "Error fetching data"})

@app.route('/get_all_indices', methods=['GET'])
def get_all_indices():
    indices_url = "https://nepalipaisa.com/api/GetIndexLive?_={}"
    subindices_url = "https://nepalipaisa.com/api/GetSubIndexLive?_={}"

    indices_data = fetch_json(indices_url)
    subindices_data = fetch_json(subindices_url)

    if indices_data is not None and subindices_data is not None:
        combined_data = indices_data + subindices_data
        return jsonify(combined_data)
    else:
        return jsonify({"error": "Error fetching data"})

if __name__ == '__main__':
    app.run(debug=True)
