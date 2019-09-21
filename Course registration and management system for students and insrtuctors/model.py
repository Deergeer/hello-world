import MySQLdb

conn=MySQLdb.connect(host="localhost",user="root",passwd="",db="dean",charset="utf8") #连接“dean”数据库    
cursor = conn.cursor()      

#检查登录，如果账号密码匹配则返回用户信息，否则返回False
def checklogin(userid, password):
    sql = "select * from person where id=%s and password=%s"     
    param = (userid, password)      
    cursor.execute(sql, param)
    try:
        result = cursor.fetchall()[0]
        return result
    except:
        return False

#修改指定用户的密码
def changepassword(userid, newpassword):
    sql = "update person set password=%s WHERE id=%s"
    param = (newpassword, userid)
    cursor.execute(sql, param)
    conn.commit()

#更新个人信息（修改个人描述）
def updateinfo(userid, description):
    print(userid, description)
    sql = "update person set description=%s WHERE id=%s"
    param = (description, userid)
    cursor.execute(sql, param)
    conn.commit()

#根据用户身份，返回导航栏元素及URL
def navbaritems(type):
    if type == '教务员':
        return {'人员名单': '/person', '课程信息': '/course', '教师任课总表': '/teachlist', '查询人员信息': '/find'}
    elif type == '教师':
        return {'已教课程': '/teached', '认领课程': '/teach'}
    else:
        return {'选课': '/select', '查看成绩': '/grade'}

#获取所有人员信息
def getpersons():
    sql = "select * from person"
    cursor.execute(sql)
    persons = cursor.fetchall()
    return persons

#获取所有课程信息
def getcourses():
    sql = "select * from course"
    cursor.execute(sql)
    courses = cursor.fetchall()
    return courses

#根据学生ID获取该学生的已选课程，可选（未选）课程，可选课程的选课人数
def getallteach(userid):
    sql = 'select teach.id, person.name, course.name, credit, course.description, percent1, percent2, percent3 from (teach inner join course on courseid=course.id) inner join person on teacherid=person.id'
    cursor.execute(sql)
    courses = cursor.fetchall()
    selected = []
    unselected = []
    unselectednums = []
    sql = 'select * from choose where personid=%s' % userid
    cursor.execute(sql)
    choosed = cursor.fetchall()
    teachid = []
    for i in choosed:
        teachid.append(i[1])
    for course in courses:
        if course[0] not in teachid:
            sql = 'select * from choose where teachid=%s' % course[0]
            cursor.execute(sql)
            chooses = cursor.fetchall()
            unselectednums.append(len(chooses))
            unselected.append(course)
        else:
            selected.append(course)
    return selected, unselected, unselectednums

#获取所有教师任教信息        
def getteachlist():
    sql = 'select courseid, course.name, person.name, credit, course.description, teach.id from (teach inner join course on courseid=course.id) inner join person on teacherid=person.id'
    cursor.execute(sql)
    teaches = cursor.fetchall()
    return teaches

#根据教师ID获取已任教的课程，和已任教课程对应的选课名单
def getteached(userid):
    sql = 'select courseid, name, credit, description, percent1, percent2, percent3, teach.id from teach inner join course on courseid=course.id where teacherid=%s' %userid
    cursor.execute(sql)
    teached = cursor.fetchall()
    chooselists = []
    for t in teached:
        chooselist = getchooselist(t[-1])
        chooselists.append(chooselist)
    return teached, chooselists

#根据任教信息表的id获取某教师教授的某课程的选课名单
def getchooselist(teachid):
    sql = 'select personid, name, grade1, grade2, grade3, grade from choose inner join person on personid=person.id where teachid=%s' % teachid
    cursor.execute(sql)
    chooselist = cursor.fetchall()
    return chooselist

#根据教师ID获取可认领（未任教）的课程
def getnotteached(userid):
    sql = "select * from course"
    cursor.execute(sql)
    courses = cursor.fetchall()
    notteached = []
    sql = "select * from teach where teacherid=%s" % userid
    cursor.execute(sql)
    teached = cursor.fetchall()
    for c in courses:
        notteached.append(c)
    for t in teached:
        for c in notteached:
            if t[2] == c[0]:
                notteached.remove(c)
    return notteached

#根据学生ID获取已选课程的成绩
def getgrade(userid):
    sql = "select course.name, credit, grade1, grade2, grade3, grade from (choose inner join teach on teachid = teach.id) inner join course on courseid = course.id where choose.personid=%s" % userid
    cursor.execute(sql)
    grades = cursor.fetchall()
    return grades

#根据人员ID获取人员信息，如果该人员是教师，还会获取任教列表和选课名单；如果是学生，还会获取选课列表
def searchinfo(userid):
    sql = 'select * from person where id=%s' % userid
    cursor.execute(sql)
    try:
        baseinfo = cursor.fetchall()[0]
    except:
        return None
    if baseinfo[3] == '教师':
        addinfo, chooselist = getteached(userid)
    else:
        addinfo, unselected, unselectednums = getallteach(userid)
    return baseinfo, addinfo

#选课，根据学生ID和任教信息表的id，选修某门课程
def selectcourse(userid, teachid):
    sql = "insert into choose(personid, teachid) values(%s, %s)"
    param = (userid, teachid)
    cursor.execute(sql, param)
    conn.commit()

#任教，根据教师ID，课程ID，平时、期中、期末成绩占比，添加任教信息
def addteach(teacherid, courseid, p1, p2, p3):
    sql = "insert into teach(teacherid, courseid, percent1, percent2, percent3) values(%s, %s, %s, %s, %s)"
    param = (teacherid, courseid, int(p1), int(p2), int(p3))
    cursor.execute(sql, param)
    conn.commit()

#录入成绩，根据学生ID，任教信息表的id，平时、期中、期末成绩，为该学生计算总成绩并录入
def updategrade(personid, teachid, g1, g2, g3):
    sql = 'select * from teach where id=%s' % teachid
    cursor.execute(sql)
    teachinfo = (cursor.fetchall())[0]
    g1 = int(g1); g2 = int(g2); g3 = int(g3)
    p1 = teachinfo[3]; p2 = teachinfo[4]; p3 = teachinfo[5]
    grade = g1*p1 + g2*p2 + g3*p3
    grade = int(grade/100)
    sql = 'update choose set grade1=%s, grade2=%s, grade3=%s, grade=%s where personid=%s and teachid=%s'
    param = (g1, g2, g3, grade, personid, teachid)
    n = cursor.execute(sql, param)
    print(n)
    conn.commit()
    
#添加课程
def addcourse(id, name, credit, description):
    try:
        credit = int(credit)
    except:
        return False
    sql = "select * from course where id=%s" % id
    cursor.execute(sql)
    courses = cursor.fetchall()
    if len(courses) > 0:
        return False
    sql = "insert into course values(%s, %s, %s, %s)"
    param = (id, name, credit, description)
    cursor.execute(sql, param)
    conn.commit()
    return True

#添加人员
def addperson(id, name, role, description):
    sql = "select * from person where id=%s" % id
    cursor.execute(sql)
    courses = cursor.fetchall()
    if len(courses) > 0:
        return False
    sql = "insert into person(id, name, role, description) values(%s, %s, %s, %s)"
    param = (id, name, role, description)
    cursor.execute(sql, param)
    conn.commit()
    return True

