from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import random

# 注册支持中文字符的字体
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

def generate_questions(num_questions, max_number):
    questions = []
    for _ in range(num_questions):
        # 生成两个随机数
        try:
            question = generate_question(max_number)
        except:
            # retry one more time
            question = generate_question(max_number)
        questions.append(question)
    return questions

def generate_question(max_number):
    num1 = random.randint(1, max_number)
    num2 = random.randint(1, max_number)
        
        # 生成随机的操作符（加法或减法）
    operator = random.choice(['+', '-'])
        
        # 根据操作符计算结果，并进行调整
    if operator == '+':
        result = num1 + num2
        if result > max_number:
            num1 = random.randint(0, max_number - num2)  # 调整第一个数的范围
    else:  # operator == '-'
        result = num1 - num2
        if result < 0:
            num1, num2 = num2, num1  # 交换两个数的位置

    question = f"{num1} {operator} {num2} ="
    return question

def generate_pdf(pages, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    for questions in pages:
        generate_page(c, questions)
        c.showPage()
    c.save()

def generate_page(c, questions):
    # 设置字体和字号
    font_name = 'STSong-Light'
    font_size = 14
    c.setFont(font_name, font_size)


    # 计算标题文本和商标的宽度
    title_text = "小学生 100 以内加减运算"
    trademark_text = "美丽香香口算"
    title_width = c.stringWidth(title_text, font_name, font_size)
    trademark_width = c.stringWidth(trademark_text, font_name, font_size)

    # 居中对齐标题和商标
    page_center_x = A4[0] / 2
    title_x = page_center_x - title_width / 2
    trademark_x = page_center_x - trademark_width / 2

    # 绘制标题和商标
    c.drawString(title_x, A4[1] - 0.8 * inch, title_text)
    c.setFont(font_name, 12)  # 设置字号为12用于绘制商标
    c.drawString(trademark_x, A4[1] - 1.2 * inch, trademark_text)

    # 设置字体和字号
    c.setFont("Helvetica", 12)

    # 计算每行显示的题目数量
    max_questions_per_row = 4
    num_rows = len(questions) // max_questions_per_row
    if len(questions) % max_questions_per_row != 0:
        num_rows += 1

    # 计算每个题目框的大小和位置
    margin = 0.5 * inch
    box_width = (A4[0] - 2 * margin) / max_questions_per_row
    box_height = 0.7 * inch
    x = margin
    y = A4[1] - margin - box_height - 1 * inch  # 下移 0.2 inch

    # 逐行绘制题目框，并填入题目内容
    for i in range(num_rows):
        for j in range(max_questions_per_row):
            question_index = i * max_questions_per_row + j
            if question_index >= len(questions):
                break

            # 绘制题目框
            c.rect(x, y, box_width, box_height)
            # 填入题目内容
            c.drawString(x + 5, y + 5, questions[question_index])

            x += box_width

        # 换行
        x = margin
        y -= box_height
