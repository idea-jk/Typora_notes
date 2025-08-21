# Centos 9升级系统内核

## 在线升级

```shell
# 查看系统版本
cat /etc/redhat-release

# 导入 ELRepo 仓库
# 访问 ELRepo 官方网站 获取仓库的安装方式。执行以下命令导入 ELRepo 仓库：导入公钥，用于校验软件包
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org

# 导入 yum 源，用于从该仓库下载软件包
yum install https://www.elrepo.org/elrepo-release-9.el9.elrepo.noarch.rpm


# 安装最新内核
yum install --enablerepo=elrepo-kernel kernel-ml

yum install -y --downloadonly --downloaddir=/root/elrepo-kernel_kernel-ml --enablerepo=elrepo-kernel kernel-ml

# 内核包名：
kernel-ml-core-6.12.1-1.el9.elrepo.x86_64
kernel-ml-modules-6.12.1-1.el9.elrepo.x86_64
kernel-ml-6.12.1-1.el9.elrepo.x86_64

# 查看系统内部有多少个内核
rpm -qa | grep kernel

# 重启系统
init 6
```

## 离线升级

```shell
# 查看系统版本
cat /etc/redhat-release

# rpm包地址
rpm -Uvh kernel-ml-core-6.12.1-1.el9.elrepo.x86_64.rpm
rpm -Uvh kernel-ml-modules-6.12.1-1.el9.elrepo.x86_64.rpm
rpm -Uvh kernel-ml-6.12.1-1.el9.elrepo.x86_64.rpm

# 查看系统内部有多少个内核
rpm -qa | grep kernel

# 重启系统
init 6
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
# 使用 yum 命令来删除不再需要的内核版本。例如，如果你要删除 kernel-ml-core-5.14.0-522.el9.elrepo.x86_64 这个版本，可以运行：
yum remove -y kernel-core-5.14.0-522.el9.x86_64
yum remove -y kernel-tools-5.14.0-522.el9.x86_64

# 重启系统
init 6
```

## 系统重启命令

```shell
# reboot和init 6

“init 6” 基于一系列/etc/inittab文件，并且每个应用都会有一个相应shutdown脚本。
‘init 6’ 调用一系列shutdown脚本(/etc/rc0.d/K*)来使系统优雅关机;
'reboot’并不执行这些过程，reboot更是一个kernel级别的命令，不对应用使用shutdown脚本。 

在出问题的状况下或强制重启时使用reboot.
init 6比较优雅 reboot比较暴力
```

## yum源更新命令

```shell
#清空dnf缓存
dnf clean all

dnf makecache

dnf -y update

#列出所有软件名称
dnf list all
#列出已经安装的软件名称
dnf list installed
```

