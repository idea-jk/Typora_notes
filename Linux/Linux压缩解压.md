# Linux解压压缩

### 一、分卷压缩

#### **方式一： 先压缩、再分卷**

将service压缩为service.tar.gz

```shell
tar -zcvf service/* service.tar.gz
tar zcvf service.tar.gz service/*
```

**参数说明：**
-c, --create 创建一个新归档
-v, --verbose 详细地列出处理的文件
–warning=KEYWORD 警告控制:
-f, --file=ARCHIVE 使用归档文件或 ARCHIVE 设备
–force-local 即使归档文件存在副本还是把它认为是本地归档
-z, --gzip, --gunzip, --ungzip 通过 gzip 过滤归档



**将service.tar.gz包分卷切割成100M大小、以service为开头的包**

```shell
split -b 100m -d service.tar.gz service
```

**参数说明：**

-b<字节> : 指定多少字节切成一个小文件
-d : 使用数字后缀而不是字母



#### 方式二（推荐）：1步，压缩+分卷

将service打包，并分割为100m大小的包，分割后的文件名以service为开头，service00、service01、service02…

```shell
tar cvzf - service/* | split -b 100m -d - service
```

**参数说明：**

| ：竖杠为管道命令
-：中间的横杠表示输出流，在采用管道命令竖杠时需要用到。





### 二、分卷解压缩

1.先合卷，将service*等分卷文件合并为service.tar.gz

```shell
cat service* > service.tar.gz
```

2.解压缩

```shell
tar -zxvf servcie.tar.gz
```

**参数说明**：
-x, --extract, --get 从归档中解出文件