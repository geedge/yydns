const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave:false,
  // 开启代理服务器
  devServer:{
    proxy:{
      '/api':{
        target: 'http://124.221.228.62:2525',
        pathRewrite:{'^/api':''},
        ws: true,
        changeOrigin: true
      },
      '/DNSProxy':{
        target: 'http://localhost:8888',
        pathRewrite:{'^/DNSProxy': ''},
        ws: true,
        changeOrigin: true
      }
    }
  }
})
