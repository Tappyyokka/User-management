from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        conn.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            (name, email)
        )
        conn.commit()
        conn.close()

        flash("User added successfully 🎉")
        return redirect('/')

    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    return render_template('index.html', users=users)

# DELETE
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash("User deleted ❌")
    return redirect('/')

# UPDATE PAGE (LOAD FORM)
@app.route('/edit/<int:id>')
def edit(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    conn.close()

    return render_template('edit.html', user=user)

# UPDATE ACTION
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    email = request.form['email']

    conn = get_db_connection()
    conn.execute(
        'UPDATE users SET name = ?, email = ? WHERE id = ?',
        (name, email, id)
    )
    conn.commit()
    conn.close()

    flash("User updated successfully ✏️")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)