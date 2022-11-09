## Docker命令

```shell
# 显示所有镜像名
docker images
docker image ls
# 查询镜像
docker search 镜像名字
# 下载镜像
docker pull 镜像名:版本(latest，5.7)
# 删除镜像
docker rmi -f 镜像ID
# 修改镜tag名称
docker tag 镜像ID mysql:v8.29
# docker打包镜像
docker save -o [要保存文件名] [需要保存的镜像名]
# 载入容器
docker import new-phpdev.tar phpdev:v1
cat new-phpdev.tar | docker import new-phpdev/phpdev:v1

docker load --import [文件名]
docker load < [文件名]

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
docker images prune -a

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
docker stop $(docker ps -aq)
systemctl stop docker

# 迁移/var/lib/docker目录下面的文件到/data/docker/lib
# 迁移后的完成docker路径：/data/docker/lib/dockerd
rsync -avz /var/lib/docker/ /data/docker/lib/dockerd

# 配置 /usr/lib/systemd/system/docker.service

vim /usr/lib/systemd/system/docker.service
# docker.service添加如下内容：

[Service]
ExecStart=/usr/bin/dockerd  --graph=/data/docker/lib/dockerd

# 重新加载unit配置文件并重启docker
systemctl daemon-reload
systemctl restart docker

# 确认Docker Root Dir修改是否已经生效
docker info
# 查看docker磁盘占用情况
docker system df
```

```shell
docker run -it nginx:latest /bin/bash

docker run [OPTIONS] IMAGE [COMMAND] [ARG...]    

-d, --detach=false         # 指定容器运行于前台还是后台，默认为false     
-i, --interactive=false    # 打开STDIN，用于控制台交互    
-t, --tty=false            # 分配tty设备，该可以支持终端登录，默认为false    
-u, --user=""              # 指定容器的用户    
-a, --attach=[]            # 登录容器（必须是以docker run -d启动的容器）  
-w, --workdir=""           # 指定容器的工作目录   
-c, --cpu-shares=0         # 设置容器CPU权重，在CPU共享场景使用    
-e, --env=[]               # 指定环境变量，容器中可以使用该环境变量    
-m, --memory=""            # 指定容器的内存上限    
-P, --publish-all=false    # 指定容器暴露的端口    
-p, --publish=[]           # 指定容器暴露的端口   
-h, --hostname=""          # 指定容器的主机名    
-v, --volume=[]            # 给容器挂载存储卷，挂载到容器的某个目录    
--volumes-from=[]          # 给容器挂载其他容器上的卷，挂载到容器的某个目录  
--cap-add=[]               # 添加权限，权限清单详见：http://linux.die.net/man/7/capabilities    
--cap-drop=[]              # 删除权限，权限清单详见：http://linux.die.net/man/7/capabilities    
--cidfile=""               # 运行容器后，在指定文件中写入容器PID值，一种典型的监控系统用法    
--cpuset=""                # 设置容器可以使用哪些CPU，此参数可以用来容器独占CPU    
--device=[]                # 添加主机设备给容器，相当于设备直通    
--dns=[]                   # 指定容器的dns服务器    
--dns-search=[]            # 指定容器的dns搜索域名，写入到容器的/etc/resolv.conf文件    
--entrypoint=""            # 覆盖image的入口点    
--env-file=[]              # 指定环境变量文件，文件格式为每行一个环境变量    
--expose=[]                # 指定容器暴露的端口，即修改镜像的暴露端口    
--link=[]                  # 指定容器间的关联，使用其他容器的IP、env等信息    
--lxc-conf=[]              # 指定容器的配置文件，只有在指定--exec-driver=lxc时使用    
--name=""                  # 指定容器名字，后续可以通过名字进行容器管理，links特性需要使用名字    
--net="bridge"             # 容器网络设置:  
                           # bridge 使用docker daemon指定的网桥       
                           # host    //容器使用主机的网络    
                           # container:NAME_or_ID  >//使用其他容器的网路，共享IP和PORT等网络资源    
                           # none 容器使用自己的网络（类似--net=bridge），但是不进行配置   
--privileged=false         # 指定容器是否为特权容器，特权容器拥有所有的capabilities    
--restart="no"             # 指定容器停止后的重启策略:  
                           # no：容器退出时不重启    
                           # on-failure：容器故障退出（返回值非零）时重启   
                           # always：容器退出时总是重启    
--rm=false                 # 指定容器停止后自动删除容器(不支持以docker run -d启动的容器)    
--sig-proxy=true           # 设置由代理接受并处理信号，但是SIGCHLD、SIGSTOP和SIGKILL不能被代理    
```
