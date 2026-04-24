from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import get_connection, init_db

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_connection()
    jobs = conn.execute('SELECT * FROM jobs ORDER BY date_applied DESC').fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs)

@app.route('/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        company = request.form['company']
        role = request.form['role']
        location = request.form['location']
        date_applied = request.form['date_applied']
        status = request.form['status']
        notes = request.form['notes']
        link = request.form['link']
        conn = get_connection()
        conn.execute('''
            INSERT INTO jobs (company, role, location, date_applied, status, notes, link)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (company, role, location, date_applied, status, notes, link))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_job.html')

@app.route('/update/<int:id>', methods=['POST'])
def update_status(id):
    status = request.form['status']
    conn = get_connection()
    conn.execute('UPDATE jobs SET status = ? WHERE id = ?', (status, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_job(id):
    conn = get_connection()
    conn.execute('DELETE FROM jobs WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    