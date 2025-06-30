# Armbian命令：

1. `armbian-config`：配置Armbian系统的工具，可以通过命令行方式进行系统设置，包括语言、时区、网络等。--图形化配置界面

2. `armbian-update`：更新Armbian系统，获取最新的系统更新和安全补丁。

3. `armbianmonitor`：监控系统的各种指标和性能数据，如CPU温度、内存使用情况等。

   ```shell
   `armbianmonitor` 具体用法：
   
    `armbianmonitor -c /path/to/test`：执行磁盘健康/性能测试
    `armbianmonitor -d`：监视对 `$device` 的写入
    `armbianmonitor -D`：尝试上传调试磁盘信息以改进 `armbianmonitor`
    `armbianmonitor -m`：提供简单的命令行监视 - 滚动输出
    `armbianmonitor -M`：提供简单的命令行监视 - 固定行输出
    `armbianmonitor -n`：提供简单的命令行网络监视 - 滚动输出
    `armbianmonitor -N`：提供简单的命令行网络监视 - 固定行输出
    `armbianmonitor -p`：尝试安装 `cpuminer` 进行性能测量
    `armbianmonitor -r`：尝试安装 `RPi-Monitor`
    `armbianmonitor -u`：尝试上传 `armbian-hardware-monitor.log` 以获取支持
    `armbianmonitor -v`：尝试验证已安装软件包的完整性
    `armbianmonitor -z`：运行快速的 7-zip 基准测试以估计 CPU 性能
   ```

4. `armbian-software`：管理系统的软件设置，如安装/卸载软件包、配置软件仓库等(*注意部分应用基于Docker所以需要先安装Docker)。

5. `sudo apt list --installed`:列出系统上安装的所有软件包。

6. `sudo fdisk -l`:检测存储设备名称。

7. `armbian-install`： 安装系统

   ```shell
    从SD卡引导 - 系统安装在SATA、USB或NVMe设备上
    从eMMC引导 - 系统安装在eMMC设备上
    从eMMC引导 - 系统安装在SATA、USB或NVMe设备上
    在SD卡或eMMC上安装/更新引导程序
   ```

8. armbian-ddbr` ：备份和恢复系统镜像的工具。它可以帮助用户轻松地创建系统备份，并在需要时进行系统恢复。以下是 armbian-ddbr 的具体用法：

   ```shell
    `armbian-ddbr backup`：执行系统备份，将当前系统镜像备份到指定路径。
    `armbian-ddbr restore /path/to/backup.img`：恢复系统，使用指定的备份镜像进行系统恢复。
    `armbian-ddbr verify /path/to/backup.img`：验证备份镜像的完整性，确保备份镜像没有损坏。
    `armbian-ddbr list`：列出已经存在的备份镜像列表。
    `armbian-ddbr delete /path/to/backup.img`：删除指定的备份镜像文件。
    `armbian-ddbr help`：获取帮助信息，列出 armbian-ddbr 的所有可用选项和用法。
   ```

9. 修改Armbian的root密码

   ```shell
   # 在终端中输入以下命令
   passwd
   
   # 系统会提示输入新的密码：
   New password: # 输入新密码
   Retype new password: # 再次输入新密码
   
   # 输入两次相同的新密码后，系统会提示密码修改成功：
   passwd: password updated successfully
   ```

10. 修改Armbian的root密码和IP地址

    ```shell
    # 查看网卡信息--使用ifconfig命令查看系统中所有的网卡信息，包括当前的IP地址。
    ifconfig
    
    # 备份配置文件--在修改之前，先备份原始的网络配置文件。
    sudo cp /etc/network/interfaces /etc/network/interfaces.bak
    
    # 编辑配置文件--使用文本编辑器（如nano）编辑网络配置文件。
    sudo nano /etc/network/interfaces
    
    # 在配置文件中找到对应网卡的配置部分（通常是eth0），然后修改为静态IP地址。例如：
    
    allow-hotplug eth0
    iface eth0 inet static
    address 192.168.1.100 # 设置IP地址
    netmask 255.255.255.0 # 设置子网掩码
    gateway 192.168.1.1 # 设置网关
    dns-nameservers 8.8.8.8 8.8.4.4 # 设置DNS服务器
    
    # 重启网络服务--保存并退出编辑器后，重启网络服务以使更改生效。
    sudo systemctl restart networking
    
    # 或者，在某些版本的Armbian系统中，可能需要使用以下命令：
    sudo /etc/init.d/networking restart
    
    # 验证设置--重启网络服务后，可以使用ifconfig命令再次查看网卡信息，确保IP地址、网关和DNS服务器已正确设置。
    ifconfig
    ```

    

# Ubuntu/Debian通用命令：

1. `reboot`：重启系统。

2. `apt-get update`：更新软件包列表。

3. `apt-get upgrade`：升级已安装的软件包。

4. `apt-get dist-upgrade`：升级系统中的所有软件包。

5. `apt-get autoclean`：清理已下载的软件包文件。

6. `apt-get clean`：清理软件包缓存。