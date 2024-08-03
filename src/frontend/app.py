from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__, static_folder='/root/app/html')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/config.js')
def config():
    backend_domain = os.getenv('BACKEND_DOMAIN', 'localhost')
    config_js = f'window.config = {{ API_BASE_URL: "http://{backend_domain}/api" }};'
    return app.response_class(config_js, mimetype='application/javascript')

# Example API route
@app.route('/api/example', methods=['GET'])
def example_api():
    return jsonify({'message': 'Hello from Flask!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
