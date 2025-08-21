```shell
# 安装依赖包
rpm -Uvh ./packages/*rpm || rpm -Uvh --force --nodeps ./packages/*rpm
# 安装gitlab
rpm -i gitlab-ce-15.0.0-ce.0.el7.x86_64.rpm


修改服务器IP
/etc/gitlab/gitlab.rb
external_url 'http://gitlab.test.domain.com:9999'

# 修改储存位置
vi /etc/gitlab/gitlab.rb
git_data_dirs -> 修改成目标位置

# 在后面加一句
git_data_dir "/data/gitlab"

# 执行配置
gitlab-ctl reconfigure

# 启动
gitlab-ctl start

# 重新启动
gitlab-ctl restart

# 重启gitlab并访问
gitlab-ctl restart
# 进入gitlab控制台
gitlab-rails console -e production

# 获得用户数据，修改用户密码
user = User.where(id: 1).first
user.password='2YkDixw6xJiD/68kCsAZBu9W9ZhGdRlT0YykDYiOvOAE=1'
user.password_confirmation='2YkDixw6xJiD/68kCsAZBu9W9ZhGdRlT0YykDYiOvOAE=1'
user.save!
quit

# 查看gitlab版本
cat /opt/gitlab/embedded/service/gitlab-rails/VERSION

# gitlab-ce初装以后，把密码放在了一个临时文件中了
# /etc/gitlab/initial_root_password
# 这个文件将在首次执行reconfigure后24小时自动删除
grep -n "Password" /etc/gitlab/initial_root_password

# 防火墙开发9999端口，并更新防火墙
firewall-cmd --zone=public --add-port=9999/tcp --permanent
firewall-cmd --reload


gitlab-ctl start                 # 启动所有 gitlab 组件；
gitlab-ctl stop                  # 停止所有 gitlab 组件；
gitlab-ctl restart               # 重启所有 gitlab 组件；
gitlab-ctl status                # 查看服务状态；
vim /etc/gitlab/gitlab.rb        # 修改gitlab配置文件；
gitlab-ctl reconfigure           # 重新编译gitlab的配置；
gitlab-rake gitlab:check SANITIZE=true --trace    # 检查gitlab；
gitlab-ctl tail                  # 查看日志；
gitlab-ctl tail nginx/gitlab_access.log
```
