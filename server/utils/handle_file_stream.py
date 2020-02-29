import datetime

from server import db
from server.models import Task, Other
from server.utils.handleExcel import handle_excel
from flask import g


def status_trans(status):
    """转化任务状态"""
    if status == 0:
        return '未完成'
    elif status == 1:
        return '已完成'
    elif status == 2:
        return '进行中'


def handle_file_stream():
    """处理文件流，整合今日和明日的任务
    """
    # 当天日期
    current_time = datetime.datetime.now().strftime('%Y-%m-%d')
    # 第二天日期
    tomorrow_time = (
            datetime.datetime.now() + datetime.timedelta(days = 1)
    ).strftime("%Y-%m-%d")
    # 今日任务
    today_tasks = Task.query.filter_by(time = str(current_time),
                                       ownerId = g.userId).all()
    today_task_list = []
    for item in today_tasks:
        node = dict(
            id = item.id,
            title = item.title,
            status = status_trans(item.status),
            time = datetime.datetime.now(),
            edit = False
        )
        today_task_list.append(node)
        # 未完成任务添加到明天
        if item.status != 1:
            target = Task.query.filter_by(id = item.id).first()
            if not Task.query.filter_by(title = item.title, time = tomorrow_time, ownerId = g.userId).first():
                tomorrow_task = Task(
                    title = target.title,
                    status = target.status,
                    time = tomorrow_time,
                    ownerId = g.userId
                )
                db.session.add(tomorrow_task)
                db.session.commit()

    # 明日任务
    tomorrow_tasks = Task.query.filter_by(time = str(tomorrow_time),
                                          ownerId = g.userId).all()
    tomorrow_task_list = [
        dict(
            id = item.id,
            title = item.title,
            status = status_trans(item.status),
            time = item.time,
            edit = False
        )
        for item in tomorrow_tasks
    ]

    # 问题/建议
    other = Other.query.filter_by(
        time = str(current_time),
        ownerId = g.userId
    ).first()
    if other:
        advice = other.advice
    else:
        advice = ''

    filename = '{0}-{1}.xlsx'.format(
        g.username,
        datetime.datetime.now().strftime('%Y%m%d')
    )
    file_stream = handle_excel(g.username, today_task_list, tomorrow_task_list, advice)
    return file_stream, filename
