# -*- coding: utf-8 -*-

from flask import request, render_template, redirect, url_for, abort
import json
from . import myapp, getDB
import time


@myapp.route('/data/maplist', methods=['GET', 'POST'])
def listMapNames():
    conn = getDB()
    cur = conn.cursor()
    filter = request.form['map_name']
    s1 = ''
    if filter != "":
        s1 = "Where upper(t.map_name) like '%" + filter + "%'"
    sql_str = '''
      select * from t_tab_map t
    ''' + s1 + ' order by t.map_name'
    cur.execute(sql_str)
    data = []
    data_rows = cur.fetchall()

    for single_row in data_rows:
        # print single_row['map_name']
        data.append({'map_name': single_row['map_name'],
                     'tgt_tab_name': single_row['tgt_tab_name'],
                     'user_name': single_row['user_name'],
                     'last_save_time': single_row['last_save_time']})
    return json.dumps(data, ensure_ascii=False)


@myapp.route('/data/mapdetail', methods=['GET', 'POST'])
def getMapDetail():
    map_name = request.form['map_name']
    conn = getDB()
    cur = conn.cursor()
    data = {}
    # add map header
    cur.execute(''' select * FROM t_tab_map
    WHERE map_name=?''', (map_name,))
    r = cur.fetchone()
    data['map'] = {'tgt_sys_name': r['tgt_sys_name'],
                   'tgt_tab_name': r['tgt_tab_name'],
                   'mapping_version': r['mapping_version'],
                   'user_name': r['user_name'],
                   'mapping_status': r['mapping_status'],
                   'map_name': r['map_name']
                   }

    # add columns
    cur.execute('''select
   ifnull(col_map_id      ,'') col_map_id ,
   ifnull(tgt_sys_name    ,'') tgt_sys_name,
   ifnull(tgt_tab_name    ,'') tgt_tab_name,
   ifnull(tgt_tab_cname   ,'') tgt_tab_cname,
   ifnull(tgt_field_name  ,'') tgt_field_name,
   ifnull(tgt_field_cname ,'') tgt_field_cname,
   ifnull(tgt_field_type  ,'') tgt_field_type,
   ifnull(isprimary       ,'') isprimary,
   ifnull(col_order       ,'') col_order,
   ifnull(src_sys_name    ,'') src_sys_name,
   ifnull(src_tab_name    ,'') src_tab_name   ,
   ifnull(src_tab_cname   ,'') src_tab_cname  ,
   ifnull(src_field_name  ,'') src_field_name ,
   ifnull(src_field_cname ,'') src_field_cname,
   ifnull(map_rule        ,'') map_rule       ,
   ifnull(map_rule_desc   ,'') map_rule_desc  ,
   ifnull(map_status      ,'') map_status     ,
   ifnull(map_name        ,'') map_name       ,
   ifnull(mapping_version ,'') mapping_version,
   ifnull(standard        ,'') standard
from t_col_map
    WHERE map_name=? order by col_order''', (map_name,))
    r = cur.fetchall()

    # first initialize the list
    # then append each row
    data['columns'] = []
    for r1 in r:
        data['columns'].append(
            {
                'tgt_sys_name': r1['tgt_sys_name'],
                'tgt_tab_cname': r1['tgt_tab_cname'],
                'tgt_field_cname': r1['tgt_field_cname'],
                'tgt_tab_name': r1['tgt_tab_name'],
                'tgt_field_name': r1['tgt_field_name'],
                'tgt_field_type': r1['tgt_field_type'],
                'isprimary': r1['isprimary'],
                'src_sys_name': r1['src_sys_name'],
                'src_tab_cname': r1['src_tab_cname'],
                'src_tab_name': r1['src_tab_name'],
                'src_field_cname': r1['src_field_cname'],
                'src_field_name': r1['src_field_name'],
                'map_rule': r1['map_rule'],
                'map_rule_desc': r1['map_rule_desc'],
                'map_status': r1['map_status']
            }
        )

    # add table lists
    cur.execute('''select
   ifnull(src_sys_name          ,'') AS   src_sys_name         ,
   ifnull(src_tab_name          ,'') AS   src_tab_name         ,
   ifnull(tab_order             ,'') AS   tab_order            ,
   ifnull(join_condition        ,'') AS   join_condition       ,
   ifnull(join_condition_desc   ,'') AS   join_condition_desc  ,
   ifnull(filter_condition      ,'') AS   filter_condition     ,
   ifnull(filter_condition_desc ,'') AS   filter_condition_desc,
   ifnull(comments              ,'') AS   comments             ,
   ifnull(tgt_sys_name          ,'') AS   tgt_sys_name         ,
   ifnull(tgt_tab_name          ,'') AS   tgt_tab_name         ,
   ifnull(map_name              ,'') AS   map_name             ,
   ifnull(src_tab_id            ,'') AS   src_tab_id           ,
   ifnull(mapping_version       ,'') AS   mapping_version
   from
      t_src_table
     WHERE map_name=? order by tab_order''', (map_name,))
    r = cur.fetchall()

    # first initialize the list, then append
    data['sources'] = []
    for r1 in r:
        data['sources'].append(
            {
                'src_sys_name': r1['src_sys_name'],
                'src_tab_name': r1['src_tab_name'],
                'join_condition': r1['join_condition'],
                'join_condition_desc': r1['join_condition_desc'],
                'filter_condition': r1['filter_condition'],
                'filter_condition_desc': r1['filter_condition_desc'],
                'comments': r1['comments']
            }
        )
    return json.dumps(data, ensure_ascii=False)


