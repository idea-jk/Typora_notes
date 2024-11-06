# Linux常用命令

##### mkdir用大括号同时建立多个同级和下级目录

```shell
# 1.在当前目录下创建a  b   c三个目录.
mkdir –p {a,b,c}

# 2.在当前目录下创建father目录，并在father目录下创建child1   child2   child3三个子目录。
mkdir -p father/{child1,child2,child3}

# 3.在当前目录下创建father1  father2两个目录，并在这两个目录下分别创建child1   child2   child3三个子目录。
mkdir -p {father1,father2}/{child1,child2,child3}
```

##### 复制与移动命令

```shell
cp:复制文件或目录
# 例: cp -rp ./mydir /home
-r 代表递归复制目录下的文件
-p 代表不改变原有属性，例如权限以上命令意为：把当前目录下mydir目录复制到/home目录下

mv:移动文件或重命名
# 例: mv file ./home 把当前目录下的file文件移动到home目录下
# 例: mv file file_back 把当前目录的file文件重命名为file_back
```



## 搜索命令

#### find

```shell
# 根据 文件或目录名称 搜索

# find 【搜索目录】【-name或者-iname】【搜索字符】：-name和-iname的区别一个区分大小写，一个不区分大小写
# init精准搜索，名字必须为 init 才能搜索的到
find /etc -name init

# 精准搜索，名字必须为 init或者有字母大写也能搜索的到
find /etc -iname init

# 模糊搜索，以 init 结尾的文件或目录名
find /etc -name *init

# 模糊搜索，？ 表示单个字符，即搜索到 init___
find /etc -name init???
```

#### grep

```shell
# 【模糊匹配 】输出行号

# 输出内容同时输出行号
grep -n "要匹配的字符串" 文件名

# 输出行号，并不输出内容
# 注意是单引号
awk '/要匹配字符串/{print NR}' 文件名





# 【精确匹配（全匹配）】输出行号

grep -wn "要匹配的字符串" 文件名

# 其中 grep -w 是完全匹配要匹配的字符串，字符串只是字段内一部分也可以匹配。比如
# 结果为abcd, abcde, abc等
grep "abc" 
# 结果为abc
grep -w "abc" 

# awk并不能像grep那样去过滤单词。grep可以过滤到单词，awk只能过滤到字段。
# 匹配以逗号为分隔（如csv）的第三列/第三个字段，打印行号
awk -F, '$3=="要匹配的字符串" {print NR}' 文件名

# 匹配以逗号为分隔（如csv）的第三列/第三个字段
# 打印该行内容 写{print}或{print $0} 都可以
awk -F, '$3=="要匹配的字符串" {print}' 文件名
```

#### whereis

```shell
whereis nginx
```

#### 查看linux 用户登录信息及IP

```shell
# 查看可疑IP登陆
last -f /var/log/wtmp
# 寻找可疑ip登陆次数及信息
cat /var/log/secure

# 查看当前登陆用户
who
-h # 忽略头文件信息
-u # 显示结果的加载时间
```

#### 查看Linux资源命令



![20230521170205](D:\me\Typora_notes\image\Linux\20230521170205.png)

总核数 = 物理CPU个数 X 每颗物理CPU的核数

总逻辑CPU数 = 物理CPU个数 X 每颗物理CPU的核数 X 超线程数

\# 查看物理CPU个数

```shell
cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l
```

\# 查看每个物理CPU中core的个数(即核数)

```shell
cat /proc/cpuinfo| grep "cpu cores"| uniq
```

\# 查看逻辑CPU的个数

```shell
cat /proc/cpuinfo| grep "processor"| wc -l
```

\# 查看CPU信息（型号）

```shell
cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c
```

\# 如何查看Linux 内核

```shell
uname -a
cat /proc/version
```

\# 查看内存情况

```shell
free -m
free -g
```

-m  以MB为单位来显示服务器的内存

-g    以GB为单位来显示服务器的内存

-h   以合理单位来显示服务器的内存

#### Linux解压压缩

##### 一、分卷压缩

##### **方式一： 先压缩、再分卷**

将service压缩为service.tar.gz

```shell
tar -zcvf service/* service.tar.gz
tar zcvf service.tar.gz service/*

**参数说明：**
-c, --create 创建一个新归档
-v, --verbose 详细地列出处理的文件
–warning=KEYWORD 警告控制:
-f, --file=ARCHIVE 使用归档文件或 ARCHIVE 设备
–force-local 即使归档文件存在副本还是把它认为是本地归档
-z, --gzip, --gunzip, --ungzip 通过 gzip 过滤归档
```



