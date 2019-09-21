from flask import *
from model import *


app = Flask(__name__)
app.secret_key = '10242048' #配置secret_key,否则不能实现session对话

@app.route("/")
#首页，验证登录，验证失败则转回登录页面，并根据用户身份确定显示在导航栏的条目，如果密码为初始密码“666666”，则强制跳转到修改密码页面
def index():
    if checklogin(session.get('username'), session.get('password')):
        if session.get('password') == '666666':
            return redirect(url_for('changepw'))
        logininfo = checklogin(session['username'], session['password'])
        type = logininfo[3]
        baritems = navbaritems(type)
        session['baritems'] = baritems
        session['logininfo'] = logininfo
        return render_template('index.html', logininfo=logininfo, baritems=baritems)
    return redirect(url_for('login'))

@app.route("/login", methods=["POST","GET"])
#登录页面，不需要权限
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for('index'))

    if session.get('username') != None and session.get('username') != '' and \
       session.get('password') != None and session.get('password') != '' and not checklogin(session.get('username'), session.get('password')):
        session.pop('username', None)
        session.pop('password', None)
        return render_template('login.html', flag=1)
    else:
        session.pop('username', None)
        session.pop('password', None)
        return render_template('login.html', flag=0)

@app.route("/logout")
#登出页面，并不会实际显示，只是会注销登录信息并跳转到登录页面
def logout():
    session.pop('username',None)
    session.pop('password',None)
    session.pop('logininfo', None)
    return redirect(url_for('login'))

@app.route("/info", methods=["POST","GET"])
#个人信息页面，需要已登录用户权限
def info():
    if session.get('logininfo') == None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        description = request.form['description']
        updateinfo(session['username'], description)
        logininfo = checklogin(session['username'], session['password'])
        session['logininfo'] = logininfo
        return render_template('info.html', baritems = session['baritems'], logininfo = session['logininfo'], flag=1)
    return render_template('info.html', baritems = session['baritems'], logininfo = session['logininfo'], flag=0)

@app.route("/course", methods=["POST","GET"])
#课程信息页面，可以添加新的课程，需要“教务员”权限
def course():
    if session.get('logininfo') == None:
        return redirect(url_for('login'))
    if session['logininfo'][3] != '教务员':
        return redirect(url_for('index'))
    courses = getcourses()
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        credit = request.form['credit']
        description = request.form['description']
        if not addcourse(id, name, credit, description):
            return render_template('course.html', baritems = session['baritems'], logininfo = session['logininfo'], courses = courses, flag = 0)
    courses = getcourses()
    return render_template('course.html', baritems = session['baritems'], logininfo = session['logininfo'], courses = courses, flag = 1)

@app.route("/person", methods=["POST","GET"])
#人员名单页面，可以添加新的人员，需要“教务员”权限
def person():
    if session.get('logininfo') == None:
        return redirect(url_for('login'))
    if session['logininfo'][3] != '教务员':
        return redirect(url_for('index'))
    persons = getpersons()
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        role = request.form['role']
        description = request.form['description']
        if not addperson(id, name, role, description):
            return render_template('person.html', baritems = session['baritems'], logininfo = session['logininfo'], persons = persons, flag = 0)
    persons = getpersons()
    return render_template('person.html', baritems = session['baritems'], logininfo = session['logininfo'], persons = persons, flag = 1)
        
@app.route("/teach", methods=["POST","GET"])
#认领课程页面，可以选择担任哪门课程的教师，需要“教师”权限
def teach():
    if session.get('logininfo') == None:
        return redirect(url_for('login'))
    if session['logininfo'][3] != '教师':
        return redirect(url_for('index'))
    courses = getnotteached(session['username'])
    if request.method == 'POST':
        courseid = request.form['courseid']
        p1 = request.form['percent1']
        p2 = request.form['percent2']
        p3 = request.form['percent3']
        addteach(session['username'], courseid, p1, p2, p3)
        courses = getnotteached(session['username'])
        return render_template('teach.html', baritems = session['baritems'], logininfo = session['logininfo'], courses = courses)
    return render_template('teach.html', baritems = session['baritems'], logininfo = session['logininfo'], courses = courses)

@app.route("/teachlist")
#教师任课总表页面，显示所有任教情况，需要“教务员”权限
def teachlist():
    if session.get('logininfo') == None:
        return redirect(url_for('login'))
    if session['logininfo'][3] != '教务员':
        return redirect(url_for('index'))
    courses = getteachlist()
    return render_template('teachlist.html', baritems = session['baritems'], logininfo = session['logininfo'], courses = courses)

