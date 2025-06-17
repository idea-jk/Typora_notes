#  CentOS 9 的 SELinux `enforcing` 模式下放行指定程序

### 1、创建自定义 SELinux 策略模块

**触发 SELinux 拒绝事件** 

运行目标程序，确保触发 SELinux 拒绝（查看日志确认）：

```bash
ausearch -m AVC -ts recent -i | grep "openlist"
```

**安装必要的 SELinux 工具包**

```bash
dnf install -y policycoreutils-python-utils setools-console
```

这个命令会安装：

- `audit2allow`：用于从审计日志生成策略模块
- `sealert`：SELinux 诊断工具
- 其他 SELinux 分析工具

### 2、**生成自定义策略模块**

**根据拒绝日志生成模块模板：**

```bash
grep "openlist" /var/log/audit/audit.log | audit2allow -M openlist
```

输出示例：

```bash
******************** 重要 ***********************
要激活这个策略包，执行：

semodule -i openlist.pp

```

### 3、**编译并加载模块**

```bash
semodule -i openlist.pp
```

### 4、**验证操作**

```bash
semodule -l | grep openlist
```

