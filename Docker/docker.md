## Docker命令

##### Docker镜像

```shell
# 显示所有镜像名
docker images
docker image ls
# 查询镜像
docker search 镜像名字
# 下载镜像
docker pull 镜像名:版本(latest，5.7)
# 修改镜tag名称
docker tag 镜像ID mysql:v8.29
# docker打包镜像
docker save -o [要保存文件名] [需要保存的镜像名]
# docker打包多个镜像
docker save -o docker.tar mysql:v5.7 nginx:v2.6.1 mysql:v8.29
# docker save 自定义打包文件存放位置
dcoker save -o /root/docker-images/docker.tar mysql.tar
tar -zcvf mysql.tar.gz mysql.tar

# docker打包并使用gzip压缩
docker save mysql:v5.7 | gzip > mysql.tar.gz
# docker打包并使用gzip压缩到指定目录
docker save mysql:v5.7 | gzip > /root/mysql/mysql.tar.gz

# 删除镜像
docker rmi -f 镜像ID

# 查看已下载的Docker镜像latest具体版本
docker image inspect (docker image名称):latest|grep -i version
# docker image inspect zabbix/zabbix-server-mysql:latest|grep -i version
# "ZBX_VERSION=5.0.1"  ## zabbix-server的镜像版本为5.0.1

# docker查看镜像占用空间 -v:列出详情 
docker system df -v

# 使用sed 拼接命令 借助管道符 交给bash（注意修改成你对应的文件后缀）
ls *.tat|awk '{print $NF}'|sed -r 's#(.*)#sudo docker load -i \1#' |bash

# docker查看网络列表
docker network ls
# 查看网络详情格式：docker network inspect [OPTIONS] NETWORK [NETWORK...]
docker network inspect 204dc15aaeec

# 直接删除带none的镜像，直接报错了。提示先停止容器。
docker stop $(docker ps -a | grep "Exited" | awk '{print $1 }') //停止容器
docker rm $(docker ps -a | grep "Exited" | awk '{print $1 }') //删除容器
docker rmi $(docker images | grep "none" | awk '{print $3}') //删除镜像

# 运行prune命令清理垃圾并释放资源
docker system prune --volumes
docker images prune -a

# 除了 mysql、postgresql、kibana、elastic、mongo 除外的没有在运行的容器会被删除，xargs 的 - t 参数会打印出执行的命令
docker ps -a|egrep -v 'mysql|post|kiban|elas|mongo'|awk '{print $1}'|xargs -t docker rm
# 命令解析
docker ps -a : 列出所有的docker 容器
grep “Exited” : 过滤出所有状态为退出的容器
awk ‘{print $1}’ : 以空格为分割符，打印出第一列的信息
xargs : 将管道传递过来的参数进行处理，依次传递给后面的命令
docker rm : 删除容器
```

##### Docker容器

