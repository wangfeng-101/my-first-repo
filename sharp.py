# import pandas as pd
# import numpy as np
#
# df_Y = pd.read_csv(r'C:\Users\10187\Desktop\YYY私募证券投资基金夏普比率_nav - 副本.csv',
#                    encoding='gbk',
#                    index_col='净值日期')
# df_Y.index = df_Y.index.astype(str)
# df_Y.index = pd.to_datetime(df_Y.index)
#
#
# from pandas.tseries.offsets import BDay
#
# # 假设df_Y的索引是datetime类型
# # 保留所有工作日数据
# # 创建显式副本以避免 SettingWithCopyWarning
# df_trading = df_Y[df_Y.index.isin(pd.date_range(start=df_Y.index[0],
#                                                   end=df_Y.index[-1],
#                                                   freq=BDay()))].copy()
#
# # 安全地计算日收益率
# df_trading['日收益率'] = df_trading['单位净值'].pct_change()
# print(df_trading)
# # 2. 计算日样本标准差
# daily_returns = df_trading['日收益率'].dropna()
# daily_std = daily_returns.std(ddof=1)  # ddof=1 表示样本标准差
#
# # 3. 年化样本标准差
# annualized_std = daily_std * np.sqrt(252)  # 假设252个交易日
#
#
# # 计算几何年化收益率
# cumulative_return = (df_trading['单位净值'].iloc[-1] / df_trading['单位净值'].iloc[0]) - 1
#
# years = (df_trading.index[-1] - df_trading.index[0]).days / 365.25
#
# annualized_return = (1 + cumulative_return) ** (1/years) - 1
#
# # 计算夏普比率（添加此行）
# risk_free_rate = 0.016  # 年化无风险收益率1.6%
# sharpe_ratio = (annualized_return - risk_free_rate) / annualized_std
#
# # 打印结果（添加此行）
# print(f"年化收益率: {annualized_return:.2%}")
# print(f"年化标准差: {annualized_std:.2%}")
# print(f"夏普比率: {sharpe_ratio:.4f}")



import pandas as pd
import numpy as np

# 1. 读取数据
df_Y = pd.read_csv(r'C:\Users\10187\Desktop\YYY私募证券投资基金夏普比率_nav - 副本.csv',
                   encoding='gbk',
                   index_col='净值日期')
df_Y.index = pd.to_datetime(df_Y.index)  # 直接转为datetime

# 2. 计算日收益率 - 不需要筛选工作日
df_Y['日收益率'] = df_Y['单位净值'].pct_change()

# 3. 计算年化标准差
daily_returns = df_Y['日收益率'].dropna()
daily_std = daily_returns.std(ddof=1)  # 样本标准差
annualized_std = daily_std * np.sqrt(252)  # 年化波动率

# 4. 更准确的年化收益率计算
def calculate_annualized_return(daily_returns):
    """计算考虑复利的年化收益率"""
    cumulative_return = (1 + daily_returns).prod() - 1
    years = len(daily_returns) / 252  # 按交易日折算年数
    return (1 + cumulative_return) ** (1/years) - 1

annualized_return = calculate_annualized_return(daily_returns)

# 5. 计算夏普比率
risk_free_rate = 0.016  # 1.6% 年化无风险利率
sharpe_ratio = (annualized_return - risk_free_rate) / annualized_std

# 6. 打印结果
print(f"数据期间: {df_Y.index[0].date()} 至 {df_Y.index[-1].date()}")
print(f"总交易日数: {len(daily_returns)}")
print(f"年化收益率: {annualized_return:.4f} 或 {annualized_return:.2%}")
print(f"年化波动率: {annualized_std:.4f} 或 {annualized_std:.2%}")
print(f"夏普比率: {sharpe_ratio:.4f}")

# 7. 额外诊断信息
print("\n诊断信息:")
print(f"日收益率均值: {daily_returns.mean():.6f}")
print(f"日收益率标准差: {daily_std:.6f}")
print(f"最大单日涨幅: {daily_returns.max():.4f}")
print(f"最大单日跌幅: {daily_returns.min():.4f}")

