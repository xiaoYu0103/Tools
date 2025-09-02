import argparse
import os
import subprocess
import sys
import re

baseDir = '/Users/yu/KeyWords'  # 请替换为你的实际目录

parser = argparse.ArgumentParser(
    description='''
    文件操作工具
    支持：
      1. 用vim打开文件
      2. 使用正则查找文件内容
      3. 在文件末尾插入字符串

    用法示例：
      python script.py                # 默认打开 default.txt
      python script.py test.txt       # 用vim打开 test.txt
      python script.py test.txt -f "hello"  # 查找hello
      python script.py test.txt -f "\\d+"   # 查找数字
      python script.py test.txt -a "new line" # 末尾插入字符串
      python script.py test.txt -f "abc" -i # 忽略大小写查找
    '''
)

parser.add_argument('filename', nargs='?', default='default', help='要操作的文件名（默认: default.txt）')
parser.add_argument('-f', '--find', help='查找文件中匹配该正则表达式的行')
parser.add_argument('-i', '--ignore-case', action='store_true', help='查找时忽略大小写')
parser.add_argument('-a', '--add', help='在文件末尾插入该字符串')

args = parser.parse_args()

filename = os.path.join(baseDir, args.filename)

# 文件不存在时自动创建
if not os.path.isfile(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        pass
    print(f"文件不存在，已自动创建: {filename}")

if args.add:
    # 在文件末尾插入字符串
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(args.add + '\n')
    print(f"已在文件末尾插入: {args.add}")

elif args.find:
    # 正则查找
    flags = re.IGNORECASE if args.ignore_case else 0
    pattern = re.compile(args.find, flags)
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if pattern.search(line):
                print(line.rstrip())
else:
    # 用vim打开
    subprocess.call(['vim', filename])
