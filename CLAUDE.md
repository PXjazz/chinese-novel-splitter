# Chinese Novel Splitter - 中文小说智能切片器

## 项目用途
检测超长小说 txt 文件是否超过 70 万 token，若超过则自动切片输出多个分片文件，供大模型分段阅读。

## 核心文件
- `check_file.py` - 检测文件 token 数，判断是否需要切片
- `split_novel.py` - 执行智能切片
- `novel-splitter.md` - Skill 定义文件（可安装到 ~/.claude/skills/）

## 关键参数
- 单文件上限：700,000 tokens
- 重叠窗口：200 汉字
- 中文字符 token 系数：1.5
- 切片策略：优先章节边界 → 段落边界

## 常用命令
```bash
# 检测文件
python check_file.py "小说.txt"

# 切片（默认 70 万 token）
python split_novel.py "小说.txt"

# 自定义上限切片
python split_novel.py "小说.txt" 500000
