# Kubernetes配置yaml文件详解

### Yaml文件详解

##### 1、YAML介绍

YAML 语言（发音 /ˈjæməl/ ）的设计目标，就是方便人类读写。它实质上是一种通用的数据串行化格式。

YAML是专门用来写配置文件的语言，非常简洁和强大，使用比json更方便。

##### 2、使用YAML用于K8s的定义的优势

便捷性： 不必添加大量的参数到命令行中执行命令
可维护性：YAML文件可以通过源头控制，跟踪每次操作
灵活性： YAML可以创建比命令行更加复杂的结构

##### 3、YAML的语法规则

大小写敏感
使用缩进表示层级关系
缩进时不允许使用Tab键，只允许使用空格
缩进的空格数不重要，只要相同层级的元素左侧对齐即可
"表示注释
注：在同一个yaml配置文件内可以同时定义多个资源

##### 4、YAML结构类型

YAML 支持的数据结构有三种。

对象：键值对的集合，又称为映射（mapping）/ 哈希（hashes） / 字典（dictionary）
数组：一组按次序排列的值，又称为序列（sequence） / 列表（list）
纯量（scalars）：单个的、不可再分的值

1.Lists List即列表，说白了就是数组
2.Maps Map顾名思义指的是字典，即一个Key:Value 的键值对信息

##### 5、YAML字典写法解释

```yaml
# 字典
    a={key:value,key1:{key2:value2},key3:{key4:[1,{key5:value5},3,4,5]}}

key: value
key1:
  key2: value2
key3:
  key4:
    - 1
    - key5: value5
    - 3
    - 4
    - 5
spec:
    container:
{key:value,key1:{key2:value2,key8:value8},key3:{key4:[1,{key5:value5,key9:value9},3,4,5]}}

key: value
key1:
  key2:value2
  key8:value8
key3:
  key4:
    - 1
    - key5:value5
      key9:value9
    - 3
    - 4
    - 5
```

注：上述的YAML文件中，metadata这个KEY对应的值为一个Maps，而嵌套的labels这个KEY的值又是一个Map。实际使用中可视情况进行多层嵌套。

**YAML Maps**
Map指的是字典，即一Key:Value 的键值对信息

```yaml
---
apiVersion: v1
kind: Pod
{apiVersion:v1,kind:Pod}
注：--- 为可选的分隔符 ，当需要在一个文件中定义多个结构的时候需要使用。上述内容表示有两个键apiVersion和kind，分别对应的值为v1和Pod。

```

Maps的value既能够对应字符串也能够对应一个Maps

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: kube100-site
  labels:
    app: web    
  {apiVersion:v1,kind:Pod,metadata:{name:kube100-site,labels:{app:web}}}  
# 注：上述的YAML文件中，metadata这个KEY对应的值为一个Maps，而嵌套的labels这个KEY的值又是一个Map。实际使用中可视情况进行多层嵌套。
```

YAML处理器根据行缩进来知道内容之间的关联。例子中，使用两个空格作为缩进，缩进至少要求一个空格并且所有缩进保持一致的空格数 。

**PS.在YAML中不要使用tab键！**

##### 6、YAML数组

**YAML Lists**
List即列表，就是数组

```yaml
例如：
args:
 - beijing
 - shanghai
 - shenzhen
 - guangzhou
    可以指定任何数量的项在列表中，每个项的定义以连字符（-）开头，并且与父元素之间存在缩进。
    在JSON格式中，表示如下：
{
  "args": ["beijing", "shanghai", "shenzhen", "guangzhou"]
}
```

Lists的子项也可以是Maps，Maps的子项也可以是List

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: kube100-site
  labels:
    app: web
spec:
  containers:
    - name: front-end
      image: nginx
      ports:
        - containerPort: 80     
    - name: flaskapp-demo
      image: jcdemo/flaskapp
      ports: 8080
  {apiversion:v1,kind:Pod,metadata:{name:kube100,labels:{app:web}},spec:{containers:[name,image,ports]},}        
#如上述文件所示，定义一个containers的List对象，每个子项都由name、image、ports组成，每个ports都有一个KEY为containerPort的Map组成，转成JSON格式文件：
{
  "apiVersion": "v1",
  "kind": "Pod",
  "metadata": {
        "name": "kube100-site",
        "labels": {
            "app": "web"
        },

  },
  "spec": {
        "containers": [{
            "name": "front-end",
            "image": "nginx",
            "ports": [{
                "containerPort": "80"
            }]
        }, {
            "name": "flaskapp-demo",
            "image": "jcdemo/flaskapp",
            "ports": [{
                "containerPort": "5000"
            }]
        }]
  }
}
```

