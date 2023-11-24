import Vue from 'vue'
import VueRouter from "vue-router";
import DNSRecordTest from "../components/DNSRecordTest"
import LatencyTest from "../components/LatencyTest"

Vue.use(VueRouter)

export default new VueRouter({
    routes:[{
            path:'/DNSRecordTest',
            component:DNSRecordTest
        },{
            path:'/LatencyTest',
            component:LatencyTest
        }
    ]
})