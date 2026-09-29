from flask import Flask, render_template, request, redirect, url_for
from models import db, Student

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/students")
def students():
    all_students = Student.query.all()
    return render_template("students.html", students=all_students)
@app.route("/edit_student/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == "POST":
        student.name = request.form["name"]
        student.email = request.form["email"]
        student.course = request.form["course"]
        student.phone = request.form["phone"]

        db.session.commit()

        return redirect(url_for("students"))

    return render_template("edit_student.html", student=student)
@app.route("/delete_student/<int:id>")
def delete_student(id):
    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return redirect(url_for("students"))


@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        phone = request.form["phone"]

        new_student = Student(
            name=name,
            email=email,
            course=course,
            phone=phone
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("students"))

    return render_template("add_student.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)