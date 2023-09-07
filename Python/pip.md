## pip的基本功能

```shell
# 安装
pip install pandas      
# 卸载
pip uninstall pandas

# 更新pip
python.exe -m pip install --upgrade pip

# 导出 freeze
pip freeze > requirement.txt

# 显示 show/list
pip show pandas  ##列出包的具体信息
Name: pandas
Version: 1.0.5
#Summary: Powerful data structures for data analysis, time series, and statistics
#Home-page: https://pandas.pydata.org
#Author: None
#Author-email: None
#License: BSD
#Location: c:\users\zhangyang\anaconda3\lib\site-packages
#Requires: python-dateutil, numpy, pytz
#Required-by: statsmodels, seaborn

pip list         ##列出所有的包

pip install package -i https://pypi.mirrors.ustc.edu.cn/simple/   ##使用中科大镜像源
pip install -r requirement.txt  ##安装脚本里列出的库

pip download -d ./path pyinstaller -i https://pypi.mirrors.ustc.edu.cn/simple/
# <-d ./path>的意思是将下载的文件存放到当前目录下的path文件夹里面，<-i url>的意思是从中科大镜像源下载文件。

# 使用本地索引依赖包
pip install --no-index --find-links=C:\Users\path\ pyinstaller

# 关于pipdeptree和pipreqs。
# pipdeptree可以列出一个库所需要的所有依赖库以及版本号，也可以列出哪些库依赖这个库。
# 安装pipdeptree

pip install pipdeptree

##列出依赖库
pipdeptree -p pyinstaller   
pipdeptree -p pyinstaller -r


# 使用步骤
# 1.在项目根目录下执行命令
pipreqs ./ # 报错就执行下面这条
# pipreqs ./ --encoding=utf-8
# 2.可以看到生成了requirements.txt文件
# 3.执行下面代码就会把项目用到的所有组件装上
pip3 install -r requirements.txt
```

