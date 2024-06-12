import statistics
import time
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
REAL_SERVICE_URL = 'http://localhost:5002/'
LOG_FILE_PATH = "request_logs.txt"
baseline_response_times = []
threshold=1.5

def log_request(request, file_path=LOG_FILE_PATH, response_t=0, response_time_alert="", status_code=""):
    file_path.write(f"Received request: {request.method} {request.path}\n")
    file_path.write(f"Response time: {response_t}\n")
    file_path.write(f"Status code: {status_code}\n")
    file_path.write(response_time_alert)
    file_path.write(f"\n-------------------------------\n")

def forward_request(method, path, data=None):
    url = REAL_SERVICE_URL + path
    print(url) 
    headers = {'Content-Type': 'application/json'}
    start_time = time.time()
    if data is not None:
       response = requests.request(method, url, json=data, headers=headers)
    else:
        response = requests.request(method, url)
    end_time = time.time()
    response_time = end_time - start_time

    return response.json(), response.status_code, response_time

def get_median_of_response_times(res_time):
    global baseline_response_times
    if len(baseline_response_times)<100:
        baseline_response_times.append(res_time)
    else:
        baseline_response_times.pop(0)
        baseline_response_times.append(res_time)
    print(baseline_response_times)
    return statistics.median(baseline_response_times)


@app.route('/', defaults={'path': ''}, methods=['GET', 'PUT', 'DELETE', 'POST'])
@app.route('/<path:path>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def proxy(path):
    method = request.method
    data = request.json if request.json else None
    response, status_code, response_time = forward_request(method, path, data)
    baseline_median = get_median_of_response_times(response_time)
    if response_time > baseline_median * threshold:
        response_time_alert = f"Alert! Response time {response_time} ms is significantly higher than baseline median {baseline_median} ms - STT service"
    elif response_time==0:
        response_time_alert = f"Alert! No response, response timeout - STT service"
    else:
        response_time_alert = f"Response time {response_time} ms is within acceptable range. - STT service"

    with open(LOG_FILE_PATH, "a") as f:
        log_request(request, f, response_time, response_time_alert, status_code)
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(host="localhost",port=3002, debug=True)