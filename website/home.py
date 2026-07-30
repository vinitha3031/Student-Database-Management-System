from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required,current_user
from .models import Student_db
from . import db

views=Blueprint("views",__name__)

@views.route("/",methods=['GET','POST'])
@login_required
def home():
    data = Student_db.query.filter_by(user_id=current_user.id)
    page=request.args.get("page",1,type=int)
    searched=False

    if request.method=='POST':
        rn=request.form.get('rn')
        name=request.form.get('name')
        age=request.form.get('age')
        Class=request.form.get('Class')
        action=request.form.get('action')
        sort=request.form.get('sort')
        srh = request.form.get("search", "").strip()

        if action=='add':
            if not rn or not name or not age or not Class:
                flash("Please fill all the fields.", category="error")
                return redirect(url_for("views.home"))
            student = Student_db.query.filter_by(
                            user_id=current_user.id,
                            Roll_No=int(rn)).first()
            if student:
                flash('Roll No already exist',category='error')
            else:
                if int(age) <= 0:
                    flash("Enter a Valid Age",category='error')
                    return redirect(url_for("views.home"))
                if int(rn) <= 0:
                    flash("Student Roll No must be greater than 0",category='error')
                    return redirect(url_for("views.home"))
                if int(Class) <= 0:
                    flash("Enter a Valid student Class No",category='error')
                    return redirect(url_for("views.home"))
                stu_db=Student_db(Roll_No=rn,Name=name,Age=age,Class=Class, user_id=current_user.id)
                db.session.add(stu_db)
                db.session.commit()
                flash('Added Successfully!!!', category='success')
                return redirect(url_for('views.home'))
        elif action=='search':
            searched=True
            if srh.isdigit():
                data = Student_db.query.filter_by(
                user_id=current_user.id,
                Roll_No=int(srh))
            elif srh.isalpha():
                data = Student_db.query.filter_by(user_id=current_user.id).filter(
                        Student_db.Name.ilike(f"%{srh}%"))
            else:
                data = Student_db.query.filter_by(user_id=current_user.id)
                
            if sort=='A-Z':
                data=data.order_by(Student_db.Name.asc())
            elif sort=="Z-A":
                data=data.order_by(Student_db.Name.desc())
            elif sort=="Age":
                data=data.order_by(Student_db.Age)
            else:
                data=data.order_by(Student_db.Roll_No)
    data=data.paginate(
                        page=page,
                        per_page=5
                    )
    if searched and data.total==0:
        flash('Search result is not found',category='error')
    return render_template('home.html',user=current_user, stu=data)


@views.route('/edit', methods=['POST'])
@login_required
def edit():
    id=request.form.get('id',type=int)
    stu_info = Student_db.query.filter_by(
                id=id,
                user_id=current_user.id).first()
    rn = request.form.get("rn")
    name = request.form.get("name")
    age = request.form.get("age")
    Class = request.form.get("Class")

    if not rn or not name or not age or not Class:
        flash("Please fill all the fields.", category="error")
        return redirect(url_for("views.home"))

    existing = Student_db.query.filter(
        Student_db.user_id == current_user.id,
        Student_db.Roll_No == int(rn),
        Student_db.id != id
    ).first()

    if existing:
        flash("Roll No already exists.", category="error")
        return redirect(url_for("views.home"))

    stu_info.Roll_No = int(rn)
    stu_info.Name = name
    stu_info.Age = int(age)
    stu_info.Class = int(Class)

    db.session.commit()
    flash("Student updated successfully!", category="success")

    return redirect(url_for("views.home"))

@views.route('/delete/<int:id>')
@login_required
def delete(id):
    stu_id= Student_db.query.filter_by(
                id=id,
                user_id=current_user.id).first()
    if stu_id:
        db.session.delete(stu_id)
        db.session.commit()
        flash("Deleted Sucessfully",category='success')
    else:
        flash("Student not found", category='error')
    return redirect(url_for('views.home'))

    
