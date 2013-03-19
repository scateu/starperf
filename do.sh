IPERF_LIST=http://laser.k.ramlab.net/iperf.list
PING_LIST=http://laser.k.ramlab.net/ping.list
LOADTIME_LIST=http://laser.k.ramlab.net/loadtime.list

fetch_iperf_list()
{
    echo fetching iperf list >&2
    wget $IPERF_LIST -O /tmp/iperf.list -q
}

fetch_ping_list()
{
    echo fetching ping list >&2
    wget $PING_LIST -O /tmp/ping.list -q
}
fetch_loadtime_list()
{
    echo fetching loadtime list >&2
    wget $LOADTIME_LIST -O /tmp/loadtime.list -q
}

test_iperf()
{
    echo iperfing $1 >&2
    result=`iperf -c laser.k.ramlab.net -f M -t 1 -x CMSV  |tail -n 1| cut -d's' -f3 |sed "s/MByte/MB\/s/" |sed "s/^  //"`
    echo throughput,$1,$result
}

test_ping()
{
    echo pinging $1 >&2
    result=`ping $1 -c 4 |tail -n 1 | cut -d'=' -f2 |cut -d'/' -f2`
    echo ping,$1,$result
}
test_loadtime()
{
    echo loading $1 >&2
    result=`(time wget $1 -O /dev/null -q) 2>&1 | grep real |cut -f2 | cut -dm -f2`
    echo loadtime,$1,$result
}

StarTest(){
        fetch_loadtime_list
        while read urls
        do
            test_loadtime $urls
        done < /tmp/loadtime.list

        fetch_iperf_list
        while read urls
        do
            test_iperf $urls
        done < /tmp/iperf.list

        fetch_ping_list
        while read urls
        do
            test_ping $urls
        done < /tmp/ping.list
}
current_date=`TZ="Asia/Shanghai" date +%Y-%m-%d-%H.%M.%S`

myip() {
    echo >&2 "Getting your public IPv4 address"
    if type wget >/dev/null 2>/dev/null; then
        wget -qO- 'http://ipv4.icanhazip.com'
    elif type curl >/dev/null 2>/dev/null; then
        curl 'http://ipv4.icanhazip.com'
    else
        echo >&2 "Neither of wget and curl found. Install one of them. Abort."
        exit 1
    fi
}

ip=`myip`

StarTest > $current_date_$ip.result
