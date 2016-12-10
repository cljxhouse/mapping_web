# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, session, g, abort
from flask import request, url_for, render_template
import sys,sqlite3


reload(sys)
sys.setdefaultencoding("utf-8")
myapp = Flask(__name__)
myapp.config.from_object(__name__)

def getDB():
    if not hasattr(g, 'postgresdb'):
        #conn = connect(database='postgres', user='mapuser', password='mapuser')
        conn = sqlite3.connect(database="/Users/wujixiong/PycharmProjects/mapping.db")
        conn.text_factory = str
        conn.row_factory=sqlite3.Row
        #conn = connect(database='postgres', user='mapuser', password='mapuser', host='192.168.0.200', port='5432')
        g.postgresdb = conn
    return g.postgresdb

import mappingtool
import qaruletool
import dataapi
import repo
#import qa_rule_mgnt






