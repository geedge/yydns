import Vue, { del } from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex)
// 本地运行时请将此处改为localhost:8080
axios.defaults.baseURL = process.env.VUE_APP_BASE_URL
// axios.defaults.baseURL = 'http://localhost:8080'
var myMap = new Map()   // 存储一个DNS服务器的映射关系 {key: id, value: {idx, cnt, sum, delay, avgDelay, minDelay}}
var updateSwitch = true   // 更新开关

export default new Vuex.Store({
    actions:{
        queryAllNodes(context) {
            axios.get("/api/allnode").then(
                res => {
                    context.commit('UPDATE_NODES', res.data.nodes)
                }
            ).catch(
                err => {
                    alert(err)
                }
            )
        },
        queryDelay(context, params) {
            axios.get(`/api/delay/${params.type}?ip=${params.ip}`).then(
                res => {
                    console.log(res.data.delay_data)
                    context.commit('UPDATE_DELAY', res.data.delay_data)
                }
            ).catch(
                err => {
                    console.log(err)
                }
            )
        },
    },
    mutations:{
        SWITCH(state, value) {
            updateSwitch = value
        },
        UPDATE_NODES(state, nodeInfo) {
            for(let i = 0; i < nodeInfo.length; i++) {
                nodeInfo[i].avgDelay = '-'
                nodeInfo[i].minDelay = '-'
                nodeInfo[i].delay = 0
                myMap.set(nodeInfo[i].Id, {idx: i, cnt: 0, sum:0, delay: 0, avgDelay: 0, minDelay: 0})
            }
            state.allNodesData = nodeInfo
        },
        UPDATE_DELAY(state, data) {
            if(updateSwitch) {  // 如果可以就更新，否则不更新
                for(let i = 0; i < data.length; i++) {
                    var delay = parseFloat(data[i].CurrDelay)
                    if(!myMap.get(data[i].Id)) {    //如果node里没有这个节点
                        //提示节点有更新，刷新页面
                    }
                    else {
                        var tmp = myMap.get(data[i].Id)
                        var node = state.allNodesData[tmp.idx]
                        // 计算平均时延、最小
                        tmp.cnt += 1
                        tmp.delay = delay
                        tmp.sum += delay
                        if(tmp.sum < 0) {   //是否越界
                            tmp.sum = delay
                            tmp.cnt = 1
                        }
                        if(tmp.minDelay === 0 || tmp.minDelay > delay){
                            tmp.minDelay = delay
                        }
                        tmp.avgDelay = (tmp.sum / tmp.cnt).toFixed(3)
                        //存储
                        myMap.set(data[i].Id, tmp)
                        node.delay = tmp.delay
                        node.avgDelay = tmp.avgDelay
                        node.minDelay = tmp.minDelay
                        state.allNodesData[tmp.idx] = node
                    }
                }
            }else {

            }
        },
    },
    state:{
        allNodesData:[{//展示的数据
            Id: '1',
            Name: '节点1',
            Loc: '上海市普陀区金沙江路 1518',
            Ip:'114.114.114.114',
            port:'',
            delay:'40',
            avgDelay:'30',
            minDelay:'10'
        },],
    }
})