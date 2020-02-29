# -*- coding: utf-8 -*-
import click

from server import app, db
from server.models import User, Task, Log, MailConfig

from datetime import datetime


@app.cli.command()
@click.option('--drop', is_flag = True, help = 'Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort = True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def insert():
    """灌数据"""
    for user in ['jack', 'jerry', 'mark']:
        newUser = User(username = user, password = "admin")
        db.session.add(newUser)
        click.echo('insert User: %s' % user)
    db.session.commit()
    for item in range(1, 11):
        newTask = Task(title = "task%s" % (item), ownerId = 1)
        db.session.add(newTask)
    db.session.commit()
    click.echo('Done.')
