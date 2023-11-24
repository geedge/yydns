## BIND9安装

### 包管理器安装

执行`yum install bind bind-utils`安装BIND9

### 容器安装

在安装了docker的服务器上执行以下命令。

    docker run -d --name bind9-container \
        -e TZ=UTC -p 0.0.0.0:5353:53/udp -p 0.0.0.0:5353:53/tcp \
        ubuntu/bind9:9.18-22.04_beta