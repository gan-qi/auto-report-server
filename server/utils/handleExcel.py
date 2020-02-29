#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlwt
from io import BytesIO
from datetime import datetime


def handle_excel(name, today_task_list, tomorrow_task_list, user_advice):
    # 居中
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER

    # 前两行标题
    # 标题字体
    font = xlwt.Font()
    font.name = '宋体'
    font.bold = True
    font.height = 500

    # 头两行样式：居中、字体设置
    center_style = xlwt.XFStyle()
    center_style.alignment = alignment
    center_style.font = font

    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    # 头部信息
    worksheet.write_merge(0, 0, 0, 1,
                          '{}日报表'.format(datetime.now().strftime('%Y年%m月%d日')), center_style)
    worksheet.write_merge(1, 1, 0, 1, '提交人：{}'.format(name), center_style)
    # 前两行标题 结束

    # 今日工作总结标题
    # 添加背景颜色且居中
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 30

    # 字体
    font2 = xlwt.Font()
    font2.name = '宋体'
    font2.height = 350

    color_style = xlwt.XFStyle()
    color_style.pattern = pattern
    color_style.alignment = alignment
    color_style.font = font2

    worksheet.write(2, 0, '今日工作总结', color_style)
    worksheet.write(2, 1, '完成情况', color_style)
    # 今日工作总结标题 结束

    # 从第4行开始
    line_number = 3

    # 写入今日计划
    font3 = xlwt.Font()
    font3.name = '宋体'
    font3.height = 200

    content_style = xlwt.XFStyle()
    content_style.alignment = alignment
    content_style.font = font2

    for item in today_task_list:
        worksheet.write(line_number, 0, '{}'.format(item.get('title')), content_style)
        worksheet.write(line_number, 1, '{}'.format(item.get('status')), content_style)
        line_number += 1
    # 写入今日计划 结束

    # 明日工作计划标题
    worksheet.write(line_number, 0, '明日工作计划', color_style)
    worksheet.write(line_number, 1, '预计完成情况', color_style)
    # 明日工作计划标题 结束

    # 写入明日工作计划
    if len(tomorrow_task_list) == 0:
        line_number += 1
        worksheet.write(line_number, 0, '无', content_style)
        worksheet.write(line_number, 1, '无', content_style)
    else:
        for item in tomorrow_task_list:
            line_number += 1
            worksheet.write(line_number, 0, '{}'.format(item.get('title')),
                            content_style)
            worksheet.write(line_number, 1, '', content_style)
    # 写入明日工作计划 结束

    # 遇到什么问题/您有什么建议/需要什么帮助
    worksheet.write_merge(line_number + 1, line_number + 1, 0, 1, '遇到什么问题/您有什么建议/需要什么帮助', color_style)
    worksheet.write_merge(line_number + 2, line_number + 4, 0, 1, user_advice, content_style)
    # 遇到什么问题/您有什么建议/需要什么帮助 结束

    # 设置单元格宽度
    worksheet.col(0).width = 25000
    worksheet.col(1).width = 10000

    output_file_stream = BytesIO()
    workbook.save(output_file_stream)
    output_file_stream.seek(0)
    return output_file_stream


if __name__ == '__main__':
    username = 'tom'
    todayTaskList = [
        {
            'title':  'task1',
            'status': '完成'
        },
        {
            'title':  'task2',
            'status': '完成'
        },
        {
            'title':  'task3',
            'status': '完成'
        }
    ]
    tomorrowTaskList = [
        {
            'title':  'task4',
            'status': ''
        },
        {
            'title':  'task5',
            'status': ''
        }
    ]
    advice = 'hello'
    file_stream = handle_excel(username, todayTaskList, tomorrowTaskList, advice)
