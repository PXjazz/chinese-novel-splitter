def generate_report(original_file, saved_files):
    """生成切片报告"""
    total_tokens = sum(f['tokens'] for f in saved_files)
    total_chars = sum(f['chars'] for f in saved_files)
    
    report = f"""
    📊 切片报告
    {'='*40}
    原文件: {original_file}
    分片总数: {len(saved_files)}
    总 Token 数: {total_tokens:,}
    总字符数: {total_chars:,}
    {'='*40}
    分片详情:
    """
    
    for i, f in enumerate(saved_files, 1):
        report += f"\n  [{i}] {f['filename']}"
        report += f"\n      Token: {f['tokens']:,} | 字符: {f['chars']:,}"
        report += f"\n      路径: {f['path']}"
    
    return report