@myapp.route('/data/mapsubmit', methods=['GET', 'POST'])
def submit_map():
    # 兴凯完成此函数,处理excel提交的数据
    # 传递的数据可以是自由的json格式
    # 数据包包括三个头部信息,map,columns,sources
    # if request.method == 'POST' :
    a = request.get_data()
    dict1 = json.loads(a)
    print dict1["col_map"]
    print "--------------------------------------------------------"
    print json.dumps(dict1["TGT_SYS_NAME"], ensure_ascii=False)
    print dict1["TGT_SYS_NAME"]
    print json.dumps(dict1["col_map"], ensure_ascii=False)
    print json.dumps(dict1["src_table"], ensure_ascii=False)
    p_TgtSysName = dict1["TGT_SYS_NAME"]
    p_TgtTabName = dict1["TGT_TAB_NAME"]
    p_MapName = dict1["MAP_NAME"]
    p_MappingVersion = dict1["MAPPING_VERSION"]

    p_MappingStatus = dict1["MAPPING_STATUS"]
    p_LastSaveTime = dict1["LAST_SAVE_TIME"]
    p_UserName = dict1["USER_NAME"]

    # 逻辑如下
    # 获得传送过来的数据包
    # map_detail = request.form['map_detail']
    # 操作数据库
    # conn = getDB()
    cur = getDB().cursor()
    cur.execute(
        "delete  from T_TAB_MAP where TGT_SYS_NAME='%s' and TGT_TAB_NAME='%s' and MAP_NAME ='%s' and mapping_version='%s'" % (
            p_TgtSysName, p_TgtTabName, p_MapName, p_MappingVersion))
    cur.execute(
        "insert into T_TAB_MAP(TGT_SYS_NAME,TGT_TAB_NAME,MAPPING_VERSION,MAPPING_STATUS,USER_NAME,LAST_SAVE_TIME,MAP_NAME) values('%s','%s','%s','%s','%s',date('now') ,'%s')"
        % (p_TgtSysName, p_TgtTabName, p_MappingVersion, p_MappingStatus, p_UserName, p_MapName))
    print "######################################################"
    print (
        "delete  from T_TAB_MAP where TGT_SYS_NAME=%s and TGT_TAB_NAME=%s and MAP_NAME =%s and mapping_version=%s" % (
            p_TgtSysName, p_TgtTabName, p_MapName, p_MappingVersion))
    print "######################################################"
    print (
        "insert into T_TAB_MAP(TGT_SYS_NAME,TGT_TAB_NAME,MAPPING_VERSION,MAPPING_STATUS,USER_NAME,LAST_SAVE_TIME,MAP_NAME) values(%s,%s,%s,%s,%s,date('now') ,%s)"
        % (p_TgtSysName, p_TgtTabName, p_MappingVersion, p_MappingStatus, p_UserName, p_MapName))
    getDB().commit()
    # 检查映射是否存在,如果不存在,返回映射不存在,直接退出
    # 如果映射存在,则继续插入

    # 更新mapping header部分数据,仅更新时间和用户,其他不更新.

    # 清空并插入mapping columns部分数据

    # 清空并插入关联关系部分数据

    # 如果插入成功,返回成功信息,否则返回失败信息
    return "A message"


@myapp.route('/data/mapcreate', methods=['GET', 'POST'])
def create_map():
    conn = getDB()
    cur = conn.cursor()
    mapname = request.args.get('map_name', '')
    tabname = request.args.get('tab_name', '')
    username = request.args.get('user_name', '')
    lastsavetime = time.strftime('%Y%m%d', time.localtime(time.time()))

    data = {}
    if mapname != "":
        cur.execute(''' select 1 FROM t_tab_map
      WHERE map_name=?''', (mapname,))
        r = cur.fetchone()
    if r == "1":
        return "same mapping already exists!"
    else:
        data['map'] = {'tgt_sys_name': "RDM",
                       'tgt_tab_name': tabname,
                       'mapping_version': "1",
                       'mapping_status': "新增",
                       'user_name': username,
                       'last_save_time': lastsavetime,
                       'map_name': mapname
                       }
        cur.execute('''select * from t_column
        where tab_name=? order by col_position''', (tabname,))
        r = cur.fetchall
        for r1 in r:
            i = 1
            data['column'].append = {'tgt_sys_name': "RDM",
                                     'tgt_tab_name': r1['tab_name'],
                                     'tgt_tab_cname': r1['tab_ch_name'],
                                     'tgt_field_name': r1['col_name'],
                                     'tgt_field_cname': r1['col_ch_name'],
                                     'tgt_field_type': r1['dtype'],
                                     'isprimary': r1['isprimary'],
                                     'col_order': i
                                     }
            i = i + 1
        return json.dumps(data, ensure_ascii=False)
        return "SUCCESS"
