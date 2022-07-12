# Centos 更改MySQL5.7数据库目录位置

Centos 通过`yum`安装(RPM分发进行安装)MySQL的几个人默认目录如下：

| 目录             | 目录内容             |
| ---------------- | -------------------- |
| /usr/bin         | 客户端程序和脚本     |
| /usr/sbin        | mysqld服务器         |
| /var/lib/mysql   | 日志文件，数据库文件 |
| /usr/share/mysql | 错误消息和字符集文件 |
| /etc/my.cnf      | 配置文件             |

假如要把目录移到/data下需要进行下面几步：

1、/目录下建立data目录

```shell
mkdir -p /data
cd /data
```

把MySQL服务进程停掉

```shell
systemctl stop mysqld
systemctl status mysqld
```

把`/var/lib/mysql`整个目录移到`/data/mysql`

```shell
 cp -R /var/lib/mysql/* /data/mysql
```

```shell
chown -R mysql:mysqlgroup /data/mysql
```

修改配置文件`/etc/my.cnf`

为保证MySQL能够正常工作，需要指明`mysql.sock`文件的产生位置。修改`socket=/var/lib/mysql/mysql.sock`一行中等号右边的值为：`/data/mysql/mysql.sock` 以及修改`datadir`为`/data/mysql`操作如下：

```shell
#datadir=/var/lib/mysql
datadir=/data/mysql
#socket=/var/lib/mysql/mysql.sock
socket=/data/mysql/mysql.sock
```

重新启动MySQL服务

```shell
# 启动报错，设置一个SELinux即可
setenforce 0
service mysqld start
```

