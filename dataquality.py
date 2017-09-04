
import pandas as pd
import numpy as np
import scipy.stats as st
import os
from sklearn import preprocessing
from sklearn.preprocessing import *
from sklearn.feature_selection import *


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

    #分析空值，0值，极大、极小，中值，均值等指标
    def dq_Analyze(self, output=""):
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
            print(st1)
        return st1

    #离散值分析每个值的分布
    def dq_Frequency(self,X,output):
        if isinstance(X,str):
            df1 = self.df_data[X].value_counts(ascending=False)
            df1["field_name"] = X
            df1.iloc[0:100].to_csv(output)
        elif isinstance(X,list):
            if os.path.exists(output):
                os.remove(output)
            for col_name in X:
                total_count=len(self.df_data.index)
                df1 = pd.DataFrame({"count":
                    self.df_data[col_name].value_counts(ascending=False)[0:100]})
                df1['frequency']=df1['count']/total_count
                df1['total_freq']=df1['frequency'].cumsum()
                #print df1.index
                df1["field_name"]=col_name
                df1.to_csv(output,mode="a")
               # print type(df1)
        else:
            print ("Error X entered")
        pass


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
#TODO start from here
#migrate from excel code

    #采用第一种方法进行logistic变换
    def T_logistic1(self,X):
        pass

    def T_logistic2(self,X):
        pass

    # 中心化,将原始数组换成相对中心的比例
    def T_centralize(self, X):
        if isinstance(X, str):
            df1 = pd.DataFrame(self.df_data[X] - self.df_data[X].mean())
            df1.columns = df1.columns + '_centralized'
            return df1
        elif isinstance(X, list):
            df1 = self.df_data[X] - self.df_data[X].mean()
            df1.columns = df1.columns + '_centralized'
            return df1
        else:
            print("Error X entered")
        pass

     # 分位线，将袁术数据集转换成百分比
    def T_percentile(self, X='*'):
        if X == '*':
            df5 = self.df_data.rank() / self.df_data.count()
            df5.columns = df5.columns + '_precent'
            return df5
        elif isinstance(X, str):
            # df1 = pd.DataFrame(self.df_data[X]-self.df_data[X].mean())
            df5 = pd.DataFrame(self.df_data[X].rank() / self.df_data[X].count())
            df5.columns = df5.columns + '_precent'
            return df5
        elif isinstance(X, list):
            df5 = self.df_data[X].rank() / self.df_data[X].count()
            df5.columns = df5.columns + '_precent'
            return df5
        else:
            print("Error X entered")

        pass

        # 根据频数转换连续值到离散值
    def bin_by_frequency(self, X, k=4):
        # k = 4
        if isinstance(X, str):
            d1 = pd.cut(self.df_data[X], k, labels=list(range(k)))  # 等宽离散化，各个类比依次命名为0,1,2,3
            return d1
        else:
            print("Error X entered")
        pass

        # 根据距离转换连续值到离散值
    def bin_by_distance(self, X, k=4):
        # 等频率离散化
        if isinstance(X, str):
            w = [1.0 * i / k for i in range(k + 1)]
            w = self.df_data[X].describe(percentiles=w)[4:4 + k + 1]  # 使用describe函数自动计算分位数
            w[0] = w[0] * (1 - 1e-10)
            d2 = pd.cut(self.df_data[X], w, labels=list(range(k)))
            return d2
        else:
            print("Error X entered")
        pass

    #转换离散代码成数值
    def T_WOE(self,X, Y):
        pass

    #转换离散代码成AR数值
    def T_AR(self,X,Y):
        pass

    def IV(self,X,Y):
        pass

    def compute_ks(self,X,Y):
        pass

    def compute_ar(self,X,Y):
        pass

#TODO 增加亚变量


    def draw_ar(self,X,Y):
        pass

    def F_chi_square(self,X,Y):
        #此处Y必须为0-好客户，1-坏客户
        #X可以为单个字符串，或者字符串的list
        chi_list=[]
        if isinstance(X,str):
            x_columns = [X]
        else :
            x_columns = list(X)
        for x1 in x_columns:
            #生成交叉表，结果f1[0]为好客户，f1[1]为坏客户
            f1 = pd.crosstab(self.df_data[x1],self.df_data[Y])
            #total列为总客户数，expected_bad为期望的坏客户数
            f1['total']=f1[0]+f1[1]
            total_prob = f1[1].sum()*1.0/f1['total'].sum()
            f1['expected_bad']=total_prob*f1['total']
            #调用函数计算卡方系数
            chi=st.chisquare(f1[1],f1['expected_bad'])
            chi_list.append([x1,chi.statistic,chi.pvalue])
        return chi_list


dq = DataQuality()
dq.load_file("LoanStats_clean.csv")
#x=dq.df_data["loan_amnt"]
#y=dq.df_data['loan_status1']
#SelectKBest(chi2,k=1).fit_transform(x,y)
#dq.dq_Analyze("test1.csv")
#dq.dq_Frequency(["grade","loan_amnt"],"test2.csv")

#TODO s1=np.random.rand(10)
print(dq.F_chi_square(["grade","term"],"loan_status1"))
