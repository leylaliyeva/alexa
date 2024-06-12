import statistics
from flask import Flask, request, jsonify
import requests
import time


app = Flask(__name__)
REAL_SERVICE_URL = 'http://localhost:5005/'
LOG_FILE_PATH = "request_logs.txt"
baseline_response_times = []
threshold=2
timeout=3

def log_request(request, file_path=LOG_FILE_PATH, response_t=0, response_time_alert="", status_code=""):
    file_path.write(f"Received request: {request.method} {request.path}\n")
    file_path.write(f"Response time: {response_t}\n")
    file_path.write(f"Status code: {status_code}\n")
    file_path.write(response_time_alert)
    file_path.write(f"\n-------------------------------\n")

def forward_request(method, path, data=None):
    url = REAL_SERVICE_URL + path
    headers = {'Content-Type': 'application/json'}
    start_time = time.time()
    try:
        if data is not None:
            response = requests.request(method, url, json=data, headers=headers, timeout=timeout)
        else:
            response = requests.request(method, url, headers=headers, timeout=timeout)

        response.raise_for_status()
        
        end_time = time.time()
        response_time = end_time - start_time
        
        return response.json(), response.status_code, response_time
    
    except requests.Timeout:
        end_time = time.time()
        response_time = end_time - start_time
        print(f"Request to {url} timed out after {timeout} seconds")
        return {"error": "Request timed out"}, 504, 0
    
    except requests.HTTPError as e:
        end_time = time.time()
        response_time = end_time - start_time
        print(f"HTTP error occurred: {e}")
        return {"error": str(e)}, response.status_code, 0
    
    except requests.RequestException as e:
        end_time = time.time()
        response_time = end_time - start_time
        print(f"An error occurred: {e}")
        return {"error": str(e)}, 500, 0

def get_median_of_response_times(res_time):
    global baseline_response_times
    global timeout

    if len(baseline_response_times)<100 and res_time>0:
        baseline_response_times.append(res_time)
    elif len(baseline_response_times)>=100 and res_time<0:
        baseline_response_times.pop(0)
        baseline_response_times.append(res_time)
    print(baseline_response_times)
    timeout=statistics.median(baseline_response_times)*threshold
    return statistics.median(baseline_response_times)
    


@app.route('/', defaults={'path': ''}, methods=['GET', 'PUT', 'DELETE', 'POST'])
@app.route('/<path:path>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def proxy(path):
    method = request.method
    data = request.json if request.json else None
    response, status_code, response_time = forward_request(method, path, data)
    baseline_median = get_median_of_response_times(response_time)
    if response_time > baseline_median * threshold:
        response_time_alert = f"Alert! Response time {response_time} ms is significantly higher than baseline median {baseline_median} ms - KE service"
    else:
        response_time_alert = f"Response time {response_time} ms is within acceptable range. - KE ChatGPT service"

    with open(LOG_FILE_PATH, "a") as f:
        log_request(request, f, response_time, response_time_alert, status_code)
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(host="localhost",port=3005, debug=True)