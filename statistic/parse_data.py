import os
import os.path
import time
import csv
import rrdtool


#ROOT_DIR='../result-sample/'
ROOT_DIR='/home/scateu/tmp/starperf-log/'

data = []


def ParseData(filename):
    """
    for example:
    item = {'ip': '59.66.84.66', 
            'result':{
                'ping': [
                        ['166.111.8.28', '0.562', 'ms'], 
                        ['8.8.8.8', '41.973', 'ms']
                        ], 
                'loadtime': [
                        ['http://www.baidu.com', '0.03', 's'], 
                        ['http://www.youku.com', '0.07', 's'], 
                        ['http://www.google.com.hk', '0.21', 's'], 
                        ['http://www.10086.cn/bj/', '7.39', 's'], 
                        ['http://www.kernel.org/', '0.42', 's'], 
                        ['http://www.renren.com/', '0.02', 's']
                        ], 
                'throughput': [
                        ['166.111.111.91', '11.2', 'MB/s']
                        ], },
            'time': 1363791918.9046614
            }

    """

    global data

    item={}

    # get time
    item['time'] = os.path.getmtime(filename)

    # get ip # example filename = './abc/def/59.66.66.66/some.result'
    item['ip'] = os.path.split(os.path.split(filename)[0])[-1]

    # get data
    item['result'] = {}
    csv_data = csv.reader(open(filename,'r'))
    for row in csv_data:
        # example : ['loadtime', 'http://www.baidu.com', '0.252 s']
        _type = row[0].strip()
        _target = row[1].strip()
        _result = row[2].strip().split(' ')[0].strip()
        _unit = row[2].strip().split(' ')[-1].strip()
        if not item['result'].has_key(_type):
            item['result'][_type] = []

        item['result'][_type].append([_target,_result,_unit])

    # add to global data
    data.append(item)

    # remove file
    os.remove(filename)


    # touch rrd database ; create and update
    touch_rrd(item)



def format_url(url):
    """
    input : 'http://www.10086.cn/bj/'
    output : www.10086.cn
    """
    url = str(url)
    return url.replace("http://","").replace("ftp://","").split('/')[0]

def touch_rrd(item):
    """
    create a rrd database for each ip, if not exists
    """

    for _type,_target in item['result'].items(): 
        ip = item['ip']
        if not os.path.isdir('./%s'%ip):
            os.mkdir('./%s'%ip)

        for result in item['result'][_type]:
            # example: ['166.111.8.28','30','ms']
            rrd_filename = './%s/%s_%s.rrd'%(ip,_type,format_url(result[0]))
            
            if not os.path.exists(rrd_filename):
                rrdtool.create(rrd_filename, '--step','900',
                               '--start','-8640000',
                                "DS:result:GAUGE:2000:U:U",
                                "RRA:AVERAGE:0.5:1:600",
                                "RRA:AVERAGE:0.5:24:775",
                                "RRA:MAX:0.5:1:600",
                                "RRA:MAX:0.5:24:775",
                                )
            #then update it
            rrdtool.update(rrd_filename,"%d:%s"%(item['time'],result[1]))

def graph_rrd():
    for dirName,subdirList,fileList in os.walk('.'):
        for fname in fileList:
            if fname.endswith('.rrd'):
                print 'graphing'
                for sched in ['hourly','daily' , 'weekly', 'monthly']:
                    if sched == 'weekly':
                        period = '1w'
                    elif sched == 'daily':
                        period = '3d'
                    elif sched == 'monthly':
                        period = '1m'
                    elif sched == 'hourly':
                        period = '1h'
                    os.chdir(dirName)
                    ret = rrdtool.graph("%s-%s.png" %(fname,sched), "--start", "-%s" %(period), "--vertical-label=Num",
                         "--slope-mode",
                         "-w 800",
                         "DEF:m1_num=%s:result:AVERAGE"%fname,
                         "LINE1:m1_num#0000FF:result\\r",
                         "GPRINT:m1_num:AVERAGE:Avg m1\: %6.0lf ",
                         "GPRINT:m1_num:MAX:Max m1\: %6.0lf \\r")
                    print ret
                    os.chdir('..')

if __name__ == "__main__":
    for dirName,subdirList,fileList in os.walk(ROOT_DIR):
        for fname in fileList:
             ParseData(os.path.join(dirName,fname))

    graph_rrd()
