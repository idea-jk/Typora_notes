#### PostgreSQL 数据库异地备份脚本

该脚本是备份`PostgreSQL`数据库并将备份文件传输到远端备份服务器上。首先，使用`date`命令获取了今天的日期、当前时间点和 7 天前的日期，分别赋给了`today`、`nowtime`和`yestoday`变量。

定义了本机 IP 地址、远端备份服务器 IP、PostgreSQL 数据库的端口号、数据库用户名和密码，分别赋给了`host_ip`、`backup_ip`、`port_id`、`username`和`export PGPASSWORD`变量。

指定了本地备份目录和远端备份目录，分别赋给了`dmpDir`和`destination`变量。

使用`pg_dumpall`命令来备份整个`PostgreSQL`数据库，并将备份文件保存在本地备份目录中。备份完成后，对备份文件进行了压缩。使用`scp`命令将压缩后的备份文件传输到远端备份服务器上的指定目录。

最后，输出备份和传输的相关信息，并结束脚本的执行。

```shell
#!/bin/bash
#Description：备份 PostgreSQL 数据库必能压缩成 gz 文件，最后删除 3 天前的备份文件。

echo "开始执行 PostgreSQL 数据库的备份..."
echo "backup ing..."
today=$(date +%Y-%m-%d)                       # 今天的日期
nowtime=$(date +%F+%T)                        # 当前时间点
yestoday=$(date -d '-7 day' +%Y-%m-%d)        # 7天前的日期
host_ip=127.0.0.1                             # 本机 IP 地址
backup_ip=192.168.1.111                       # 远端备份服务器 IP
port_id=5432                                  # 端口号，PostgreSQL默认的端口号是5432    
username=postgres                             # 数据库用户             
export PGPASSWORD=7u&8i*9o(                   # 数据库密码
dmpDir=/opt/pgbak                             # 本地备份目录
destination=/bigdata/pg_backup                # 远端备份目录
echo "时间：" $nowtime
set timeout 600

#/monchickey/bin/ 为 pg_dump 备份工具安装路径，根据实际情况更新此路径。
/monchickey/bin/pg_dumpall --file ""$dmpDir"/pg_backup_"$today".sql" --host "$host_ip" --port "$port_id" --username "$username"
#--verbose --role "postgres" --format=c --blobs --encoding "UTF8" 备份转换扩展配置

echo "PostgreSQL 数据库备份完成！"

echo "当天备份文件压缩中..."
gzip "$dmpDir"/pg_backup_"$today".sql.gz ;
echo "7 天前的 PostgreSQL 数据库备份文件已删除！"

echo "开始远端备份..."
scp -r $dmpDir"/pg_backup_"$today".sql.gz root@backup_ip:destination

echo "远端备份完毕，感谢您使用此脚本！"
exit;
```

利用`find`查找`pg_dumpall`工具安装路径，并修改脚本中的参数。

```shell
find / -name pg_dumpall
```

给`pg_dump_backup.sh`脚本增加可执行权限，并在`Linux`的`/etc/crontab`文件中创建定时任务。

```shell
chmod +x pg_dump_backup.sh

crontab -e
# PostgreSQL 数据库备份
0 3 * * 6 root sh /home/postgres/pg_dump_backup.sh >> /home/postgres/postgres_backup.log 2>&1 &
```

#### PostgreSQL 数据库的恢复

使用`pg_restore`命令将备份文件恢复到新数据库中，需确保已创建目标数据库。

首先，确保已经登录到拥有足够权限的数据库用户账号。然后，使用以下命令将备份文件恢复到新数据库中：

```shell
pg_restore -U <username> -d <database_name> <backup_file_path>
```

- `<username>`：具有足够权限的数据库用户的用户名
- `<database_name>`：将备份文件恢复到的目标数据库的名称
- `<backup_file_path>`：数据库备份文件的完整路径及文件名

输入用户密码后，`pg_restore`将开始从备份文件中恢复数据库。

最后，在分享个脚本，该脚本的作用主要是删除指定目录中7天前的数据库备份文件。首先，是在终端中打印一条消息，告诉用户脚本开始删除 7 天前的数据库备份文件。

然后，执行`find /home/postgresql_backup/ -name "*sql" -mtime +7 -exec rm -rf {} \;`命令，这行命令实际上是执行删除操作。让我来解释一下这个命令：

- `find`：是一个用于在指定目录中查找文件的命令
- `/home/postgresql_backup/`：要查找的目录
- `-name "*sql"`：查找以`.sql`结尾的文件
- `-mtime +7`：查找修改时间在 7 天之前的文件
- `-exec rm -rf {} \;`：对查找到的文件执行 `rm -rf` 命令，`{}` 会被替换为实际的文件名。

最后，在终端中打印一条消息，告诉用户 7 天前的数据库备份文件已经删除完毕！

```shell
#！/bin/bash
echo "开始删除 7 天前的 数据库备份文件..."
find /home/postgresql_backup/ -name "*sql" -mtime +7 -exec rm -rf {} \;
set timeout 1000
echo " 7 天前的数据库备份文件删除完毕！"
```

