<template>
    <div class="LT-body">
        <el-tabs v-model="activeName"
                 @tab-click="handleClick"
                 :stretch=true
                 tab-position="bottom">
            <el-tab-pane label="ICMP/IPv6时延" name="first"></el-tab-pane>
            <el-tab-pane label="DNS查询时延" name="second"></el-tab-pane>
            <el-tab-pane label="TCP连接时延" name="third"></el-tab-pane>
        </el-tabs>
        <div style="text-align: left;">
            <h3>目标地址：{{ DNSip }}</h3>
            <div style="text-align: center;">     
                <div style="width: 50%; display: inline-block;"><el-input v-model="inputText" @keyup.native.enter="changeDNSip" placeholder="请输入目标IPv4地址，输入回车/Enter结束"></el-input></div>
                <el-button style="margin-left: 10px;" type="primary"  @click="startGet"> 开始 </el-button>
                <el-button style="margin-left: 10px;" type="primary"  @click="stopGet"> 停止 </el-button>
            </div>
        </div>
    
        <div class="LT-body-dataShow">
            <div class="LT-body-dataShow-control">
                
            </div>
            <!-- chart 是图表的id， 下面单个div最终渲染成直方图图表-->
            <div id="chart"></div>
            <!-- <div style="height: 1px; width: 400px; display: inline-block;"></div> -->
            <div class="LT-body-dataShow-table">
                <el-table
                    :data="allNodesData"
                    :cell-class-name="cellName"
                    style="width: 100%; max-height:86%; overflow-y: auto"
                    border>
                    <el-table-column
                        prop="Name"
                        label="节点"
                        min-width="20">
                    </el-table-column>
                    <el-table-column
                        prop="delay"
                        label="实时时延/ms"
                        min-width="20">
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <FooterTable></FooterTable>
    </div>
</template>

<script>
import * as echarts from 'echarts';
import { mapState } from 'vuex';

