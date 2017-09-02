# -*- coding: utf-8 -*-

from flask import request,render_template,redirect,url_for,abort,g
from . import myapp,getDB
import sqlite3

@myapp.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgresdb'):
        g.postgresdb.close()


@myapp.route('/',methods=['GET', 'POST'] )
def main_entry():
    return redirect("/map/view")


@myapp.route('/map/show', methods=['GET', 'POST'])
def ShowMapping():
    conn = getDB()
    cur = conn.cursor()
    map_name = request.args.get('map_name', '')
    s1 = ''
    if map_name != "":
        s1 = "Where upper(t.map_name) like upper('" + map_name + "')"
    sql_str = '''
      SELECT t.src_sys_name,
       t.src_tab_name,
       ifnull(t.join_condition,''),
       ifnull(t.join_condition_desc,''),
       ifnull(t.filter_condition,''),
       ifnull(t.filter_condition_desc,''),
       ifnull(t.comments,''),
       t.tab_order
  FROM t_src_table t  ''' + s1 + " order by t.tab_order"
    # print sql_str

    cur.execute(sql_str)
    tab_row = cur.fetchall()
    # cur.close()
    tab_info = []
    isstart = True
    map_sql = ""
    where_sql = ""
    for r in tab_row:
        tab_info.append({'src_sys_name': r[0]
                            , 'src_tab_name': r[1]
                            , 'join_condition': r[2]
                            , 'join_condition_desc': r[3]
                            , 'filter_condition': r[4]
                            , 'filter_condition_desc': r[5]
                            , 'comments': r[6]
                            , 'tab_order': r[7]
                         })
        # This part try to generate SQL statement of the FROM part
        if isstart:
            map_sql = "FROM " + r[1]
            isstart = False
            where_sql = "WHERE "+r[4]
        else:
            flag1 = r[2].upper().find("LEFT")
            flag2 = r[2].upper().find("ON")

            if (flag1 != -1):  # if statement has LEFT JOIN key word
                map_sql += "\r\n LEFT JOIN " + r[1] + "  " + r[2][flag2:]
            elif (flag2 != -1):
                map_sql += "\r\n JOIN " + r[1] + "  " + r[2][flag2:]
            else:
                map_sql += "\r\n JOIN " + r[1] + "  ON " + r[2]

    sql_str = '''
          SELECT t.tgt_field_name,
       t.tgt_field_cname,
       t.src_sys_name,
       t.src_tab_name,
       t.src_tab_cname,
       t.src_field_cname,
       t.src_field_name,
       t.map_rule,
       t.map_rule_desc,
       t.map_status,
       t.col_order
  FROM t_col_map t
        ''' + s1 + ' order by t.col_order'
    # print sql_str
    cur.execute(sql_str)
    col_info = []
    col_row = cur.fetchall()
    cur.close()
    isstart = True
    sql_body = ""

    for r in col_row:
        col_info.append({
            'tgt_field_name': r[0]
            , 'tgt_field_cname': r[1]
            , 'src_sys_name': r[2]
            , 'src_tab_name': r[3]
            , 'src_tab_cname': r[4]
            , 'src_field_cname': r[5]
            , 'src_field_name': r[6]
            , 'map_rule': r[7]
            , 'map_rule_desc': r[8]
            , 'map_status': r[9]
            , 'col_order': r[10]
        })

        tmp1 = r[7]
        if r[7].strip() == "":
            tmp1 = r[6].strip()

        if tmp1.strip() == "":
            tmp1 = "''"
        tmp1 = tmp1.lower().replace('send', '')

        if isstart:
            isstart = False
            sql_body = "SELECT " + tmp1 + "     /***" + r[1] +"***/"
        else:
            sql_body += "\r\n," + tmp1+ "     /***" + r[1] +"***/"

    map_sql = sql_body + "\r\n" + map_sql + "\r\n" + where_sql

    return render_template('show_entries.html', tab_info=tab_info, col_info=col_info, map_name=map_name,
                           map_sql=map_sql)


