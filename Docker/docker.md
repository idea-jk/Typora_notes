## Docker命令

**基本指令**

| 命令           | 描述               | 示例              |
| -------------- | ------------------ | ----------------- |
| dcoker network | 管理Docker网络     | dcoker network ls |
| docker volume  | 管理Docker卷       | docker volume ls  |
| docker info    | 显示Docker系统信息 | docker info       |
| docker version | 显示Docker版本信息 | docker version    |

**镜像管理指令**

| 命令           | 描述                       | 示例                                                      |
| -------------- | -------------------------- | --------------------------------------------------------- |
| docker images  | 列出本地存储的镜像         | docker images                                             |
| docker pull    | 从仓库拉取一个镜像         | docker pull ubuntu                                        |
| docker push    | 将本地镜像推送到镜像仓库   | docker push ubuntu/ubuntu:tag                             |
| docker rmi     | 删除一个或多个镜像         | docker rmi [IMAGE_ID]                                     |
| dockerbuild    | 从Dockerfile构建镜像       | docker build -t my-image:tag .                            |
| docker history | 显示镜像的历史信息         | docker history myimage                                    |
| docker inspect | 获取容器或镜像的详细信息   | docker inspect [CONTAINER_ID/IMAGE_ID]                    |
| docker tag     | 为镜像添加一个新的标签     | docker tag ubuntu:18.04 myubuntu:latest                   |
| docker save    | 将镜像保存为tar归档文件    | docker save myimage > myimage.tar                         |
| docker load    | 从tar归档文件加载镜像      | docker load < myimage.tar<br />docker load -i myimage.tar |
| docker import  | 从归档文件创建镜像         | docker import mycontainer.tar myimage                     |
| docker commit  | 从修改过的容器创建新的镜像 | docker commit [CONTAINER_ID] new-image                    |
| docker diff    | 显示容器文件系统的更改     | docker diff mycontainer                                   |
| docker search  | 在Docker Hub搜索镜像       | docker search ubuntu                                      |

```shell
docker save -o [要保存文件名] [需要保存的镜像名]
# docker打包多个镜像
docker save -o docker.tar mysql:v5.7 nginx:v2.6.1 mysql:v8.29
# docker save 自定义打包文件存放位置
dcoker save -o /root/docker-images/docker.tar mysql.tar

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

**容器管理命令**

| 命令           | 描述                                  | 示例                                         |
| -------------- | ------------------------------------- | -------------------------------------------- |
| docker run     | 创建并启动一个容器                    | docker run -it ubuntu /bin/bash              |
| docker ps      | 列出当前运行的容器                    | docker ps                                    |
| docker ps -a   | 列出所有容器，包括未运行的            | docker ps -a                                 |
| docker stop    | 停止一个运行中容器                    | docker stop [CONTAINER_ID]                   |
| docker start   | 启动一个已停止的容器                  | docker start [CONTAINER_ID]                  |
| docker restart | 重启容器                              | docker restart [CONTAINER_ID]                |
| docker kill    | 立即终止容器的运行                    | docker kill [CONTAINER_ID]                   |
| dcoker rm      | 删除一个或多个容器                    | docker rm [CONTAINER_ID]                     |
| docker exec    | 在运行的容器中执行命令                | docker exec -it [CONTAINER_ID] bash          |
| docker attach  | 连接到正在运行的容器                  | docker attach [CONTAINER_ID]                 |
| docker cp      | 从容器中复制文件/目录到主机，反之亦然 | docker cp [CONTAINER_ID]:/path/to/file /dest |
| docker logs    | 获取容器日志                          | docker logs [CONTAINER_ID]                   |
| docker inspect | 获取容器的详细信息                    | docker inspect [CONTAINER_ID]                |

```shell
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

# 查看容器大小,输出结果中SIZE列显示了每个容器的磁盘使用情况
docker ps -s

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
# 限制容器的CPU与内存使用

# 指定可用的CPU核心 可以使用--cpuset-cpus来指定容器可以使用的实际CPU核心列表。例如，只允许容器使用第0号和第1号CPU核心：
docker run -d --name some-container --cpuset-cpus 0,1 some-image

# 分配0.5个CPU核心给容器，限制容器最多只能使用512MB的内存
docker run -d --name some-container --cpus 0.5 -m 512M some-image
```

##### Docker镜像构建

```shell
# 语法
docker build [OPTIONS] PATH | URL | -

PATH: 包含 Dockerfile 的目录路径或 .（当前目录）。
URL: 指向包含 Dockerfile 的远程存储库地址（如 Git 仓库）。
-: 从标准输入读取 Dockerfile。
常用选项：

-t, --tag: 为构建的镜像指定名称和标签。
-f, --file: 指定 Dockerfile 的路径（默认是 PATH 下的 Dockerfile）。
--build-arg: 设置构建参数。
--no-cache: 不使用缓存层构建镜像。
--rm: 构建成功后删除中间容器（默认开启）。
--force-rm: 无论构建成功与否，一律删除中间容器。
--pull: 始终尝试从注册表拉取最新的基础镜像。
更多选项说明：

