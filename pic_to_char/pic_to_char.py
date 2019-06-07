from PIL import Image
import argparse

# 构建命令行输入参数处理 ArgumentParser 实例
parser = argparse.ArgumentParser()

# 定义输入文件
parser.add_argument('file')
# 定义输出文件
parser.add_argument('-o', '--output')
# 定义输出字符画的宽和高
parser.add_argument('--width', type = int, default = 140)
parser.add_argument('--height', type = int, default = 80)

# 解析并获取参数
args = parser.parse_args()

# 输入的图片文件路径
IMG = args.file

# 输出字符画的宽度
WIDTH = args.width

# 输出字符画的高度
HEIGHT = args.height

# 输出字符画的路径
OUTPUT = args.output

# 字符画所使用的字符集
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
print(len(ascii_char))
# RGB转字符
def get_char(r, g, b, alpha = 256):

    # 判断 alpha 值
    if alpha == 0:
        return ' '

    # 获取字符集的长度
    length = len(ascii_char)

    # 将 RGB 值转换为灰度值
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = 256 / length
    return ascii_char[int(gray/unit)]


# 处理图片
if __name__ == '__main__':
    
    # 打开图片并调整宽高
    im = Image.open(IMG)
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)

    txt = ""
    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j, i)))
        txt += '\n'
    print(txt)

    # 字符画输出到文件
    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(txt)
    else:
        with open("output.txt", 'w') as f:
            f.write(txt)