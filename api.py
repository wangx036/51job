import  json
import jsonHelper
from flask import Flask, request, render_template
import sqldb

app = Flask(__name__)


def get_job_list():
    session = sqldb.DBSession()
    list=session.query(sqldb.job)
    session.close()
    return list

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html', job_list=get_job_list())

@app.route('/getpoint',methods=['GET'])
def get_map_point():
    list=[]
    for job in get_job_list():
        print(job.lng)
        list.append({"id":job.id,"lng":job.lng,"lat":job.lat})
        print(list)

    print({"data":list})
    return str({"data":list})

if __name__ == '__main__':
    app.run(port = 8000)


