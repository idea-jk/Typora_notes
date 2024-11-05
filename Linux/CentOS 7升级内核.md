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

# 重启系统
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

# 重启系统
reboot

# 查看启动内核
grub2-editenv list
```

## 删除多余内核

```shell
# 确认当前使用的内核版本
# 打开终端，输入以下命令来查看当前系统正在使用的内核版本：

uname -r

# 查询已安装的所有内核版本
# 使用 rpm 命令列出所有与内核相关的包：

rpm -qa | grep kernel

# 删除多余的内核
# 使用 yum 命令来删除不再需要的内核版本。例如，如果你要删除 kernel-ml-6.9.7-1.el7.elrepo.x86_64 这个版本，可以运行：

yum remove kernel-ml-6.9.7-1.el7.elrepo.x86_64

# 对于每个不需要的内核重复此步骤。

# 更新引导加载器配置
# 删除内核后，需要更新 GRUB 配置以反映这些更改：

grub2-mkconfig -o /boot/grub2/grub.cfg

# 重启系统
reboot
```

