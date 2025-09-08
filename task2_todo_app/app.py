from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(10), default="Medium")
    due_date = db.Column(db.String(20))
    notes = db.Column(db.String(500))
    completed = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    keyword = request.args.get('search', '')
    if keyword:
        tasks = Task.query.filter(Task.title.contains(keyword)).all()
    else:
        tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template("index.html", tasks=tasks, keyword=keyword)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    priority = request.form.get("priority")
    due_date = request.form.get("due_date")
    notes = request.form.get("notes")
    if title:
        task = Task(title=title, priority=priority, due_date=due_date, notes=notes)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/toggle_complete/<int:task_id>")
def toggle_complete(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
