#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlwt
from datetime import datetime


def handleExcel(username, todayTaskList, tomorrowTaskList):
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
    CenterStyle = xlwt.XFStyle()
    CenterStyle.alignment = alignment
    CenterStyle.font = font

    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    # 头部信息
    worksheet.write_merge(0, 0, 0, 1,
            '{}日报表'.format(datetime.now().strftime('%Y年%m月%d日')), CenterStyle)
    worksheet.write_merge(1, 1, 0, 1, '提交人：{}'.format(username), CenterStyle)
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

    ColorStyle = xlwt.XFStyle()
    ColorStyle.pattern = pattern
    ColorStyle.alignment = alignment
    ColorStyle.font = font2

    worksheet.write(2, 0, '今日工作总结', ColorStyle)
    worksheet.write(2, 1, '完成情况', ColorStyle)
    # 今日工作总结标题 结束

    # 从第4行开始
    lineNumber = 3

    # 写入今日计划
    font3 = xlwt.Font()
    font3.name = '宋体'
    font3.height = 200

    ContentStyle = xlwt.XFStyle()
    ContentStyle.alignment = alignment
    ContentStyle.font = font2

    for item in todayTaskList:
        worksheet.write(lineNumber, 0, '{}'.format(item.get('task')), ContentStyle)
        worksheet.write(lineNumber, 1, '{}'.format(item.get('status')), ContentStyle)
        lineNumber += 1
    # 写入今日计划 结束


    # 明日工作计划标题
    worksheet.write(lineNumber, 0, '明日工作计划', ColorStyle)
    worksheet.write(lineNumber, 1, '预计完成情况', ColorStyle)
    # 明日工作计划标题 结束

    # 写入明日工作计划
    for item in tomorrowTaskList:
        lineNumber += 1
        worksheet.write(lineNumber, 0, '{}'.format(item.get('task')),
                ContentStyle)
        worksheet.write(lineNumber, 1, '{}'.format(item.get('status')),
                ContentStyle)
    # 写入明日工作计划 结束


    # 遇到什么问题/您有什么建议/需要什么帮助
    worksheet.write_merge(lineNumber+1, lineNumber+1, 0, 1, '遇到什么问题/您有什么建议/需要什么帮助', ColorStyle)
    worksheet.write_merge(lineNumber+2, lineNumber+4, 0, 1, '', ContentStyle)
    # 遇到什么问题/您有什么建议/需要什么帮助 结束



    # 设置单元格宽度
    worksheet.col(0).width = 25000
    worksheet.col(1).width = 10000

    workbook.save('test.xls')


if __name__ == '__main__':
    username = 'tom'
    todayTaskList = [
            {
                'task': 'task1',
                'status': '完成'
                },
            {
                'task': 'task2',
                'status': '完成'
                },
            {
                'task': 'task3',
                'status': '完成'
                }
            ]
    tomorrowTaskList = [
            {
                'task': 'task4',
                'status': ''
                },
            {
                'task': 'task5',
                'status': ''
                }
            ]
    handleExcel(username, todayTaskList, tomorrowTaskList)