#显示Mapping列表
#2017-1-6 jxk update
@myapp.route('/map/view', methods=['GET', 'POST'])
def ShowMappingList():
    print "ShowMappingList"
    conn = getDB()
    cur = conn.cursor()
    filter = request.args.get('keyword', '')
    tab_name = request.args.get('target_table','')
    tag= request.args.get('tag','')
    print tab_name
    #print tag

    s1 = ''
    if filter != "":
        s1 = "Where upper(t.map_name) like '%" + filter.upper() + "%'"
    sql_str = '''
      select t.map_name,t.tgt_tab_name,t.user_name,t.last_save_time,t.mapping_status
    from t_tab_map t
        ''' + s1 + ' order by t.tgt_tab_name, t.map_name'
    cur.execute(sql_str)
    maplist = []
    allmaps = cur.fetchall()

    # print cur.description
    for onerow in allmaps:
        dic = {}
        dic['map_name'] = onerow[0]
        dic['tgt_tab_name'] = onerow[1]
        dic['user_name'] = onerow[2]
        dic['last_save_time'] = onerow[3]
        dic['mapping_status'] = onerow[4]
        maplist.append(dic)

    #list tables
    sql_str ="select distinct tab_name from t_column where repo_id = 'RDM' order by tab_name"
    cur.execute(sql_str)
    tables=[]
    alltables = cur.fetchall()

    for onerow in alltables:
        dic = {}
        dic['tab_name'] = onerow[0]
        tables.append(dic)

    #list columns
    col_list = []
    if tab_name != "":
        print "get cols"
        sql_str = "select * from t_column where repo_id = 'RDM'  and tab_name= '%s' order by col_position"%(tab_name)
        cur.execute(sql_str)
        all_cols = cur.fetchall()
        for onerow in all_cols:
            dic = {}
            dic['col_position'] = onerow[5]
            dic['col_cn_name'] = onerow[6]
            dic['col_name'] = onerow[2]
            dic['dtype'] = onerow[4]
            dic['isprimary'] = onerow[8]
            dic['col_desc'] = onerow[3]
            dic['column_id'] = onerow[9]
            dic['tab_ch_name'] = onerow[1]
            col_list.append(dic)
        cur.close()
        return render_template('list_maps.html', maplist=maplist, tables=tables, col_list=col_list, tab_name=tab_name, tag=tag)

    return render_template('list_maps.html', maplist=maplist, tables=tables, tag=tag)


# 删除映射
# 2017-1-5 jxk update
@myapp.route('/map/delete', methods=['GET', 'POST'])
def DeleteMapping():
    map_name = request.args.get('map_name', '')
    if map_name != "":
        #with getDB() as conn:
        conn = getDB();
        curr = conn.cursor();
        #with conn.cursor() as curr:
        #print "delete from t_col_map where map_name ='" + map_name + "'"
        curr.execute("delete from t_col_map where map_name ='" + map_name + "'");
        curr.execute("delete from t_src_table where map_name ='" + map_name + "'");
        curr.execute("delete from t_tab_map where map_name ='" + map_name + "'");
        conn.commit();
        conn.close();
    return redirect('/')

@myapp.route('/map/update_status', methods=['GET', 'POST'])
def UpdateMappingStatusView():
    p_map_name = request.args.get('map_name', '')
    p_status = request.args.get('status', '')
    return render_template("map_update_status.html",map_name=p_map_name,status=p_status)

# 2017-1-5 jxk update
@myapp.route('/map/update_status_action', methods=['GET', 'POST'])
def UpdateMappingStatusAction():
    p_map_name = request.form['map_name']
    p_status = request.form['status']
    conn = getDB()
    curr = conn.cursor()
    try :
        #print "-------------"
        #print ("update t_tab_map set mapping_status='%s' where map_name='%s'" %(p_status, p_map_name))
        curr.execute("update t_tab_map set mapping_status='%s' where map_name='%s'"%(p_status,p_map_name))

        conn.commit()
    finally:
        return redirect("/map/view")



# 修改映射规则
@myapp.route('/map/update_rule', methods=['GET', 'POST'])
def UpdateMapRuleForm():
    map_name = request.args.get('map_name', '')
    col_order = request.args.get('col_order', '')
    if map_name == '' or col_order == '':
        return abort(401)
    else:
        conn = getDB()
        curr = conn.cursor()
        curr.execute(
                    "select map_rule, map_rule_desc,map_status from t_col_map where map_name='%s' and col_order=%s" % (
                    map_name, col_order))
        r = curr.fetchone()
        ruledata = {'map_name': map_name
            , 'col_order': col_order
            , 'map_rule': r[0]
            , 'map_rule_desc': r[1]
            ,'map_status':r[2]}
        return render_template('map_rule_update.html', ruledata=ruledata)


@myapp.route('/map/update_action', methods=['GET', 'POST'])
def UpdateMapRule():
    map_name = request.form['map_name']
    col_order = request.form['col_order']
    map_rule = request.form['map_rule']
    map_rule_desc = request.form['map_rule_desc']
    map_status = request.form['map_status']

    conn = getDB()
    curr = conn.cursor()
    curr.execute('''update t_col_map set map_rule = ?, map_rule_desc=?,map_status=?
                         where map_name=? and col_order=? ''', [map_rule, map_rule_desc,map_status, map_name, col_order]
                         )
    return redirect(url_for("ShowMapping", map_name=map_name))


@myapp.route('/map/editsource', methods=['GET', 'POST'])
def MapEditSourcePage():
    map_name = request.args.get('map_name', '')
    tab_order = request.args.get('tab_order', '')

    with getDB() as conn:
        with conn.cursor() as curr:
            curr.execute('''select join_condition,join_condition_desc,filter_condition, filter_condition_desc,
                            comments from t_src_table where map_name='%s' and tab_order=%s ''' % (
            map_name, tab_order))
            r = curr.fetchone()
            model = {'map_name': map_name
                , 'tab_order': tab_order
                , 'join_condition': r[0]
                , 'join_condition_desc': r[1]
                , 'filter_condition': r[2]
                , 'filter_condition_desc': r[3]
                , 'comments': r[4]}
    return render_template('map_source_update.html', model=model)


