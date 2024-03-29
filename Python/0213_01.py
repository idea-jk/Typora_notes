# 时薪为125，一天工作8小时，一年工作300天，如果每月花掉9000元，那么每年存储多少钱。
# 设定时薪
hourly_salary = 125
# 计算年薪
annual_salary = hourly_salary * 8 * 300
# 设定每月花费
monthly_fee = 9000
# 计算一年总花费
annual_fee = monthly_fee * 12
# 计算一年存储金额
annual_savings = annual_salary - annual_fee
# 列出一年存储金额
print('=========================================================================')
print('时薪为125，一天工作8小时，一年工作300天，如果每月花掉9000元，那么每年存储多少钱。')
print('一年存储金额', annual_savings, '元')
print('=========================================================================')
# 余数与整数
# 将9除以5的余数设定给变量x
x = 9 % 5
print('9÷5的余数:', x)
# 将9除以4的整数设定给变量y
y = 9 // 4
print('9÷4的整数:', y)
# 次方
x = 6 ** 2
y = 6 ** 6
print('6的平方:', x)
print('6的6次方:', y)
x = (6 + 8) * 26 - 100
y = 6 + 8 * 26 - 100
print('(6+8)*26-100 = ', x)
print('6+8*26-100 = ', y)
print('=========================================================================')
# 打印9*9乘法表 - 使用for-for
for i in range(1, 10):
    for j in range(1, i + 1):  # 下三角
        # for j in range(i, 10):     # 上三角
        print(f'{j}x{i}={i * j}', end='\t')
    print()
print('=========================================================================')
'''
# 打印9*9乘法表 - 使用while-while
i = 1
while i <= 9:
    j = 1
    while (j <= i):
        print(f'{i}*{j}={i*j}',end='\t')
        j += 1
    print('')
    i += 1
print('=========================================================================')
# 打印9*9乘法表 - 使用while-for
i = 1
while i <= 9:
    for j in range(1, i + 1):  # range() 函数左闭右开
        print(f'{i}*{j}={i * j}', end='\t')
    i += 1
    print()
print('=========================================================================')
'''
