# 查看linux 用户登录信息及IP

```shell
# 查看可疑IP登陆
last -f /var/log/wtmp
# 寻找可疑ip登陆次数及信息
cat /var/log/secure

# 查看当前登陆用户
who
-h # 忽略头文件信息
-u # 显示结果的加载时间
```

