import csv
import os
from datetime import datetime

CSV_FILE = "daily_feedback.csv"

def initialize_file():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['日期', '第几天', '训练(1/0)', '营养(1/0)', '抗干扰(次数)', '关键词', 'S', '总结'])

def load_data():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
        if rows and rows[0][0] == '日期':
            return rows[1:]
        return rows

def save_rows(rows):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['日期', '第几天', '训练(1/0)', '营养(1/0)', '抗干扰(次数)', '关键词', 'S', '总结'])
        writer.writerows(rows)

def get_yes_no(prompt):
    """强制输入 1/0 或 y/n，返回 1 或 0"""
    while True:
        val = input(prompt).strip().lower()
        if val in ('1', 'y', '是', 'yes', 'true'):
            return 1
        if val in ('0', 'n', '否', 'no', 'false'):
            return 0
        print("请输入 1/0 或 y/n")

def add_today():
    rows = load_data()
    today_str = datetime.now().strftime('%Y-%m-%d')
    rows = [r for r in rows if r[0] != today_str]  # 替换今天记录

    if not rows:
        day_num = 80
    else:
        max_day = max([int(r[1]) for r in rows])
        day_num = max_day + 1

    print(f"今天是第 {day_num} 天")
    train = get_yes_no("训练完成了吗？(1/0 或 y/n): ")
    nutrition = get_yes_no("营养完成了吗？(1/0 或 y/n): ")
    
    # 抗干扰：输入数字（次数）
    while True:
        try:
            anti = int(input("抗干扰次数（数字）: "))
            break
        except ValueError:
            print("请输入数字")

    keywords = input("关键词（逗号分隔）: ")
    s_val = input("S（独立事项）: ")
    summary = input("每日总结（可选，留空）: ")

    new_row = [today_str, str(day_num), str(train), str(nutrition), str(anti), keywords, s_val, summary]
    rows.append(new_row)
    rows.sort(key=lambda x: x[0])
    save_rows(rows)

    print(f"✅ 第 {day_num} 天已保存。训练{'✅' if train else '❌'} 营养{'✅' if nutrition else '❌'} 抗干扰{anti}次")

def show_stats():
    rows = load_data()
    if not rows:
        print("暂无数据")
        return

    total = len(rows)
    train_sum = sum(int(r[2]) for r in rows)
    nutrition_sum = sum(int(r[3]) for r in rows)
    anti_sum = sum(int(r[4]) for r in rows)

    print("\n======= 📊 统计报告 =======")
    print(f"总天数: {total} 天")
    print(f"训练: 完成 {train_sum} 天，完成率 {train_sum/total*100:.1f}%")
    print(f"营养: 完成 {nutrition_sum} 天，完成率 {nutrition_sum/total*100:.1f}%")
    print(f"抗干扰: 平均 {anti_sum/total:.1f} 次/天，累计 {anti_sum} 次")

    # S 如果是数字，显示均值；否则显示最近一次
    s_values = [r[6] for r in rows]
    s_numeric = []
    for v in s_values:
        try:
            s_numeric.append(float(v))
        except ValueError:
            pass
    if s_numeric:
        print(f"S (数值) : 平均 {sum(s_numeric)/len(s_numeric):.1f}")
    else:
        print(f"S (文本) : 最近值 -> {s_values[-1] if s_values else '无'}")

    print(f"最近一条: {rows[-1][0]} 第{rows[-1][1]}天 | 关键词: {rows[-1][5]}")
    print("==========================\n")

def view_recent():
    rows = load_data()
    if not rows:
        print("无数据")
        return
    print("\n最近5条（最新在前）:")
    for r in rows[-5:][::-1]:
        train = '✅' if r[2] == '1' else '❌'
        nutrition = '✅' if r[3] == '1' else '❌'
        print(f"{r[0]} Day{r[1]} | 训练{train} 营养{nutrition} 抗干扰{r[4]}次 | S:{r[6]} | {r[7][:10] if r[7] else ''}")

if __name__ == "__main__":
    initialize_file()
    while True:
        print("\n1. 添加/更新今天")
        print("2. 查看统计")
        print("3. 查看最近5条")
        print("4. 退出程序")
        choice = input("输入数字: ")
        if choice == '1':
            add_today()
        elif choice == '2':
            show_stats()
        elif choice == '3':
            view_recent()
        elif choice == '4':
            print("文件保存在:", os.path.abspath(CSV_FILE))
            break
        else:
            print("无效输入")