##### 7、YAML案例

k8s的pod中运行容器，一个包含简单的Hello World容器的pod可以通过YAML文件这样来定义

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-world
  labels:
    release: beta
spec:
  containers:
    - name: hello
      image: "nginx"
      ports:
        - containerPort: 80
```

##### 8、使用yaml创建pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test
  labels:
    app: web
spec:
  containers:
    - name: front-end
      image: nginx
      ports:
        - containerPort: 80
    - name: flaskapp-demo
      image: jcdemo/flaskapp
      ports:
        - containerPort: 5000
# 注意:
# apiVersion：
#     此处值是v1，这个版本号需要根据安装的Kubernetes版本和资源类型进行变化，记住不是写死的。
# kind：
#     此处创建的是Pod，根据实际情况，此处资源类型可以是Deployment、Job、Ingress、Service等。
# metadata：
#     包含Pod的一些meta信息，比如名称、namespace、标签等信息。
# spec：
#     包括一些container，storage，volume以及其他Kubernetes需要的参数，以及诸如是否在容器失败时重新启动容器的属性。可在特定Kubernetes API找到完整的Kubernetes Pod的属性。

# 以下是典型的定义容器
spec:
  containers:
    - name: front-end
      image: nginx
      ports:
        - containerPort: 80
    一个名字（front-end）、基于nginx的镜像，以及容器将会监听的指定端口号（80）
# 扩展了解:
#     容器可选的设置属性包括：name、image、command、args、workingDir、ports、env、resource、volumeMounts、livenessProbe、readinessProbe、livecycle、terminationMessagePath、imagePullPolicy、securityContext、stdin、stdinOnce、tty
```

##### 9、通过yaml文件创建Pod

```yaml
#test-pod 
apiVersion: v1 #指定api版本，此值必须在kubectl apiversion中   
kind: Pod #指定创建资源的角色/类型   
metadata: #资源的元数据/属性   
  name: test-pod #资源的名字，在同一个namespace中必须唯一   
  labels: #设定资源的标签 
    k8s-app: apache   
    version: v1   
    kubernetes.io/cluster-service: "true"   
  annotations:            #自定义注解列表   
    - name: String        #自定义注解名字   
spec: #specification of the resource content 指定该资源的内容   
  restartPolicy: Always #表明该容器一直运行，默认k8s的策略，在此容器退出后，会立即创建一个相同的容器   
  nodeSelector:     #节点选择，先给主机打标签kubectl label nodes kube-node1 zone=node1   
    zone: node1   
  containers:   
  - name: test-pod #容器的名字   
    image: 10.192.21.18:5000/test/chat:latest #容器使用的镜像地址   
    imagePullPolicy: Never #三个选择Always、Never、IfNotPresent，每次启动时检查和更新（从registery）images的策略， 
                           # Always，每次都检查 
                           # Never，每次都不检查（不管本地是否有） 
                           # IfNotPresent，如果本地有就不检查，如果没有就拉取 
    command: ['sh'] #启动容器的运行命令，将覆盖容器中的Entrypoint,对应Dockefile中的ENTRYPOINT   
    args: ["$(str)"] #启动容器的命令参数，对应Dockerfile中CMD参数   
    env: #指定容器中的环境变量   
    - name: str #变量的名字   
      value: "/etc/run.sh" #变量的值   
    resources: #资源管理 
      requests: #容器运行时，最低资源需求，也就是说最少需要多少资源容器才能正常运行   
        cpu: 0.1 #CPU资源（核数），两种方式，浮点数或者是整数+m，0.1=100m，最少值为0.001核（1m） 
        memory: 32Mi #内存使用量   
      limits: #资源限制   
        cpu: 0.5   
        memory: 1000Mi   
    ports:   
    - containerPort: 80 #容器开发对外的端口 
      name: httpd  #名称 
      protocol: TCP   
    livenessProbe: #pod内容器健康检查的设置 
      httpGet: #通过httpget检查健康，返回200-399之间，则认为容器正常
        path: / #URI地址   
        port: 80   
        #host: 127.0.0.1 #主机地址   
        scheme: HTTP   
      initialDelaySeconds: 180 #表明第一次检测在容器启动后多长时间后开始   
      timeoutSeconds: 5 #检测的超时时间   
      periodSeconds: 15  #检查间隔时间   
      #也可以用这种方法   
      #exec: 执行命令的方法进行监测，如果其退出码不为0，则认为容器正常  
      #  command:   
      #    - cat   
      #    - /tmp/health   
      #也可以用这种方法   
      #tcpSocket: //通过tcpSocket检查健康    
      #  port: number    
    lifecycle: #生命周期管理   
      postStart: #容器运行之前运行的任务   
        exec:   
          command:   
            - 'sh'   
            - 'yum upgrade -y'   
      preStop:#容器关闭之前运行的任务   
        exec:   
          command: ['service httpd stop']   
    volumeMounts:  #挂载持久存储卷 
    - name: volume #挂载设备的名字，与volumes[*].name 需要对应     
      mountPath: /data #挂载到容器的某个路径下   
      readOnly: True   
  volumes: #定义一组挂载设备   
  - name: volume #定义一个挂载设备的名字   
    #meptyDir: {}   
    hostPath:   
      path: /opt #挂载设备类型为hostPath，路径为宿主机下的/opt,这里设备类型支持很多种 
    #nfs
```

