# Centos 7 升级系统内核

## 在线升级

```shell
# 查看系统版本
cat /etc/redhat-release

#  CentOS 7 上启用 ELRepo 仓库
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm

# 列出可用的内核相关包
yum --disablerepo="*" --enablerepo="elrepo-kernel" list available

# 安装最新的主线稳定内核
yum --enablerepo=elrepo-kernel install kernel-ml -y

# 设置 GRUB 默认的内核版本，为了让新安装的内核成为默认启动选项，你需要如下修改 GRUB 配置
sed -i 's/GRUB_DEFAULT=saved/GRUB_DEFAULT=0/' /etc/default/grub

# 查看系统内部有多少个内核
grep ^menuentry /boot/grub2/grub.cfg | cut -d "'" -f2
rpm -qa | grep kernel

# 设置期望默认启动的内核版本
grub2-set-default 'CentOS Linux (5.18.2-1.el7.elrepo.x86_64) 7 (Core)'

# 重新创建内核配置
grub2-mkconfig -o /boot/grub2/grub.cfg

reboot

# 查看启动内核
grub2-editenv list
```

## 离线升级

```shell
# 查看系统版本
cat /etc/redhat-release

# rpm包地址
https://elrepo.org/linux/kernel/el7/x86_64/RPMS/kernel-ml-5.18.2-1.el7.elrepo.x86_64.rpm
rpm -ivh kernel-ml-5.18.2-1.el7.elrepo.x86_64.rpm

# 设置 GRUB 默认的内核版本，为了让新安装的内核成为默认启动选项，你需要如下修改 GRUB 配置
sed -i 's/GRUB_DEFAULT=saved/GRUB_DEFAULT=0/' /etc/default/grub

# 查看系统内部有多少个内核
grep ^menuentry /boot/grub2/grub.cfg | cut -d "'" -f2
rpm -qa | grep kernel

# 配置从默认内核启动，下面命令的内核名称根据系统内部查到的实际名称来替换
grub2-set-default 'CentOS Linux (5.18.2-1.el7.elrepo.x86_64) 7 (Core)'

# 重新创建内核配置
grub2-mkconfig -o /boot/grub2/grub.cfg

reboot

# 查看启动内核
grub2-editenv list
```