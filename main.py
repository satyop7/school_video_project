from functions import register_db,login_db,personaldash_db,videolist_db,addnewstudent_course_db,addcourse_db,addvideo_db
from flask import Flask, render_template , request , redirect , url_for
import os

class DataStore():
    a = None
    b = None
    c = None

data = DataStore()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

#Step – 4 (creating route for login)
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        email = request.form.get('Email')
        password = request.form.get('password')

        var1 = login_db(email,password)
        if var1[0] == 0:
            return f'''<h1>email  {email} or</h1>
            <h1>password {password} in wrong please register again</h1>'''    #if the username or password does not matches 
        elif var1[0] == 1 and var1[1] == 19:
            return redirect(url_for('admin_dashboard'))                        # FOR admins dashboard , 19 is admin's id
        elif var1[0] == 1:
            data.a = var1[1]                                                    # stores stu_id
            val = var1[2]                                                       # stores hashed password
            return redirect(url_for('personal_dashboard' , hash_pass=val)) 
    return render_template("login.html")


@app.route('/registration' , methods = ['POST' , 'GET'])
def registration():
    if(request.method == 'POST'):
        email = request.form.get('Email')
        password = request.form.get('password')
        name = request.form.get('name')
        user_name = request.form.get('user_name')
        x1 = register_db(email,password,name,user_name)
        if x1 == 1:
             return f'''<h1>email {email} already exist</h1>''' 
        elif x1 == 2:
             return redirect(url_for('login'))
        elif x1 == 3:
            return f'''<h1>username {user_name} already exist</h1>'''

    return render_template("registration.html")

# Personal dashboard
@app.route('/personal_dashboard/<hash_pass>' , methods = ['POST' , 'GET'])
def personal_dashboard(hash_pass):
    value = personaldash_db(data.a)
    length = len(value)
    if(request.method == 'POST'):
        data.b = request.form.get('entry')
        return redirect(url_for('video_list'))
    return render_template("personal_dashboard.html" , value = value , length=length)


#video list table
@app.route('/video_list' , methods = ['POST' , 'GET'])
def video_list():
    value = videolist_db(data.b)
    length = len(value)
    if (request.method == 'POST'):
        data.c = request.form.get('vid')
        return redirect(url_for('video'))
    return render_template("video_list.html" , value=value , length=length)


#users main video
@app.route('/video')
def video():
    value = data.c
    return render_template("video.html" , value=value)

#admins dashboard
@app.route('/admin_dashboard' , methods = ['POST' , 'GET'])
def admin_dashboard():
    if (request.method == 'POST'):
        x = request.form.get('button')
        if x == "1":                                                                   #redirects to add preexisting course of students
            return redirect(url_for('add_student_course'))
        elif x =="2":
            return redirect(url_for('upload'))                                         # upload new video
        elif x == "3":
            return redirect(url_for('add_course'))                                     # add a new course
    return render_template("admin_dashboard.html")

#add student course page
@app.route('/add_student_course' , methods = ['POST' , 'GET'])
def add_student_course():
    if (request.method == 'POST'):
        x = request.form.get('button')
        if x == "1":                                                                   #redirects to add preexisting course of students
            return redirect(url_for('add_newstudent_course'))
    return render_template("add_student_course.html")

#add new student course
@app.route('/add_newstudent_course' , methods = ['POST' , 'GET'])
def add_newstudent_course():
        if (request.method == 'POST'):
            username = request.form.get('username')
            course_name = request.form.get('course_name')
            status = request.form.get('status')
            x1 = addnewstudent_course_db(username,course_name,status)
            if x1 == 0:
                return f'''<h1>username {username} or course name{course_name} is wrong please check asap!! </h1>''' 
            elif x1 == 1:
                return f'''<h1>course succesfully updated return to home</h1>'''
        
        return render_template('add_newstudent_course.html')

# adds new course

@app.route('/add_course' , methods = ['POST' , 'GET'])
def add_course():
        if (request.method == 'POST'):
            course_name = request.form.get('course_name')
            x1 = addcourse_db(course_name)
            if x1 == 1:
                return f'''<h1>course succesfully added return to home</h1>'''
        
        return render_template('add_course.html')

# Define the static folder where uploaded files will be stored
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST' , 'GET'])
def upload():
    if(request.method == 'POST'):
        course_name = request.form.get('course_name')
        video_name = request.form.get('video_name')
        file = request.files['video_file']
        video_name = video_name+".mp4"
        # Save the uploaded file to the static folder
        filename = os.path.join(app.config['UPLOAD_FOLDER'], video_name)
        file.save(filename)
        x = addvideo_db(course_name,video_name)
        if x == 1:
            return f'''<h1>video file successfully added return to home</h1>'''
        elif x == 0:
            return f'''<h1>course name {course_name} does not exist please enter a valid course name</h1>''' 
    return render_template('add_video.html')


if __name__ == "__main__":
    app.run(debug=True,port=8000,host='0.0.0.0')