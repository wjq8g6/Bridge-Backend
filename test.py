from flask import Flask
import pandas as pd
import numpy as np
app = Flask(__name__)

@app.route("/name/<int:name_id>")
def get_name(name_id):
    data = pd.read_csv('data.csv')
    return data['Name'][name_id]

@app.route("/info/<int:id>")
def returnIDs(id):
    data = pd.read_csv('data.csv')
    stu = data.iloc[id].values
    ret = ""
    for val in stu:
        ret += str(val) + ","
    return ret


@app.route("/adduser/<string:info>")
def addStu(info):
    data = pd.read_csv('data.csv')
    lst = info.split(",")
    df_new = pd.DataFrame([lst], columns = data.columns)
    data = data.append(df_new)
    data.to_csv("data.csv",index = False)
    return "Success"


@app.route("/getnn/<int:id>/req/<string:class_name>")
def getNN(id, class_name):
    data = pd.read_csv('data.csv')
    candidates = data.loc[data[class_name] == 1]
    ind_list = candidates.index
    pot = candidates.drop('Name', axis=1).values
    data = data.drop('Name', axis=1)
    stu = data.iloc[id].values
    lst = []
    for row in pot:
        lst.append(np.linalg.norm(stu - row))
    ind = lst.index(min(lst))
    return returnIDs(ind_list[ind])
