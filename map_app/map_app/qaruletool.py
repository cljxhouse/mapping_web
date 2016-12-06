# -*- coding: utf-8 -*-

from flask import request,render_template,redirect
from . import myapp, getDB

@myapp.route("/qa/list",methods=['GET', 'POST'])
def qa_list():
    cur=getDB().cursor()
    p_col_map_id = request.args.get('col_map_id', '')

    if p_col_map_id!='' :
        cur.execute("""SELECT row_to_json (t)
  FROM (SELECT a.map_name,
               a.src_sys_name,
               split_part (a.src_tab_cname, ' ', 1)   AS src_tab_cname,
               split_part (a.src_tab_name, ' ', 1)    AS src_tab_name,
               split_part (a.src_field_cname, '.', 2) AS src_field_cname,
               split_part (a.src_field_name, '.', 2)  AS src_field_name,
               'add'                                  AS action
          FROM t_col_map a
         WHERE col_map_id = %s) t"""
                ,(p_col_map_id,))
        p_model = cur.fetchone()[0]
        #p_map_name = request.args.get('mapping_name', '')
        print p_model
        return render_template("qa_list.html",model=p_model)
    else :
        return "Function Not Ready!"

@myapp.route("/qa/getQATable",methods=['GET', 'POST'])
def qa_list_table():
    cur=getDB().cursor()
    cur.execute("SELECT row_to_json(t) FROM t_qa t")
    p_model = cur.fetchall()
    #p_map_name = request.args.get('mapping_name', '')
    #print p_model
    #print p_model(0)["qa_id"]
    return render_template("qa_list_table.html",model=p_model)

@myapp.route("/qa/remove",methods=['GET', 'POST'])
def qa_remove():
    p_id = request.args.get('id', '')
    cur = getDB().cursor()
    cur.execute("delete from t_qa where qa_id=%s",(p_id,))
    getDB().commit()
    return ""


@myapp.route("/qa/rule_management",methods=['GET', 'POST'])
def qa_add_rule():
    p_qa_id = request.form['qa_id']
    p_qa_operation_cd = request.form['qa_operation_cd']
    p_map_name=request.form['map_name']
    p_src_sys_cd=request.form["src_sys_cd"]
    p_table_cname=request.form["table_cname"]
    p_table_ename=request.form["table_ename"]
    p_col_cname=request.form["col_cname"]
    p_col_ename=request.form["col_ename"]
    p_qa_type_cd=request.form["qa_type_cd"]
    p_rule_desc=request.form["rule_desc"]
    p_sql_stmt=request.form["sql_stmt"]
    p_total_rows =request.form["total_rows"]
    p_total_errors=request.form["total_errors"]

    with getDB() as dbc:
        with dbc.cursor() as cur:
            cur.execute("""insert into t_qa(map_name,src_sys_cd,table_cname, table_ename,col_cname,col_ename,
 rule_type, rule_desc, sql_stmt,
 total_rows, total_errors)
 values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" ,
                (p_map_name,p_src_sys_cd,p_table_cname,p_table_ename,p_col_cname,p_col_ename,
                 p_qa_type_cd,p_rule_desc,p_sql_stmt,p_total_rows,p_total_errors))

    return redirect("/qa/list")