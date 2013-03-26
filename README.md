StarPerf
========
A simple network performance test tool.

upload result through rsync every 30min.

## Client
require 

* coreutils-timeout
* iperf
* wget
* rsync

available on openwrt.


## Server

### iPerf server
iperf -s

### HTTP server 
needs to provide lists, fetched by clients every time

  * iperf.list
  * loadtime.list 
  * ping.list

### rsyncd server
clients upload result through rsyncd

example:

        ~/tmp/starperf-log$ cat /etc/rsyncd.conf
        motd file = /etc/rsyncd.motd
        log file = /var/log/rsyncd.log
        pid file = /var/run/rsyncd.pid
        lock file = /var/run/rsync.lock

        [starperf]
        path = /home/scateu/tmp/starperf-log/
        comment = star perf
        uid = scateu
        gid = scateu
        read only = no

### RRD Parsing
parse data collected from rsyncd into rrddata, and draw it into png

       cd statistics
       while true;do python parse_data.py ;sleep 200;done


### result http server
a simple flask http server on 9324 port

       cd statistics
       python index.py