import FooterTable from './FooterTable.vue';

    export default {
        name: 'LatencyTest',
        components: {
            FooterTable,
        },
        data() {
            return {
                DNSip:'', // 目标ip地址
                inputText:'',
                activeName: 'first', // 当前选中了哪个分页 first -> 目标地址  second -> ICMP/IPv6时延 third -> DNS查询时延 fourth-> TCP连接时延
                activeTag: 'icmp', //当前选中分页的标志  用于 结合DNSip，作为向后台请求数据的参数
                intervalID: '', // 定时任务的id，用于停止定时任务
                myEchart:'',    //柱状图的实例对象
                option:{ //为图表设置数据
                    title: {
                        text: '节点时延统计'
                    },
                    color: '#6861ce',
                    tooltip: {},
                    xAxis: {
                        data: '',
                    },
                    legend:{
                        data:['时延/ms']
                    },
                    yAxis: {},
                    series: [
                        {
                        name: '时延/ms',
                        type: 'bar',
                        data: '',
                        }
                    ]
                },
            };
        },
        computed:{
            ...mapState({allNodesData:"allNodesData"}),
            xLable() {
                var xLable = []
                for(let i = 0; i < this.allNodesData.length; i++){
                    xLable.push(this.allNodesData[i].Loc)
                }
                return xLable
            },
            delay() {
                var delay = []
                for(let i = 0; i < this.allNodesData.length; i++){
                    delay.push(this.allNodesData[i].delay)
                }
                return delay
            }
        },
        mounted:function(){
            // 柱状图宽度跟随窗口大小变化
            window.onresize = () => {
                this.myEchart && this.myEchart.resize()
            }
            // 初始化柱状图
            this.myEchart = echarts.init(document.getElementById('chart')) // 更改样式的地方
            this.updateChart()
            // 获取测试节点信息
            this.$store.dispatch('queryAllNodes')
        },
        watch:{
            'delay':function() {
                this.updateChart()
            }
        },
        methods: {
            // 每次执行，会向后台请求一次数据，数据直接用this.$store.allnodes访问
            queryData() {
                this.$store.dispatch('queryDelay', {ip:this.DNSip, type:this.activeTag})
            },
            updateChart() {
                this.option.series=[{name:'时延/ms', type:'bar', data:this.delay}]
                this.option.xAxis={data:this.xLable}
                this.myEchart.setOption(this.option)
            },
            startGet(){//设置定时器，开始获取数据
                if(this.DNSip === '' && this.inputText === '') {    // 如果目标地址为空，也没有输入，则提示输入
                    alert('目标地址不能为空')
                }
                else if(this.inputText !== '') {    
                    this.changeDNSip()          // 如果有输入，则自动将输入存入目标地址
                    if(this.DNSip === '') return ;  // 如果没有存入，说明不合法，不能开始，直接返回
                    this.$store.commit('SWITCH', true)
                    if(this.intervalID === '') {
                        this.queryData()
                        this.intervalID = setInterval(this.queryData , 3000)
                    }
                }
            },
            stopGet(){  //关闭定时器，停止获取数据
                if(this.intervalID !== ''){
                    clearInterval(this.intervalID)
                    this.intervalID = ''
                }
                this.$store.commit('SWITCH', false)
            },
            changeDNSip(){//更改目标ip地址
                this.stopGet() //停止请求
                //1. 检查更改的ip是否合法，即检查 inputText
                var ipv4 = /^((\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))\.){4}$/;
                //2. 合法后更新 DNSip 和 firstTable
                if(ipv4.test(this.inputText + '.')) {
                    this.DNSip = this.inputText
                }
                else{
                    //提示非法ip地址
                    alert(this.inputText + "不是合法的ipv4地址")
                }
                this.inputText = ""
            },
            handleClick(tab, event) {// 触发顶部二级导航栏改变
                // 重置数据
                this.$store.dispatch('queryAllNodes')
                
                // 切换顶部（自动），更新信息（如下）
                if(tab.index === '0') {
                    this.activeTag = 'icmp'
                }
                else if(tab.index === '1') {
                    this.activeTag = 'dns'
                }
                else if(tab.index === '2'){
                    this.activeTag = 'tcp'
                }
                // 停止当前定时器
                this.stopGet()
            },
            cellName({row, column, rowIndex, columnIndex}) { // 用于渲染表格颜色 cell
                if(columnIndex === 1) {
                    if(row.delay < 50) return 'Green1'
                    else if(row.delay < 100) return 'Green2'
                    else if(row.delay < 200) return 'Yellow1'
                    else if(row.delay < 300) return 'Yellow2'
                    else if(row.delay < 400) return 'Yellow3'
                    else if(row.delay < 500) return 'Red1'
                    else return 'Red2'
                }
            },
        },
        // 即将跳转至其它页面前关闭定时器
        deactivated:function() {
            this.stopGet()
        },
        // 即将销毁前关闭定时器
        destroyed:function() {
            this.stopGet()
        }
    };
</script>

<style>
    .LT-body input{
        margin-right:10px;
        margin-top:10px;
    }
    .LT-body-dataShow-control button{
        margin-top: 10px;
    }
    .LT-body-dataShow-control{
        position: absolute;
        margin-left:15px
    }
    h3{
        position: absolute;
        display: inline-block;
        margin-left: 20px;
    }
    .LT-body-dataShow-table{
        height: 500px;
        width: 30%;
        display: inline-block;
        overflow-y: auto;
    }
    #chart{
        height: 500px;
        width: 50%;
        display: inline-block;
    }
    .LT-body-dataShow{
        position: relative;
        width: 100%;
        text-align: center;
        padding-top: 30px;
    }
    .LT-body{
        text-align: center;
        background-color: #FFFFFF;
        background-clip: border-box;
        border: 1px solid #e5e9f2;
        border-radius: 1px;
    }
    .Green1{
        background-color: #00ff00;
    }
    .Green2{
        background-color: #80ff00;
    }
    
    .Yellow1{
        background-color: #ffff00;
    }
    .Yellow2{
        background-color: #ffbf00;
    }
    .Yellow3{
        background-color: #ff8000;
    }
    .Red1{
        background-color: #ff4000;
    }
    .Red2{
        background-color: #ff0000;
    }
</style>