# -*- coding: UTF-8 -*-
from multiprocessing.pool import Pool

import requests
import json
import sqldb
from bs4 import BeautifulSoup
import re
from functools import partial
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
    html = r.text
    patter = re.compile('<script.*g_company.*lat:"([\d|\.]*)",lng:"([\d|\.]*)".*</script>', re.S)
    co_str = re.findall(patter, html)
    lat = float(co_str[0][0] or 0)
    lng = float(co_str[0][1] or 0)
    # print( {'lat':lat,'lng':lng})
    return {'lat': lat, 'lng': lng}


# 爬取某一页的所有职位
def one_page(i, para):
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
        no += 1

if __name__ == '__main__':
    paradata = {
        "jobarea": "080200",
        "keyword": ".net",
        "saltype": "05,06,07",
        "issuedate": 1,
        "keywordtype": 2,
    }

    page_with_para = partial(one_page, para=paradata)
    pool = Pool()
    pool.map(page_with_para, [i for i in range(15)])
