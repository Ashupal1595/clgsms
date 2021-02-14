# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 15:51:53 2021

@author: Administrator
"""
import mysql.connector
#import uuid
#uuidOne = uuid.uuid1()
#print(uuidOne)
from flask import Flask, render_template, request, flash, redirect, session, url_for
import re
#from flask_mysqldb import MySQL

app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'root'
#app.config['MYSQL_DB'] = 'sms_flask'
#mysql = MySQL(app)

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  database='sms_flask',
  password="mysql"
)
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method=='POST' and 'username' in request.form and 'password' in request.form: 
        username=request.form['username']
        password=request.form['password']   
        cursor=mydb.cursor()
        squery="SELECT * FROM accounts WHERE username = \"{}\" AND password = \"{}\"".format (username, password)
        #cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password))
        cursor.execute(squery)
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            #session['id'] = account['id'] 
            session['username'] = account[0] 
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg) 
        else:
            msg = 'Incorrect username / password !'
            return render_template('login.html', msg = msg)
    return render_template('login.html')

@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect(url_for('login')) 

@app.route('/register', methods =['GET', 'POST']) 
def register(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form : 
        username = request.form['username'] 
        password = request.form['password'] 
        email = request.form['email'] 
        row= request.form
        cursor=mydb.cursor()
        #cursor.execute("SELECT * FROM accounts WHERE username = \"{}\"".format(username))
        squery="SELECT * FROM accounts WHERE username = \"{}\"".format(username)
        cursor.execute(squery)
        account = cursor.fetchone() 
        if account: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email: 
            msg = 'Please fill out the form !'
        else: 
            #cursor.execute('INSERT INTO accounts VALUES ( % s, % s, % s)', (username, password, email)) 
            query="INSERT INTO accounts VALUES(%s, %s, %s)"
            cursor.execute(query,(username,password,email))
            mydb.commit() 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg) 

@app.route("/")
def home():
    return render_template("index.html")
#@app.route("/showaddstu",methods=['GET','POST'])
#def showaddstu():
 #   return render_template("addstu.html")

@app.route("/addstudent",methods=['GET','POST'])
def addstudent():
    if request.method=='POST':
        student=request.form
        row=[]
        for value in student.values():
            row.append(value)
        row=tuple(row)
        #addnumber=(request.form.get('addnumber'))
        #addname=request.form.get('addname')
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        #cursor.execute('''INSERT INTO stu VALUES(%s,%s)''',(addnumber,addname))
        #mysql.connection.commit()
        query='''insert into student(stu_roll_no,stu_first_name,stu_middle_name,stu_last_name,stu_mobile_no,stu_email_id,stu_address,stu_dob,stu_gender,stu_father_name,stu_mother_name,stu_course_id,stu_standard,stu_category)
values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''        
        cursor.execute(query,row)
        mydb.commit()
        cursor.close()
    return render_template("student/addstudent.html",message="Please enter student details")

@app.route("/searchstudent", methods=['GET','POST']) 
def searchstudent():
    if request.method=='POST':
        field= request.form.get('search_field')
        value= request.form.get('search')
        #print(field ,"   ",value)
         
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        if field=='all':
            query="select * from student"
        else:
            query="select * from student where {}=\"{}\"".format(field,value)
        cursor.execute(query)
        rows=cursor.fetchall()
        cursor.close()
        return render_template("student/searchstudent.html",table=rows)
    return render_template("student/searchstudent.html")

@app.route("/delstudent", methods=('GET','POST'))
def delstudent():
    if request.method=='POST':
        field=request.form.get('stu_roll_no')
        select_query="select * from student where stu_roll_no=\"{}\"".format(field)
        delete_query="delete from student where stu_roll_no=\"{}\"".format(field)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        cursor.execute(select_query)
        rows=cursor.fetchone()
        cursor.execute(delete_query)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
        message=""
        if len(rows) == 0:
            message="No record found with given ID"
            return render_template("delstudent.html",message=message)
        else:
            message="Record with given ID was deleted from the system"
            return render_template("student/delstudent.html",message=message)
    return render_template("student/delstudent.html")

@app.route("/editstudent", methods=('GET','POST'))
def editstudent():
    if request.method=='POST':
        field=request.form.get('stu_roll_no')
        query="select * from student where stu_roll_no=\"{}\"".format(field)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        cursor.execute(query)
        row=cursor.fetchone()
        return render_template("student/updatestudent.html", row=row)
    return render_template("student/editstudent.html")    

@app.route("/updatestudent", methods=('GET','POST'))
def updatestudent():
    if request.method=='POST':
        field=request.form.get('stu_roll_no')
        dic=request.form
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        for col,val in dic.items():
            if col != 'stu_roll_no':
                update_query="update student set {} = \"{}\" where stu_roll_no=\"{}\"".format(col,val,field)
                print(update_query)
                cursor.execute(update_query)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
        flash("The record was updated successsfully")
        return redirect("/editstudent")
    return render_template("student/updatestudent.html")


@app.route("/addstaff",methods=['GET','POST'])
def addstaff():
    if request.method=='POST':
        staff=request.form
        row=[]
        for value in staff.values():
            row.append(value)
        row=tuple(row)
        #print(row)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        query='''insert into staff(staff_id,staff_first_name,staff_middle_name,staff_last_name,staff_gender,staff_mobile_no,staff_address,staff_role,staff_designation,staff_type,staff_date_of_joining)
values(%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(query,row)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
    return render_template("staff/addstaff.html",message="Please enter staff details")


@app.route("/searchstaff", methods=['GET','POST']) 
def searchstaff():
    if request.method=='POST':
        field= request.form.get('search_field')
        value= request.form.get('search')
        #print(field ,"   ",value)
         
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        if field=='all':
            query="select * from staff"
        else:
            query="select * from staff where {}=\"{}\"".format(field,value)
        cursor.execute(query)
        rows=cursor.fetchall()
        cursor.close()
        return render_template("staff/searchstaff.html",table=rows)
    return render_template("staff/searchstaff.html")


@app.route("/delstaff", methods=('GET','POST'))
def delstaff():
    if request.method=='POST':
        field=request.form.get('staff_id')
        select_query="select * from staff where staff_id=\"{}\"".format(field)
        delete_query="delete from staff where staff_id=\"{}\"".format(field)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        cursor.execute(select_query)
        rows=cursor.fetchone()
        cursor.execute(delete_query)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
        message=""
        if len(rows) == 0:
            message="No record found with given ID"
            return render_template("delstaff.html",message=message)
        else:
            message="Record with given ID was deleted from the system"
            return render_template("staff/delstaff.html",message=message)
    return render_template("staff/delstaff.html")



@app.route("/editstaff", methods=('GET','POST'))
def editstaff():
    if request.method=='POST':
        field=request.form.get('staff_id')
        query="select * from staff where staff_id=\"{}\"".format(field)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        cursor.execute(query)
        row=cursor.fetchone()
        return render_template("staff/updatestaff.html", row=row)
    return render_template("staff/editstaff.html")


@app.route("/updatestaff", methods=('GET','POST'))
def updatestaff():
    if request.method=='POST':
        field=request.form.get('staff_id')
        dic=request.form
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        for col,val in dic.items():
            if col != 'staff_id':
                update_query="update staff set {} = \"{}\" where staff_id=\"{}\"".format(col,val,field)
                print(update_query)
                cursor.execute(update_query)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
        flash("The record was updated successsfully")
        return redirect("/editstaff")
    return render_template("staff/updatestaff.html")


@app.route("/searchcourse",methods=['GET','POST'])
def searchcourse(): 
    if request.method=='POST':
        field= request.form.get('search_field')
        value= request.form.get('search')
        cursor=mydb.cursor()
        if field=='all':
            query="select * from course"
        else:
            query="select * from course where {}=\"{}\"".format(field,value)
        cursor.execute(query)
        rows=cursor.fetchall()
        cursor.close()
        return render_template("course/searchcourse.html",table=rows)
    return render_template("course/searchcourse.html")  

@app.route("/addcourse",methods=['GET','POST'])
def addcourse():
    if request.method=='POST':
        course=request.form
        row=[]
        for value in course.values():
            row.append(value)
        row=tuple(row)
        #print(row)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        query ='''insert into course(course_id,course_name,course_stream_id)
values(%s, %s, %s)'''
        cursor.execute(query,row)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
    return render_template("course/addcourse.html",message="Please enter course details")


@app.route("/delcourse", methods=('GET','POST'))
def delcourse():
    if request.method=='POST':
        field=request.form.get('course_id')
        select_query="select * from course where course_id=\"{}\"".format(field)
        delete_query="delete from course where course_id=\"{}\"".format(field)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        cursor.execute(select_query)
        rows=cursor.fetchone()
        cursor.execute(delete_query)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
        message=""
        if len(rows) == 0:
            message="No record found with given ID"
            return render_template("delcourse.html",message=message)
        else:
            message="Record with given ID was deleted from the system"
            return render_template("course/delcourse.html",message=message)
    return render_template("course/delcourse.html")

@app.route("/editcourse", methods=('GET','POST'))
def editcourse():
    if request.method=='POST':
        field=request.form.get('course_id')
        query="select * from course where course_id=\"{}\"".format(field)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        cursor.execute(query)
        row=cursor.fetchone()
        return render_template("course/updatecourse.html", row=row)
    return render_template("course/editcourse.html")



@app.route("/updatecourse", methods=('GET','POST'))
def updatecourse():
    if request.method=='POST':
        field=request.form.get('course_id')
        dic=request.form
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        for col,val in dic.items():
            if col != 'course_id':
                update_query="update course set {} = \"{}\" where course_id=\"{}\"".format(col,val,field)
                print(update_query)
                cursor.execute(update_query)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
        flash("The record was updated successsfully")
        return redirect("/editcourse")
    return render_template("course/updatecourse.html")

  
@app.route("/addstream",methods=['GET','POST'])
def addstream():
    if request.method=='POST':
        stream=request.form
        row=[]
        for value in stream.values():
            row.append(value)
        row=tuple(row)
        #print(row)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        query='''insert into stream(stream_id,stream_name,head_id,stream_location)
values(%s, %s, %s, %s)'''
        cursor.execute(query,row)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
    return render_template("stream/addstream.html",message="Please enter stream details")


@app.route("/searchstream", methods=['GET','POST']) 
def searchstream():
    if request.method=='POST':
        field= request.form.get('search_field')
        value= request.form.get('search')
        #print(field ,"   ",value)
         
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        if field=='all':
            query="select * from stream"
        else:
            query="select * from stream where {}=\"{}\"".format(field,value)
        cursor.execute(query)
        rows=cursor.fetchall()
        cursor.close()
        return render_template("stream/searchstream.html",table=rows)
    return render_template("stream/searchstream.html")


@app.route("/delstream", methods=('GET','POST'))
def delstream():
    if request.method=='POST':
        field=request.form.get('stream_id')
        select_query="select * from stream where stream_id=\"{}\"".format(field)
        delete_query="delete from stream where stream_id=\"{}\"".format(field)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        cursor.execute(select_query)
        rows=cursor.fetchone()
        cursor.execute(delete_query)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
        message=""
        if len(rows) == 0:
            message="No record found with given ID"
            return render_template("delstream.html",message=message)
        else:
            message="Record with given ID was deleted from the system"
            return render_template("stream/delstream.html",message=message)
    return render_template("stream/delstream.html")



@app.route("/editstream", methods=('GET','POST'))
def editstream():
    if request.method=='POST':
        field=request.form.get('stream_id')
        query="select * from stream where stream_id=\"{}\"".format(field)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        cursor.execute(query)
        row=cursor.fetchone()
        return render_template("stream/updatestream.html", row=row)
    return render_template("stream/editstream.html")

@app.route("/updatestream", methods=('GET','POST'))
def updatestream():
    if request.method=='POST':
        field=request.form.get('stream_id')
        dic=request.form
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        for col,val in dic.items():
            if col != 'stream_id':
                update_query="update stream set {} = \"{}\" where stream_id=\"{}\"".format(col,val,field)
                print(update_query)
                cursor.execute(update_query)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
        flash("The record was updated successsfully")
        return redirect("/editstream")
    return render_template("stream/updatestream.html")


@app.route("/addsubject",methods=['GET','POST'])
def addsubject():
    if request.method=='POST':
        staff=request.form
        row=[]
        for value in staff.values():
            row.append(value)
        row=tuple(row)
        #print(row)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        query='''insert into subject(subject_id,subject_name,subject_course_id)
values(%s, %s, %s)'''
        cursor.execute(query,row)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
    return render_template("subject/addsubject.html",message="Please enter subject details")


@app.route("/searchsubject", methods=['GET','POST']) 
def searchsubject():
    if request.method=='POST':
        field= request.form.get('search_field')
        value= request.form.get('search')
        #print(field ,"   ",value)
         
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        if field=='all':
            query="select * from subject"
        else:
            query="select * from subject where {}=\"{}\"".format(field,value)
        cursor.execute(query)
        rows=cursor.fetchall()
        cursor.close()
        return render_template("subject/searchsubject.html",table=rows)
    return render_template("subject/searchsubject.html")


@app.route("/delsubject", methods=('GET','POST'))
def delsubject():
    if request.method=='POST':
        field=request.form.get('subject_id')
        select_query="select * from subject where subject_id=\"{}\"".format(field)
        delete_query="delete from subject where subject_id=\"{}\"".format(field)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        cursor.execute(select_query)
        rows=cursor.fetchone()
        cursor.execute(delete_query)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
        message=""
        if len(rows) == 0:
            message="No record found with given ID"
            return render_template("delsubject.html",message=message)
        else:
            message="Record with given ID was deleted from the system"
            return render_template("subject/delsubject.html",message=message)
    return render_template("subject/delsubject.html")



@app.route("/editsubject", methods=('GET','POST'))
def editsubject():
    if request.method=='POST':
        field=request.form.get('subject_id')
        query="select * from subject where subject_id=\"{}\"".format(field)
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        cursor.execute(query)
        row=cursor.fetchone()
        return render_template("subject/updatesubject.html", row=row)
    return render_template("subject/editsubject.html")


@app.route("/updatesubject", methods=('GET','POST'))
def updatesubject():
    if request.method=='POST':
        field=request.form.get('subject_id')
        dic=request.form
        #cursor = mysql.connection.cursor()
        cursor=mydb.cursor()
        for col,val in dic.items():
            if col != 'subject_id':
                update_query="update subject set {} = \"{}\" where subject_id=\"{}\"".format(col,val,field)
                print(update_query)
                cursor.execute(update_query)
        #mysql.connection.commit()
        mydb.commit()
        cursor.close()
        flash("The record was updated successsfully")
        return redirect("/editsubject")
    return render_template("subject/updatesubject.html")
app.run()