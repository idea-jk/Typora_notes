```shell
docker pull gitlab/gitlab-ce
docker load < gitlab_gitlab-ce.tar
mkdir -pv /data/gitlab/config   /data/gitlab/logs   /data/gitlab/data

# 构建容器
docker run --detach \
--hostname  gitlab \
--publish 443:443  \
--publish  9999:8012  \
--publish  9998:22 \
--privileged=true  \
--name gitlab \
--restart always \
--volume /data/gitlab/config:/etc/gitlab \
--volume /data/gitlab/logs:/var/log/gitlab \
--volume /data/gitlab/data:/var/opt/gitlab \
--volume  /data/gitlab/logs/reconfigure:/var/log/gitlab/reconfigure \
gitlab/gitlab-ce:latest

# 添加配置
vi /data/gitlab/config/gitlab.rb
# 添加下面3行
cat >> /data/gitlab/config/gitlab.rb << "EOF"
###配置http协议所使用的访问地址,不加端口号默认为80
external_url 'http://127.0.0.1:8012'
###配置ssh协议所使用的访问地址和端口
gitlab_rails['gitlab_ssh_host'] = '127.0.0.1'
###此端口是run时22端口映射的9998端口
gitlab_rails['gitlab_shell_ssh_port'] = 9998
EOF

# 限制内存，在docker启动的时候配置，命令为-m 4G
docker update --memory 4096m --memory-swap -1 gitlab

# 重启gitlab
docker restart gitlab

# 更新授权
docker exec -it gitlab update-permissions

# 进入gitlab容器
docker exec -it gitlab bash

# 重新载入配置文件，并开启
gitlab-ctl reconfigure
gitlab-ctl start

# 进入gitlab控制台
gitlab-rails console -e production

# 获得用户数据，修改用户密码
user = User.where(id: 1).first
user.password='2YkDixw6xJiD/68kCsAZBu9W9ZhGdRlT0YykDYiOvOAE=1'
user.password_confirmation='2YkDixw6xJiD/68kCsAZBu9W9ZhGdRlT0YykDYiOvOAE=1'
user.save!
quit

# 重启gitlab需要等待一段时间才能访问，否则会出现502，如果出现502，
# 还有可能是内存不够的原因，建议查看docker容器的gitlab日志
docker restart gitlab

# 防火墙开发9999端口，并更新防火墙
firewall-cmd --zone=public --add-port=9999/tcp --permanent
firewall-cmd --reload
```

