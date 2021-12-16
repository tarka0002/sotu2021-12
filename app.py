from flask import Flask,render_template,request,redirect,session

import sqlite3,random

from flask.templating import render_template_string

app = Flask(__name__)

app.config['SECRET_KEY'] = "berufaiakudasai"

@app.route("/")
def hellowould():
    return render_template("top.html")
    

# @app.route("/<login>")
# def greet (login):
    # return render_template("login.html")

# @app.route("/login")
# def task_login():
#     if "login_id" in session:
#         login_id=session["login_id"][0]

#         conn=sqlite3.connect("todo.db")
#         c = conn.cursor()

#         c.execute("select name from member where id=?",(login_id,))
#         user_name=c.fetchone()[0]

#         c.execute("select id,task from task where user_id=?",(login_id,))
#         task_list=[]
#         for row in c.fetchall():
#             task_list.append({"task_id:":row[0],"task":row[1]}) 
#         c.close

#         print(task_list)
#         return render_template("list.html",task_list=task_list)
#     else:
#         return render_template("login.html")

@app.route("/")
def template():
    py_name = "あまくさ"
    return render_template("index.html", name = py_name)

@app.route("/login",methods=["GET"])
def login_get():
    if "uid" in session:
        return redirect("/mypage")
    else:
        return render_template("login.html")


@app.route("/login",methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    conn=sqlite3.connect("todo.db")
    c=conn.cursor()
    c.execute("select * from user where email = ? and pass = ?",(email,password))
    row = c.fetchone()
    print(row)
    if row is None:
        return render_template("login.html")
    c.close()
    session["uid"]=row[0]
    return redirect("/mypage")

@app.route("/mypage")
def mypage():
    id=session.get("uid")
    conn=sqlite3.connect("todo.db")
    c=conn.cursor()
    c.execute("select * from user where id = ?",(id,))
    user = c.fetchone()
    c.execute("select veh,namber from syasyu where cop_id = ?",(id,))
    # car = c.fetchall()
    # print(car)
    sharyou = []
    for row in c.fetchall():
        sharyou.append({"veh":row[0],"namber":row[1]})
    c.close()
    conn.close()
    if user == None:
        return redirect("login")
    return render_template("my.html",user=user,sharyou = sharyou)

@app.route("/new")
def newpage():
    return render_template("new.html")

@app.route("/regist",methods=["POST"])
def regist():
    name = request.form.get("cop")
    password = request.form.get("password")
    email = request.form.get("email")
    conn=sqlite3.connect("todo.db")
    c=conn.cursor()
    c.execute("insert into user values(null,?,?,?)",(name,password,email))
    conn.commit()
    c.close()
    return redirect("/login")
@app.route("/add",methods=["GET"])
def add_get():
    return render_template("add.html")

@app.route("/add",methods=["POST"])
def add_post():
    id = session["uid"]
    syasyu = request.form.get("syasyu")
    namber = request.form.get("namber")
    conn=sqlite3.connect("todo.db")
    c=conn.cursor()
    c.execute("insert into syasyu values(null,?,?,?,0)",(syasyu,namber,id))
    conn.commit()
    c.close()
    return redirect("/mypage")

@app.route("/logout")
def logout():
    session.pop("uid",None)
    return redirect("/")

@app.route("/list")
def list():
    conn=sqlite3.connect("todo.db")
    c=conn.cursor()
    c.execute("select veh,namber from syasyu")
    syaryou = []
    for row in c.fetchall():
        syaryou.append({"veh":row[0],"namber":row[1]})
    c.close()
    return render_template("list.html",syaryou=syaryou)

if __name__ == "__main__":

    app.run(debug=True)

    # テストです



# @app.route("/color")
# def color():
    
#     conn = sqlite3.connect("color.db")

#     c = conn.cursor()

#     c.execute("SELECT * FROM colors;")

#     py_color=c.fetchall()
#     py_color=random.choice(py_color)

#     #py_color=c.fetchone()

#     c.close()

#     print(py_color)

#     return render_template("color.html",html_color=py_color)

# @app.route("/add",methods=["GET"])
# def add_get():
#     if "user_id" in session:
#         return render_template("add.html")
#     else:
#         return redirect("login")

# @app.route("/add",methods=["POST"])
# def add_post():

#     user_id=session["user_id"][0]

#     task=request.form.get("task")

#     conn=sqlite3.connect("todo.db")
#     c = conn.cursor()

#     c.execute("INSERT INTO task VALUES(null,?,?)",(task,user_id))
#     conn.commit()
#     c.close()
#     return "登録完了"




# @app.route('/edit/<int:id>')
# def edit(id):
#     conn=sqlite3.connect("todo.db")
#     c=conn.cursor()
#     c.execute("select task from task where id = ?",(id,))

#     task=c.fetchone()[0]
#     if task is None:
#         return"タスクがありません"
#     else:
#         task=task[0]
#         item={"task_id":id,"task":task}
#         c.close()
#         return render_template("edit.html",task=item)


# @app.route('/edit',methods=["POST"])
# def edit_post():
#     task=request.form.get("task")
#     id=request.form.get("task_id")
#     conn=sqlite3.connect("todo.db")
#     c=conn.cursor()

#     c.execute("update task set task=? where id=?",(task,id,))
#     conn.commit()
#     c.close()

#     return redirect("/list")

# @app.route('/del/<int:id>')
# def del_task(id):
#     conn=sqlite3.connect("todo.db")
#     c=conn.cursor()

#     c.execute("delete from task where id=?",(id,))
#     conn.commit()
#     c.close()
    
#     return redirect("/list")

# @app.route('/regist',methods=["GET"])
# def regist_get():
#     return render_template("regist.html")

# @app.route('/regist',methods=["POST"])
# def regist_post():
#     user_name=request.form.get("use_name")
#     password=request.form.get("password")
#     conn=sqlite3.connect("todo.db")
#     c=conn.cursor()
#     c.execute("insert into member values(null,?,?)",(user_name,password))
#     conn.commit()
#     c.close()
#     return"登録完了"


# @app.route("/logout")
# def logout():
#     session.pop("user_id",None)
#     return redirect("/login")


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html'), 404


# @app.route('/regist',methods=["POST"])
# def regist_post():
#     user_name=request.form.get("use_name")
#     password=request.form.get("password")
#     conn=sqlite3.connect("todo.db")
#     c=conn.cursor()
#     c.execute("insert into member values(null,?,?)",(user_name,password))
#     conn.commit()
#     c.close()
#     return"登録完了"

# @app.route('/regist')
# def toppage():
#     return render_template("top.html")


# if __name__ == '__main__':

#     app.run(debug=True)

    # <input type="checkbox" name="match" value="matchwithpairs" checked> Auto Match
    # if request.form.getlist('match')[0] == 'matchwithpairs':