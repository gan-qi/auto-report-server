#!/usr/bin/python
# -*- coding: utf-8 -*-
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr

from datetime import datetime

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendMail(path, settings):
    """发送邮件

    :path: 文件路径
    :path type: str

    :settings: 邮箱设置对象
                {
                'username': '用户名，用来生成日报信息',
                'targetUsername': '收件人',
                'from_addr': '发件人邮箱地址',
                'password': '邮箱的密钥',
                'to_addr': '收件人的地址'
                }
    """
    # 邮件发送基本信息
    [
        username,
        targetUsername,
        from_addr,
        password,
        to_addr
            ] = settings.values()
    # 获取当前时间
    current = datetime.now().strftime('%Y年%m月%d日')
    # 标题
    title='{0}{1}日报表'.format(username, str(current))
    # 输入SMTP服务器地址:
    smtp_server = 'smtp.qiye.163.com'


    msg = MIMEMultipart()
    msg['From'] = _format_addr('{0} <{1}>'.format(username, from_addr))
    msg['To'] = _format_addr('{0} <{1}>'.format(targetUsername, to_addr))
    msg['Subject'] = Header(title, 'utf-8').encode()

    # 邮件正文
    msg.attach(MIMEText(title, 'plain', 'utf-8'))

    # 添加附件
    with open(path, 'rb') as f:
        # 设置附件的MIME和文件名
        mime = MIMEBase('xlsx', 'xlsx', filename=title + '.xlsx')
        mime.add_header('Content-Disposition', 'attachment',
                filename=title +'.xlsx')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg.attach(mime)

    # 发送邮件，启用ssl加密
    server = smtplib.SMTP(smtp_server, 587)
    server.starttls()
    server.set_debuglevel(0)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


if __name__ == '__main__':
    pass
