from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'addy123'
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///videoproject.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class VideoProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


db.create_all()
    
@app.route('/projects', methods=['GET'])
def get_projects():
    projects = VideoProject.query.all()
    return jsonify([{
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'created_at': project.created_at,
        'status': project.status
    } for project in projects])

@app.route('/projects/<int:id>', methods=['GET'])
def get_project(id):
    project = VideoProject.query.get_or_404(id)
    return jsonify({
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'created_at': project.created_at,
        'status': project.status
    })

@app.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    project = VideoProject(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'active')
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({'id': project.id}), 201

@app.route('/projects/<int:id>', methods=['PUT'])
def update_project(id):
    data = request.get_json()
    project = VideoProject.query.get_or_404(id)
    project.title = data.get('title', project.title)
    project.description = data.get('description', project.description)
    project.status = data.get('status', project.status)
    db.session.commit()
    return jsonify({
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'created_at': project.created_at,
        'status': project.status
    })

@app.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = VideoProject.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return '', 204


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409

    user = User(
        username=data['username']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = create_access_token(identity=user.id)
    return jsonify({'access_token': token}), 200


if __name__ =='__main__':
    app.run(debug=True,port=5001)