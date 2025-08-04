# import pandas as pd
# import numpy as np
#
# df_Y = pd.read_csv(r'C:\Users\10187\Desktop\YYY私募证券投资基金夏普比率_nav - 副本.csv',
#                    encoding='gbk',
#                    index_col='净值日期')
# df_Y.index = df_Y.index.astype(str)
# df_Y.index = pd.to_datetime(df_Y.index)
# df_Y['日收益率'] = df_Y['单位净值'].pct_change()
#
# df_X = pd.read_csv(r'C:\Users\10187\Desktop\XXX私募证券投资基金夏普比率_nav - 副本.csv',
#                    encoding='gbk',
#                    index_col='净值日期')
# df_X.index = df_X.index.astype(str)
# df_X.index = pd.to_datetime(df_X.index)
#
# df_X['日收益率'] = df_X['单位净值'].pct_change()
#
# x = df_X['日收益率']
# y = df_Y['日收益率']
#
#
# # 假设x和y是对齐的时间序列（pandas.Series）
# pearson_corr = x.corr(y, method='pearson')  # 皮尔逊
# spearman_corr = x.corr(y, method='spearman')  # 斯皮尔曼
#
# from statsmodels.tsa.stattools import ccf
# import matplotlib.pyplot as plt
#
# # 计算滞后-5到5阶的交叉相关系数
# ccf_vals = ccf(x, y, adjusted=False)  # adjusted=False表示用总体标准差
# lags = range(-5, 6)  # 滞后阶数
#
# # 绘图
# plt.bar(lags, ccf_vals[:11])  # 取前11个值对应滞后-5到5
# plt.xlabel('滞后阶数k')
# plt.ylabel('交叉相关系数')
# plt.show()
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import ccf
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 检查可用字体并设置中文字体 - 修复版本
font_names = set()
for font_path in fm.findSystemFonts():
    try:
        # 从字体文件路径获取字体名称
        font_prop = fm.FontProperties(fname=font_path)
        font_names.add(font_prop.get_name())
    except Exception:
        continue

available_fonts = list(font_names)

# 尝试多种中文字体，确保至少有一种可用
chinese_fonts = ["SimHei", "Microsoft YaHei", "SimSun", "KaiTi", "FangSong"]
font_to_use = None

for font in chinese_fonts:
    if font in available_fonts:
        font_to_use = font
        break

if font_to_use:
    plt.rcParams["font.family"] = [font_to_use]
    print(f"使用字体: {font_to_use}")
else:
    print("警告: 未找到合适的中文字体，可能导致中文显示异常")

# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False

try:
    # 读取基金净值数据
    df_Y = pd.read_csv(r'C:\Users\10187\Desktop\YYY私募证券投资基金夏普比率_nav - 副本.csv',
                       encoding='gbk',
                       index_col='净值日期')
    df_X = pd.read_csv(r'C:\Users\10187\Desktop\XXX私募证券投资基金夏普比率_nav - 副本.csv',
                       encoding='gbk',
                       index_col='净值日期')

    # 数据预处理
    for df in [df_Y, df_X]:
        # 转换日期格式
        df.index = df.index.astype(str)
        df.index = pd.to_datetime(df.index)

        # 计算日收益率，填充NaN值（第一个值为NaN）
        df['日收益率'] = df['单位净值'].pct_change()
        df['日收益率'] = df['日收益率'].fillna(0)  # 填充第一个NaN为0

    # 提取收益率序列并对齐时间索引
    x = df_X['日收益率']
    y = df_Y['日收益率']

    # 确保两个序列的时间索引完全一致
    common_dates = x.index.intersection(y.index)
    x = x.loc[common_dates]
    y = y.loc[common_dates]

    # 计算基本相关系数
    pearson_corr = x.corr(y, method='pearson')
    spearman_corr = x.corr(y, method='spearman')

    # 计算CCF
    ccf_vals = ccf(x, y, adjusted=False)

    # 打印结果
    print(f"数据区间: {common_dates.min()} 至 {common_dates.max()}")
    print(f"有效数据点数量: {len(common_dates)}")
    print(f"皮尔逊相关系数: {pearson_corr:.4f}")
    print(f"斯皮尔曼相关系数: {spearman_corr:.4f}")

    # 可视化CCF结果
    plt.figure(figsize=(12, 6))

    # 绘制CCF柱状图
    plt.subplot(1, 2, 1)
    lags = range(-5, 6)
    plt.bar(lags, ccf_vals[:11])
    plt.title('交叉相关函数 (CCF)')
    plt.xlabel('滞后阶数')
    plt.ylabel('相关系数')
    plt.grid(True, linestyle='--', alpha=0.7)

    # 绘制收益率散点图
    plt.subplot(1, 2, 2)
    plt.scatter(x, y, alpha=0.5)
    plt.title('收益率散点图')
    plt.xlabel('XXX基金日收益率')
    plt.ylabel('YYY基金日收益率')
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print("错误: 文件未找到，请检查文件路径是否正确。")
except Exception as e:
    print(f"发生未知错误: {e}")