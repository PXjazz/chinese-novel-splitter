---
name: chinese-novel-splitter
description: 将超长小说txt文件按70万token切片，输出多个分片文件。当用户需要处理超长文本时使用此技能。
---

# 中文小说智能切片器

## 功能说明
检测 txt 文件是否超过 70 万 token，若超过则自动切片并输出多个分片文件，保证每片在安全阈值内。

## 核心参数
- **单文件上限**: 700,000 tokens（约 35-45 万汉字）
- **重叠窗口**: 200 汉字（保持上下文连贯）
- **切片策略**: 优先在段落/章节边界处切分
- **输入格式**: .txt 文件
- **输出格式**: 原文件名_part001.txt, 原文件名_part002.txt ...

## 执行流程

### 步骤 1: 读取文件并估算 token 数

使用 Python 脚本检测文件：

```python
import sys
import re
import os

def estimate_tokens_cn(text):
    """
    估算中文文本的 token 数
    中文字符: 1.5 token/字
    英文/数字: 0.3 token/字符
    其他: 0.5 token/字符
    """
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', text))
    english_chars = len(re.findall(r'[a-zA-Z0-9\s]', text))
    other_chars = len(text) - chinese_chars - english_chars
    
    return int(chinese_chars * 1.5 + english_chars * 0.3 + other_chars * 0.5)

def get_file_info(filepath):
    """获取文件信息"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    total_chars = len(text)
    estimated_tokens = estimate_tokens_cn(text)
    
    return {
        'filepath': filepath,
        'total_chars': total_chars,
        'estimated_tokens': estimated_tokens,
        'needs_split': estimated_tokens > 700000,
        'num_chunks': (estimated_tokens // 680000) + 1  # 预留对话空间
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python check_file.py <文件路径>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    info = get_file_info(filepath)
    
    print(f"文件: {info['filepath']}")
    print(f"总字符数: {info['total_chars']:,}")
    print(f"预估 Token: {info['estimated_tokens']:,}")
    print(f"是否需要切片: {'是' if info['needs_split'] else '否'}")
    if info['needs_split']:
        print(f"预计分片数: {info['num_chunks']}")
