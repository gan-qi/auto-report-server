import datetime

from server import db
from server.models import TASK
from server.handleExcel import handleExcel


def statusTrans(status):
    """转化任务状态"""
    if status == 0:
        return '未完成'
    elif status == 1:
        return '已完成'
    elif status == 2:
        return '进行中'


def handleFileStream():
    """处理文件流，整合今日和明日的任务
    """
    # 当天日期
    currentTime = datetime.datetime.now().strftime('%Y-%m-%d')
    # 第二天日期
    tomorrowTime = (
            datetime.datetime.now() + datetime.timedelta(days = 1)
    ).strftime("%Y-%m-%d")
    # 今日任务
    todayTasks = TASK.query.filter_by(time = str(currentTime),
                                      ownerId = g.userId).all()
    todayTaskList = []
    for item in todayTasks:
        node = dict(
            id = item.id,
            title = item.title,
            status = statusTrans(item.status),
            time = item.time,
            edit = False
        )
        todayTaskList.append(node)
        # 未完成任务转到明天
        if item.status != 1:
            target = TASK.query.filter_by(id = item.id).first()
            target.time = datetime.datetime.now() + datetime.timedelta(days = 1)
            db.session.commit()

    # 明日任务
    tomorrowTasks = TASK.query.filter_by(time = str(tomorrowTime),
                                         ownerId = g.userId).all()
    tomorrowTaskList = [
        dict(
            id = item.id,
            title = item.title,
            status = statusTrans(item.status),
            time = item.time,
            edit = False
        )
        for item in tomorrowTasks
    ]
    filename = '{0}-{1}.xlsx'.format(
        g.username,
        datetime.datetime.now().strftime('%Y%m%d')
    )
    fileStream = handleExcel(g.username, todayTaskList, tomorrowTaskList)
    return fileStream, filename
