from flask import Flask, render_template, redirect, url_for, request, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb+srv://saiteja:saiteja@saidev.pmtwzvn.mongodb.net/e_learning?retryWrites=true&w=majority"
mongo = PyMongo(app)

# Ensure PyMongo is correctly initialized
try:
    mongo.cx.server_info()  # Force connection on a request as the
    print("MongoDB connected!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Course:
    def __init__(self, title, description, content):
        self.title = title
        self.description = description
        self.content = content

class Enrollment:
    def __init__(self, user_id, course_id, progress=0):
        self.user_id = user_id
        self.course_id = course_id
        self.progress = progress

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username, email, hashed_password)

        mongo.db.users.insert_one(new_user.__dict__)
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = mongo.db.users.find_one({'email': email})

        if user and check_password_hash(user['password'], password):
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your credentials.', 'danger')

    return render_template('login.html')

@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        content = request.form.get('content')

        new_course = Course(title, description, content)
        mongo.db.courses.insert_one(new_course.__dict__)
        flash('Course created successfully!', 'success')
        return redirect(url_for('courses'))

    courses = mongo.db.courses.find()
    return render_template('courses.html', courses=courses)

@app.route('/course/<course_id>')
def course(course_id):
    course = mongo.db.courses.find_one({'_id': ObjectId(course_id)})
    return render_template('course.html', course=course)

@app.route('/enroll/<course_id>')
def enroll(course_id):
    user_id = get_current_user_id()  # Implement this function
    enrollment = Enrollment(user_id, course_id)
    mongo.db.enrollments.insert_one(enrollment.__dict__)
    flash('Enrolled successfully!', 'success')
    return redirect(url_for('course', course_id=course_id))

@app.route('/profile/<user_id>')
def profile(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    enrollments = mongo.db.enrollments.find({'user_id': user_id})
    return render_template('profile.html', user=user, enrollments=enrollments)

def get_current_user_id():
    # Mock implementation, replace with actual user session management
    user = mongo.db.users.find_one()  # Retrieve a single user for demo purposes
    return str(user['_id'])

if __name__ == '__main__':
    app.run(debug=True)
