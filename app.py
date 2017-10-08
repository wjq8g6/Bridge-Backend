from flask import Flask, json
import pandas as pd
import numpy as np
from firebase import firebase
app = Flask(__name__)


@app.route("/")
def init():
    global fb
    aut = firebase.FirebaseAuthentication('hY5kvBhsK4MZbShXIxeMEo0rOWyfL7LdW5TC95Od', 'wjq8g6@gmail.com')
    fb = firebase.FirebaseApplication('https://bridge-fb5ab.firebaseio.com', aut)
    global data
    data = fb.get("students", None)
    global num_students
    num_students = 0
    num_students = len(data)
    return "Finished Initialization"

@app.route("/name/<int:id>")
def get_name(id):
    init()
    global data
    return data[id].get('Name')

@app.route("/email/<int:id>")
def get_email(id):
    init()
    global data
    return data[id].get('Email')

@app.route("/year/<int:id>")
def get_year(id):
    init()
    global data
    return data[id].get('Year')

@app.route("/gender/<int:id>")
def get_gender(id):
    init()
    global data
    return data[id].get('Gender')

@app.route("/major/<int:id>")
def get_major(id):
    init()
    global data
    return data[id].get('Major')

@app.route("/courses/<int:id>")
def get_courses(id):
    init()
    global data
    lst = data[id].get('Courses')
    ret = ""
    for i in lst:
        ret += i + ','
    ret = ret[:-1]
    return ret


@app.route("/adduser/<string:info>/<string:classes>")
def addStu(info,classes):
    init()
    global num_students
    headers = ['Name','Email','Year','Gender','Ethnicity','Major']
    stu_info = info.split(",")
    courses = classes.split(",")
    dict = {headers[i]:stu_info[i] for i in range(len(headers))}
    dict_class = {courses[k]:1 for k in range(len(courses))}
    dict['Courses'] = dict_class
    fb.put("students",str(num_students),dict)
    num_students+=1
    return str(num_students-1)



@app.route("/getSim/<int:id>/<string:class_name>/<int:num_ret>")
def getNN(id, class_name, num_ret):
    init()
    global data
    global num_students
    stuids = []
    dists = []
    target = data[id]
    for i in range(num_students):
        if i != id:
            stu = data[i]
            courses = stu['Courses']
            if class_name in courses:
                stuids.append(i)
                dists.append(calDist(stu,target))
    if num_ret > len(dists):
        ret = ''
        for j in stuids:
            ret += str(j) + ','
        ret = ret[:-1]
        return ret
    else:
        ind = np.argpartition(dists, num_ret)[:num_ret]
        ret = ''
        for k in ind:
            ret += str(stuids[k])+','
        ret = ret[:-1]
        return ret

@app.route("/common/<int:id1>/<int:id2>")
def commonTraits(id1, id2):
    init()
    global data
    stu = data[id2]
    target = data[id1]
    headers = ['Year', 'Gender', 'Ethnicity', 'Major']
    ret = ''
    for head in headers:
        if stu[head] == target[head]:
            ret += head + ","
    s1 = set(stu['Courses'])
    s2 = set(target['Courses'])
    for i in s1.intersection(s2):
        ret += i + ','
    ret = ret[:-1]
    return ret

def calDist(stu, target):
    init()
    headers = ['Gender','Ethnicity','Major']
    dist = 0
    for head in headers:
        if stu[head] != target[head]:
            dist += 2
    s1 = set(stu['Courses'])
    s2 = set(target['Courses'])
    dist += 16 - len(s1.intersection(s2))
    return dist
