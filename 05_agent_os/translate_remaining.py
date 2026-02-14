#!/usr/bin/env python3
"""批量翻译剩余的Python文件"""

import os
import re

# 翻译映射
TRANSLATIONS = {
    # 常见短语
    "Example demonstrating": "演示",
    "This example shows": "此示例展示",
    "This example demonstrates": "此示例演示",
    "Prerequisites:": "前置条件：",
    "Requirements:": "要求：",
    "Usage:": "使用方法：",
    "Note:": "注意：",
    "Create Example": "创建示例",
    "Run Example": "运行示例",
    
    # Agent相关
    "You are a": "你是一个",
    "You are an": "你是一个",
    "You help": "你帮助",
    "You assist": "你协助",
    "You can": "你可以",
    "Your purpose": "你的目的",
    "Your task": "你的任务",
    "Your goal": "你的目标",
    
    # 指令
    "Search the knowledge base": "搜索知识库",
    "Answer questions": "回答问题",
    "Use the": "使用",
    "Always": "始终",
    "Never": "永不",
    "When": "当",
    "If": "如果",
    
    # 描述
    "helpful assistant": "有用的助手",
    "research assistant": "研究助手",
    "content creator": "内容创作者",
    "fact checker": "事实检查员",
    
    # 动作
    "Call a remote": "调用远程",
    "Stream responses from": "从...流式传输响应",
    "Get information about": "获取有关...的信息",
    "Run all examples": "运行所有示例",
    "Connect to": "连接到",
    
    # 技术术语保持
    "Agent": "Agent",
    "Team": "团队",
    "Workflow": "工作流",
    "Knowledge": "知识库",
}

def translate_docstring(text):
    """翻译文档字符串"""
    for en, zh in TRANSLATIONS.items():
        text = text.replace(en, zh)
    return text

def process_file(filepath):
    """处理单个文件"""
    print(f"Processing: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单检查是否已翻译
    if '你是' in content or '演示' in content:
        print(f"  已翻译，跳过")
        return False
    
    # 翻译模块级文档字符串
    content = re.sub(
        r'"""([^"]{10,500})"""',
        lambda m: f'"""{translate_docstring(m.group(1))}"""',
        content,
        count=1
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ 已翻译")
    return True

# 待处理文件列表
files_to_process = [
    "remote/03_remote_agno_a2a_agent.py",
    "remote/04_remote_adk_agent.py",
    "remote/05_agent_os_gateway.py",
]

if __name__ == "__main__":
    base_dir = "/Users/cy/PycharmProjects/agno-cookbook/05_agent_os"
    os.chdir(base_dir)
    
    translated = 0
    for file in files_to_process:
        if os.path.exists(file):
            if process_file(file):
                translated += 1
    
    print(f"\n总计翻译: {translated} 个文件")
