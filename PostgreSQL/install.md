```shell
#!/bin/bash
# 编写时间：2022/08/26
# 编写时间：2022/08/26
echo "正在安装PostgreSQL，请稍等
************************************"
rpm -Uvh ./packages/*rpm || rpm -Uvh --force --nodeps ./packages/*rpm
if [ $? -eq 0 ]; then
  echo "PostgreSQL安装成功"
  # 初始化数据库并启用自动启动：
postgresql-12-setup initdb && echo "PostgreSQL数据库初始化成功"
# /usr/pgsql-12/bin/postgresql-12-setup initdb
systemctl enable postgresql-12 && echo "PostgreSQL数据库设置开机启动成功"
systemctl start postgresql-12 && echo "PostgreSQL数据库已经启动"
else
  echo "PostgreSQL安装失败"
fi
# 备份/var/lib/pgsql/12/data/下 postgresql.conf、pg_hba.conf
mv /var/lib/pgsql/12/data/postgresql.conf /var/lib/pgsql/12/data/postgresql.conf.back && echo "备份postgresql.conf成功"
mv /var/lib/pgsql/12/data/pg_hba.conf /var/lib/pgsql/12/data/pg_hba.conf.back && echo "备份pg_hba.conf成功"
# 移动postgresql.conf、pg_hba.conf文件到 /var/lib/pgsql/12/data/下
mv ./postgresql.conf /var/lib/pgsql/12/data/ && echo "移动postgresql.conf成功"
mv ./pg_hba.conf /var/lib/pgsql/12/data/ && echo "移动pg_hba.conf成功"
# 重启服务
systemctl restart postgresql-12 && echo "重启服务成功"
# 开启防火墙端口
firewall-cmd --zone=public --add-port=5432/tcp --permanent && firewall-cmd --reload
echo "
以下步骤为手动操作步骤
*********************
su postgres 切换
进入数据库
psql -U postgres
修改密码
 \password
进入数据库后查询版本
select version();
*********************
"
```