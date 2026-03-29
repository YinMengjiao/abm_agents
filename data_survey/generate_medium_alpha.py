import numpy as np
import pandas as pd

print('='*70)
print('ACDDS 量表 - 生成中信度数据 (α  0.8)')
print('='*70)
print()

np.random.seed(42)
n_samples = 2000

dimensions = {
    'PU': {'items': 5, 'reverse': []},
    'PEOU': {'items': 4, 'reverse': []},
    'TR': {'items': 5, 'reverse': []},
    'AA': {'items': 5, 'reverse': [1, 3]},
    'AC': {'items': 4, 'reverse': [1]},
    'SF': {'items': 3, 'reverse': [1, 2]}
}

print('Step 1: 生成潜变量...')
latent = np.random.multivariate_normal(
    mean=[4.5, 4.3, 4.4, 4.2, 4.6, 4.0],
    cov=[[1.2, 0.5, 0.6, 0.4, 0.3, 0.2],
         [0.5, 1.1, 0.4, 0.3, 0.2, 0.3],
         [0.6, 0.4, 1.3, 0.5, 0.4, 0.3],
         [0.4, 0.3, 0.5, 1.0, 0.3, 0.2],
         [0.3, 0.2, 0.4, 0.3, 0.9, 0.4],
         [0.2, 0.3, 0.3, 0.2, 0.4, 0.8]],
    size=n_samples)
print('')
print()

print('Step 2: 生成题项得分（中等内部一致性，α0.8）...')
data = {}

for dim_idx, (dim_name, info) in enumerate(dimensions.items()):
    n_items = info['items']
    reverse_items = info['reverse']
    latent_factor = latent[:, dim_idx]
    
    print(f'{dim_name}: ', end='')
    
    for i in range(n_items):
        is_reverse = i in reverse_items
        
        # 关键：调整误差和载荷以控制α在 0.8 左右
        # 不同维度使用略微不同的参数以获得更一致的α
        if dim_name == 'SF':
            item_score = latent_factor * 1.0 + np.random.normal(0, 0.70, n_samples)
        else:
            item_score = latent_factor * 0.9 + np.random.normal(0, 0.75, n_samples)
        
        if is_reverse:
            item_score = 8 - item_score
        
        # 截尾到 1-7 范围
        item_score = np.clip(item_score, 1, 7)
        
        # 四舍五入为正整数
        item_score = np.round(item_score).astype(int)
        
        # 确保严格在 1-7 范围内
        item_score = np.clip(item_score, 1, 7)
        
        col_name = f'{dim_name}{i+1}'
        data[col_name] = item_score
        
        if is_reverse:
            print(f'{col_name}(R) ', end='')
        else:
            print(f'{col_name} ', end='')
    print()

df_raw = pd.DataFrame(data)
print(f'\n 数据：{df_raw.shape[0]}{df_raw.shape[1]}')
print(f' 数据类型：整数 (1-7)')
print()

# 反向题正向化
print('Step 3: 反向题正向化...')
df_corr = df_raw.copy()
for dim, info in dimensions.items():
    for idx in info['reverse']:
        col = f'{dim}{idx+1}'
        df_corr[col] = 8 - df_corr[col]
        print(f'   {col}')
print()

# 保存
print('Step 4: 保存数据...')
output_file = 'acdds_raw_data_2000_medium_alpha.csv'
df_raw.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f' {output_file}\n')

# 信度分析
print('='*70)
print('信度分析 (Cronbach α)')
print('='*70)

def calc_alpha(d):
    k = d.shape[1]
    return (k/(k-1)) * (1 - d.var(axis=0).sum()/d.sum(axis=1).var())

all_pass = True
for dim_name, info in dimensions.items():
    cols = [f'{dim_name}{i+1}' for i in range(info['items'])]
    alpha = calc_alpha(df_corr[cols])
    quality = '优秀 ' if alpha > 0.8 else '良好 ' if alpha > 0.7 else '不足 '
    if alpha <= 0.7:
        all_pass = False
    print(f'{dim_name:6s}: α = {alpha:.4f} ({quality})')

total_alpha = calc_alpha(df_corr)
print(f'\n总问卷：α = {total_alpha:.4f} (优秀 )')

if all_pass:
    print('\n' + '='*70)
    print(' 所有维度的α系数均大于 0.7！')
    print('='*70)

print()

# 描述统计
print('='*70)
print('描述统计')
print('='*70)
print(f'样本量：{n_samples}')
print(f'题项数：{df_raw.shape[1]}\n')

print('各维度均值标准差:')
for dim_name, info in dimensions.items():
    cols = [f'{dim_name}{i+1}' for i in range(info['items'])]
    mean_val = df_raw[cols].mean().mean()
    std_val = df_raw[cols].std().mean()
    print(f'  {dim_name}: {mean_val:.2f}  {std_val:.2f}')

print()
print('='*70)
print(' 完成！')
print('='*70)
