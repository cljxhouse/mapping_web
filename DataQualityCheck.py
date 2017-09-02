# -*- coding:utf-8 -*-
# 这段代码主要的功能是把读取dq检查的配置文件
# lastdate:2011-8-15 14:21 version 1.1
import os
import sys
# import codecs
# import xlrd
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf-8')

# table_dict={}#存放表名和表的路径
# dq_dict={}#存放表的数据质量检查规则
df_tab = pd.DataFrame()
df_dq = pd.DataFrame()
df_code_cfg = pd.DataFrame()
df_data = pd.DataFrame()
df_code = pd.DataFrame()


# def readConfig(ConfigXlsFile):
#    data = xlrd.open_workbook(ConfigXlsFile)
#    index = data.sheet_by_name(u"索引")
#    rs = index.nrows
#    for r in range(1,rs):
#        #print(r)
#        #print (index.cell_value(r,0), "==>", index.cell_value(r,1))
#        table_dict[index.cell_value(r,0)]=index.cell_value(r,1)
#    #print(table_dict)
#    config = data.sheet_by_name(u"配置")
#    rs = config.nrows
#    for r in range(1,rs):
#       x={}
#       x=

def readConfig(configXlsFile):
    global df_tab
    global df_dq
    global df_code_cfg
    df_tab = pd.read_excel(configXlsFile, "index")
    df_dq = pd.read_excel(configXlsFile, "config")
    df_code_cfg = pd.read_excel(configXlsFile, "code")
    # print(df_tab)
    # print(df_dq)
    # return df_tab,df_dq


def checkDataQuality():
    loadCodeData(df_code_cfg.iat[0, 0])
    for r in range(len(df_tab)):
        # print ("jxk:",r)
        # print(df_tab.loc[r])
        tab_name = df_tab.iat[r, 0]
        tab_path = df_tab.iat[r, 1]
        print("检查表:", tab_name)
        # print(df_tab.iat[r,0])
        # print(df_tab.iat[r,1])
        loadData(tab_path)
        analyzeDataDescribe()
        analyzeDataMissing()
        analyzeFrequency(tab_name)
        analyerCode(tab_name)
    return 1


def loadCodeData(fileName):
    global df_code
    df_code = pd.read_csv(fileName)
    # print(df_code)


# 连续变量分析
def analyzeDataDescribe():
    print("\r\n连续变量分析")
    print(df_data.describe())


# 缺失值分析
def analyzeDataMissing():
    print("\r\n缺失值分析")
    print(df_data.apply(num_missing, axis=0))


# 离散变量频数分析
def analyzeFrequency(tabName):
    print("\r\n离散变量频数分析")
    df_freq_col = df_dq[(df_dq.TABLE == tabName) & (df_dq.IS_CAT == "离散")]
    # print(df_freq_col);
    for r in range(len(df_freq_col)):
        b = df_data.groupby(df_freq_col.iat[r, 1]).size()
        print("\r\n", b)


# 值域检查
def analyerCode(tabName):
    print("\r\n值域检查")
    df_code_col = df_dq[(df_dq["表名"] == tabName) & pd.isnull(df_dq["值域检查"]) == False]
    for r in range(len(df_code_col)):
        col = df_code_col.iat[r, 1]
        code = df_code_col.iat[r, 6]
        df_code_sub = df_code[df_code["代码类型"] == code]["数据项"]
        df_code_sub.columns = [col]
        # print(col)
        # print (df_code_sub)
        # print ("------------")
        # dtype(
        err_data = df_data[~df_data[col].isin(df_code_sub)]
        print(err_data)
        # print(df_code_col)
        # return 1


# 缺失值的统计
def num_missing(x):
    return sum(x.isnull())


def loadData(fileName):
    global df_data
    df_data = pd.read_csv(fileName)


def main():
    #config_file=
    readConfig('dq_template.xlsx')
    checkDataQuality()
    # print(df_tab)
    # print(df_dq)
    # print(df_dq.loc[1:3, ['表名', '字段名']])
    # a=['表名', '字段名']
    # ccc=df_dq.loc[:,a]
    # print('----')
    # print(ccc)
    # print('----')
    # print(len(ccc))
    # datafile


if __name__ == "__main__":
    main()