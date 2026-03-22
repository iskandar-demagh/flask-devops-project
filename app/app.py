from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from models import db, Todo
import os
import time

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize the database with the app
db.init_app(app)

# ─── Database initialization with retry logic ─────────────────

def init_db():
    max_retries = 10
    retry_delay = 3  # seconds

    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.create_all()
            print("✅ Database connected and tables created!")
            return
        except Exception as e:
            print(f"⏳ Attempt {attempt + 1}/{max_retries} - Database not ready: {e}")
            time.sleep(retry_delay)

    raise Exception("❌ Could not connect to database after multiple retries")

init_db()
# Create tables if they don't exist
with app.app_context():
    db.create_all()

# ─── Routes ───────────────────────────────────────────

# Health check route (Jenkins will use this later)
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0'    # add this line
    }), 200
# Serve the UI
@app.route('/')
def index():
    return render_template('index.html')

# Get all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos]), 200

# Create a new todo
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    new_todo = Todo(title=data['title'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

# Update a todo (mark as done)
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return jsonify(todo.to_dict()), 200

# Delete a todo
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('DEBUG'))
