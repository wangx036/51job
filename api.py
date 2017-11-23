from flask import Flask, request, render_template
import sqldb
from sqldb import job
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', job_list=sqldb.JOBS)


@app.route('/getpoint', methods=['GET'])
def get_map_point():
    list = []
    for job in sqldb.JOBS:
        list.append({"id": job.id, "lng": job.lng, "lat": job.lat})
    return json.dumps({"data": list})


@app.route('/getjob', methods=['GET'])
def get_job_json():
    id = request.args.get("id")
    model = sqldb.get_job_model(id)
    m = {"id": model.id,
         "name": model.name,
         "coid": model.coid,
         "coname": model.coname,
         "salaryname": model.salaryname,
         "lng": model.lng,
         "lat": model.lat,
         "comment": model.comment,
         "createdate": str(model.createdate)
         }
    return json.dumps(m)


if __name__ == '__main__':
    app.run(port=8000)
