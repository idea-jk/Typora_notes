# CentOS添加新用户

### 1、创建新用户

```shell
useradd [用户名]  	// 默认主文件夹在 `/home` 目录 
passwd [用户名]  	// 设置用户密码
```

### 2、授权,添加 sudoers 文件可写权限

```shell
chmod -v u+w /etc/sudoers

# 修改 sudoers 文件
vim /etc/sudoers

# 在 sudoers 文件中找到如下位置并添加如下内容：
[用户名]    ALL=(ALL)    ALL  	// (若新用户需要使用 sudo 时不输密码, 则将此行最后一个 ALL 改为 NOPASSWD:ALL 即可)
```

### 3、收回 sudoers 文件可写权限

```shell
chmod -v u-w /etc/sudoers

# Linux 删除用户账号和主目录
userdel -r [用户名]


cat     由第一行开始显示内容，并将所有内容输出
tac     从最后一行倒序显示内容，并将所有内容输出
more    根据窗口大小，一页一页的现实文件内容
less    和more类似，但其优点可以往前翻页，而且进行可以搜索字符
head    只显示头几行
tail    只显示最后几行
nl      类似于cat -n，显示时输出行号
tailf   类似于tail -f 
```