--build-arg=[]: 设置构建镜像时的变量。
--cpu-shares: 设置 CPU 使用权重。
--cpu-period: 限制 CPU CFS 周期。
--cpu-quota: 限制 CPU CFS 配额。
--cpuset-cpus: 指定可使用的 CPU ID。
--cpuset-mems: 指定可使用的内存节点 ID。
--disable-content-trust: 忽略内容信任验证（默认启用）。
-f: 指定 Dockerfile 的路径。
--force-rm: 强制在构建过程中删除中间容器。
--isolation: 使用指定的容器隔离技术。
--label=[]: 设置镜像的元数据。
-m: 设置内存的最大值。
--memory-swap: 设置交换空间的最大值（内存 + 交换空间），-1 表示不限制交换空间。
--no-cache: 构建镜像时不使用缓存。
--pull: 尝试拉取基础镜像的最新版本。
--quiet, -q: 安静模式，构建成功后只输出镜像 ID。
--rm: 构建成功后删除中间容器（默认启用）。
--shm-size: 设置 /dev/shm 的大小，默认值为 64M。
--ulimit: 设置 Ulimit 配置。
--squash: 将 Dockerfile 中所有步骤压缩为一层。
--tag, -t: 为镜像指定名称和标签，格式为 name:tag 或 name；可以在一次构建中为一个镜像设置多个标签。
--network: 在构建期间设置 RUN 指令的网络模式，默认值为 default。

# 1、构建镜像
# 这会从当前目录读取 Dockerfile 并构建一个名为 myimage:latest 的镜像。
docker build -t myimage:latest .

# 2、指定 Dockerfile 路径
# 这会从 /path/to/ 目录读取 Dockerfile 并构建一个名为 myimage:latest 的镜像。
docker build -f /path/to/Dockerfile -t myimage:latest .

# 3、设置构建参数
# 这会在构建过程中使用 HTTP_PROXY 环境变量。
docker build --build-arg HTTP_PROXY=http://proxy.example.com -t myimage:latest .

# 4、不使用缓存层构建镜像
# 这会在构建镜像时忽略所有缓存层，确保每一步都重新执行。
docker build --no-cache -t myimage:latest .


# 实例 - 使用 Dockerfile 构建镜像
# 1、创建 Dockerfile，内容如下：

# Dockerfile 示例
FROM ubuntu:20.04
LABEL maintainer="yourname@example.com"
RUN apt-get update && apt-get install -y nginx
COPY index.html /var/www/html/index.html
CMD ["nginx", "-g", "daemon off;"]
# 2、构建镜像

docker build -t mynginx:latest .


# docker buildx build 构建linux/arm64架构镜像
docker buildx build --platform linux/arm64,linux/amd64 -f /root/HivisionIDPhotos/Dockerfile -t hivision_idphotos:1.2.9 .

# docker buildx build 构建linux/amd64架构镜像
docker buildx build --platform linux/arm64 -f /root/HivisionIDPhotos/Dockerfile -t hivision_idphotos:1.2.9 .


-------------------------------------------------------------------------------------------------------
# docker buildx 离线安装
mkdir -pv /usr/local/lib/docker/cli-plugins
mv buildx-v0.17.1.linux-amd64 /usr/local/lib/docker/cli-plugins/docker-buildx
chmod +x /usr/local/lib/docker/cli-plugins/docker-buildx

# 如果想让其在系统级别可用，可将其拷贝至如下路径：
/usr/local/lib/docker/cli-plugins OR /usr/local/libexec/docker/cli-plugins
/usr/lib/docker/cli-plugins OR /usr/libexec/docker/cli-plugins
-------------------------------------------------------------------------------------------------------
# 安装模拟器的主要作用是让buildx支持跨CPU架构编译。
# 模拟器对应的仓库名称是：tonistiigi/binfmt:latest ，如果你的环境能联网，使用一下命令：
docker run --privileged --rm tonistiigi/binfmt --install all

# 如果你的环境不能联网，则需先在外网环境下载好镜像，导入内网之后，再安装：
# 外网下载镜像，注意（如果你的内网环境机器是arm架构，就下载arm版本，如果你的内网环境机器是amd架构，就下载amd版本；这里我下载的是arm版本）
docker pull tonistiigi/binfmt:latest@sha256:01882a96113f38b1928a5797c52f7eaa7e39acf6cc15ec541c6e8428f3c2347d
# 导出镜像
docker save -o tonistiigi_binfmt_arm64.tar f1d8c13be37e
# 在内网机器执行如下命令，导入镜像
docker load -i tonistiigi_binfmt_arm64.tar
# 安装模拟器
docker run --privileged --rm tonistiigi/binfmt --install all

# 验证是否安装成功
docker buildx ls 
default       docker
  default     default    running   linux/amd64, linux/arm64, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/arm/v7, linux/arm/v6

# 验证arm机器上的amd模拟器是否安装成功，则执行如下命令，输出结果包含enable即可
cat /proc/sys/fs/binfmt_misc/qemu-x86_64
enabled

# 如果你是amd机器，需要验证arm模拟器是否安装成功，则执行如下命令，输出结果包含enable即可
cat /proc/sys/fs/binfmt_misc/qemu-aarch64
enabled
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
