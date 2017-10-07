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
    return "Finished Initialization"

@app.route("/name/<int:name_id>")
def get_name(name_id):
    return data['Name'][name_id]

@app.route("/info/<int:id>")
def returnIDs(id):
    return data[id]

'''
@app.route("/adduser/<string:info>")
def addStu(info):
    data = pd.read_csv('data.csv')
    lst = info.split(",")
    df_new = pd.DataFrame([lst], columns = data.columns)
    data = data.append(df_new)
    data.to_csv("data.csv",index = False)
    return "Success"
'''


@app.route("/getnn/<int:id>/<string:class_name>/<int:num_ret>")
def getNN(id, class_name, num_ret):
    stuids = []
    dists = []
    target = data[id]
    for i in range(len(data)):
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
