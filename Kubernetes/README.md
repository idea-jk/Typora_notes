# kubernetes (k8s) 二进制高可用安装

# 常见异常

1. 安装会出现kubelet异常，无法识别 `--node-labels` 字段问题，原因如下。

将 `--node-labels=node.kubernetes.io/node=''` 替换为 `--node-labels=node.kubernetes.io/node=`  将 `''` 删除即可。

2. 注意hosts配置文件中主机名和IP地址对应

3. 在文档7.2，却记别忘记执行`kubectl create -f bootstrap.secret.yaml`命令

# 介绍

我使用IPV6的目的是在公网进行访问，所以我配置了IPV6静态地址。

若您没有IPV6环境，或者不想使用IPv6，不对主机进行配置IPv6地址即可。

不配置IPV6，不影响后续，不过集群依旧是支持IPv6的。为后期留有扩展可能性。

如果本地没有IPv6，那么Calico需要使用IPv4的yaml配置文件。

后续尽可能第一时间更新新版本文档，更新后内容在GitHub。

# 当前文档版本

1.21.13 和 1.22.10 和 1.23.3 和 1.23.4 和 1.23.5 和 1.23.6 和 1.23.7 和 1.24.0 和 1.24.1 和 1.24.2 和 1.24.3 文档以及安装包已生成。

# 访问地址

https://github.com/cby-chen/Kubernetes/

手动项目地址：https://github.com/cby-chen/Kubernetes

脚本项目地址：https://github.com/cby-chen/Binary_installation_of_Kubernetes

kubernetes 1.24 变化较大，详细见：https://kubernetes.io/zh/blog/2022/04/07/upcoming-changes-in-kubernetes-1-24/

# 文档

## 二进制安装每个版本文档

### 1.23版本
[v1.23.3-CentOS-binary-install](./v1.23.3-CentOS-binary-install.md)

[v1.23.4-CentOS-binary-install](./v1.23.4-CentOS-binary-install.md)

[v1.23.5-CentOS-binary-install](./v1.23.5-CentOS-binary-install.md)

[v1.23.6-CentOS-binary-install](./v1.23.6-CentOS-binary-install.md)

### 1.24版本
[v1.24.0-CentOS-binary-install-IPv6-IPv4.md](./v1.24.0-CentOS-binary-install-IPv6-IPv4.md)

[v1.24.1-CentOS-binary-install-IPv6-IPv4.md](./v1.24.1-CentOS-binary-install-IPv6-IPv4.md)

[v1.24.2-CentOS-binary-install-IPv6-IPv4.md](./v1.24.2-CentOS-binary-install-IPv6-IPv4.md)

[v1.24.3-CentOS-binary-install-IPv6-IPv4.md](./v1.24.3-CentOS-binary-install-IPv6-IPv4.md)

### 三主俩从版本
[v1.21.13-CentOS-binary-install-IPv6-IPv4-Three-Masters-Two-Slaves.md](./v1.21.13-CentOS-binary-install-IPv6-IPv4-Three-Masters-Two-Slaves.md)

[v1.22.10-CentOS-binary-install-IPv6-IPv4-Three-Masters-Two-Slaves.md](./v1.22.10-CentOS-binary-install-IPv6-IPv4-Three-Masters-Two-Slaves.md)

[v1.23.7-CentOS-binary-install-IPv6-IPv4-Three-Masters-Two-Slaves.md](./v1.23.7-CentOS-binary-install-IPv6-IPv4-Three-Masters-Two-Slaves.md)

[v1.24.0-CentOS-binary-install-IPv6-IPv4-Three-Masters-Two-Slaves.md](./v1.24.0-CentOS-binary-install-IPv6-IPv4-Three-Masters-Two-Slaves.md)

[v1.24.1-CentOS-binary-install-IPv6-IPv4-Three-Masters-Two-Slaves.md](./v1.24.1-CentOS-binary-install-IPv6-IPv4-Three-Masters-Two-Slaves.md)

