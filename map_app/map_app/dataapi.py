# -*- coding: utf-8 -*-

from flask import request,render_template,redirect,url_for,abort
import json
import base64
from . import myapp,getDB


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
    data_rows=cur.fetchall()

    for single_row in data_rows:
        #print single_row['map_name']
        data.append({'map_name':single_row['map_name'],
                     'tgt_tab_name': single_row['tgt_tab_name'],
                     'user_name': single_row['user_name'],
                     'last_save_time':single_row['last_save_time']})
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
    data['map'] = {'tgt_sys_name':r['tgt_sys_name'],
                   'tgt_tab_name':r['tgt_tab_name'],
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

    #first initialize the list
    #then append each row
    data['columns'] = []
    for  r1 in r:
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

    #first initialize the list, then append
    data['sources'] = []
    for r1 in r:
        data['sources'].append(
            {
                'src_sys_name':r1['src_sys_name'],
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
    #兴凯完成此函数,处理excel提交的数据
    #传递的数据可以是自由的json格式
    #数据包包括三个头部信息,map,columns,sources
	 #if request.method == 'POST' :
    a = request.get_data()
    #print a
    dict1 = json.loads(a)

    #print "--------------------------------------------------------"
    #print dict1
    #print "--------------------------------------------------------"
    #print "--------------------------------------------------------"
    #print json.dumps(dict1["TGT_SYS_NAME"], ensure_ascii=False)
    #print dict1["TGT_SYS_NAME"]
    #print json.dumps(dict1["col_map"], ensure_ascii=False)
    #print json.dumps(dict1["src_table"], ensure_ascii=False)
    p_TgtSysName = dict1["TGT_SYS_NAME"]
    p_TgtTabName = dict1["TGT_TAB_NAME"]
    p_MapName =    dict1["MAP_NAME"]
    p_MappingVersion = dict1["MAPPING_VERSION"]

    p_MappingStatus = dict1["MAPPING_STATUS"]
    #p_LastSaveTime = dict1["LAST_SAVE_TIME"]
    p_UserName = dict1["USER_NAME"]

    #col_map = json.dumps(dict1["col_map"], ensure_ascii=False)
    col_map = dict1["col_map"]
    #src_table= json.dumps(dict1["src_table"], ensure_ascii=False)
    src_table = dict1["src_table"]
    #print a
    #print dict1.keys()
    #print dict1['col_map']
    #print col_map
    #print col_map,type(col_map)
    #print col_map.items()
    #逻辑如下
    #获得传送过来的数据包
    #map_detail = request.form['map_detail']
    #操作数据库
    conn = getDB()

    try:
        cur = conn.cursor()
        #cur.execute("delete from T_TAB_MAP where TGT_SYS_NAME='%s' and TGT_TAB_NAME='%s' and MAP_NAME ='%s' and mapping_version='%s'" %(p_TgtSysName, p_TgtTabName, p_MapName, p_MappingVersion))
        #cur.execute("insert into T_TAB_MAP(TGT_SYS_NAME,TGT_TAB_NAME,MAPPING_VERSION,MAPPING_STATUS,USER_NAME,LAST_SAVE_TIME,MAP_NAME) values('%s','%s','%s','%s','%s',date('now') ,'%s')"
    #%(p_TgtSysName,p_TgtTabName,p_MappingVersion,p_MappingStatus,p_UserName,p_MapName))
        #print "######################################################"
        #print ("delete from T_TAB_MAP where TGT_SYS_NAME=%s and TGT_TAB_NAME=%s and MAP_NAME =%s and mapping_version=%s" %(p_TgtSysName, p_TgtTabName, p_MapName, p_MappingVersion))
        #print "######################################################"
        #print ("insert into T_TAB_MAP(TGT_SYS_NAME,TGT_TAB_NAME,MAPPING_VERSION,MAPPING_STATUS,USER_NAME,LAST_SAVE_TIME,MAP_NAME) values(%s,%s,%s,%s,%s,date('now') ,%s)"
    #%(p_TgtSysName,p_TgtTabName,p_MappingVersion,p_MappingStatus,p_UserName,p_MapName))

        # 检查映射是否存在,如果不存在,返回映射不存在,直接退出
        cur.execute("select count(1) as cnt from T_TAB_MAP where TGT_SYS_NAME='%s' and TGT_TAB_NAME='%s' and MAP_NAME ='%s' " %(p_TgtSysName, p_TgtTabName, p_MapName))
        r = cur.fetchone()

        if r[0]== 0:
            return "Mapping does not exist!"
        # 如果映射存在,则继续插入
        #print p_UserName
        #print p_MapName
        # 更新mapping header部分数据,仅 更新时间和用户,其他不更新.
        conn.execute("update T_TAB_MAP set LAST_SAVE_TIME= date('now'),USER_NAME = '%s' where MAP_NAME='%s'" %(p_UserName,p_MapName))

        #print r[0]


        # 清空并插入mapping columns部分数据
        cur.execute("delete from T_COL_MAP where MAP_NAME = '%s'" %(p_MapName))
        print "--------------------------------------------------------1"
        #print col_map
        print "--------------------------------------------------------11"
        for row in col_map:
            ##print type(row)
            #print "--------------------------------------------------------#"
            #print row
            #print row["TGT_SYS_NAME"]
            #print row["TGT_TAB_NAME"]
            #print row["TGT_TAB_CNAME"]
            #print row["TGT_FIELD_NAME"]
            #print row["TGT_FIELD_CNAME"]
            #print row["TGT_FIELD_TYPE"]
            #print row["ISPRIMARY"]
            #print row["COL_ORDER"]
            #print row["SRC_SYS_NAME"]
            #print row["SRC_TAB_NAME"]
            #print row["SRC_TAB_CNAME"]#
            #print row["SRC_FIELD_NAME"]
            #print row["SRC_FIELD_CNAME"]
            #print row["MAP_RULE"]
            #print row["MAP_RULE_DESC"]
            #print row["MAP_STATUS"]##
            #print row["MAP_NAME"]
            #print row["MAPPING_VERSION"]

            #row["TGT_SYS_NAME"].replace("''","''''")
            ##print 'TGT_SYS_NAME:'+row["TGT_SYS_NAME"]
            ##print 'TGT_TAB_NAME:'+row["TGT_TAB_NAME"]
            ##print 'TGT_TAB_CNAME:'+row["TGT_TAB_CNAME"]
            ##print 'TGT_FIELD_NAME:'+row["TGT_FIELD_NAME"]
            ##print 'TGT_FIELD_CNAME:'+row["TGT_FIELD_CNAME"]
            ##print 'TGT_FIELD_TYPE:'+row["TGT_FIELD_TYPE"]
            #print 'ISPRIMARY:'+row["ISPRIMARY"]
            #print 'COL_ORDER:'+row["COL_ORDER"]
            #print 'SRC_SYS_NAME:'+row["SRC_SYS_NAME"]
            #print 'SRC_TAB_NAME:'+row["SRC_TAB_NAME"]
            #print 'SRC_TAB_CNAME:'+row["SRC_TAB_CNAME"]#
            #print 'SRC_FIELD_NAME:'+row["SRC_FIELD_NAME"]
            #print 'SRC_FIELD_CNAME:'+row["SRC_FIELD_CNAME"]
            #row["MAP_RULE"].replace("'", "''")
            #print 'MAP_RULE:'+row["MAP_RULE"].replace("'", "''")
            #print 'MAP_RULE_DESC:'+row["MAP_RULE_DESC"]
            #print 'MAP_STATUS:'+row["MAP_STATUS"]
            #print 'MAP_NAME:'+row["MAP_NAME"]
            #print 'MAPPING_VERSION:'+row["MAPPING_VERSION"]
            #print "insert into T_COL_MAP(TGT_SYS_NAME, TGT_TAB_NAME, TGT_TAB_CNAME, TGT_FIELD_NAME, TGT_FIELD_CNAME, tgt_field_type, ISPRIMARY,COL_ORDER, SRC_SYS_NAME, SRC_TAB_NAME, SRC_TAB_CNAME, SRC_FIELD_NAME, SRC_FIELD_CNAME, MAP_RULE, MAP_RULE_DESC, MAP_STATUS,MAP_NAME,mapping_version) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(row["TGT_SYS_NAME"],row["TGT_TAB_NAME"],row["TGT_TAB_CNAME"],row["TGT_FIELD_NAME"],row["TGT_FIELD_CNAME"],row["TGT_FIELD_TYPE"],row["ISPRIMARY"],row["COL_ORDER"],row["SRC_SYS_NAME"],row["SRC_TAB_NAME"],row["SRC_TAB_CNAME"],row["SRC_FIELD_NAME"],row["SRC_FIELD_CNAME"],row["MAP_RULE"].replace("'", "''"),row["MAP_RULE_DESC"],row["MAP_STATUS"],row["MAP_NAME"],row["MAPPING_VERSION"])
            #print row.keys()
            #row["TGT_SYS_NAME"], row["TGT_TAB_NAME"], row["TGT_TAB_CNAME"], row["TGT_FIELD_NAME"],
            #row["TGT_FIELD_CNAME"], row["TGT_FIELD_TYPE"], row["ISPRIMARY"], row["COL_ORDER"], row["SRC_SYS_NAME"],
            #row["SRC_TAB_NAME"], row["SRC_TAB_CNAME"], row["SRC_FIELD_NAME"], row["SRC_FIELD_CNAME"], row["MAP_RULE"],
            #row["MAP_RULE_DESC"], row["MAP_STATUS"], row["MAP_NAME"], row["MAPPING_VERSION"])
            cur.execute("insert into T_COL_MAP(TGT_SYS_NAME, TGT_TAB_NAME, TGT_TAB_CNAME, TGT_FIELD_NAME, TGT_FIELD_CNAME, tgt_field_type, ISPRIMARY,COL_ORDER, SRC_SYS_NAME, SRC_TAB_NAME, SRC_TAB_CNAME, SRC_FIELD_NAME, SRC_FIELD_CNAME, MAP_RULE, MAP_RULE_DESC, MAP_STATUS,MAP_NAME,mapping_version) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(row["TGT_SYS_NAME"],row["TGT_TAB_NAME"],row["TGT_TAB_CNAME"],row["TGT_FIELD_NAME"],row["TGT_FIELD_CNAME"],row["TGT_FIELD_TYPE"],row["ISPRIMARY"],row["COL_ORDER"],row["SRC_SYS_NAME"],row["SRC_TAB_NAME"],row["SRC_TAB_CNAME"],row["SRC_FIELD_NAME"],row["SRC_FIELD_CNAME"],row["MAP_RULE"].replace("'", "''"),row["MAP_RULE_DESC"].replace("'", "''"),row["MAP_STATUS"],row["MAP_NAME"],row["MAPPING_VERSION"]))
            #print row["TGT_FIELD_CNAME"]
        print "--------------------------------------------------------2"

        #cx.commit()
        # 清空并插入关联关系部分数据
        cur.execute("delete from T_SRC_TABLE where MAP_NAME = '%s'" % (p_MapName))
        for row in src_table:
            #print "===========================1"
            #print "insert into T_SRC_TABLE(SRC_SYS_NAME,SRC_TAB_NAME,TAB_ORDER,JOIN_CONDITION,JOIN_CONDITION_DESC,FILTER_CONDITION,FILTER_CONDITION_DESC,COMMENTS,TGT_SYS_NAME,TGT_TAB_NAME,MAP_NAME,mapping_version) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(row["SRC_SYS_NAME"],row["SRC_TAB_NAME"],row["TAB_ORDER"],row["JOIN_CONDITION"],row["JOIN_CONDITION_DESC"],row["FILTER_CONDITION"],row["FILTER_CONDITION_DESC"],row["COMMENTS"],row["TGT_SYS_NAME"],row["TGT_TAB_NAME"],row["MAP_NAME"],row["MAPPING_VERSION"])
            #print "===========================2"
            cur.execute("insert into T_SRC_TABLE(SRC_SYS_NAME,SRC_TAB_NAME,TAB_ORDER,JOIN_CONDITION,JOIN_CONDITION_DESC,FILTER_CONDITION,FILTER_CONDITION_DESC,COMMENTS,TGT_SYS_NAME,TGT_TAB_NAME,MAP_NAME,mapping_version) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(row["SRC_SYS_NAME"],row["SRC_TAB_NAME"],row["TAB_ORDER"],row["JOIN_CONDITION"],row["JOIN_CONDITION_DESC"],row["FILTER_CONDITION"],row["FILTER_CONDITION_DESC"],row["COMMENTS"],row["TGT_SYS_NAME"],row["TGT_TAB_NAME"],row["MAP_NAME"],row["MAPPING_VERSION"]))

        getDB().commit()
        # 如果插入成功,返回成功信息,否则返回失败信息
        return "Mapping Saved!"
    except Exception,e:
        return Exception,":",e

#jxk
@myapp.route('/data/sync_source_list', methods=[ 'GET','POST'])
def sync_source_list():
    print "1"
    conn = getDB()
    cur = conn.cursor()

    sql_str = "select " \
              "ifnull(repo_id,'') as repo_id," \
              "ifnull(tab_ch_name,'') as tab_ch_name, " \
              "ifnull(tab_name,'')  as tab_name," \
              "ifnull(col_ch_name,'') as col_ch_name, " \
              "ifnull(col_name,'') as col_name," \
              "ifnull(dtype,'') as dtype ," \
              "ifnull(isprimary,'') as isprimary from t_column order by repo_id, tab_name/*where tab_name = 'FF_IBOUT'*/"
    print sql_str
    cur.execute(sql_str)
    data = []
    data_rows=cur.fetchall()
    return_str=''
    line_str=''
    for single_row in data_rows:
        #print single_row['map_name']
        data.append({'SRC_NAME':base64.b64encode(single_row['repo_id']),
                     'CHN_TAB_NAME':base64.b64encode(single_row['tab_ch_name']),
                     'ENGLISH_NAME':base64.b64encode(single_row['tab_name']),
                     'CHN_COL_NAME': base64.b64encode(single_row['col_ch_name']),
                     'COLUMN_NAME': base64.b64encode(single_row['col_name']),
                     'DATA_TYPE': base64.b64encode(single_row['dtype']),
                     'IS_PRIMARY':base64.b64encode(single_row['isprimary'])})
        line_str=base64.b64encode(single_row['repo_id'])+'@'+base64.b64encode(single_row['tab_ch_name'])+'@'+base64.b64encode(single_row['tab_name'])+'@'+ base64.b64encode(single_row['col_ch_name'])+'@'+ base64.b64encode(single_row['col_name'])+'@'+ base64.b64encode(single_row['dtype'])+'@'+ base64.b64encode(single_row['isprimary'])
        if return_str=='':
            return_str = line_str
        else:
            return_str=return_str+"#"+line_str
    #print data
    #print json.dumps(data, ensure_ascii=False)
    #data1 = []
    #data1.append({'data':data})
    #return json.dumps(data, ensure_ascii=False)
    return return_str

@myapp.route('/data/mapcreate', methods=['GET', 'POST'])
def create_map():
    #王超完成此函数
    #传递数据是json格式,包括映射名称,目标表,用户,时间,状态=new
    #数据库检查映射是否存在
    #数据库插入头部信息,列信息
    #如果成功则返回SUCCESS,否则返回ERROR
    return "SUCCESS"