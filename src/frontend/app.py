from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory, flash
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'

# Routes for rendering HTML templates
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

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
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.form
    response = requests.post('http://your-backend-domain/api/auth/login', json=data)
    if response.status_code == 200:
        token = response.json().get('token')
        flash('Login successful', 'success')
        return redirect(url_for('profile'))
    else:
        flash('Login failed', 'danger')
        return redirect(url_for('login'))

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.form
    response = requests.post('http://your-backend-domain/api/auth/register', json=data)
    if response.status_code == 200:
        flash('Registered successfully, please login', 'success')
        return redirect(url_for('login'))
    else:
        flash('Registration failed', 'danger')
        return redirect(url_for('register'))

@app.route('/api/user', methods=['POST'])
def update_user():
    token = request.headers.get('x-access-tokens')
    data = request.form
    headers = {'x-access-tokens': token}
    response = requests.put('http://your-backend-domain/api/user', json=data, headers=headers)
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
    response = requests.post('http://your-backend-domain/api/blogs', json=data, headers=headers)
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
    response = requests.delete(f'http://your-backend-domain/api/blogs/{blog_id}', headers=headers)
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
    response = requests.put(f'http://your-backend-domain/api/blogs/{blog_id}', json=data, headers=headers)
    if response.status_code == 200:
        flash('Blog updated', 'success')
        return redirect(url_for('profile'))
    else:
        flash('Update failed', 'danger')
        return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
