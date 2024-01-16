

# 数据库备份 ，支持多数据库，清理过期备份数据

```shell
#!/bin/bash
#功能说明：本功能用于备份
#编写日期：2022/06/22

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
export PATH
#数据库用户名
dbUser='root'
#数据库密码
dbPasswd='password'
#数据库IP
dbIp='192.168.92.12'
#需要备份的数据库，多个数据库用空格分开
dbName='ef-cloud ef-config iss-ims'
#备份时间
backtime=`date +%Y%m%d%H%M%S`
#日志备份到当前路径mysql文件夹下
logpath=/data/mysql/back/log
#数据备份到当前路径mysql文件夹下
datapath=/data/mysql/back/data
#自动创建目录
if [ ! -d ${logpath} ];then
    mkdir -pv ${logpath}
fi
#自动创建目录
if [ ! -d ${datapath} ];then
    mkdir -pv ${datapath}
fi
#日志记录头部
echo "备份时间为${backtime},备份数据库: ${dbName} 开始" >> ${logpath}/mysqllog.log
echo "备份时间为${backtime},备份数据库: ${dbName} 开始"
#正式备份数据库
for table in $dbName; do
    echo "备份时间为${backtime},备份数据库: ${table} 备份开始!!" >> ${logpath}/mysqllog.log
    echo "备份时间为${backtime},备份数据库: ${table} 备份开始!!"
    source=`/usr/local/mysql/bin/mysqldump --skip-lock-tables -u ${dbUser} -h ${dbIp} -p${dbPasswd} ${table} > ${datapath}/${backtime}-${table}.sql` 2>> ${logpath}/mysqllog.log;
    #备份成功以下操作
    if [ "$?" == 0 ];then
        cd $datapath
        #为节约硬盘空间，将数据库文件压缩,压缩需要时间,视sql文件大小决定,耐心等待即可
        tar zcvf ${backtime}-${table}.tar.gz ${backtime}-${table}.sql > /dev/null
        #删除原始文件，只留压缩后文件
        rm -f ${datapath}/${backtime}-${table}.sql
        echo "备份时间为${backtime},备份数据库: ${table} 备份成功!!" >> ${logpath}/mysqllog.log
        echo "备份时间为${backtime},备份数据库: ${table} 备份成功!!"
    else
        #备份失败则进行以下操作
        echo "备份时间为${backtime},备份数据库: ${table} 备份失败!!" >> ${logpath}/mysqllog.log
        echo "备份时间为${backtime},备份数据库: ${table} 备份失败!!"
    fi
done

#删除30天前备份，也就是只保存30天内的备份
find $datapath -name "*.tar.gz" -type f -print -mtime +30 -exec rm -rf {} \; > /dev/null 2>&1
```

## 单数据库单表备份 ，支持多表备份，清理过期备份数据

```shell
#!/bin/bash
#功能说明：本功能用于备份
#编写日期：2022/06/22

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
export PATH
#数据库用户名
dbUser='root'
#数据库密码
dbPasswd='password'
#数据库IP
dbIp='192.168.92.12'
#需要备份的数据库
dbName='test1'
#需要备份的数据库表,多个数据表用空格分开
dbTableName='table1 table2'
#备份时间
DATA=`date +%Y-%m-%d`
backTime=`date +%Y%m%d%H%M%S`
#日志备份到当前路径mysql文件夹下
logpath=$(pwd)/mysql/log
#数据备份到当前路径mysql文件夹下
datapath=$(pwd)/mysql/data/${DATA}-${dbName}-backfils
#自动创建目录
if [ ! -d ${logpath} ];then
    mkdir -pv ${logpath}
fi
#自动创建目录
if [ ! -d ${datapath} ];then
    mkdir -pv ${datapath}
fi
#日志记录头部
echo "备份时间为${backTime},备份数据库表: ${dbName}->${dbTableName} 开始" >> ${logpath}/mysqllog.log
echo "备份时间为${backTime},备份数据库表: ${dbName}->${dbTableName} 开始"
#正式备份数据库
for table in $dbTableName; do
																										 
																			  
    source=`/usr/local/mysql/bin/mysqldump --skip-lock-tables -u ${dbUser} -h ${dbIp} -p${dbPasswd} ${dbName} ${table} > ${datapath}/${backTime}-${dbName}-${table}.sql` 2>> ${logpath}/mysqllog.log;
    #备份成功以下操作
    if [ "$?" == 0 ];then
        cd $datapath
        #为节约硬盘空间，将数据库文件压缩,压缩需要时间,视sql文件大小决定,耐心等待即可
        tar zcvf ${backTime}-${table}.tar.gz ${backTime}-${dbName}-${table}.sql > /dev/null
        #删除原始文件，只留压缩后文件
        rm -f ${datapath}/${backTime}-${dbName}-${table}.sql
        echo "备份时间为${backTime},备份数据库表: ${dbName}->${table} 备份成功!!" >> ${logpath}/mysqllog.log
        echo "备份时间为${backTime},备份数据库表: ${dbName}->${table} 备份成功!!"
    else
        #备份失败则进行以下操作
        echo "备份时间为${backTime},备份数据库表: ${dbName}->${table} 备份失败!!" >> ${logpath}/mysqllog.log
        echo "备份时间为${backTime},备份数据库表: ${dbName}->${table} 备份失败!!"
    fi
done

#删除30天前备份，也就是只保存30天内的备份
find $datapath -name "*backfils" -type d -print -mtime +30 -exec rm -rf {} \; > /dev/null 2>&1
```

