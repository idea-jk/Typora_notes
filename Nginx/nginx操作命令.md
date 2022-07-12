# nginx命令查询

```shell
# nginx进程
ps -ef | grep nginx

# 查询nginx配置路径
lsof -p 进程id

# 重新加载nginx配置信息
service nginx reload

# 杀死指定程序
kill -QUIT 进程id

# 启动nginx
service nginx start
systemctl start nginx.service

# 添加至服务管理列表，设置开机自启
chkconfig --add nginx
chkconfig nginx on

# nginx错误日志目录
/var/log/nginx/
# 查询服务器所有访问者
IPawk '{print $1}' /var/log/nginx/acces.log | sort | uniq -c | sort -n

# 在nginx的安装目录下面,新建屏蔽ip文件，命名为guolv_ip.conf，以后新增加屏蔽ip只需编辑这个文件即可。加入如下内容并保存：
deny 66.249.79.84 ; 
```

