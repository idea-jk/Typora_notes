# journalctl命令

```shell
# 查看当前systemd日志所占用的磁盘空间
journalctl --disk-usage

# 保留最近的2个日志文件
journalctl --vacuum-files=2

# 要删除7天之前的日志
journalctl --vacuum-time=7d
journalctl --vacuum-size=10M

# 仅查看当前启动的日志
journalctl -b

# 列出所有启动记录
journalctl --list-boots

# 查看特定启动（如上一次启动）的日志
journalctl -b -1

# 可以通过时间范围过滤日志
journalctl --since "2025-08-19 08:00:00" --until "2025-08-19 12:00:00"

# 使用相对时间
journalctl --since "1 hour ago"

# 查看特定服务的日志（如 nginx）
journalctl -u nginx.service

```