## 定时运行备份

```shell
# 查看当前服务器的定时任务
crontab -e

# 添加定时任务脚本，每天0点运行一次，根据业务需要调整时间
0 0 0 1/1 * cd /data/mysql;./mysqlback.sh
# 每周日 3:00 执行任务
0 3 * * sun cd /data/mysql;./mysqlback.sh

# 执行权限分配命令
chmod u+x *.sh

# 测试运行一下定时任务命令，查看是否运行正常
cd /data/mysql;./mysqlback.sh
```

```shell
# 安装：yum install vixie-cron crontabs (服务器环境下默认都会安装)
/sbin/chkconfig --level 35 crond on  # 开机自启动
crontab -e   # 修改 crontab 文件. 如果文件不存在会自动创建。 
crontab -l   # 显示 crontab 文件。 
crontab -r   # 删除 crontab 文件。
crontab -ir  # 删除 crontab 文件前提醒用户。
cron文件语法:
    　　分     小时    日       月       星期     命令
      　0-59   0-23   1-31   1-12      0-6   command     (取值范围,0表示周日一般一行对应一个任务)
       　“*”代表取值范围内的数字,
          “/”代表”每”,
          “-”代表从某个数字到某个数字,
          “,”分开几个离散的数字
/sbin/service crond start      # 启动服务
/sbin/service crond stop       # 关闭服务
/sbin/service crond restart    # 重启服务
/sbin/service crond reload     # 重新载入配置
```

## 超实用的Crontab使用实例

```shell
# 每天 02:00 执行任务
0 2 * * * /bin/sh backup.sh
# 每天 5:00和17:00执行任务
0 5,17 * * * /scripts/script.sh
# 每分钟执行一次任务
* * * * * /scripts/script.sh
# 每周日 17:00 执行任务
0 17 * * sun /scripts/script.sh
# 每 10min 执行一次任务
*/10 * * * * /scripts/monitor.sh
# 在特定的某几个月执行任务
* * * jan,may,aug * /script/script.sh
# 在特定的某几天执行任务(在每周五、周日的17点执行任务)
0 17 * * sun,fri /script/scripy.sh
# 在某个月的第一个周日执行任务
0 2 * * sun [ $(date +%d) -le 07 ] && /script/script.sh　　
# 每四个小时执行一个任务
0 */4 * * * /scripts/script.sh　　
# 每周一、周日执行任务
0 4,17 * * sun,mon /scripts/script.sh
# 每个30秒执行一次任务
我们没有办法直接通过上诉类似的例子去执行，因为最小的是1min。但是我们可以通过如下的方法。
* * * * * /scripts/script.sh 
* * * * * sleep 30; /scripts/script.sh 
# 多个任务在一条命令中配置
* * * * * /scripts/script.sh; /scripts/scrit2.sh
# 每年执行一次任务
@yearly /scripts/script.sh
@yearly 类似于“0 0 1 1 *”。它会在每年的第一分钟内执行，通常我们可以用这个发送新年的问候。
# 系统重启时执行
@reboot /scripts/script.sh
```

