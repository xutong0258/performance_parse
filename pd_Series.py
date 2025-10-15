import pandas as pd
from base.logger import *

# 创建原始 Series
s = pd.Series([10, 20, 30, 40, 50])
logger.info("原始 Series：")
logger.info(s)

# 1. 向量化运算（每个元素乘以 2）
s_new1 = s * 2
logger.info("\n向量化运算后的新 Series：")
logger.info(s_new1)

# 2. 条件修改（大于 30 的元素改为 0）
s_new2 = s.where(s <= 30, 0)  # 满足条件保留原值，不满足则替换为 0
logger.info("\n条件修改后的新 Series：")
logger.info(s_new2)

new_list = []
for idx, line in enumerate(s_new2):
    new_list.append(line)
logger.info(f'new_list:{new_list}')

new_series = pd.Series(new_list)
logger.info(f'new_series:{new_series}')
