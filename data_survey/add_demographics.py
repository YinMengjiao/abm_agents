"""
为ACDDS数据添加人口统计信息
按照现实世界的合理逻辑生成：性别、年龄、受教育程度
"""

import pandas as pd
import numpy as np
import os

# 设置随机种子以确保可重复性
np.random.seed(42)

# 1. 读取原始数据
input_file = 'data_survey/acdds_raw_data.csv'
df = pd.read_csv(input_file)

print(f"原始数据总行数: {len(df)}")

# 2. 随机选取577个案例
sample_size = 577
if len(df) >= sample_size:
    df_sampled = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
else:
    print(f"警告：数据不足{sample_size}条，使用全部{len(df)}条数据")
    df_sampled = df.reset_index(drop=True)

print(f"抽样后数据行数: {len(df_sampled)}")

# 3. 生成年龄（14-52岁，符合现实世界的年龄分布）
# 使用加权分布：20-40岁人群更多
age_ranges = [
    (14, 19, 0.08),   # 14-19岁：8%（青少年）
    (20, 29, 0.35),   # 20-29岁：35%（年轻成年人）
    (30, 39, 0.32),   # 30-39岁：32%（中年人）
    (40, 49, 0.18),   # 40-49岁：18%（中年）
    (50, 52, 0.07),   # 50-52岁：7%（中老年）
]

ages = []
for age_min, age_max, weight in age_ranges:
    n_people = int(sample_size * weight)
    age_group = np.random.randint(age_min, age_max + 1, size=n_people)
    ages.extend(age_group)

# 如果由于四舍五入导致数量不够或超出，进行调整
ages = np.array(ages)
if len(ages) > sample_size:
    ages = ages[:sample_size]
elif len(ages) < sample_size:
    # 补充缺少的年龄（主要集中在25-40岁）
    missing = sample_size - len(ages)
    additional_ages = np.random.randint(25, 41, size=missing)
    ages = np.concatenate([ages, additional_ages])

# 打乱顺序
np.random.shuffle(ages)
df_sampled['年龄'] = ages

# 4. 生成性别（男女比例约1:1）
genders = np.random.choice(['男', '女'], size=sample_size, p=[0.5, 0.5])
df_sampled['性别'] = genders

# 5. 生成受教育程度（与年龄合理对应）
education_levels = []
for age in ages:
    if age <= 18:
        # 14-18岁：主要是初中和高中在读
        edu = np.random.choice(['低', '中'], p=[0.6, 0.4])
    elif age <= 24:
        # 19-24岁：高中到大学阶段
        edu = np.random.choice(['低', '中', '高'], p=[0.15, 0.55, 0.30])
    elif age <= 35:
        # 25-35岁：教育基本完成，中高学历较多
        edu = np.random.choice(['低', '中', '高'], p=[0.10, 0.45, 0.45])
    elif age <= 45:
        # 36-45岁：受教育程度分布更均衡
        edu = np.random.choice(['低', '中', '高'], p=[0.20, 0.50, 0.30])
    else:
        # 46-52岁：年长一代，中等教育为主
        edu = np.random.choice(['低', '中', '高'], p=[0.25, 0.55, 0.20])
    education_levels.append(edu)

df_sampled['受教育程度'] = education_levels

# 6. 添加编号
df_sampled.insert(0, '编号', range(1, sample_size + 1))

# 7. 重新排列列顺序（将人口统计信息放在最前面）
cols = ['编号', '性别', '年龄', '受教育程度'] + [col for col in df_sampled.columns if col not in ['编号', '性别', '年龄', '受教育程度']]
df_sampled = df_sampled[cols]

# 8. 保存结果
output_file = 'data_survey/acdds_with_demographics.csv'
df_sampled.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n✅ 成功生成{sample_size}个案例的人口统计信息")
print(f"\n📊 数据统计:")
print(f"   性别分布:")
print(f"   男: {(df_sampled['性别'] == '男').sum()} ({(df_sampled['性别'] == '男').mean()*100:.1f}%)")
print(f"   女: {(df_sampled['性别'] == '女').sum()} ({(df_sampled['性别'] == '女').mean()*100:.1f}%)")
print(f"\n   年龄分布:")
print(f"   平均年龄: {df_sampled['年龄'].mean():.1f}岁")
print(f"   年龄范围: {df_sampled['年龄'].min()}-{df_sampled['年龄'].max()}岁")
print(f"   14-19岁: {((df_sampled['年龄'] >= 14) & (df_sampled['年龄'] <= 19)).sum()}人")
print(f"   20-29岁: {((df_sampled['年龄'] >= 20) & (df_sampled['年龄'] <= 29)).sum()}人")
print(f"   30-39岁: {((df_sampled['年龄'] >= 30) & (df_sampled['年龄'] <= 39)).sum()}人")
print(f"   40-49岁: {((df_sampled['年龄'] >= 40) & (df_sampled['年龄'] <= 49)).sum()}人")
print(f"   50-52岁: {((df_sampled['年龄'] >= 50) & (df_sampled['年龄'] <= 52)).sum()}人")
print(f"\n   受教育程度分布:")
print(f"   低: {(df_sampled['受教育程度'] == '低').sum()} ({(df_sampled['受教育程度'] == '低').mean()*100:.1f}%)")
print(f"   中: {(df_sampled['受教育程度'] == '中').sum()} ({(df_sampled['受教育程度'] == '中').mean()*100:.1f}%)")
print(f"   高: {(df_sampled['受教育程度'] == '高').sum()} ({(df_sampled['受教育程度'] == '高').mean()*100:.1f}%)")

# 9. 验证年龄与教育的合理性
print(f"\n🔍 年龄与教育程度交叉验证:")
for age_group, label in [(14, '14-18岁'), (19, '19-24岁'), (25, '25-35岁'), (36, '36-45岁'), (46, '46-52岁')]:
    if age_group == 14:
        mask = (df_sampled['年龄'] >= 14) & (df_sampled['年龄'] <= 18)
    elif age_group == 46:
        mask = (df_sampled['年龄'] >= 46) & (df_sampled['年龄'] <= 52)
    else:
        mask = (df_sampled['年龄'] >= age_group) & (df_sampled['年龄'] <= age_group + 9)
    
    if mask.sum() > 0:
        group = df_sampled[mask]
        print(f"\n   {label} ({mask.sum()}人):")
        for edu in ['低', '中', '高']:
            count = (group['受教育程度'] == edu).sum()
            print(f"     {edu}: {count}人 ({count/mask.sum()*100:.1f}%)")

print(f"\n💾 结果已保存至: {output_file}")
