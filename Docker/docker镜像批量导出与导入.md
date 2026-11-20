# Docker镜像批量导出与导入

#### 1、docker镜像批量导出脚本

```shell
#!/bin/bash
set -u
set -o pipefail          # 关键：docker save 失败时管道返回非零

OUTDIR=/data/project/images_back
mkdir -p "$OUTDIR"

ok=0
fail=0
failed_list=()

# 用进程替换避免 while 在子 shell 中导致统计变量丢失
while read -r img; do
    # 跳过悬空镜像
    case "$img" in
        *'<none>'*) echo "skip dangling: $img"; continue ;;
    esac

    # 文件名转换：/ -> - ，: 删除
    fname=$(echo "$img" | sed 's|/|-|g; s|:||g')
    out="$OUTDIR/${fname}.tar.gz"

    echo "==> [$(date +%T)] $img  ->  $out"
    if docker save "$img" | gzip > "$out"; then
        # 校验 gzip 完整性
        if gzip -t "$out" 2>/dev/null; then
            ok=$((ok+1))
        else
            echo "!!! gzip 校验失败: $out" >&2
            rm -f "$out"
            fail=$((fail+1)); failed_list+=("$img")
        fi
    else
        echo "!!! docker save 失败: $img" >&2
        rm -f "$out"        # 清理不完整文件
        fail=$((fail+1)); failed_list+=("$img")
    fi
done < <(docker images --format '{{.Repository}}:{{.Tag}}')

echo "----------------------------------------"
echo "完成：成功 $ok 个，失败 $fail 个"
if [ $fail -gt 0 ]; then
    printf '失败列表:\n%s\n' "${failed_list[@]}"
    exit 1
fi


```

#### 2、docker镜像批量导入脚本

```shell
#!/bin/bash
set -u
LOADDIR=/data/project/images_back
ok=0
fail=0
failed_list=()

for f in "$LOADDIR"/*.tar.gz; do
    echo "==> [$(date +%T)] Loading: $(basename "$f")"
    if docker load -i "$f"; then
        ok=$((ok+1))
    else
        fail=$((fail+1))
        failed_list+=("$f")
        echo "!!! FAILED: $f" >&2
    fi
done

echo "----------------------------------------"
echo "完成：成功 $ok 个，失败 $fail 个"
if [ $fail -gt 0 ]; then
    printf '失败列表:\n%s\n' "${failed_list[@]}"
    exit 1
fi

```