**将service.tar.gz包分卷切割成100M大小、以service为开头的包**

```shell
split -b 100m -d service.tar.gz service

**参数说明：**

-b<字节> : 指定多少字节切成一个小文件
-d : 使用数字后缀而不是字母
```



##### 方式二（推荐）：一步压缩+分卷

将service打包，并分割为100m大小的包，分割后的文件名以service为开头，service00、service01、service02…

```shell
tar cvzf - service/* | split -b 100m -d - service

**参数说明：**

| ：竖杠为管道命令
-：中间的横杠表示输出流，在采用管道命令竖杠时需要用到。
```



##### 二、分卷解压缩

1.先合卷，将service*等分卷文件合并为service.tar.gz

```shell
cat service* > service.tar.gz
```

2.解压缩

```shell
tar -zxvf servcie.tar.gz

**参数说明**：
-x, --extract, --get 从归档中解出文件
```

##### Linux挂载磁盘

```shell
# 查看各个盘的大小和分区信息
fdisk -l
# 查看磁盘挂载
lsblk
# 创建data文件夹
mkdir -pv /data

# 格式化磁盘，格式化磁盘格式为ext4
mkfs.ext4 /dev/sdb
mkfs -t ext4 /dev/sdb
mkfs -V -t ext4 /dev/sdb

mkfs [-V] [-t fstype] [fs-options] file sys [blocks]
-V 详细显示模式
-t 给定档案系统的型式，Linux下预设值为ext2
-c 在制做档案前，检查partition是否有坏轨
-l bad_blocks_file 将有坏轨的block资料加到bad_blocks_file里面
block 给定block的大小

# 挂载磁盘
mount /dev/sdb /data
# 将挂载信息执行开机自启动(只能执行一次)
cat /etc/mtab | grep /data >> /etc/fstab
# 查看磁盘挂载
lsblk
```

##### yum命令

```shell
# 将yum下载的包保存到本地
# 例如，将 policycoreutils-python 下载到 /root/gitlab/packages/
yum install -y --downloadonly --downloaddir=/root/gitlab/packages/ policycoreutils-python

# 修改yum源(CentOS 7)
# 阿里云开源镜像站
wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
# 网易开源镜像站
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.163.com/.help/CentOS7-Base-163.repo
# 生成缓存
yum clean all && yum makecache
```

#### du

```shell
du -sh : 查看当前目录总共占的容量，而不单独列出各子项占用的容量；
du -sh ./* : 单独列出各子项占用的容量。

# 以上命令需要在root权限下操作，或者在命令行前加sudo命令也可以。

# 用到了两个参数来控制命令du：

-h：以K，M，G为单位，提高信息的可读性
-s：仅显示总计

# 查看磁盘剩余空间
# 利用df命令

df -hl [目录名] ：查看磁盘剩余空间

其他
du命令的一些常用参数:
-a或-all 显示目录中个别文件的大小
-b或-bytes 显示目录或文件大小时，以byte为单位
-c或–total 除了显示个别目录或文件的大小外，同时也显示所有目录或文件的总和
-D或–dereference-args 显示指定符号连接的源文件大小
-h或–human-readable 以K，M，G为单位，提高信息的可读性
-k或–kilobytes 以1024 bytes为单位
-l或–count-links 重复计算硬件连接的文件
-L或–dereference 显示选项中所指定符号连接的源文件大小
-m或–megabytes 以1MB为单位
-s或–summarize 仅显示总计
-S或–separate-dirs 显示个别目录的大小时，并不含其子目录的大小
-X<文件>或–exclude-from=<文件>
–exclude=<目录或文件> 略过指定的目录或文件
–max-depth=<目录层数> 超过指定层数的目录后，予以忽略
```

```shell
# 查询到本机/本网络所在的 IP 地址
curl ping0.cc/geo
curl ipinfo.io
```

#### 查看系统/服务器运行时间

```shell
uptime

# uptime命令能够打印系统总共运行了多长时间和系统的平均负载。
# uptime命令可以显示的信息显示依次为：现在时间、系统已经运行了多长时间、目前有多少登陆用户、系统在过去的1分钟、5分钟和15分钟内的平均负载。

w

# w命令用于显示已经登陆系统的用户列表，并显示用户正在执行的指令。执行这个命令可得知目前登入系统的用户有那些人，以及他们正在执行的程序。
# 单独执行w命令会显示所有的用户，您也可指定用户名称，仅显示某位用户的相关信息。
```