[v1.24.1-Ubuntu-binary-install-IPv6-IPv4-Three-Masters-Two-Slaves.md](./v1.24.1-Ubuntu-binary-install-IPv6-IPv4-Three-Masters-Two-Slaves.md)


## 修复kube-proxy证书权限过大问题

[kube-proxy_permissions.md](./kube-proxy_permissions.md)

## 使用kubeadm初始化IPV4/IPV6集群

[kubeadm-install-IPV6-IPV4.md](./kubeadm-install-IPV6-IPV4.md)

## IPv4集群启用IPv6功能，关闭IPv6则反之

[Enable-implement-IPv4-IPv6.md](./Enable-implement-IPv4-IPv6.md)

## 升级kubernetes集群  

[Upgrade_Kubernetes.md](./Upgrade_Kubernetes.md)  

# 安装包

（下载更快）我自己的网盘：https://pan.oiox.cn/s/PetV

（下载更快）123网盘：https://www.123pan.com/s/Z8ArVv-PG60d

每个初始版本会打上releases，安装包在releases页面

https://github.com/cby-chen/Kubernetes/releases

注意：1.23.3 版本当时没想到会后续更新，所以当时命名不太规范。

wget https://ghproxy.com/https://github.com/cby-chen/Kubernetes/releases/download/cby/Kubernetes.tar

wget https://ghproxy.com/https://github.com/cby-chen/Kubernetes/releases/download/v1.23.4/kubernetes-v1.23.4.tar

wget https://ghproxy.com/https://github.com/cby-chen/Kubernetes/releases/download/v1.23.5/kubernetes-v1.24.5.tar

wget https://ghproxy.com/https://github.com/cby-chen/Kubernetes/releases/download/v1.23.6/kubernetes-v1.23.6.tar

wget https://ghproxy.com/https://github.com/cby-chen/Kubernetes/releases/download/v1.23.7/kubernetes-v1.23.7.tar

wget https://ghproxy.com/https://github.com/cby-chen/Kubernetes/releases/download/v1.24.0/kubernetes-v1.24.0.tar

wget https://ghproxy.com/https://github.com/cby-chen/Kubernetes/releases/download/v1.24.1/kubernetes-v1.24.1.tar

wget https://ghproxy.com/https://github.com/cby-chen/Kubernetes/releases/download/v1.24.2/kubernetes-v1.24.2.tar

wget https://ghproxy.com/https://github.com/cby-chen/Kubernetes/releases/download/v1.24.3/kubernetes-v1.24.3.tar

wget https://ghproxy.com/https://github.com/cby-chen/Kubernetes/releases/download/v1.22.10/kubernetes-v1.22.10.tar

wget https://ghproxy.com/https://github.com/cby-chen/Kubernetes/releases/download/v1.21.13/kubernetes-v1.21.13.tar

# 旧版本地址

建议查看main版本中的文档。https://github.com/cby-chen/Kubernetes/

若找对应版本文档中的安装包，可以在上方下载安装包，可以在在下方地址中查找。

https://github.com/cby-chen/Kubernetes/tree/cby

https://github.com/cby-chen/Kubernetes/tree/v1.23.4

https://github.com/cby-chen/Kubernetes/tree/v1.23.5

https://github.com/cby-chen/Kubernetes/tree/v1.23.6

https://github.com/cby-chen/Kubernetes/tree/v1.23.7

https://github.com/cby-chen/Kubernetes/tree/v1.24.0

https://github.com/cby-chen/Kubernetes/tree/v1.24.1

https://github.com/cby-chen/Kubernetes/tree/v1.24.2

https://github.com/cby-chen/Kubernetes/tree/v1.24.3

https://github.com/cby-chen/Kubernetes/tree/v1.22.10

https://github.com/cby-chen/Kubernetes/tree/v1.21.13

