---sqlplus登录 新建目录 导入时数据库文件所在目录，导出时硬盘上的文件夹作为存放导出的数据库文件
--导入导出都需执行 （创建逻辑目录）

```oracle
create or replace directory dump_dir as '/data/oracle/dump';
grant create any directory to system; 
grant read,write on directory dump_dir to system;
```

---源库导出
--全库导出

```shell
expdp system/system@orcl dumpfile=TSP_NURSE.dmp directory=dump_dir full=y logfile=TSP_NURSE.log
```

--schemas=NURSE此写法仅导入用户为nurse的数据

```shell
expdp system/system@orcl dumpfile=TSP_NURSE.dmp directory=dump_dir schemas=NURSE logfile=TSP_NURSE.log
```

--创建表空间、用户、权限
--查询替换数据库安装路径 C:\APP\ADMINISTRATOR\ORADATA\ORCL

```oracle
select file_name , tablespace_name from dba_data_files; 

create tablespace BJLD datafile '/data/oracle/oradata/orcl/BJLD.dbf' size 100m autoextend on next 10m maxsize unlimited extent management local autoallocate segment space management auto;

create user BJLD identified by BJLD default tablespace BJLD;

grant connect,resource to BJLD;

grant create session to BJLD; 
```


--目标库导入
--导入全部（不推荐，建议分用户逐步导入）

```shell
impdp system/AFprIhgCqb_520610@orcl directory=dump_dir dumpfile=2022516-bjld.dmp logfile=2022516-bjld.log full =y

impdp system/AFprIhgCqb_520610@orcl directory=dump_dir dumpfile=2022516-bjld.dmp full =y

imp system/AFprIhgCqb_520610@192.168.0.249/orcl file="/data/oracle/dump/2022516-bjld.dmp" full =y
```

--导入指定用户
--schemas=NURSE此写法仅导入用户为BJLD的数据

```shell
impdp system/AFprIhgCqb_520610@orcl directory=dump_dir dumpfile=2022516-bjld.dmp logfile=2022516-bjld.log schemas=BJLD
```

