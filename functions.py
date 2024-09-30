#registeration database function
import mysql.connector
def register_db(email , password , name , username):
    con = mysql.connector.connect(host = "localhost" , user = "root" , password = "sonu1234" , database = "school_video_system")
    cur = con.cursor()
    if con.is_connected():
        print('lol')
    cur.execute("select email from student")
    data1 = cur.fetchall()
    email_1 = "('"+email+"',)"
    username_1 = "('"+username+"',)"
    cur.execute("select username from student")
    data2 = cur.fetchall()
    for i in data1:
        x = str(i)
        if email_1 == x:
            print ('lol1')
            a = 1
            break
    for i in data2:
        y = str(i)
        if username_1 == y:
            print ('lol3')
            a = 3
            break
    else:
        print('lol2')
        query1 = "insert into student(name , username , email , pass) values('{}','{}','{}',MD5('{}'))".format(name,username,email,password)
        cur.execute(query1)
        query2 = "insert into login(email , pass) values('{}',MD5('{}'))".format(email,password)
        cur.execute(query2)
        con.commit()
        a = 2
    return a

#creating login connection with required personal dashboard details

def login_db(email , password):
    con = mysql.connector.connect(host = "localhost" , user = "root" , password = "sonu1234" , database = "school_video_system")
    if con.is_connected():
        cur=con.cursor()
        query1 = "select * from login where email='{}' and pass = MD5('{}')".format(email,password)
        cur.execute(query1)
        data = cur.fetchall()
        if data == []:
            a = 0
            b = 0
            c = 0
        else:
            a = 1
            query2 = "select * from student where email='{}' and pass = MD5('{}')".format(email,password)
            cur.execute(query2)
            data = cur.fetchall()
            b = data[0][0]
            query3 = "select pass from login where email='{}'".format(email)
            cur.execute(query3)
            data1 = cur.fetchall()
            c = data1[0][0]                                                        #hashed pass of user
    return [a,b,c]

#for personal dashboard
def personaldash_db(stu_id):
    con = mysql.connector.connect(host = "localhost" , user = "root" , password = "sonu1234" , database = "school_video_system")
    if con.is_connected():
        cur=con.cursor()
        query = "select c_name , c_id from student_course_status where stu_id ={}".format(stu_id)
        cur.execute(query)
        data = cur.fetchall()
        return data
    

#for video list
def videolist_db(c_id):
    con = mysql.connector.connect(host = "localhost" , user = "root" , password = "sonu1234" , database = "school_video_system")
    if con.is_connected():
        cur=con.cursor()
        query = "select vid_name , vid_src from video where c_id ={}".format(c_id)
        cur.execute(query)
        data = cur.fetchall()
        return data
    

#for addnewstudents course in the student course status table
def addnewstudent_course_db(username , course_name , status):
    con = mysql.connector.connect(host = "localhost" , user = "root" , password = "sonu1234" , database = "school_video_system")
    cur = con.cursor()
    if con.is_connected():
        print('lol')
    cur.execute("select username from student")
    data1 = cur.fetchall()
    username_1 = "('"+username+"',)"
    course_name_1 = "('"+course_name+"',)"
    cur.execute("select c_name from course")
    data2 = cur.fetchall()
    a = 0                                             #username or course name is wrong
    for i in data1:
        x = str(i)
        if username_1 == x:
            print ('lol1')
            for j in data2:
                y = str(j)
                if course_name_1 == y:
                    print ('lol3')
                    query3 = "select stu_id from student where username ='{}'".format(username)
                    cur.execute(query3)
                    data3 = cur.fetchone()
                    print(data3)
                    new_string = str(data3)
                    new_string = new_string[1:]
                    new_string1=new_string[:-2]
                    print(new_string1)
                    query4 = "select c_id from course where c_name ='{}'".format(course_name)
                    cur.execute(query4)
                    data4 = cur.fetchone()
                    print(data4)
                    new_string2 = str(data4)
                    new_string2 = new_string2[1:]
                    new_string3=new_string2[:-2]
                    print(new_string3)
                    cur.execute("select MAX(sc_id) from student_course_status")
                    data5 = cur.fetchone()
                    print(data5)
                    new_string4 = str(data5)
                    new_string4 = new_string4[1:]
                    new_string5 = new_string4[:-2]
                    int_sc_id = int(new_string5)
                    int_sc_id = int_sc_id + 1
                    query5 = "insert into student_course_status(sc_id , stu_id , c_id , c_name , status) values({},{},{},'{}',{})".format(int_sc_id,new_string1,new_string3,course_name,status)
                    cur.execute(query5)
                    con.commit()
                    a = 1                             # everything correct proceed further
                    return a          
    return a

#for adding new course
def addcourse_db(course_name):
    con = mysql.connector.connect(host = "localhost" , user = "root" , password = "sonu1234" , database = "school_video_system")
    if con.is_connected():
        cur=con.cursor()
        cur.execute("select MAX(c_id) from course")
        data5 = cur.fetchone()
        print(data5)
        new_string4 = str(data5)
        new_string4 = new_string4[1:]
        new_string5 = new_string4[:-2]
        int_c_id = int(new_string5)
        int_c_id = int_c_id + 1
        query = "insert into course(c_id , c_name) values({},'{}')".format(int_c_id,course_name)
        cur.execute(query)
        con.commit()
    return 1

#for adding new video to static files
def addvideo_db(course_name , video_name):
    con = mysql.connector.connect(host = "localhost" , user = "root" , password = "sonu1234" , database = "school_video_system")
    cur = con.cursor()
    if con.is_connected():
        print('lol')
    cur.execute("select c_name from course")
    data1 = cur.fetchall()
    course_name_1 = "('"+course_name+"',)"
    a = 0                                             #username or course name is wrong
    for i in data1:
        x = str(i)
        if course_name_1 == x:
                    query4 = "select c_id from course where c_name ='{}'".format(course_name)
                    cur.execute(query4)
                    data4 = cur.fetchone()
                    print(data4)
                    new_string2 = str(data4)
                    new_string2 = new_string2[1:]
                    new_string3=new_string2[:-2]
                    int_c_id = int(new_string3)
                    print(new_string3)
                    cur.execute("select MAX(vid_id) from video")
                    data5 = cur.fetchone()
                    print(data5)
                    new_string4 = str(data5)
                    new_string4 = new_string4[1:]
                    new_string5 = new_string4[:-2]
                    int_vid_id = int(new_string5)
                    int_vid_id = int_vid_id + 1
                    new_vid = video_name[:-4]
                    new_vid_1 = new_vid.replace(" ", "%20")

                    src_string = "../static/"+new_vid_1+".mp4"
                    query5 = "insert into video(vid_id , c_id  , vid_name , vid_src) values({},{},'{}','{}')".format(int_vid_id,int_c_id,new_vid,src_string)
                    cur.execute(query5)
                    con.commit()
                    a = 1                             # everything correct proceed further
                    return a          
    return a