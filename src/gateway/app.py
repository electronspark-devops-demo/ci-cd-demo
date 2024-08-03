from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Define the URLs for the backend services
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://auth-service:5002')
BLOG_SERVICE_URL = os.getenv('BLOG_SERVICE_URL', 'http://blog-service:5003')
BACKEND_SERVICE_URL = os.getenv('BACKEND_SERVICE_URL', 'http://backend-service:5001')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

def forward_request(service_url):
    try:
        response = requests.request(
            method=request.method,
            url=f'{service_url}{request.full_path}',
            headers={key: value for key, value in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False)
        
        response_headers = [(name, value) for name, value in response.raw.headers.items()]
        return response.content, response.status_code, response_headers
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error forwarding request: {e}")
        return jsonify({'error': 'Service unavailable'}), 503

@app.route('/api/auth/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def auth_proxy(path):
    return forward_request(AUTH_SERVICE_URL)

@app.route('/api/blog/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def blog_proxy(path):
    return forward_request(BLOG_SERVICE_URL)

@app.route('/api/backend/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def backend_proxy(path):
    return forward_request(BACKEND_SERVICE_URL)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    app.logger.warning(f"Invalid path accessed: /{path}")
    return jsonify({'error': 'Invalid path'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