@app.route("/teached")
#已教课程页面，显示自己已任教的课程，可以查看选课名单，并录入成绩，需要“教师”权限
def teached():
    if session.get('logininfo') == None:
        return redirect(url_for('login'))
    if session['logininfo'][3] != '教师':
        return redirect(url_for('index'))
    courses, chooselists = getteached(session['username'])
    return render_template('teached.html', baritems = session['baritems'], logininfo = session['logininfo'], courses = courses, chooselists = chooselists)

@app.route("/chooselist/<teachid>")
#选课名单页面，显示某教师任教的某门课的选课名单，需要“教师”或“教务员”权限
def chooselist(teachid):
    if session.get('logininfo') == None:
        return redirect(url_for('login'))
    if session['logininfo'][3] == '学生':
        return redirect(url_for('index'))
    chooselist = getchooselist(teachid)
    return render_template('chooselist.html', baritems = session['baritems'], logininfo = session['logininfo'], chooselist = chooselist)

@app.route("/addgrade/<teachid>", methods=["POST","GET"])
#录入成绩页面，录入选该门课的学生的成绩，需要“教师”权限
def addgrade(teachid):
    if session.get('logininfo') == None:
        return redirect(url_for('login'))
    if session['logininfo'][3] != '教师':
        return redirect(url_for('index'))
    if request.method == 'POST':
        stuid = request.form['stuid'] 
        g1 = request.form['grade1']
        g2 = request.form['grade2']
        g3 = request.form['grade3']
        updategrade(stuid, teachid, g1, g2, g3)
    courses, chooselists = getteached(session['username'])
    for i in range(len(courses)):
        if courses[i][-1] == int(teachid):
            return render_template('addgrade.html', baritems = session['baritems'], logininfo = session['logininfo'], chooselist = chooselists[i])


@app.route('/changepw', methods=["POST","GET"])
#修改密码页面，如果现密码是初始密码，则不显示导航栏，否则按用户身份显示导航栏，需要已登录用户权限
def changepw():
    if request.method == 'POST':
        session['password'] = request.form['newpw']
        changepassword(session['username'], session['password'])
        return redirect(url_for('index'))
    if session.get('username') == None:
        return redirect(url_for('login'))
    flag = 1
    if session['password'] == '666666':
        flag = 0
    return render_template('changepw.html', flag=flag, pw=session['password'], baritems = session.get('baritems'), logininfo = session.get('logininfo'))

@app.route('/select', methods=["POST","GET"])
#选课页面，显示可选课程和已选课程，并且可以选课，需要“学生”权限
def select():
    if session.get('logininfo') == None:
        return redirect(url_for('login'))
    if session['logininfo'][3] != '学生':
        return redirect(url_for('index'))
    if request.method == 'POST':
        teachid = request.form['teachid']
        selectcourse(session['username'], teachid)
        selected, unselected, unselectednums = getallteach(session['username'])
        return render_template('select.html', baritems = session['baritems'], logininfo = session['logininfo'], teachlist=unselected, selectlist=selected, nums=unselectednums, flag=1)
    selected, unselected, unselectednums = getallteach(session['username'])
    return render_template('select.html', baritems = session['baritems'], logininfo = session['logininfo'], teachlist=unselected, selectlist=selected, nums=unselectednums, flag=0)

@app.route('/grade')
#查看成绩页面，查看自己已选的所有课程的成绩，需要“学生”权限
def grade():
    if session.get('logininfo') == None:
        return redirect(url_for('login'))
    if session['logininfo'][3] != '学生':
        return redirect(url_for('index'))
    grades = getgrade(session['username'])
    return render_template('grade.html', baritems = session['baritems'], logininfo = session['logininfo'], grades=grades)

@app.route('/find', methods=["POST","GET"])
#查询人员信息页面，输入ID查询对应用户信息，需要“教务员”权限
def find():
    if session.get('logininfo') == None:
        return redirect(url_for('login'))
    if session['logininfo'][3] != '教务员':
        return redirect(url_for('index'))
    if request.method == 'POST':
        userid = request.form['userid']
        baseinfo, addinfo = searchinfo(userid)
        role = baseinfo[3]
        return render_template('find.html', baritems = session['baritems'], logininfo = session['logininfo'], baseinfo=baseinfo, addinfo=addinfo, role=role, flag=1)
    return render_template('find.html', baritems = session['baritems'], logininfo = session['logininfo'], baseinfo=None, addinfo=None, role='', flag=0)


if __name__ == "__main__":
    app.run()


