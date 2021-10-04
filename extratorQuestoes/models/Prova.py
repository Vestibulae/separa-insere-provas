
from peewee import *
from ..util.db import db


class Prova(Model):

    id = AutoField(index=True)
    prova = CharField()
    ano = SmallIntegerField()
    fase = SmallIntegerField()

    class Meta:
        database = db


db.connect()
db.create_tables([Prova])
# db.close()
