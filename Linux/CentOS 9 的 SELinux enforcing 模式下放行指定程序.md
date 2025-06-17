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

------

### 移除在 CentOS 9 上安装的自定义 SELinux 策略模块

### 1. 列出已安装的 SELinux 模块

```bash
semodule -l
```

在输出中查找您的自定义模块名称（例如 `openlist`）

### 2. 移除指定模块

```bash
semodule -r openlist
```

或使用完整名称（如果包含版本号）：

```bash
semodule -r openlist 1.0
```

### 3. 验证移除结果

```bash
semodule -l | grep openlist
```

如果没有任何输出，表示模块已成功移除

### 额外步骤（如果需要）

#### 如果忘记模块名称

查看所有自定义模块：

```bash
semodule -l | grep -v "^base\|^abrt\|^accounts\|^acct\|^admin\|^alsa\|^apache\|^application\|^auth\|^automount\|^avahi\|^backup"
```

#### 删除策略文件源文件（可选）

```bash
rm -i /etc/selinux/local/openlist.*
```

#### 重置文件上下文

如果您之前修改了文件标签：

```bash
restore
```
