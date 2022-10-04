# PostgreSQL部署脚本

```shell
#!/bin/bash
# 编写时间：2022/08/26
# 编写时间：2022/08/29
PostgresSQL_dir=$(cd $(dirname $0);pwd)
echo "正在安装PostgresSQL，请稍等
************************************"
rpm -Uvh ./packages/postgresql12/*rpm || rpm -Uvh --force --nodeps ./packages/postgresql12/*rpm
if [ $? -eq 0 ]; then
  echo "PostgresSQL安装成功"
  mkdir -pv /data/postgresql/pgdata
  chown -R postgres:postgres /data/postgresql/pgdata && echo "/data/postgresql/pgdata权限附加成功"
  mv ./postgresql-12.service.d /etc/systemd/system/ && echo "移动文件成功"
  # 初始化数据库并启用自动启动：
  postgresql-12-setup initdb && echo "PostgresSQL数据库初始化成功"
  # /usr/pgsql-12/bin/postgresql-12-setup initdb
  systemctl enable postgresql-12 && echo "PostgresSQL数据库设置开机启动成功"
  systemctl start postgresql-12 && echo "PostgresSQL数据库已经启动"
else
  echo "PostgresSQL安装失败"
fi
: <<!
# 备份/var/lib/pgsql/12/data/下 postgresql.conf、pg_hba.conf
mv /var/lib/pgsql/12/data/postgresql.conf /var/lib/pgsql/12/data/postgresql.conf.back && echo "备份postgresql.conf成功"
mv /var/lib/pgsql/12/data/pg_hba.conf /var/lib/pgsql/12/data/pg_hba.conf.back && echo "备份pg_hba.conf成功"
# 移动postgresql.conf、pg_hba.conf文件到 /var/lib/pgsql/12/data/下
mv ./postgresql.conf /var/lib/pgsql/12/data/ && echo "移动postgresql.conf成功"
mv ./pg_hba.conf /var/lib/pgsql/12/data/ && echo "移动pg_hba.conf成功"
!
# 备份/data/postgresql/pgdata/下 postgresql.conf、pg_hba.conf
mv /data/postgresql/pgdata/postgresql.conf /data/postgresql/pgdata/postgresql.conf.back && echo "备份postgresql.conf成功"
mv /data/postgresql/pgdata/pg_hba.conf /data/postgresql/pgdata/pg_hba.conf.back && echo "备份pg_hba.conf成功"
# 移动postgresql.conf、pg_hba.conf文件到 /data/postgresql/pgdata/下
mv ./packages/postgresql.conf /data/postgresql/pgdata/ && echo "移动postgresql.conf成功"
mv ./packages/pg_hba.conf /data/postgresql/pgdata/ && echo "移动pg_hba.conf成功"
# 重启服务
systemctl restart postgresql-12 && echo "重启服务成功"
# 开启防火墙端口
firewall-cmd --zone=public --add-port=5432/tcp --permanent && firewall-cmd --reload
echo "正在安装PostGIS3.0，请稍等
************************************"
rpm -Uvh ./packages/*.rpm || rpm -Uvh --force --nodeps ./packages/*.rpm
if [ $? -eq 0 ]; then
  echo "PostGIS3.0安装成功"
  rpm -Uvh ./packages/postgis/*.rpm || rpm -Uvh --force --nodeps ./packages/postgis/*.rpm
  # 查看安装信息
  rpm -qi postgis30_12
else
  echo "PostGIS3.0安装失败"
fi
echo "
===========================
PostgresSQL数据库配置文件路径：
/data/postgresql/pgdata/
===========================

以下步骤为手动操作步骤
*********************
# 切换到postgres
su postgres
# 进入数据库
psql -U postgres
# 修改密码
 \password
# 进入数据库后查询版本
select version();
# 数据存储默认路径
show data_directory;

# 创建扩展
CREATE EXTENSION postgis;
# 查看扩展
SELECT PostGIS_version();
*********************
"
rm -rf $PostgresSQL_dir
```