# -*- coding: utf-8 -*-

from flask import Flask,request,render_template,redirect
import  sys
from . import myapp,getDB

@myapp.route("/repo/list")
def repo_list():

    model={}
    sql = '''
       SELECT distinct t.tab_name
     FROM t_column t
    WHERE t.repo_id='RDM'
    order by 1
       '''
    sql2= """
            SELECT t.col_name,t.col_ch_name,t.col_desc,t.col_position
  FROM t_column t
 WHERE t.repo_id='RDM' and t.tab_name=?
 order by col_position"""
    cur = getDB().cursor()

    target_table = request.args.get('target_table', '')
    cur.execute(sql)
    model['tables'] = tables=cur.fetchall()

    if target_table != "":
        cur.execute( sql2 , (target_table,))
    model['rows'] = cur.fetchall()

    return render_template("repo_list.html",selected_table=target_table,model=model)

@myapp.route("/repo/DeleteRow",methods=['GET', 'POST'])
def repo_delete_row():
    t1 =request.form['target_table']
    r1 = request.form['column_name']
    p1 = request.form['position']
    with getDB() as conn:
        with conn.cursor() as cur:
            cur.execute("insert into etlmap.t_audit_log(type,table_name,column_name) values (%s,%s,%s)",("DELETE COLUMN",t1,t1))
            cur.execute("delete from etlmap.t_col_map WHERE tgt_tab_name=%s and tgt_field_name=%s and col_order=%s",(t1,r1,p1))
            cur.execute("delete from etlmap.t_column where tab_name=%s and col_name=%s and col_position=%s",(t1,r1,p1))
            cur.execute("update etlmap.t_column set col_position=col_position-1 where tab_name=%s and col_position>%s ",(t1,p1))
            cur.execute("update etlmap.t_col_map set col_order=col_order-1 where tgt_tab_name=%s and col_order>%s ",(t1,p1))
    return redirect("/repo/list?target_table="+t1)
