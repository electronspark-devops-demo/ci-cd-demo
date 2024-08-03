from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app)

db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_HOST', 'localhost')
db_uri = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yoursecretkey'
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/blogs', methods=['GET'])
def get_blogs():
    blogs = Blog.query.all()
    output = []
    for blog in blogs:
        blog_data = {'id': blog.id, 'title': blog.title, 'content': blog.content, 'user_id': blog.user_id, 'created_at': blog.created_at}
        output.append(blog_data)
    return jsonify(output)

@app.route('/blogs/<user_id>', methods=['GET'])
def get_user_blogs(user_id):
    blogs = Blog.query.filter_by(user_id=user_id).all()
    output = []
    for blog in blogs:
        blog_data = {'id': blog.id, 'title': blog.title, 'content': blog.content, 'created_at': blog.created_at}
        output.append(blog_data)
    return jsonify(output)

@app.route('/blogs', methods=['POST'])
def create_blog():
    token = request.headers['x-access-tokens']
    if not token:
        return make_response('Token is missing!', 401)
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id']
    except:
        return make_response('Token is invalid!', 401)

    data = request.json
    new_blog = Blog(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(new_blog)
    db.session.commit()
    return jsonify({'message': 'Blog created!'})

@app.route('/blogs/<blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    token = request.headers['x-access-tokens']
    if not token:
        return make_response('Token is missing!', 401)
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id']
    except:
        return make_response('Token is invalid!', 401)

    blog = Blog.query.filter_by(id=blog_id, user_id=user_id).first()
    if not blog:
        return jsonify({'message': 'Blog not found!'})

    db.session.delete(blog)
    db.session.commit()
    return jsonify({'message': 'Blog deleted!'})

@app.route('/blogs/<blog_id>', methods=['PUT'])
def update_blog(blog_id):
    token = request.headers['x-access-tokens']
    if not token:
        return make_response('Token is missing!', 401)
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id']
    except:
        return make_response('Token is invalid!', 401)

    blog = Blog.query.filter_by(id=blog_id, user_id=user_id).first()
    if not blog:
        return jsonify({'message': 'Blog not found!'})

    data = request.json
    blog.title = data['title']
    blog.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Blog updated!'})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({'error': 'Invalid path: %s' % path, 'svc': 'blog'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=80)
