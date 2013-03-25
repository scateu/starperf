#! -*- coding:utf8 -*-
from flask import Flask,url_for,render_template,send_file,abort
import re
import os
app = Flask(__name__)
app.debug = True

def isIP(address):
    try:
        m = re.match('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})',address)
        ip = m.group(0)
        return True
    except: 
        return False


@app.route('/')
@app.route('/<host>')
def show_result(host='59.66.84.66'):
    results = []

    toTitle = {'throughput':u'吞吐量(MB/s)',
              'loadtime':u'Web页面载入时间 (s)',
              'ping':u'ping时延 (ms)',
            }

    if not isIP(host):
        abort(404)
    for dirName,subdirList,fileList in os.walk('./%s/'%host):
        for fname in fileList:
            if fname.endswith('-daily.png'):
                #fname='throughput_166.111.111.91.rrd-daily.png'
                _type = fname.split('_')[0]
                _dest = fname.split('_')[1].split('.rrd-')[0]
                _title = toTitle[_type]
                results.append(dict(title=_title,destination=_dest,image=fname))
    results.sort()
    return render_template('result.html', host=host,results=results)

@app.route("/images/<host>/<path>")
def getImage(host,path):
    if not isIP(host):
        abort(404)
    if path.startswith('..') or path.startswith('/') or not path.endswith('.png'):
        abort(404)
    filename='./%s/%s'%(host,path)
    resp = send_file(filename)
    #resp.cache_control.no_cache = True
    return resp

if __name__ == "__main__":
    app.run('0.0.0.0',9324)
