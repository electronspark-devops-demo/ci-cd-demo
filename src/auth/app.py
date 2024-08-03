from flask import Flask, request, jsonify, make_response
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

app = Flask(__name__)

# Wrap the Flask application with DispatcherMiddleware
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/api/auth': app
})

# Get database configurations from environment variables
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_HOST', 'localhost')
db_uri = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yoursecretkey'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(200))
    
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password, email=data['email'], avatar=data['avatar'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return make_response('Login failed!', 401)
    
    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
    return jsonify({'token': token})

@app.route('/user', methods=['GET'])
def get_user():
    token = request.headers['x-access-tokens']
    if not token:
        return make_response('Token is missing!', 401)
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = User.query.filter_by(id=data['user_id']).first()
    except:
        return make_response('Token is invalid!', 401)
    
    user_data = {
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'avatar': current_user.avatar
    }
    return jsonify(user_data)

@app.route('/user', methods=['PUT'])
def update_user():
    token = request.headers['x-access-tokens']
    if not token:
        return make_response('Token is missing!', 401)
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = User.query.filter_by(id=data['user_id']).first()
    except:
        return make_response('Token is invalid!', 401)

    data = request.json
    if 'password' in data:
        current_user.password = generate_password_hash(data['password'], method='sha256')
    if 'email' in data:
        current_user.email = data['email']
    if 'avatar' in data:
        current_user.avatar = data['avatar']
    db.session.commit()
    
    return jsonify({'message': 'user updated'})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({'error': 'Invalid path: %s' % path, 'svc': 'auth'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001)
