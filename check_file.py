import re
import os

def estimate_tokens_cn(text):
    """同上 - 估算 token 数"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', text))
    english_chars = len(re.findall(r'[a-zA-Z0-9\s]', text))
    other_chars = len(text) - chinese_chars - english_chars
    return int(chinese_chars * 1.5 + english_chars * 0.3 + other_chars * 0.5)

def smart_split_novel(filepath, max_tokens=700000, overlap_chars=200):
    """
    智能切片小说文件
    - 优先在段落边界切分
    - 尝试在章节标记处切分
    - 保持 overlap_chars 的重叠以维持上下文
    """
    
    # 读取文件
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 检测章节标记模式
    chapter_patterns = [
        r'\n\s*(第[一二三四五六七八九十百千\d]+[章回节卷部篇])',
        r'\n\s*(Chapter\s+\d+)',
        r'\n\s*([一二三四五六七八九十百千\d]+[、．.])',
        r'\n\s*(\d+[\.\、]\s+)',
    ]
    
    # 统一用换行符分割
    paragraphs = text.split('\n')
    
    chunks = []
    current_chunk_lines = []
    current_token_count = 0
    
    for i, line in enumerate(paragraphs):
        line_text = line + '\n'
        line_tokens = estimate_tokens_cn(line_text)
        
        # 检查是否在章节边界
        is_chapter_start = any(re.match(pattern, line) for pattern in chapter_patterns)
        
        # 如果当前块加上这行会超过限制
        if current_token_count + line_tokens > max_tokens and current_chunk_lines:
            # 优先在章节边界切分
            if is_chapter_start:
                chunks.append(''.join(current_chunk_lines))
                current_chunk_lines = []
                current_token_count = 0
            
            # 否则在段落边界切分
            elif current_chunk_lines:
                chunks.append(''.join(current_chunk_lines))
                # 保留最后一段作为重叠
                overlap_text = current_chunk_lines[-1][-overlap_chars:] if len(current_chunk_lines[-1]) > overlap_chars else current_chunk_lines[-1]
                current_chunk_lines = [overlap_text] if overlap_text else []
                current_token_count = estimate_tokens_cn(overlap_text) if overlap_text else 0
        
        current_chunk_lines.append(line_text)
        current_token_count += line_tokens
    
    # 保存最后一块
    if current_chunk_lines:
        chunks.append(''.join(current_chunk_lines))
    
    return chunks

def save_chunks(filepath, chunks):
    """保存分片文件"""
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_dir = os.path.dirname(filepath) or '.'
    
    saved_files = []
    for i, chunk in enumerate(chunks, 1):
        output_filename = f"{base_name}_part{i:03d}.txt"
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(chunk)
        
        chunk_tokens = estimate_tokens_cn(chunk)
        saved_files.append({
            'path': output_path,
            'filename': output_filename,
            'tokens': chunk_tokens,
            'chars': len(chunk)
        })
        
        print(f"✓ {output_filename} - {chunk_tokens:,} tokens, {len(chunk):,} 字符")
    
    return saved_files

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python split_novel.py <文件路径> [最大token数]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    max_tokens = int(sys.argv[2]) if len(sys.argv) > 2 else 700000
    
    print(f"正在切片: {filepath}")
    print(f"上限: {max_tokens:,} tokens/片\n")
    
    chunks = smart_split_novel(filepath, max_tokens)
    saved = save_chunks(filepath, chunks)
    
    print(f"\n完成！共切分为 {len(chunks)} 个文件")
    print(f"总 token 估算: {sum(s['tokens'] for s in saved):,}")
