from flask import Flask, jsonify, request, g
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# ---------- Prometheus metrics ----------
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)

# ---------- Request timing ----------
@app.before_request
def before_request():
    # Do not track the /metrics endpoint itself
    if request.path == "/metrics":
        return
    g.start_time = time.time()

@app.after_request
def after_request(response):
    # Do not track the /metrics endpoint itself
    if request.path == "/metrics":
        return response

    latency = time.time() - g.start_time
    endpoint = request.endpoint or "unknown"

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=endpoint
    ).observe(latency)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        status=response.status_code
    ).inc()

    return response

# ---------- Application routes ----------
@app.route("/health")
def health():
    return jsonify(status="healthy"), 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)