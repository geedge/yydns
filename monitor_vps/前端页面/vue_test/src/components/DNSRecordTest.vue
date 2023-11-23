<template>
  <!-- 此处注意高度和宽度 -->
  <div class="body">
    <div class="body-div">
      <!-- 左边的选择、输入框等 -->
      <div class="body-div-left">
        <h3>目标地址：{{ DNSip }}</h3>
        <!-- <span style="visibility: hidden;">------</span> -->
        <div style="padding-left: 40px; margin-top: 40%">
          <div>
            <span> 待解析域名：</span><span style="visibility: hidden">-</span>
            <el-input
              v-model="url"
              style="width: 60%; padding-left: 2px"
              size="medium"
              placeholder="请输入域名，如baidu.com"
            >
            </el-input>
          </div>
          <div style="padding-top: 20px">
            <span> DNS服务器： </span>
            <el-select
              @change="selectChange"
              style="width: 60%"
              size="medium"
              v-model="value"
              placeholder="请选择DNS服务器"
            >
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
          </div>
          <div style="width: 100%; text-align: center; padding-top: 20px">
            <el-button type="primary" @click="Visit" :disabled="isClick">浏览器测试访问</el-button>
          </div>
        </div>
      </div>

      <!-- 右边的 iframe -->
      <div class="body-div-right">
        <h3 style="margin-left: 0px; padding-left: 0px; margin-top: 20px">浏览器访问结果</h3>
        <iframe v-show="correctVisble" v-bind:src="src" ref="correctPage"></iframe>
        <iframe v-show="!correctVisble" v-bind:srcDoc="srcDoc" ref="errorPage"> </iframe>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DNSRecordTest",
  data() {
    return {
      DNSip: "请选择",
      srcDoc: "", // 出现错误时，此页面展示错误信息
      correctVisble: true, // correctPage和errorPage同时只能展现一个，用此变量控制
      options: [{
          value: 0,
          label: "8.8.8.8",
        },{
          value: 1,
          label: "114.114.114.114",
        },{
          value: 2,
          label: "223.5.5.5",
        },{
          value: 3,
          label: "119.29.29.29",
        },
      ],
      url: "",
      protocol: "", 
      domain: "", // 输入的域名
      port: "",
      uri: "",
      ipArr: "", //解析后的ip地址数组
      value: "", //选择框选中的 value, 从 0 开始的 index
      src:"",
    };
  },
  computed: {
    isClick: function () {
      if (this.value !== "") {
        return !true;
      }
      return !false;
    },
  },
  mounted: function () {
    //设置选项
    // this.setOptions(this.allNodesData)
  },
  methods: {
    setOptions(tableData) {
      //设置下拉框选项
      var tp_options = [];
      for (let i = 0; i < tableData.length; i++) {
        var val = i;
        var lab = "节点" + tableData[i].Id + "/ " + tableData[i].Loc;
        tp_options.push({ value: val, label: lab});
      }
      this.options = tp_options;
    },
    checkURL() {
      //初始化
      this.protocol = this.domain = this.port = this.uri = ""
      // 开始分解
      var arr = this.url.split('/')
      var begin = 0   //uri在arr中第 begin + 1个开始
      // 分解出协议
      if(arr[0].charAt(arr[0].length-1) === ':') {  // 第一部分带 : 说明带协议
        this.protocol = arr[0].split(':')[0]
        this.domain = arr[2]
        begin = 3
      }
      else {
        this.protocol = 'http' // 否则，默认 http协议
        this.domain = arr[0]
        begin = 1
      }
      // 分解出uri
      for( ; begin < arr.length; begin ++) {
        this.uri += '/' + arr[begin]
      }
      // 分解出端口号  如果有则用，没有则默认为空
      arr = this.domain.split(':')
      if(arr.length === 2) {
        this.domain = arr[0]
        this.port = arr[1]
      }
      else {
        this.domain = arr[0]
      }
    },
    selectChange(value) {
      this.DNSip = this.options[value].label;
    },
    // 访问测试
    Visit() {
      this.checkURL()
      axios.defaults.baseURL = process.env.VUE_APP_BASE_URL
      // axios.defaults.baseURL = 'http://localhost:8080'
      axios.get(`/api/check/?rev=${this.DNSip}&domain=${this.domain}&qtype=A`).then(
        response => {
          this.correctVisble = true
          console.log(response.data.ans);
          this.ipArr = response.data.ans
          this.src = this.protocol + '://' + this.domain + ':' + this.port + this.uri
        }
      ).catch(
        err => {
          this.correctVisble = false
          console.log(err)
          this.srcDoc = err.response.data
        }
      )
    },
  },
};
</script>

<style scoped>
h3 {
  position: initial;
  padding-left: 20px;
}
.body {
  text-align: center;
  position: absolute;
  height: 90%;
  width: 96%;
  background-color: #ffffff;
}
.body-div {
  height: 100%;
  text-align: left;
  background-clip: border-box;
  border: 2px solid #e5e9f2;
  border-radius: 2px;
}
iframe {
  height: 85%;
  width: 95%;
  border: black 2px solid;
}
.body-div-left {
  display: inline-block;
  height: 100%;
  width: 30%;
  vertical-align: top;
}
.body-div-right {
  display: inline-block;
  height: 100%;
  width: 70%;
}
</style>
