<template>
    <div>
        <el-container>
            <el-header>
                <div class="home" style="width: 100%;">
                <div class="line"></div>
                <el-menu
                    :default-active="activeIndex2"
                    class="el-menu-demo" 
                    mode="horizontal" 
                    @select="handleSelect"
                    background-color="#6861ce" 
                    text-color="#fff"
                    active-text-color="#ffd04b" :router="true">
                    <el-menu-item index="/shouye" disabled>
                        <img src="./assets/logo.png" 
                            class="icon" data-v-204a8542="" style="width: 40px; height: 40px;">
                            
                    </el-menu-item>
                    <el-menu-item index="/LatencyTest">目标时延</el-menu-item>
                    <el-menu-item index="/DNSRecordTest" >应答内容</el-menu-item>
                    
                    </el-menu>
                    
                </div>
            </el-header>
            <el-main>
                <keep-alive>
                    <router-view></router-view>
                </keep-alive>
            </el-main>
            <!-- <el-footer>
                <FooterTable></FooterTable>
            </el-footer> -->
        </el-container>
        
    </div>
</template>

<script>
import DNSRecordTest from './components/DNSRecordTest.vue';
import LatencyTest from './components/LatencyTest.vue';
import FooterTable from './components/FooterTable.vue'

export default ({
    name: 'App',
    data() {
        return {
            activeIndex2:'/shouye', // 默认打开的路由
        }
    },
    components:{
        LatencyTest,
        DNSRecordTest,
        FooterTable,
    },
    mounted:function(){ //组件挂载完毕后执行
        this.$router.push({ //重复了
            path:'/LatencyTest'
        }).catch(err=>{
            console.log("此处存在重复路由问题，", err.message)
        })
    },
    methods:{
        handleSelect(key, keyPath) { //此方法目前只进行了页面跳转
            console.log('选中顶部导航栏应该执行的动作', key, keyPath)
        }
    }
})

</script>

<style>
    
</style>