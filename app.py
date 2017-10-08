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
    data = fb.get("", None)
    global num_students
    num_students = len(data)
    return "Finished Initialization"

@app.route("/name/<int:name_id>")
def get_name(name_id):
    return data['Name'][name_id]

@app.route("/info/<int:id>")
def returnIDs(id):
    return data[id]


@app.route("/adduser/<string:info>/<string:classes>")
def addStu(info,classes):
    num_students = len(data)
    headers = ['Name','Email','Year','Gender','Ethnicity','Major']
    stu_info = info.split(",")
    courses = classes.split(",")
    dict = {headers[i]:stu_info[i] for i in range(len(headers))}
    dict_class = {courses[k]:1 for k in range(len(courses))}
    dict['Courses'] = dict_class
    fb.put("",str(num_students),dict)
    num_students+=1
    return "Success"



@app.route("/getSim/<int:id>/<string:class_name>/<int:num_ret>")
def getNN(id, class_name, num_ret):
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

@app.route("/common/<int:stu>/<int:target>")
def commonTraits(stu, target):
    headers = ['Year', 'Gender', 'Ethnicity', 'Major']
    common = []
    for head in headers:
        if stu[head] == target[head]:
            common.append(head)
    s1 = set(stu['Courses'])
    s2 = set(target['Courses'])
    for i in s1.intersection(s2):
        common.append(i)
    return common

def calDist(stu, target):
    headers = ['Year','Gender','Ethnicity','Major']
    dist = 0
    for head in headers:
        if stu[head] != target[head]:
            dist += 1
    s1 = set(stu['Courses'])
    s2 = set(target['Courses'])
    dist += 16 - len(s1.intersection(s2))
    return dist
