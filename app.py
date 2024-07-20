from flask import Flask, render_template,request, redirect,session, url_for
import mysql.connector
import bcrypt



db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Piuli12@.#",
        database="lmsdb"
    )

cursor = db.cursor();

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/help')
def help():

    return render_template('help.html')

@app.route('/about')
def about():

    return render_template('about.html')

@app.route('/login')
def login():

    return render_template('Log in.html')

@app.route('/admin')
def admin():

    return render_template('admin.html',username=session ['username'])

@app.route('/student')
def student():

    return render_template('student.html',username=session ['username'])

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect('/')

@app.route('/bookentry')
def bookentry():
    return render_template('book entry.html')

@app.route('/issuebook')
def issuebook():
    return render_template('Issue Book by admin.html')


@app.route('/more')
def more():
    return render_template('more.html')

@app.route('/adminfine1')
def adminfine1():
    return render_template('admin_fine_1.html')

@app.route('/adminfine3')
def adminfine3():
    return render_template('admin_fine_3.html')

@app.route('/faculty')
def faculty():
    return render_template('faculty.html',username=session ['username'])

@app.route('/isuebystudent')
def issuebystudent():
    username= session ['username']

    cursor.execute ("SELECT studentID from student WHERE username= %s", (username,))
    userID = cursor.fetchone()
    cursor.execute ("SELECT BookID, ISBN, userID, First_name, Last_name, deptcode, Edition, Issue_date, Return_date, Author1, Author2, Author3, Title, subject, type  from issue_book WHERE username= %s", (username,))
    result = cursor.fetchall ()
    return render_template('issued by student.html', result = result)

@app.route('/isuebyfaculty')
def issuebyfaculty():
    username= session ['username']

    cursor.execute ("SELECT facultyID from faculty WHERE username= %s", (username,))
    userID = cursor.fetchone()
    cursor.execute ("SELECT BookID, ISBN, userID, First_name, Last_name, deptcode, Edition, Issue_date, Return_date, Author1, Author2, Author3, Title, subject, type  from issue_book WHERE username= %s", (username,))
    result = cursor.fetchall ()
    return render_template('issued by faculty.html', result = result)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return "Error: No search query provided", 400
    
    # Execute SQL query to search for books
    cursor.execute("SELECT * FROM book WHERE Title LIKE %s OR Author1 LIKE %s OR Author2 LIKE %s OR Author3 LIKE %s OR Subject LIKE %s OR Accn_No LIKE %s OR call_No LIKE %s", ('%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%'))
    result = cursor.fetchall()
    
    return render_template('search.html', result=result)

@app.route('/search1')
def search1():
    return render_template('/adminfine2')


    

#@app.route('/signup_form', methods =['POST'])
#def signup_form():

  #  username = request.form['username']
  #  email  = request.form['email']
  #  password = request.form['password']

   # cursor.execute("SELECT * from test where username = %s OR email = %s",(username,email))
  #  existing_user = cursor.fetchone()

 #   if(existing_user):
 #       return "user is already exists"
    
   # hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt(10))

   # sql = "INSERT INTO test (username,email,password) VALUES (%s, %s, %s)" 
 #   val = (username,email,hashed_password)
 #   cursor.execute(sql,val)
 #   db.commit();

  #  return redirect('/');


@app.route('/login_form',methods =['POST'])
def login_form():

    username = request.form['username']
    password = request.form['password']
    usertype = request.form['UserType']

    cursor.execute("SELECT * FROM signup WHERE username = %s AND UserType = %s" , (username,usertype))
    user = cursor.fetchone();

    if user and  (password == user [1]):
    #bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        if ( user [2] == 'student'):
          session ['username'] = username
          return redirect('/student')
        elif (user [2] == 'admin'):
          session ['username'] = username
          return redirect('/admin')
        elif (user [2] == 'faculty'):
          session ['username'] = username
          return redirect('/faculty')
    else:
        return "Invalid Input Credentials."
    
@app.route('/bookentry_form',methods =['POST'])
def bookentry_form():

    Book_ID = request.form['book_id']
    Title = request.form['Title']
    Author1 = request.form['author_name1']
    Author2 = request.form['author_name2']
    Author3 = request.form['author_name3']
    ISBN = request.form['ISBN']
    Type = request.form['book_type']
    Category = request.form['Category']
    No_of_pages = request.form['No_of_pages']
    Edition = request.form['Edition']
    Subject = request.form['subject']
    Price = request.form['Price']

    sql="INSERT into book (bookID, Title, Author1, Author2, Author3, ISBN, Type, Subject, category, No_of_Pages, Edition, Price) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(Book_ID,Title,Author1,Author2,Author3,ISBN,Type,Category,No_of_pages,Edition,Subject,Price)
    cursor.execute (sql,val)
    db.commit()

    if cursor.rowcount>0:
        db.commit()
        return "Book Added Successfully"
    else:
        return "Internal Server Error !"
    

@app.route('/issuebook_form',methods =['POST'])
def issuebook_form():

    Book_ID = request.form['BookID']
    Title = request.form['Title']
    Author1 = request.form['Author1']
    Author2 = request.form['Author2']
    Author3 = request.form['Author3']
    ISBN = request.form['ISBN']
    Type = request.form['type']
    FirstName = request.form['First_name']
    LastName = request.form['Last_name']
    userID = request.form['userID']
    Edition = request.form['Edition']
    deptcode = request.form['deptcode']
    IssueDate = request.form['Issue_date']
    ReturnDate = request.form['Return_date']
    username = request.form['username']
    subject = request.form['subject']

    sql="INSERT into issue_book (BookID,Title,Author1,Author2,Author3,ISBN,type,First_name,Last_name,userID,Edition,deptcode,Issue_date,Return_date,username,subject) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(Book_ID,Title,Author1,Author2,Author3,ISBN,Type,FirstName,LastName,userID,Edition,deptcode,IssueDate,ReturnDate,username,subject)
    cursor.execute (sql,val)
    db.commit()

    if cursor.rowcount>0:
        db.commit()
        return "Book Issued Successfully"
    else:
        return "Internal Server Error !"
    


@app.route('/adminfine2', methods=['GET'])
def adminfine2():
    department = request.args.get('department')
    year = request.args.get('year')
    
    # Query database to fetch data based on selected department and year
    cursor.execute("SELECT * FROM signup WHERE department = %s AND year = %s", (department, year))
    data = cursor.fetchall()
    
    return render_template('admin_fine_2.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    dept = request.form.get('department')
    year = request.form.get('year')
    
    # Perform any necessary processing with department and year data
    
    # Redirect to the fine detail page with department and year parameters
    return redirect(url_for('adminfine2', department=dept, year=year))


import mysql.connector

# Establish a connection to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project"
    )



if __name__ == '__main__':
    app.run(debug=True)