创建一个yaml:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx-server
        image: nginx:1.16
        ports:
        - containerPort: 80
# 创建deployment:
[root@master yaml-test]# kubectl create -f  deployment.yaml 
deployment.apps/nginx-deployment created
[root@master yaml-test]# kubectl get pods -o wide
NAME      READY   STATUS        RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
nginx-deployment-86dc686b9f-8xnqj                     0/1     ContainerCreating   0          5s    <none>        node-1   <none>           <none>
nginx-deployment-86dc686b9f-8zwnw                     0/1     ContainerCreating   0          5s    <none>        node-2   <none>           <none>
nginx-deployment-86dc686b9f-t9b26                     0/1     ContainerCreating   0          5s    <none>        node-1   <none>           <none>
[root@master yaml-test]# kubectl get deployment
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment        3/3     3            3           6m20s
# 查看标签,通过标签查找pod
[root@master yaml-test]# kubectl get pod --show-labels
NAME     READY   STATUS    RESTARTS   AGE     LABELS
nginx-deployment-86dc686b9f-8xnqj                     1/1     Running   0          7m26s   app=nginx,pod-template-hash=86dc686b9f
nginx-deployment-86dc686b9f-8zwnw                     1/1     Running   0          7m26s   app=nginx,pod-template-hash=86dc686b9f
nginx-deployment-86dc686b9f-t9b26                     1/1     Running   0          7m26s   app=nginx,pod-template-hash=86dc686b9f
[root@master yaml-test]# kubectl get pod -l app=nginx
NAME      READY   STATUS    RESTARTS   AGE
nginx-deployment-86dc686b9f-8xnqj  1/1 Running   0 8m8s
nginx-deployment-86dc686b9f-8zwnw   1/1 Running   0 8m8s
nginx-deployment-86dc686b9f-t9b26   1/1 Running   0  8m8s
```

**Deployment创建过程:**
过程中，Deployment 管理的是replicaset-controller，RC会创建Pod。Pod自身会下载镜像并启动镜像。

```yaml
[root@master yaml-test]# kubectl describe rs nginx-deployment
Name:           nginx-deployment-86dc686b9f
Namespace:      default
Selector:       app=nginx,pod-template-hash=86dc686b9f
Labels:         app=nginx
                pod-template-hash=86dc686b9f
Annotations:    deployment.kubernetes.io/desired-replicas: 3
                deployment.kubernetes.io/max-replicas: 4
                deployment.kubernetes.io/revision: 1
Controlled By:  Deployment/nginx-deployment
Replicas:       3 current / 3 desired
Pods Status:    3 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  app=nginx
           pod-template-hash=86dc686b9f
  Containers:
   nginx-server:
    Image:        nginx:1.16
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason    Age   From   Message
  Normal  SuccessfulCreate  10m   replicaset-controller  Created pod: nginx-deployment-86dc686b9f-8xnqj
  Normal  SuccessfulCreate  10m   replicaset-controller  Created pod: nginx-deployment-86dc686b9f-t9b26
  Normal  SuccessfulCreate  10m   replicaset-controller  Created pod: nginx-deployment-86dc686b9f-8zwnw
