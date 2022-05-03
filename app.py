from flask import render_template,request,url_for,redirect
import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.sqlite3'
db=SQLAlchemy(app)
class Student(db.Model):
    student_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    roll_number=db.Column(db.String(75), nullable=False, unique=True)
    first_name=db.Column(db.String(75), nullable=False)
    last_name=db.Column(db.String(75))

class Course(db.Model):
    course_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    course_code=db.Column(db.String(75), nullable=False, unique=True)
    course_name=db.Column(db.String(75), nullable=False)
    course_description=db.Column(db.String(75))


class Enrollments(db.Model):
    enrollment_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    estudent_id=db.Column(db.Integer, db.ForeignKey('student.student_id'),nullable=False)
    ecourse_id=db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

@app.route("/")
def index():
    all=Student.query.all()
    if all:
        return render_template('all-students.html',all=all)
    else:
        return render_template('no_students.html')


@app.route("/student/create",methods=['GET','POST'])
def add_student():
    if request.form:
        roll=request.form['roll']
        fname=request.form['f_name']
        lname=request.form['l_name']
        courses=request.form.getlist('courses')

        missing=Student.query.filter_by(roll_number=roll).first()
        if missing is None:
            s=Student(roll_number=roll,first_name=fname,last_name=lname)
            db.session.add(s)
            db.session.commit()
            this_student=Student.query.filter_by(roll_number=roll).first()
            s_id=this_student.student_id
            for course in courses:
                print(course)

                if course=='course_1':
                    cid=1
                elif course=='course_2':
                    cid=2
                elif course=='course_3':
                    cid=3
                elif course=='course_4':
                    cid=4
                c=Enrollments(estudent_id=s_id,ecourse_id=cid)
                db.session.add(c)
                db.session.commit()

            return redirect(url_for('index'))
        else:
            return render_template('student_exists.html')
    return render_template('add_students.html')


@app.route('/student/<int:student_id>')
def student_details(student_id):
    row=Student.query.filter_by(student_id=student_id).first()

    enrolls=Enrollments.query.with_entities(Enrollments.ecourse_id).filter_by(estudent_id=student_id).all()
    cid=[]
    for enroll in enrolls:
        cid.append(enroll[0])
    courses=Course.query.filter(Course.course_id.in_(cid)).all()
    return render_template('student-details.html',row=row,courses=courses)

@app.route('/student/<int:student_id>/update',methods=['GET','POST'])
def update(student_id):
    if request.method=='GET':
        this_student=Student.query.filter_by(student_id=student_id).first()
        enrolls_cid=Enrollments.query.with_entities(Enrollments.ecourse_id).filter_by(estudent_id=student_id).all()
        cid=[]
        for enroll in enrolls_cid:
            cid.append(enroll[0])
        return render_template('update.html',row=this_student,cid=cid)

    elif request.method=='POST':
        fname=request.form['f_name']
        lname=request.form['l_name']
        courses=request.form.getlist('courses')
        s=Student.query.filter_by(student_id=student_id).update(dict(first_name=fname,last_name=lname))
        db.session.commit()
        Enrollments.query.filter_by(estudent_id=student_id).delete()
        db.session.commit()
        for course in courses:
            if course=='course_1':
                cid=1
            elif course=='course_2':
                cid=2
            elif course=='course_3':
                cid=3
            elif course=='course_4':
                cid=4
            c=Enrollments(estudent_id=student_id,ecourse_id=cid)
            db.session.add(c)
            db.session.commit()
        return redirect(url_for('index'))

@app.route('/student/<int:student_id>/delete')
def delete(student_id):
    Student.query.filter_by(student_id=student_id).delete()
    Enrollments.query.filter_by(estudent_id=student_id).delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__=='__main__':
    '''
    db.create_all()
    c1 = Course(course_code='CSE01', course_name='MAD 1',course_description='Modern Application Development - 1')
    c2 = Course(course_code='CSE02', course_name='DBMS',course_description='Database management Systems')
    c3 = Course(course_code='CSE03', course_name='PDSA',course_description='Programming, Data Structures and Algorithms using Python')
    c4 = Course(course_code='BST13', course_name='BDM',course_description='Business Data Management')
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    db.session.commit()
    '''
    app.run()

