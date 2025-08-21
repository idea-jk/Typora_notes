

## 升级二进制kubernetes集群



### 基础操作

#### 查看当前版本信息

```shell
[root@k8s-master01 ~]# kubectl  get node
NAME           STATUS   ROLES    AGE   VERSION
k8s-master01   Ready    <none>   57d   v1.23.6
k8s-master02   Ready    <none>   57d   v1.23.6
k8s-master03   Ready    <none>   57d   v1.23.6
k8s-node01     Ready    <none>   57d   v1.23.6
k8s-node02     Ready    <none>   57d   v1.23.6
[root@k8s-master01 ~]#
```



#### 主机域名以及IP地址

```shell
[root@k8s-master01 ~]# cat /etc/hosts | grep k8s
192.168.1.230 k8s-master01
192.168.1.231 k8s-master02
192.168.1.232 k8s-master03
192.168.1.233 k8s-node01
192.168.1.234 k8s-node02
[root@k8s-master01 ~]#
```



#### 下载二进制安装包

```shell
[root@k8s-master01 ~]# wget https://dl.k8s.io/v1.23.9/kubernetes-server-linux-amd64.tar.gz
[root@k8s-master01 ~]#
```



#### 解压二进制安装包

```shell
[root@k8s-master01 ~]# tar xf kubernetes-server-linux-amd64.tar.gz
[root@k8s-master01 ~]# 
```



### 升级Maser

#### 升级三台主节点上的客户端

```shell
[root@k8s-master01 ~]# scp kubernetes/server/bin/kubectl root@192.168.1.230:/usr/local/bin/
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# scp kubernetes/server/bin/kubectl root@192.168.1.231:/usr/local/bin/
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# scp kubernetes/server/bin/kubectl root@192.168.1.232:/usr/local/bin/
[root@k8s-master01 ~]#
```



#### 升级三台主节点api组件

```shell
[root@k8s-master01 ~]# ssh root@192.168.1.230 "systemctl stop kube-apiserver"
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# scp kubernetes/server/bin/kube-apiserver root@192.168.1.230:/usr/local/bin/
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# ssh root@192.168.1.230 "systemctl start kube-apiserver"
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# kube-apiserver --version
Kubernetes v1.23.9
[root@k8s-master01 ~]#
```



#### 升级三台主节点控制器组件

```shell
[root@k8s-master01 ~]# ssh root@192.168.1.230 "systemctl stop kube-controller-manager"
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# scp kubernetes/server/bin/kube-controller-manager root@192.168.1.230:/usr/local/bin/
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# ssh root@192.168.1.230 "systemctl start kube-controller-manager"
[root@k8s-master01 ~]#
```



#### 升级三台主节点选择器组件

```shell
[root@k8s-master01 ~]# ssh root@192.168.1.230 "systemctl stop kube-scheduler"
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# scp kubernetes/server/bin/kube-scheduler root@192.168.1.230:/usr/local/bin/
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# ssh root@192.168.1.230 "systemctl start kube-scheduler"
[root@k8s-master01 ~]#
```



### 升级Worker

#### 每一台机器都要升级kubelet

```shell
[root@k8s-master01 ~]# ssh root@192.168.1.230 "systemctl stop kubelet"
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# scp kubernetes/server/bin/kubelet root@192.168.1.230:/usr/local/bin/
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# ssh root@192.168.1.230 "systemctl start kubelet"
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# ssh root@192.168.1.230 "kubelet --version"
Kubernetes v1.23.9
[root@k8s-master01 ~]#
```



#### 每一台机器都要升级kube-proxy

```shell
[root@k8s-master01 ~]# ssh root@192.168.1.230 "systemctl stop kube-proxy"
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# scp kubernetes/server/bin/kube-proxy root@192.168.1.230:/usr/local/bin/
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# ssh root@192.168.1.230 "systemctl start kube-proxy"
[root@k8s-master01 ~]#
```



### 验证

```shell
[root@k8s-master01 ~]# kubectl  get node
NAME           STATUS   ROLES    AGE   VERSION
k8s-master01   Ready    <none>   57d   v1.23.9
k8s-master02   Ready    <none>   57d   v1.23.9
k8s-master03   Ready    <none>   57d   v1.23.9
k8s-node01     Ready    <none>   57d   v1.23.9
k8s-node02     Ready    <none>   57d   v1.23.9
[root@k8s-master01 ~]#
[root@k8s-master01 ~]# kubectl  version
Client Version: version.Info{Major:"1", Minor:"23", GitVersion:"v1.23.9", GitCommit:"c1de2d70269039fe55efb98e737d9a29f9155246", GitTreeState:"clean", BuildDate:"2022-07-13T14:26:51Z", GoVersion:"go1.17.11", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"23", GitVersion:"v1.23.9", GitCommit:"c1de2d70269039fe55efb98e737d9a29f9155246", GitTreeState:"clean", BuildDate:"2022-07-13T14:19:57Z", GoVersion:"go1.17.11", Compiler:"gc", Platform:"linux/amd64"}
[root@k8s-master01 ~]#
```
