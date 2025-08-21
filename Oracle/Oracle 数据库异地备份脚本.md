#### Oracle 数据库异地备份脚本

该脚本用来自动备份`Oracle`数据库。首先，输出一些提示信息，然后获取当前时间，并设置日志文件路径、备份日期时间、保留文件的日期时间、本地备份路径、远端备份路径、Oracle 数据库服务器本机 IP、远端备份 IP、用户名、密码、告警邮箱变量。

脚本会检查本地备份目录路径是否存在，如果不存在则创建定义的目录。然后，使用 `exp` 命令进行`Oracle`数据库的全量备份，并将备份文件保存在指定的本地备份目录路径中。

通过`SSH`连接到远程备份服务器，检查远程备份目录路径是否存在，如果不存在则创建定义的路径。然后删除本地备份目录路径下两星期前的备份文件，并通过`SSH`删除远程备份路径下两星期前的备份文件。

对当前备份文件进行压缩，并通过`SCP`将压缩后的备份文件传输到远程备份服务器。最后，会根据备份和传输的结果发送相应的通知邮件。

```shell
#!/bin/bash
echo "开始执行 Oracle 数据库备份..."
echo "backup ing -------------------"
echo "时间：" nowtime
oraclelog=/opt/originbackup/oraclebackup.log                   # Oracle 日志查看位置
current_date=`date +%Y-%m-%d`                                  # 当前执行日期时间
nowtime=$(date +%F+%T)                                         # 显示当前时间，用于记录脚本运行开始时间
seven_day_date=`date -d -7day '+%Y-%m-%d'`                     # 保留一星期前 dmp 文件时间
fourteen_day_date=`date -d -14day '+%Y-%m-%d'`                 # 保留两星期前 dmp 文件时间

### 需修改参数部分 ###
dmpDir=/data/originbackup                                      # 本地备份路径
destination=/opt/backup/                                       # 远端备份路径
localhost_ip=192.168.1.111                                     # Oracle 本机 IP
backup_ip=192.168.1.110                                        # 远端备份服务器 IP
oracle_user=oracle_db                                                   # Oracle 用户名
oracle_password=4r$5t%6y^                                               # Oracle 密码
mail=xxx@163.com,xxx@126.com                                   # 告警邮箱

source /home/oracle/.bash_profile

### 判断是否有目录，没有则创建目录 ### 
echo "---${current_date}--start dmp all-----"
if [ ! -d ${dmpDir} ];then
    echo "${dmpDir} is not exists,try to create"
    mkdir -p ${dmpDir}
fi

### 开始本地备份（exp 为 oracle 备份工具） ###
exp $oracle_user/$oracle_password@$localhost_ip:1521/orcl file=$dmpDir/$current_date.dmp full=y > /dev/null 2>&1

#touch $dmpDir/$current_date.dmp > /dev/null 2>&1

### 连接远端备份 IP 判断是否有目录 ###
if [ $? -eq 0 ]
then
    ssh $backup_ip ls $destination > /dev/null 2>&1
        if [ $? -eq 0 ]
        then
            echo "$destination exist mkdir"
        else
            ssh $backup_ip mkdir -p $destination
            echo "$destination mkdir success"
        fi
### 本地删除备份文件，保留两个星期前的 ### 
    ssh $backup_ip ls $destination >> /tmp/linshi
    while read myline
    do
        if [ ${myline} == ${seven_day_date}.dmp.gz -o ${myline} == ${fourteen_day_date}.dmp.gz ];then
            echo "$myline.dmp persist success"
        else
            rm -rf `ls ${dmpDir}/*|grep -v ${current_date}|grep -v ${seven_day_date}| grep -v ${fourteen_day_date}`
            ssh $backup_ip rm -rf `ls ${destination}/*| grep -v ${seven_day_date}| grep -v ${fourteen_day_date}` > /dev/null 2>&1
#            ssh $backup_ip rm -rf `ls $destination/*| egrep -v '(${a}|${b})'`
                if [ $? -eq 0 ]
                then
                    echo "Two weeks ago file delete success"
                else
                    echo "Two weeks ago file delete fail"
                    echo $current_date | mail -s "$current_date oracle.dmp file delete faile" $mail  # 保留两星期前数据，其他 dmp 文件删除失败
            fi
        fi
    done < /tmp/linshi
    rm -rf /tmp/linshi
else
    echo "$current_date  文件备份失败"   
    echo $current_date | mail -s "$current_date  file backup fail $localhost_ip" $mail    # 文件备份失败
    echo -e "-----end dmp all-----------------\n"
    exit -1      # 终止后面的所有脚本执行
fi
### 本地压缩，将压缩文件传到远端 IP ###
if [ -f $dmpDir/$current_date.dmp ]   
then
    gzip -q -r $dmpDir/$current_date.dmp $dmpDir
    echo "compress success"
    scp -r $dmpDir/$current_date.dmp.gz root@$backup_ip:$destination > /dev/null 2>&1
        if [ $? -eq 0 ]
                then
                    echo "backup_file transfer success"
                else
                    echo "backup_file transfer fail"
                        echo $current_date | mail -s "$current_date oracle_dmp_file transfer fail $localhost_ip" $mail  # dmp 文件传递失败
                fi
else                            
    echo "backup_file not found"
        if [ $? -eq 0 ]
                then
                        #echo "backup_file found fail"
                        echo $current_date | mail -s "$current_date oracle_dmp_file not found $localhost_ip" $mail  # dmp 文件未发现
                fi
fi

echo -e "-----end dmp all-----------------\n"
```

同样，异地备份免密是必不可少的一步，参考上述`MySQL`配置的免密步骤即可。

给`oracle_backup.sh`脚本增加可执行权限，并在`Linux`的`/etc/crontab`文件中创建定时任务。

```shell
chmod +x oracle_backup.sh

crontab -e
# Oracle 数据库备份
0 3 * * 6 root sh /opt/oracle_backup.sh >> /opt/oraclebackup.log
```

#### Oracle 数据库的恢复

前提是`oracle`数据库已经安装好

然后，创建目录 `/opt/oracle/oraclebak` 并将数据库备份文件 `oracle_db.dmp` 复制到该目录中。

```shell
mkdir -p /opt/oracle/oraclebak
cp oracle_db.dmp /opt/oracle/oraclebak
```

授予 `/opt/oracle/oraclebak` 目录权限给 `oracle` 用户和 `dba` 组。

```shell
chown oracle:dba /opt/oracle/oraclebak
```

在数据库中创建备份目录，以便数据库可以访问备份文件。

```shell
create or replace directory oracle_exp as '/opt/oracle/oraclebak';
```

授予 `oracle_db` 用户对备份目录的读写权限。

```shell
grant read, write on directory oracle_exp to oracle_db;
```

最后，使用以下命令在数据库服务器上切换到 `oracle` 用户，并执行数据库恢复操作：

```shell
su - oracle
impdp oracle_db/oracle_db@orcl SCHEMAS=oracle_db DUMPFILE=oracle_exp:oracle_db.dmp LOGFILE=oracle_exp:oracle_db.log
```

- `oracle_exp`：备份路径定义的目录别名
- `oracle_db/oracle_db@orcl`：本地数据库恢复的用户名、密码和数据库 SID
- `SCHEMAS`：指定要导入的表空间
- `DUMPFILE`：指定数据库恢复文件
- `LOGFILE`：指定数据库恢复日志