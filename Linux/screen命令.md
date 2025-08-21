# screen命令  

Screen是一个全屏窗口管理器，它在多个进程（通常是交互式shell）之间多路传输物理终端。

##### centos安装screen
```shell
 yum install -y screen
```

##### 在Ubuntu上安装并使用screen
```shell
## 更新包列表
sudo apt update 

## 安装screen工具
sudo apt install screen
```


```shell
## 创建一个新的窗口
screen -S test

## 进入窗口后 执行文件
python test.py

## 退出当前窗口
ctrl+a+d   （方法1：保留当前窗口）
screen -d  （方法2：保留当前窗口）
exit       （方法3：退出程序，并关闭窗口）

# 查看窗口
screen -ls

# 重新连接窗口
screen -r id或窗口名称
```

#####  示例：

```shell
screen -r 344 
screen -r test
快捷键：
Ctrl+a c ：创建窗口
Ctrl+a w ：窗口列表

Ctrl+a n ：下一个窗口
Ctrl+a p ：上一个窗口

Ctrl+a 0-9 ：在第0个窗口和第9个窗口之间切换

Ctrl+a K(大写) ：关闭当前窗口，并且切换到下一个窗口
（当退出最后一个窗口时，该终端自动终止，并且退回到原始shell状态）

exit ：关闭当前窗口，并且切换到下一个窗口
（当退出最后一个窗口时，该终端自动终止，并且退回到原始shell状态）

Ctrl+a d ：退出当前终端，返回加载screen前的shell命令状态	
```

