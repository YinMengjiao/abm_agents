#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成子课题研究框架信息图
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_infographic():
    # 创建画布 (宽, 高)
    width, height = 1600, 1200
    img = Image.new('RGB', (width, height), color='#FAFBFC')
    draw = ImageDraw.Draw(img)
    
    # 尝试加载中文字体
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",  # 黑体
        "C:/Windows/Fonts/simsun.ttc",  # 宋体
        "C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
    ]
    
    font_title = None
    font_header = None
    font_body = None
    font_small = None
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font_title = ImageFont.truetype(font_path, 36)
                font_header = ImageFont.truetype(font_path, 24)
                font_body = ImageFont.truetype(font_path, 18)
                font_small = ImageFont.truetype(font_path, 14)
                break
            except:
                continue
    
    if font_title is None:
        font_title = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 颜色定义
    colors = {
        'title_bg': '#1A365D',
        'sub1': '#3182CE',  # 蓝色
        'sub2': '#38A169',  # 绿色
        'sub3': '#D69E2E',  # 橙色
        'sub4': '#805AD5',  # 紫色
        'sub5': '#E53E3E',  # 红色
        'text_dark': '#2D3748',
        'text_light': '#FFFFFF',
        'arrow': '#4A5568',
        'bg_light': '#F7FAFC'
    }
    
    # 绘制标题栏
    draw.rectangle([0, 0, width, 100], fill=colors['title_bg'])
    title_text = "AI驱动的消费决策代理依赖演化研究"
    subtitle_text = "子课题研究框架"
    
    # 计算标题位置（居中）
    bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 25), title_text, fill=colors['text_light'], font=font_title)
    
    bbox = draw.textbbox((0, 0), subtitle_text, font=font_header)
    subtitle_width = bbox[2] - bbox[0]
    draw.text(((width - subtitle_width) // 2, 65), subtitle_text, fill='#A0AEC0', font=font_header)
    
    # 定义5个子课题模块
    modules = [
        {
            'title': '子课题1：Ising-D-I-B耦合模型构建',
            'color': colors['sub1'],
            'items': [
                'Ising层汉密尔顿量',
                'D-I-B决策框架',
                'AI代理推荐算法',
                '三层耦合方程',
                '相变临界条件推导'
            ],
            'pos': (50, 150)
        },
        {
            'title': '子课题2：ACDDS量表开发与实证',
            'color': colors['sub2'],
            'items': [
                '量表设计：6维度26题项',
                '小样本预测试：n=200',
                '信效度检验',
                '正式调查：n≥2000',
                'L1-L5分布数据'
            ],
            'pos': (850, 150)
        },
        {
            'title': '子课题3：多情境仿真实验',
            'color': colors['sub3'],
            'items': [
                '基线实验',
                '记忆实验',
                'AI进化实验',
                '网络结构实验',
                '代际动态实验'
            ],
            'pos': (50, 480)
        },
        {
            'title': '子课题4：干预策略设计',
            'color': colors['sub4'],
            'items': [
                '信息干预',
                '过滤气泡治理',
                '系统性风险防控',
                'AI竞争实验',
                '情境敏感性实验'
            ],
            'pos': (850, 480)
        },
        {
            'title': '子课题5：AI治理政策框架',
            'color': colors['sub5'],
            'items': [
                '平台算法透明度',
                '用户控制权保障',
                '多样性保障机制',
                '数字素养教育方案',
                '政策建议报告'
            ],
            'pos': (450, 810)
        }
    ]
    
    # 绘制模块
    module_width = 700
    module_height = 280
    
    for i, module in enumerate(modules):
        x, y = module['pos']
        
        # 绘制模块背景（圆角矩形效果）
        draw.rectangle([x, y, x + module_width, y + module_height], 
                       fill=colors['bg_light'], outline=module['color'], width=3)
        
        # 绘制模块标题栏
        draw.rectangle([x, y, x + module_width, y + 50], fill=module['color'])
        
        # 绘制标题文字
        draw.text((x + 20, y + 12), module['title'], fill=colors['text_light'], font=font_header)
        
        # 绘制项目列表
        for j, item in enumerate(module['items']):
            item_y = y + 70 + j * 40
            # 绘制圆点
            draw.ellipse([x + 25, item_y + 5, x + 35, item_y + 15], fill=module['color'])
            # 绘制文字
            draw.text((x + 45, item_y), item, fill=colors['text_dark'], font=font_body)
    
    # 绘制连接箭头
    arrow_color = colors['arrow']
    arrow_width = 4
    
    # Sub1 -> Sub2 (水平箭头)
    draw.line([750, 290, 850, 290], fill=arrow_color, width=arrow_width)
    draw.polygon([(850, 285), (850, 295), (860, 290)], fill=arrow_color)
    
    # Sub1 -> Sub3 (垂直箭头)
    draw.line([400, 430, 400, 480], fill=arrow_color, width=arrow_width)
    draw.polygon([(395, 480), (405, 480), (400, 490)], fill=arrow_color)
    
    # Sub2 -> Sub4 (垂直箭头)
    draw.line([1200, 430, 1200, 480], fill=arrow_color, width=arrow_width)
    draw.polygon([(1195, 480), (1205, 480), (1200, 490)], fill=arrow_color)
    
    # Sub3 -> Sub5 (斜箭头)
    draw.line([750, 620, 450, 810], fill=arrow_color, width=arrow_width)
    draw.polygon([(445, 805), (455, 815), (450, 810)], fill=arrow_color)
    
    # Sub4 -> Sub5 (斜箭头)
    draw.line([850, 620, 1150, 810], fill=arrow_color, width=arrow_width)
    draw.polygon([(1145, 805), (1155, 815), (1150, 810)], fill=arrow_color)
    
    # 添加底部说明
    footer_text = "研究路径：理论建模 → 量表开发 → 仿真实验 → 干预策略 → 政策框架"
    bbox = draw.textbbox((0, 0), footer_text, font=font_body)
    footer_width = bbox[2] - bbox[0]
    draw.text(((width - footer_width) // 2, 1130), footer_text, fill=colors['text_dark'], font=font_body)
    
    # 保存图片
    output_path = "c:/Users/admin/WPSDrive/2197502/WPS云盘/【科研】/【论文】ABM消费决策代理/量表/子课题研究框架信息图.png"
    img.save(output_path, 'PNG', dpi=(300, 300))
    print(f"信息图已保存至: {output_path}")
    
    return output_path

if __name__ == "__main__":
    create_infographic()
