#### MySQL 数据库异地备份脚本

该脚本主要是用于在`Linux`系统上备份`MySQL`数据库，自定义数据库用户名、密码、IP 地址、远程备份服务器 IP、本地备份路径、远程备份路径、当前时间、7 天前的日期变量。

使用`mkdir -p`命令创建以当前日期为名的目录，存放数据库备份文件。

使用`mysqldump`命令备份所有数据库，并将输出重定向至`mysql_backup_$DATE.sql`文件中。

使用`tar`命令将备份文件压缩为：`.tar.gz`格式的文件内，并附加日志到备份文件中，然后删除原始的备份文件。

使用`rm -rf`命令删除 7 天前的备份文件，删除的是以 7 天前日期为名的目录和目录下的所有文件。

使用`scp`命令将本地备份文件传到远程备份服务器上。

```shell
#!/bin/bash
# Database info
DB_USER="root"                          # 数据库备份用户
DB_PASS="1Q!2W@3E#"                     # 备份用户密码
DB_HOST="192.168.1.100"                 # 数据库 IP
DBBACK_IP="192.168.1.200"               # 远程备份服务器 IP
BCK_DIR="/bigdata/mysql"                # 本地备份路径
DBBACK_PATH=/bigdata/mysqlbackup        # 远程备份路径
DATE=`date +%F`                         # 获取当前时间
yestoday=$(date -d '-7 day' +%Y-%m-%d)  # 取 7 天前的时间，格式为：2023-12-30，用于删除备份文件取文件时间，该参数可自行调整

#BACK_NAME="db_$var.sql"
#TB_NAME=("" "" "" "" "")               # 需要备份的表名

#create file

mkdir -p $BCK_DIR/$DATE                 # 创建本地备份日期目录
echo "开始本地备份中..."

/usr/local/mysql/bin/mysqldump -u$DB_USER -p$DB_PASS -h$DB_HOST --all-databases > $BCK_DIR/$DATE/mysql_backup_$DATE.sql
cd $BCK_DIR/$DATE && tar -zcvf mysql_backup_$DATE.sql.tar.gz mysql_backup_$DATE.sql >>/$BCK_DIR/$DATE/$DATE.log && rm -fr mysql_backup_$DATE.sql
echo "$DATE db bakcup success！" >>/$BCK_DIR/$DATE/$DATE.log

echo "开始删除 7 天前的数据库备份文件..."
rm -rf $BCK_DIR/$yestoday
echo "7 天前的数据库备份文件删除完毕！"

echo "开始远程备份中..."
scp -r $BCK_DIR/$DATE/mysql_backup_$DATE.sql.tar.gz root@$DBBACK_IP:$DBBACK_PATH
echo "远程备份完毕！"
```

需要注意的是：远程备份需要做免密，在`MySQL`数据库所在服务器与需要远程备份的服务器做免密，并进行`ssh`验证登录是否正常。

```shell
ssh-keygen
cd ~/.ssh/
scp id_rsa.pub 目标主机IP：~/.ssh/authorized_keys
```

利用`find`命令查找`mysqldump`工具安装路径，并按实际路径更改脚本中的参数。

```shell
find / -name mysqldump
```

给`mysql_backup.sh`脚本增加可执行权限，并创建`crontab`定时任务。

```shell
chmod +x mysql_backup.sh

crontab -e
# MySQL 数据库备份
0 3 * * 6 root sh /bigdata/mysql_backup.sh >> /bigdata/mysql_backup.log 2>&1 &
```

#### MySQL 数据库的恢复

首先确保已安装好`MySQL`数据库

可使用以下语法命令从`.sql`文件中恢复`MySQL`数据库

```shell
mysql -u [用户名] -p [密码] [数据库名] < [备份文件名.sql]
```