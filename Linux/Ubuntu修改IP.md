```shell
# Ubuntu设置固定IP：
ubuntu1804:~$ip route show
ubuntu1804:~$ sudo vi /etc/netplan/50-cloud-init.yaml

#假设IP地址修改为192.168.1.100，子网掩码24位即255.255.255.0，网关设置为192.168.1.1，DNS1：223.5.5.5，DNS2：223.6.6.6
network:
    ethernets:
        ens33:
            dhcp4: no
            addresses: [192.168.1.100/24]
            optional: true
            gateway4: 192.168.1.1
            nameservers:
                    addresses: [223.5.5.5,223.6.6.6]

version: 2

# 应用新配置
ubuntu1804:~$ sudo netplan apply

# 使用ip addr检查新地址
ubuntu2004:~$ ip addr
```

