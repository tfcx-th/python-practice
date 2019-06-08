# 将文本分成文本块

# 生成器，在文本最后加空行
def lines(file):
    for line in file: yield line
    yield '\n'

# 生成器，生成单独的文本块
def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []