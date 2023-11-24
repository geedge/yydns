import Vue from 'vue'
import App from './App.vue'
import router from './router/index'
import store from './store/index'

import 'element-ui/lib/theme-chalk/index.css'
import './assets/theme/purpleTheme.scss'
import ElementUI from 'element-ui'

//使用插件
Vue.use(ElementUI)

// 关闭生产提示
Vue.config.productionTip = false

// 存了一个ip，应该修改的更符合标准
// window.DNSip = '114.114.114.114'

// 创建 vm
const vm = new Vue({
    router,
    store,
    el:'#app',
    render: h => h(App),
    beforeCreate() {
        Vue.prototype.$bus = this // 创建全局事件总线，供组件间信息交流
    }
})