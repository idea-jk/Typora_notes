# Linux挂载磁盘

```shell
# 查看各个盘的大小和分区信息
fdisk -l
# 查看磁盘挂载
lsblk
# 创建data文件夹
mkdir -pv /data

# 格式化磁盘，格式化磁盘格式为ext4
mkfs.ext4 /dev/sdb
mkfs -t ext4 /dev/sdb
mkfs -V -t ext4 /dev/sdb


mkfs [-V] [-t fstype] [fs-options] file sys [blocks]
-V 详细显示模式
-t 给定档案系统的型式，Linux下预设值为ext2
-c 在制做档案前，检查partition是否有坏轨
-l bad_blocks_file 将有坏轨的block资料加到bad_blocks_file里面
block 给定block的大小

# 挂载磁盘
mount /dev/sdb /data
# 将挂载信息执行开机自启动(只能执行一次)
cat /etc/mtab | grep /data >> /etc/fstab
# 查看磁盘挂载
lsblk
```

