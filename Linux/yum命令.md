# yum命令

```shell
# 将yum下载的包保存到本地
# 例如，将 policycoreutils-python 下载到 /root/gitlab/packages/
yum install -y --downloadonly --downloaddir=/root/gitlab/packages/ policycoreutils-python

# 修改yum源(CentOS 7)
# 阿里云开源镜像站
wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
# 网易开源镜像站
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.163.com/.help/CentOS7-Base-163.repo
# 生成缓存
yum clean all && yum makecache
```

