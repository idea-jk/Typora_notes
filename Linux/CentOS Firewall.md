# CentOS防火墙设置

```shell
# 查看firewall服务状态
systemctl status firewalld
# 查看firewall状态
firewall-cmd --state

# 开启、重启、关闭、firewalld.service服务
# 查看Linux哪些程序正在使用互联网
firewall-cmd --list-services ssh dhcpv6-client --permanent

# 开启
service firewalld start
# 重启
service firewalld restart
# 关闭
service firewalld stop
# 刷新
firewall-cmd --reload

# 查看防火墙规则
firewall-cmd --list-all

# 查询、开放、移除端口
# 查询8080端口是否开放
firewall-cmd --query-port=8080/tcp
# 开放8080端口
firewall-cmd --add-port=8080/tcp --permanent
firewall-cmd --add-port=8080-8088/tcp --permanent
# 移除8080端口
firewall-cmd --remove-port=8080/tcp --permanent
firewall-cmd --remove-port=8080-8088/tcp --permanent

# 查看防火墙的开放端口
firewall-cmd --list-ports

# 重启防火墙
firewall-cmd reload

# 参数解释
1、firwall-cmd：是Linux提供的操作firewall的一个工具；
2、--permanent：表示设置为持久；
3、--add-port：标识添加的端口；
```

