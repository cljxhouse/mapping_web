# -*- encoding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn import preprocessing


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

    #本函数处理极大极小值变换
    def T_min_max(self,X):
        min_max_scaler = preprocessing.MinMaxScaler()
        return min_max_scaler.fit_transform(self.df_data[X])

    #本函数处理zscore 归一化变换
    def T_zscore(self,X):
        return preprocessing.scale(self.df_data[X])

    #本函数处理去极值
    def T_winsorize(s, std, have_negative=True):
        '''
        s为series化的数据
        factor为strings的因子
        std为几倍的标准查
        输出Series
        '''
        r = s.copy()
        if have_negative == False:
            r = r[r >= 0]
        else:
            pass
        # 取极值
        edge_up = r.mean() + std * r.std()
        edge_low = r.mean() - std * r.std()
        r[r > edge_up] = edge_up
        r[r < edge_low] = edge_low
        return r

    def T_logistic1(self,X):
        pass

    def T_logistic2(self,X):
        pass

    def T_centralize(self,X):
        pass

    def T_percentile(self,X):
        pass

    def Frequency(self,X):
        pass

    def T_WOE(self,X, Y):
        pass

    def AR(self,X,Y):
        pass

    def compute_ks(self,X,Y):
        pass

    def compute_ar(self,X,Y):
        pass

    def draw_ar(self,X,Y):
        pass

dq = DataQuality()
dq.load_file("LoanStats_clean.csv")
df1=dq.Analyze("test1.csv")
