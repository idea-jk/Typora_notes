# Linux常用命令

##### mkdir用大括号同时建立多个同级和下级目录

```shell
# 1.在当前目录下创建a  b   c三个目录.
mkdir –p {a,b,c}

# 2.在当前目录下创建father目录，并在father目录下创建child1   child2   child3三个子目录。
mkdir -p father/{child1,child2,child3}

# 3.在当前目录下创建father1  father2两个目录，并在这两个目录下分别创建child1   child2   child3三个子目录。
mkdir -p {father1,father2}/{child1,child2,child3}
```

