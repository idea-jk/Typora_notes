# Linux下命令行方式导入/出MySQL数据库（sql文件）

## 1、使用mysqldump导出数据库

1.1【数据库结构+数据一起导出】

```shell
mysqldump -u 数据库连接用户名 -p 目标数据库（要导出的数据库） > 存储的文件名
mysqldump -u root -p  db_doc > 20220616.sql
```

输入密码
1.2【导出整个数据库结构（不包含数据）】
与1.1的区别在于增加一个’-d’参数，忽略数据，只导出结构

```shell
mysqldump -h localhost -uroot -p000000  -d database > dump.sql
```

## 2、将sql文件导入数据库

```shell
# 查看数据库
show databases;
# 先创建数据库
create database `db_doc`;
mysql -u 用户名 -p 要导入的数据库名 < 数据库名.sql
mysql -u root -p db_doc < 20220616.sql
```