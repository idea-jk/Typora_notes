## Docker命令

```shell
# 显示所有镜像名
docker images
docker image ls
# 查询镜像
docker search 镜像名字
# 下载镜像
docker pull 镜像名:版本(lates，5.7)
# 删除镜像
docker rmi -f 镜像ID
# 修改镜tag名称
docker tag 镜像ID mysql:v8.29
# 载入容器
docker import new-phpdev.tar phpdev:v1

# 使用sed 拼接命令 借助管道符 交给bash（注意修改成你对应的文件后缀）
ls *.tat|awk '{print $NF}'|sed -r 's#(.*)#sudo docker load -i \1#' |bash

# docker查看镜像占用空间 -v:列出详情 
docker system df -v
# docker查看网络列表
docker network ls
# 查看网络详情格式：docker network inspect [OPTIONS] NETWORK [NETWORK...]
docker network inspect 204dc15aaeec

# 显示当前正在运行的容器
docker ps
# 显示所有容器
docker ps -a
# 列出最近创建的2个容器信息
docker ps -a -n 2
# 根据名称过滤
docker ps --filter"name=test-nginx"
# 根据状态过滤，STATUS: 容器状态有7种：
created（已创建）
restarting（重启中）
running（运行中）
removing（迁移中）
paused（暂停）
exited（停止）
dead（死亡）
docker ps -a --filter 'exited=0'
docker ps --filter status=running      // docker ps -a -f status=running
docker ps --filter status=paused


# 启动容器
docker start 容器ID
# 启动所有的容器命令
docker start $(docker ps -a|awk '{print$1}'|tail -n +2)
# 重启容器
docker restart 容器ID
# 停止容器
docker stop 容器ID
# 强制停止容器
docker kill 容器ID
# 删除容器
docker rm 容器ID
docker rm -rf 容器ID
# docker 批量删除状态为退出的容器
docker ps -a|grep "Exited"|awk '{print $1}'|xargs docker rm
docker rm -v $(docker ps --all --quiet --filter 'status=exited')

# 除了 mysql、postgresql、kibana、elastic、mongo 除外的没有在运行的容器会被删除，xargs 的 - t 参数会打印出执行的命令
docker ps -a|egrep -v 'mysql|post|kiban|elas|mongo'|awk '{print $1}'|xargs -t docker rm
# 命令解析
docker ps -a : 列出所有的docker 容器
grep “Exited” : 过滤出所有状态为退出的容器
awk ‘{print $1}’ : 以空格为分割符，打印出第一列的信息
xargs : 将管道传递过来的参数进行处理，依次传递给后面的命令
docker rm : 删除容器


# 查看容器日志，-f 跟踪日志输出，--tail=30 仅列出最新的30条容器日志
docker logs -f --tail=30 容器ID
# 查看容器mysql从2022年5月1日后的最新10条日志
docker logs --since="2022-05-01" --tail=10 mysql

# 运行prune命令清理垃圾并释放资源
docker system prune --volumes

# 查看容器内进程
docker top 容器ID
# 进入容器
docker exec -it 容器ID /bin/bash

# docker容器时间同步物理机时间
# 运行时添加如下参数
docker run -it -v /etc/localtime:/etc/localtime:ro
# 正在运行的容器，时间同步
docker cp -L /usr/share/zoneinfo/Asia/Shanghai  容器ID:/etc/localtime


# docker修改默认存储路径
# 在linux下通常docker都是默认安装的，且默认的镜像，容器存储路径都位于/var/lib/docker中，可以通过docker info命令来查看

# 迁移/var/lib/docker目录下面的文件到/data/docker/lib
# 迁移后的完成docker路径：/data/docker/lib/docker
rsync -avz /var/lib/docker/ /data/docker/lib/

# 配置 /etc/systemd/system/docker.service.d/devicemapper.conf
# 查看/etc/systemd/system/docker.service.d目录及devicemapper.conf是否存在。如果不存在，就新建

mkdir -p /etc/systemd/system/docker.service.d/
vi /etc/systemd/system/docker.service.d/devicemapper.conf

# devicemapper.conf添加如下内容：

[Service]
ExecStart=
ExecStart=/usr/bin/dockerd  --graph=/data/docker/lib/docker

systemctl daemon-reload
systemctl restart docker

# 确认Docker Root Dir修改是否已经生效
docker info
```

