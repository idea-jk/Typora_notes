# 查看Linux资源命令



![20230521170205](..\image\Linux\20230521170205.png)

总核数 = 物理CPU个数 X 每颗物理CPU的核数

总逻辑CPU数 = 物理CPU个数 X 每颗物理CPU的核数 X 超线程数

\# 查看物理CPU个数

```shell
cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l
```

\# 查看每个物理CPU中core的个数(即核数)

```shell
cat /proc/cpuinfo| grep "cpu cores"| uniq
```

\# 查看逻辑CPU的个数

```shell
cat /proc/cpuinfo| grep "processor"| wc -l
```

\# 查看CPU信息（型号）

```shell
cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c
```

\# 如何查看Linux 内核

```shell
uname -a
cat /proc/version
```

\# 查看内存情况

```shell
free -m
free -g
```

-m  以MB为单位来显示服务器的内存

-g    以GB为单位来显示服务器的内存

-h   以合理单位来显示服务器的内存