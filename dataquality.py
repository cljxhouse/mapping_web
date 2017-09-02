# -*- encoding: utf-8 -*-

import pandas as pd
import numpy as np

class DataQuality :

    df_data = pd.DataFrame()
    cols = pd.DataFrame()
    pd_column=""

    def load_file(self,filename,header=0,pd_column=""):
        self.df_data = pd.read_csv(filename, header=header)
        self.pd_column=pd_column
        self.cols=pd.DataFrame({'dtype':self.df_data.dtypes})
        self.cols['con_flag']=np.where(self.cols.dtype=='object','D','C' )
        #print self.cols
        pass

    def Analyze(self, output=""):
        #获得连续变量的统计值
        st1 = self.df_data.describe()
        st1 = pd.concat([st1.T,self.cols],axis=1)
        #获得每个字段的缺失值个数
        st1['num_missing']=self.df_data.isnull().apply(lambda x:x.sum())
        #获得每个字段的零值个数
        st1['num_zero'] = self.df_data.apply(lambda x:np.equal(x,0.0).sum())
        #计算每个字段的不同值，由此可判断该字段是否唯一
        st1['num_distinct'] = self.df_data.apply(lambda x: x.value_counts().count())
        if output != "" :
            st1.to_csv(output)
        else:
            print st1
        return st1


dq = DataQuality()
dq.load_file("LoanStats_clean.csv")
df1=dq.Analyze("test1.csv")