[root@master yaml-test]# kubectl describe pods nginx-deployment-86dc686b9f-8xnqj
.......
  Type     Reason     Age    From               Message
  Normal   Scheduled  12m                  default-scheduler  Successfully assigned default/nginx-deployment-86dc686b9f-8xnqj to node-1
  Normal   BackOff    9m50s (x4 over 12m)  kubelet            Back-off pulling image "nginx:1.16"
  Warning  Failed     9m50s (x4 over 12m)  kubelet            Error: ImagePullBackOff
  Normal   Pulling    9m35s (x4 over 13m)  kubelet            Pulling image "nginx:1.16"
  Normal   Pulled     9m28s                kubelet            Successfully pulled image "nginx:1.16" in 7.474603103s
  Normal   Created    9m27s                kubelet            Created container nginx-server
```

扩展:nginx升级

```yaml
[root@master yaml-test]# kubectl set image deploy/nginx-deployment nginx-server=nginx:1.18
deployment.apps/nginx-deployment image updated
nginx-server:容器name
[root@master yaml-test]# kubectl exec -it nginx-deployment-7948d65cd5-dfmtd bash
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl exec [POD] -- [COMMAND] instead.
root@nginx-deployment-7948d65cd5-dfmtd:/# nginx -v       
nginx version: nginx/1.18.0
# 升级镜像的过程是逐步进行的，pod不会一下子全部关闭，而是一个一个升级
# 查看发布状态:
[root@master yaml-test]# kubectl rollout status deploy/nginx-deployment
deployment "nginx-deployment" successfully rolled out
# 查看deployment历史修订版本:
[root@master yaml-test]# kubectl rollout history deploy/nginx-deployment
deployment.apps/nginx-deployment 
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
[root@master yaml-test]#  kubectl rollout history deploy/nginx-deployment --revision=1
deployment.apps/nginx-deployment with revision #1
Pod Template:
  Labels:	app=nginx
	pod-template-hash=86dc686b9f
  Containers:
   nginx-server:
    Image:	nginx:1.16
    Port:	80/TCP
    Host Port:	0/TCP
    Environment:	<none>
    Mounts:	<none>
  Volumes:	<none>

[root@master yaml-test]#  kubectl rollout history deploy/nginx-deployment --revision=2
deployment.apps/nginx-deployment with revision #2
Pod Template:
  Labels:	app=nginx
	pod-template-hash=7948d65cd5
  Containers:
   nginx-server:
    Image:	nginx:1.18
    Port:	80/TCP
    Host Port:	0/TCP
    Environment:	<none>
    Mounts:	<none>
  Volumes:	<none>
```

编辑delpoyment

```yaml
[root@master yaml-test]# kubectl edit deploy/nginx-deployment
# 通过编辑也可以进行容器应用的升级
```

扩容和缩容

```yaml
[root@master yaml-test]# kubectl scale deploy/nginx-deployment --replicas=4
deployment.apps/nginx-deployment scaled
[root@master yaml-test]# kubectl get pods
NAME      READY   STATUS    RESTARTS   AGE
nginx-deployment-7948d65cd5-dfmtd                     1/1     Running   0          45m
nginx-deployment-7948d65cd5-kz6mk                     1/1     Running   0          44m
nginx-deployment-7948d65cd5-mcsqh                     1/1     Running   0          45m
nginx-deployment-7948d65cd5-mlv82                     1/1     Running   0          18s
```

##### 10、创建Service

创建Service提供对外访问的接口

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  labels:
    app: nginx
spec:
  ports:
  - port: 88
    targetPort: 80
  selector:
    app: nginx
    
apiVersion: 指定版本 
kind: 类型 
name: 指定服务名称 
labels: 标签 
port: Service 服务暴露的端口 
targetPort: 容器暴露的端口 
seletor: 关联的Pod的标签

[root@master yaml-test]# kubectl create -f service.yaml
[root@master yaml-test]# kubectl get svc
NAME                                   TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
nginx-service                          ClusterIP      10.97.30.85      <none>        88/TCP                       4m52s
测试访问:
[root@master yaml-test]# curl 10.97.30.85:88
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
```

扩展:使用NodePort

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-services
  labels:
    app: nginx
spec:
  type: NodePort
  ports:
  - port: 88
    targetPort: 80
    nodePort: 30010
  selector:
    app: nginx
```

