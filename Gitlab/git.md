# Git 本地与GitHub远程同步

## 基本步骤：

本地添加仓库： 创建文件夹 打开git 初始化仓库

```shell
git init
```

设置提交代码时的用户信息：

```shell
git config --global user.name "username"
git config --global user.email "123@qq.com"
```

建立本地仓库与远程仓库的链接：

```shell
git remote -v  //查看与远程仓库连接情况
```

![](..\image\git\aecb61e34c3baa8032c03cea7c80793d.png)

```shell
git remote add origin [远程仓库连接地址]  //新建远程仓库连接
```

![](..\image\git\4765b6d1ae11ce825ef09224db86760a.png)

```shell
git remote rm origin [远程仓库连接地址]   //解除连接

git pull origin main//拉取同步文件

git add . //添加需要同步上传的文件 . 表示上传全部

git commit -m "备注说明”

git push origin main//开始进行push，弹出GitHub登录窗口，输入注册的GitHub账号即可
```

## 连接当中遇到的问题：

无法进行push 提示： 

![](..\image\git\984b869f3130ac1ac442645f47e50637.png)

## 解决办法：

在进行拉取同步文件那一步改为:

```shell
git pull origin main --allow-unrelated-histories //把远程仓库和本地同步，消除差异
```

重新add和commit相应文件 git push origin main

此时就能够上传成功了

## 其他指令：

查看git仓库中各文件状态

```shell
git status
```

git删除文件夹：

```shell
git rm [文件名] -r -f
git commit -m 'del config' 
git push origin main
```

查看日志：

```shell
git log
```

git回退到指定版本

```shell
# 先查看日志
git log
# 回退命令
git reset --hard <commitId>
# 例如
git reset --hard c9357709df57e8397ca25e404948658cfa6ffed1
```

![image-20220615160647840](..\image\git\20220615160647840.png)

修改仓库名：

```shell
git branch -M main
```