<template>
    <div class="body">
        <el-table
            :data="allNodesData" style="width: 100%;">
            <el-table-column
                prop="Id"
                label="节点ID"
                min-width="20">
            </el-table-column>
            <el-table-column
                prop="Name"
                label="节点名称"
                min-width="20">
            </el-table-column>
            <el-table-column
                prop="Loc"
                label="地理位置"
                min-width="20">
            </el-table-column>
            <el-table-column
                prop="Ip"
                label="IP地址"
                min-width="20">
            </el-table-column>
            <el-table-column
                prop="delay"
                label="实时时延/ms"
                min-width="20">
            </el-table-column>
            <el-table-column
                prop="avgDelay"
                label="平均时延/ms"
                min-width="20">
            </el-table-column>
            <el-table-column
                prop="minDelay"
                label="最小时延/ms"
                min-width="20">
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default ({
    name:'FooterTable',
    computed:{
        ...mapState({allNodesData:"allNodesData"})
    },
})
</script>

<style scoped>
    .body{
        padding: 40px;
        background-color: #FFFFFF;
        background-clip: border-box;
        border: 1px solid #e5e9f2;
        border-radius: 1px;
    }
</style>
