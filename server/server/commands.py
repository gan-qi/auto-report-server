# -*- coding: utf-8 -*-
import click

from server import app, db
from server.models import USER, TASK, LOG, MAILCONFIG

from datetime import datetime


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def insert():
    """灌数据"""
    newUser = USER(username="tom", password="admin")
    db.session.add(newUser)
    db.session.commit()
    click.echo('insert User: Tom')
    for item in range(1, 11):
        newTask=TASK(title="task%s"%(item), ownerId=1)
        db.session.add(newTask)
    db.session.commit()
    click.echo('Done.')
