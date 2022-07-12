```shell
hostnamectl命令修改主机名
hostnamectl set-hostname <newhostname>
nmtui
# tui字符界面图形模式配置

Linux 双网卡配置优先级
# 查看网卡IP
ip addr

# 查看路由信息
ip route show

# 修改网卡路由优先级
# 我们需要通过修改metric(跃点数)，来修改网卡的优先级

vim /etc/sysconfig/network-scripts/ifcfg-ens**

# 添加了一个参数（放在【IPV4_FAILURE_FATAL="no"】后面好区分）
IPV4_ROUTE_METRIC=90

# 重启网卡
service network restart
```

# **动态获取ip**

```shell
# 修改网卡配置文件
vi /etc/sysconfig/network-scripts/ifcfg-ens33
动态获取IP地址需要修改两处地方即可
（1）bootproto=dhcp
（2）onboot=yes
# 重启网络服务
systemctl restart network
```

# **配置静态IP地址**

```shell
# 修改网卡配置文件
vi /etc/sysconfig/network-scripts/ifcfg-ens33
静态获取IP地址需要修改两处地方即可
（1）bootproto=static
（2）onboot=yes
# 重启网络服务
systemctl restart network
```

