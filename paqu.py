# -*- coding: UTF-8 -*-

import requests
import json
import sqldb
from bs4 import BeautifulSoup
import re
import time


# 获取每页的职位 dict
def get_job_list(para, pageno):
    para['pageno'] = pageno
    r = requests.post('http://m.51job.com/ajax/search/joblist.ajax.php', params=para);
    r.encoding = 'utf-8'
    return json.loads(r.text)['data']


# 获取详情
def get_job_commont(jobid):
    r = requests.get('http://m.51job.com/search/jobdetail.php', params={'jobid': jobid})
    html = r.text.encode(r.encoding).decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    commont = soup.find('article').text.strip() or ""
    return commont


# 获取经纬度
def get_job_point(jobid):
    r = requests.get('http://search.51job.com/jobsearch/bmap/map.php', params={'jobid': jobid})
    html = r.text.encode(r.encoding).decode('GB2312').replace(' ', '')
    co_str = re.findall(r"g_company=({.+});", html)[0]
    lat = float(re.findall(r"lat:\"((\d|\.)*)\"", co_str)[0][0] or 0)
    lng = float(re.findall(r"lng:\"((\d|\.)*)\"", co_str)[0][0] or 0)
    # print( {'lat':lat,'lng':lng})
    return {'lat': lat, 'lng': lng}


if __name__ == '__main__':
    para = {
        "jobarea": "080200",
        "keyword": ".net",
        "saltype": "06",
        "issuedate": 1,
        "keywordtype": 2,
    }

    for i in range(1, 21):
        # 已存在的职位的id
        job_id = [str(job.id) for job in sqldb.get_job_list()]

        job_list = get_job_list(para, i)
        add_list = list(filter(lambda o: o['jobid'] not in job_id, job_list))
        no = 0
        for item in add_list:
            point = get_job_point(item['jobid'])
            new_job = sqldb.job(
                id=item['jobid'],
                name=item['cjobname'],
                salaryname=item['jobsalaryname'],
                lng=point['lng'],
                lat=point['lat'],
                comment=get_job_commont(item['jobid']),
                coid=item['coid'],
                coname=item['cocname'],
            )

            sqldb.add_job(new_job)
            print(str(i) + '页  ' + str(no))
            time.sleep(0.5)
        time.sleep(1)
