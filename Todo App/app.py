from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.app_context().push()


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500))
    lastdate = db.Column(db.Date)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        keyword = request.args.get("search", "")
        tasks = Todo.query.filter(
            db.or_(
                Todo.title.ilike(f"%{keyword}%"),
                Todo.desc.ilike(f"%{keyword}%"),
            )
        ).all()
    else:
        tasks = Todo.query.all()
    return render_template("index.html", tasks=tasks)


@app.route("/addtask", methods=["GET", "POST"])
def addtask():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        lastdate = request.form["lastdate"]
        lastdate = datetime.strptime(lastdate, "%Y-%m-%d").date()
        task = Todo(title=title, desc=desc, lastdate=lastdate)
        db.session.add(task)
        db.session.commit()
        return redirect("/")
    return render_template("addtask.html")


@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        lastdate = request.form["lastdate"]
        lastdate = datetime.strptime(lastdate, "%Y-%m-%d").date()
        task = Todo.query.filter_by(sno=sno).first()
        task.title = title
        task.desc = desc
        task.lastdate = lastdate
        db.session.add(task)
        db.session.commit()
        return redirect("/")

    task = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", task=task)


@app.route("/delete/<int:sno>")
def delete(sno):
    task = Todo.query.filter_by(sno=sno).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