```shell
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

# 查看一个容器的详情
docker inspect 容器ID | more
docker inspect 容器ID | grep -i version

# 载入容器
docker import new-phpdev.tar phpdev:v1
cat new-phpdev.tar | docker import new-phpdev/phpdev:v1

docker load --import [文件名]
docker load < [文件名]

# 将容器打包为镜像
docker commit <容器ID或名称> <镜像名称>:<标签>

# 例如，如果容器的ID是089464e100a8，我们想将其保存为名为my_image的镜像，并打上latest标签，则可以使用以下命令：
docker commit 089464e100a8 my_image:latest

# 启动容器
docker start 容器ID
# 启动所有的容器命令
docker start $(docker ps -a|awk '{print$1}'|tail -n +2)
# 修改容器为自启
docker update --restart=always 容器ID
# 重启容器
docker restart 容器ID
# 停止容器
docker stop 容器ID
# 强制停止容器
docker kill 容器ID
# 删除容器
docker rm 容器ID
# docker 批量删除状态为退出的容器
docker ps -a|grep "Exited"|awk '{print $1}'|xargs docker rm
docker rm -v $(docker ps --all --quiet --filter 'status=exited')

# Docker容器中文件与本地相互复制拷贝
# 本地到容器
docker cp 本地路径 容器id或者容器名字:容器内路径
# 容器到本地
docker cp 容器id或者容器名字:容器内路径 本地路径

# 查看容器日志，-f 跟踪日志输出，--tail=30 仅列出最新的30条容器日志
docker logs -f --tail=30 容器ID
# 查看容器mysql从2022年5月1日后的最新10条日志
docker logs --since="2022-05-01" --tail=10 mysql
# 导出日志
docker logs 容器ID >> /路径/docker.log
# 指定范围导出
docker logs --since='2023-01-01T00:00:00' --until='2023-02-01T00:00:00'  容器id   >>  存储在宿主机的文件位置

# 查看容器内进程
docker top 容器ID
# 进入容器
docker exec -it 容器ID /bin/bash
docker exec -it 容器ID /bin/sh

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

# 查看容器状态（可以用来查看docker容器的状态（cpu、内存、磁盘IO等））
# 查看所有运行的容器
docker stats

# 查看指定运行的容器
docker stats d6d71fe0e04f
```

##### Docker run

```shell
# 限制内存使用
# 使用--memory或-m标志来指定容器的最大内存使用量。例如，如果你想要限制一个容器最多只能使用512MB的内存
docker run -d --name some-container -m 512M some-image

# 设置CPU核心数量 如果你想直接指定容器可以访问的CPU核心数量，可以使用--cpus参数。例如，分配0.5个CPU核心给容器
docker run -d --name some-container --cpus 0.5 some-image

# 指定可用的CPU核心 可以使用--cpuset-cpus来指定容器可以使用的实际CPU核心列表。例如，只允许容器使用第0号和第1号CPU核心：
docker run -d --name some-container --cpuset-cpus 0,1 some-image

docker run -d --name some-container --cpus 0.5 -m 512M some-image


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

#### Docker可视化web界面管理-Portainer部署

**查询当前有哪些Portainer镜像**

```shell
[root@centos-7 docker-images]# docker search portainer
```

![portainer](..\image\docker\portainer.png)

**拉取Portainer镜像**

```shell
[root@centos-7 install_docker]# docker pull portainer/portainer
Using default tag: latest
latest: Pulling from portainer/portainer
772227786281: Pull complete 
96fd13befc87: Pull complete 
0bad1d247b5b: Pull complete 
b5d1b01b1d39: Pull complete 
Digest: sha256:47b064434edf437badf7337e516e07f64477485c8ecc663ddabbe824b20c672d
Status: Downloaded newer image for portainer/portainer:latest
docker.io/portainer/portainer:latest
```

**Portainer运行方式:**

**单机版运行** -- 运行以下命令就可以启动了:

```shell
[root@centos-7 install_docker]# docker images
REPOSITORY            TAG       IMAGE ID       CREATED        SIZE
portainer/portainer   latest    5f11582196a4   9 months ago   287MB

[root@centos-7 docker-images]# docker run -it -d --name portainer -p 9099:9000 --restart=always -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer
1e52d954082cc6bd4fa4809a4a8cd9011b3ce265717aa9a1396189c43bbdd4b1

[root@centos-7 docker-images]# docker ps -a
CONTAINER ID   IMAGE                 COMMAND        CREATED         STATUS         PORTS                                                           NAMES
1e52d954082c   portainer/portainer   "/portainer"   5 seconds ago   Up 4 seconds   8000/tcp, 9443/tcp, 0.0.0.0:9099->9000/tcp, :::9099->9000/tcp   portainer

[root@centos-7 install_docker]# firewall-cmd --add-port=9099/tcp --permanent && firewall-cmd --reload
success
success
[root@centos-7 install_docker]# 
```

##### *首次登陆需要注册用户，给admin用户设置密码。*
