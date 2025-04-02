from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3


# def submit_data(data):
#     conn = sqlite3.connect("database.db", timeout=10)  # Add timeout
#     cursor = conn.cursor()
    
#     try:
#         cursor.execute("INSERT INTO students (name, branch, semester) VALUES (?, ?, ?)", data)
#         conn.commit()
#     except sqlite3.OperationalError as e:
#         print(f"Database error: {e}")
#     finally:
#         cursor.close()
#         conn.close()  # Ensure the connection is closed


app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

# Initialize database
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            branch TEXT NOT NULL,
            semester TEXT NOT NULL,
            subject1 TEXT NOT NULL,
            marks1 INTEGER NOT NULL,
            subject2 TEXT NOT NULL,
            marks2 INTEGER NOT NULL,
            subject3 TEXT NOT NULL,
            marks3 INTEGER NOT NULL,
            subject4 TEXT NOT NULL,
            marks4 INTEGER NOT NULL,
            subject5 TEXT NOT NULL,
            marks5 INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Student page
@app.route('/')
def home():
    return render_template('student.html')

# Student submits marks
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    branch = request.form.get('branch')
    semester = request.form.get('semester')
    
    subject1 = request.form.get('subject1')
    marks1 = request.form.get('marks1')

    subject2 = request.form.get('subject2')
    marks2 = request.form.get('marks2')

    subject3 = request.form.get('subject3')
    marks3 = request.form.get('marks3')

    subject4 = request.form.get('subject4')
    marks4 = request.form.get('marks4')

    subject5 = request.form.get('subject5')
    marks5 = request.form.get('marks5')

    if not name or not branch or not semester:
        return "Please fill all required fields!", 400

    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO marks (name, branch, semester, subject1, marks1, subject2, marks2, subject3, marks3, subject4, marks4, subject5, marks5)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, branch, semester, subject1, marks1, subject2, marks2, subject3, marks3, subject4, marks4, subject5, marks5))

    conn.commit()
    conn.close()

    return redirect(url_for('home'))
    return "Data inserted successfully!"

# Teacher login page
@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == "admin123":  # Change this to a secure password
            session['teacher_logged_in'] = True
            return redirect(url_for('teacher'))
        else:
            return "Incorrect password!", 403
    return render_template('teacher_login.html')


# Teacher page to view all student marks (only if logged in)
@app.route('/teacher')
def teacher():
    if not session.get('teacher_logged_in'):
        return redirect(url_for('teacher_login'))
    
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM marks")
    data = c.fetchall()
    conn.close()
    return render_template('teacher.html', data=data)

# Logout route for teachers
@app.route('/logout')
def logout():
    session.pop('teacher_logged_in', None)
    return redirect(url_for('teacher_login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
