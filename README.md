StarPerf
========
A simple network performance test tool.

upload result through rsync every 30min.

## Client
require 

* coreutils-timeout
* iperf


## Server

* iperf -s
* http server 
  * iperf.list
  * loadtime.list 
  * ping.list
* rsyncd
 * example

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

* parse\_data.py

       while true;do python parse_data.py ;sleep 200;done

* flask http server on 9324 port

       python index.py

