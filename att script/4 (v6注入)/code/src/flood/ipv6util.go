package main

import (
	"encoding/hex"
	"fmt"
	"net"
	"os/exec"
	"strings"
	"syscall"
	"unsafe"
)

type router struct {
	ifaces []net.Interface
	addrs  []net.IP
	v6     routeSlice
}
type routeSlice []*rtInfo

type rtInfo struct {
	// Dst              net.IPNet
	Gateway, PrefSrc net.IP
	OutputIface      uint32
	Priority         uint32
}

func getv6Gateway() (net.IP, error) {
	rtr := &router{}

	tab, err := syscall.NetlinkRIB(syscall.RTM_GETROUTE, syscall.AF_INET6)
	if err != nil {
		return nil, err
	}

	msgs, err := syscall.ParseNetlinkMessage(tab)
	if err != nil {
		return nil, err
	}

	for _, m := range msgs {
		switch m.Header.Type {
		case syscall.NLMSG_DONE:
			break
		case syscall.RTM_NEWROUTE:
			// rtmsg := (*syscall.RtMsg)(unsafe.Pointer(&m.Data[0]))
			attrs, err := syscall.ParseNetlinkRouteAttr(&m)
			if err != nil {
				return nil, err
			}
			routeInfo := rtInfo{}
			rtr.v6 = append(rtr.v6, &routeInfo)
			for _, attr := range attrs {
				switch attr.Attr.Type {
				// case syscall.RTA_DST:
				// 	routeInfo.Dst.IP = net.IP(attr.Value)
				// 	routeInfo.Dst.Mask = net.CIDRMask(int(rtmsg.Dst_len), len(attr.Value)*8)
				case syscall.RTA_GATEWAY:
					routeInfo.Gateway = net.IP(attr.Value)
				case syscall.RTA_OIF:
					routeInfo.OutputIface = *(*uint32)(unsafe.Pointer(&attr.Value[0]))
				case syscall.RTA_PRIORITY:
					routeInfo.Priority = *(*uint32)(unsafe.Pointer(&attr.Value[0]))
				case syscall.RTA_PREFSRC:
					routeInfo.PrefSrc = net.IP(attr.Value)
				}
			}
		}
	}
	ips := []net.IP{}
	for _, rt := range rtr.v6 {
		if rt.Gateway != nil {
			ips = append(ips, rt.Gateway)
		}
	}
	return ips[0], nil
}

func getGatewayV6Mac(ifacename string, gwIP net.IP) (net.HardwareAddr, error) {
	if debugOutput {
		println("邻居发现--使用网卡接口为:" + ifacename)
	}
	out, err := exec.Command("ip", "-6", "neighbor", "show", "dev", ifacename).Output()
	if err != nil {
		println(err.Error())
	} else {
		outlines := strings.Split(string(out), "/n")
		for _, line := range outlines {
			linelist := strings.Split(line, " ")
			// 与网关对应的MAC地址
			if linelist[0] == gwIP.String() {

				maclist := strings.Split(linelist[2], ":")
				var macbyte []byte
				for _, m := range maclist {
					b, _ := hex.DecodeString(m)
					macbyte = append(macbyte, b[0])
				}
				return net.HardwareAddr(macbyte), nil
			}
		}
	}
	return nil, fmt.Errorf("无法找到网关" + gwIP.String() + "对应的MAC地址")
}
