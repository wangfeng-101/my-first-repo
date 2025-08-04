import pandas as pd
import numpy as np

df_Y = pd.read_csv(r'C:\Users\10187\Desktop\XXX私募证券投资基金夏普比率_nav - 副本.csv',
                   encoding='gbk',
                   index_col='净值日期')
df_Y.index = df_Y.index.astype(str)


# # 向量法
# running_max = df_Y['累计单位净值'].expanding().max()
#
# # 计算每个时间点的回撤
# drawdown = df_Y['累计单位净值'] / running_max - 1
#
# # 找出最大回撤（最小值）
# max_drawdown = drawdown.min()
# max_drawdown_date = drawdown.idxmin()
#
# print(f"最大回撤值: {max_drawdown:.6f}")
# print(f"发生日期: {max_drawdown_date}")

#错误循环，每次更新current_max时，都会重新计算整个序列的回撤并覆盖之前的cum
# cum = []  # 明确定义变量
# current_max = 0 # 初始化当前最大值
# for value in df_Y['累计单位净值']:
#    if value > current_max:
#        current_max = value
#        cum = df_Y['累计单位净值']/current_max-1
# max_drawdown = min(cum)
# print(max_drawdown)


# 正确循环
# 正确循环法
current_max = df_Y['累计单位净值'].iloc[0]  # 正确初始化
drawdown_list = []  # 存储每个点的回撤

for value in df_Y['累计单位净值']:
    # 更新历史峰值
    if value > current_max:
        current_max = value

    # 计算当前点的回撤
    current_drawdown = value / current_max - 1
    drawdown_list.append(current_drawdown)

# 转换为Series
drawdown_series = pd.Series(drawdown_list, index=df_Y.index)

# 找到最大回撤
max_drawdown = drawdown_series.min()
max_drawdown_date = drawdown_series.idxmin()

print(f"正确循环法 - 最大回撤值: {max_drawdown:.6f}")
print(f"发生日期: {max_drawdown_date}")


