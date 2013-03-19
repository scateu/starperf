StarPerf
========
A simple network performance test tool.

upload result through rsync every 30min.

## Client




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

