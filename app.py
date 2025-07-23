from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB = os.path.join(BASE_DIR, 'blog.db')

# Initialize DB
def init_db():
    if not os.path.exists(DB):
        with sqlite3.connect(DB) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE posts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            content TEXT NOT NULL,
                            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
            conn.commit()

@app.route('/')
def index():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY created DESC")
    posts = c.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('new_post.html')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        c.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, post_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    c.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    post = c.fetchone()
    conn.close()
    return render_template('edit_post.html', post=post)

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
