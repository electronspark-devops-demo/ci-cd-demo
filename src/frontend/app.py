from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory, flash
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'

BACKEND_DOMAIN = os.getenv("BACKEND_DOMAIN", "localhost")
API_URL_PREFIX = "http://{0}/api".format(BACKEND_DOMAIN)

# Routes for rendering HTML templates
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', "GET"])
def login():
    errMsg = None
    if request.method == 'POST':
        data = request.form
        response = requests.post(API_URL_PREFIX + '/auth/login', json=data)
        if response.status_code == 200:
            token = response.json().get('token')
            flash('Login successful', 'success')
            return redirect(url_for('profile'))
        else:
            errMsg = 'Login failed'
    
    return render_template('login.html', error=errMsg)

@app.route('/register', methods=['POST', "GET"])
def register():
    errMsg = None
    if request.method == 'POST':
        data = request.form
        response = requests.post(API_URL_PREFIX + '/auth/register', json=data)
        if response.status_code == 200:
            flash('Registered successfully, please login', 'success')
            return redirect(url_for('login'))
        else:
            errMsg = 'Login failed'
    
    return render_template('register.html', error=errMsg)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

@app.route('/blog_edit')
def blog_edit():
    return render_template('blog_edit.html')

@app.route('/account_setting')
def account_setting():
    return render_template('account_setting.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Routes for handling form submissions and API calls
@app.route('/api/user', methods=['POST'])
def update_user():
    token = request.headers.get('x-access-tokens')
    data = request.form
    headers = {'x-access-tokens': token}
    response = requests.put(API_URL_PREFIX + '/user/user', json=data, headers=headers)
    if response.status_code == 200:
        flash('User updated', 'success')
        return redirect(url_for('profile'))
    else:
        flash('Update failed', 'danger')
        return redirect(url_for('account_setting'))

@app.route('/api/blogs', methods=['POST'])
def create_blog():
    token = request.headers.get('x-access-tokens')
    data = request.form
    headers = {'x-access-tokens': token}
    response = requests.post(API_URL_PREFIX + '/blog/blogs', json=data, headers=headers)
    if response.status_code == 200:
        flash('Blog created', 'success')
        return redirect(url_for('profile'))
    else:
        flash('Creation failed', 'danger')
        return redirect(url_for('profile'))

@app.route('/api/blogs/<int:blog_id>/delete', methods=['POST'])
def delete_blog(blog_id):
    token = request.headers.get('x-access-tokens')
    headers = {'x-access-tokens': token}
    response = requests.delete(API_URL_PREFIX + f'/blog/blogs/{blog_id}', headers=headers)
    if response.status_code == 200:
        flash('Blog deleted', 'success')
    else:
        flash('Deletion failed', 'danger')
    return redirect(url_for('profile'))

@app.route('/api/blogs/<int:blog_id>/edit', methods=['POST'])
def edit_blog(blog_id):
    token = request.headers.get('x-access-tokens')
    data = request.form
    headers = {'x-access-tokens': token}
    response = requests.put(API_URL_PREFIX + f'blog/blogs/{blog_id}', json=data, headers=headers)
    if response.status_code == 200:
        flash('Blog updated', 'success')
        return redirect(url_for('profile'))
    else:
        flash('Update failed', 'danger')
        return redirect(url_for('profile'))
    
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/init_db', methods=['GET'])
def database_initialize():
    response = requests.post(API_URL_PREFIX + '/auth/init_db')
    if response.status_code == 200:
        jsonify({'status': 'created'}), 200
    return jsonify({'status': 'error'}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