@myapp.route('/map/map_source_update', methods=['GET', 'POST'])
def MapSourceUpdate():
    map_name = request.form['map_name']
    tab_order = request.form['tab_order']
    j1 = request.form['join_condition']
    j2 = request.form['join_condition_desc']
    f1 = request.form['filter_condition']
    f2 = request.form['filter_condition_desc']
    c1 = request.form['comments']

    with getDB() as conn:
        with conn.cursor() as curr:
            curr.execute('''update t_src_table set join_condition = %s, join_condition_desc=%s,
                          filter_condition=%s, filter_condition_desc=%s, comments=%s
                         where map_name=%s and tab_order=%s ''', [j1, j2, f1, f2,c1,map_name, tab_order]
                         )
    return redirect(url_for("ShowMapping", map_name=map_name))


# 删除一个字段
# 2017-1-6 jxk update
@myapp.route('/repo/deleteRepoRow', methods=['GET', 'POST'])
def DeleteRepoRow():
    #print "DeleteRepoRow"
    tab_name = request.args.get('tab_name', '')
    col_name = request.args.get('col_name', '')
    column_id = request.args.get('column_id','')
    #print tab_name
    #print col_name
    if tab_name != "":
        #with getDB() as conn:
        conn = getDB();
        curr = conn.cursor();
        #with conn.cursor() as curr:
        #print "delete from t_col_map where map_name ='" + map_name + "'"
        curr.execute("delete from t_column where column_id='%s' "%(column_id))
        conn.commit();
        conn.close();
    return redirect(url_for("ShowMappingList",tag="table",target_table=tab_name))

#保存一个字段
#2017-1-7 jxk
@myapp.route('/repo/saveRepoRow', methods=['GET', 'POST'])
def SaveRepoRow():
    tab_name = request.args.get('tab_name', '')
    tab_ch_name = request.args.get('tab_ch_name','')
    col_name = request.args.get('col_name', '')
    column_id = request.args.get('column_id', '')
    col_desc = request.args.get('col_desc','')
    dtype = request.args.get('dtype','')
    col_position = request.args.get('col_position','')
    col_ch_name = request.args.get('col_ch_name','')
    isprimary = request.args.get('isprimary','')
    is_necessary = request.args.get('is_necessary','')

    print "column_id:"+column_id
    conn = getDB()
    curr = conn.cursor()

    if column_id  =="":
        #新增字段

        curr.execute("insert into t_column(repo_id,tab_ch_name,col_name,col_desc,dtype,col_position,col_ch_name,tab_name,isprimary,is_necessary)"
                     " values('RDM','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(tab_ch_name,col_name,col_desc,dtype,col_position,col_ch_name,tab_name,isprimary,is_necessary))
    else:
        #更新字段
        print ("delete from t_column where column_id='%s'"%(column_id))
        curr.execute("delete from t_column where column_id='%s'"%(column_id))
        print ("insert into t_column values('RDM','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',null)" % (
        tab_ch_name, col_name, col_desc, dtype, col_position, col_ch_name, tab_name, isprimary, column_id, is_necessary))
        curr.execute("insert into t_column values('RDM','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',null)" % (
        tab_ch_name, col_name, col_desc, dtype, col_position, col_ch_name, tab_name, isprimary, column_id, is_necessary))

    conn.commit()
    conn.close()

    return redirect(url_for("ShowMappingList",tag="table",target_table=tab_name))

#修改字段
#2017-1-7 jxk
@myapp.route('/repo/editRepoColumn', methods=['GET', 'POST'])
def RepoEditRepoColumnPage():
    column_id = request.args.get('column_id', '')
    tab_name = request.args.get('tab_name', '')
    tab_ch_name = request.args.get('tab_ch_name', '')

    #print "column_id:"+column_id
    #print "tab_name:" + tab_name

    #curr.execute("select * from t_column where column_id=%s" %(column_id))
    column_info={ }
    if column_id !="":
        conn = getDB();
        curr = conn.cursor();
        curr.execute("select * from t_column where column_id="+column_id)
        r = curr.fetchone()
        column_info = {'tab_name': tab_name, 'column_id': column_id, 'col_name': r[2], 'col_desc': r[3], 'dtype': r[4], 'col_position': r[5], 'col_ch_name': r[6], 'isprimary': r[8], 'is_necessary': r[10],'tab_ch_name':r[1]}
        conn.commit()
        conn.close()
    else:
        column_info = {'tab_name': tab_name, 'column_id': "", 'col_name': "", 'col_desc': "", 'dtype': "",'col_position': "", 'col_ch_name': "", 'isprimary': "", 'is_necessary': "",'tab_ch_name':tab_ch_name}

    return render_template('show_repo_columns.html', column_info=column_info)