# -*- encoding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn import preprocessing

#data scale using z-score
X = np.array([[ 1., -1.,  2.],
               [ 2.,  0.,  0.],
               [ 0.,  1., -1.]])
X_scaled = preprocessing.scale(X)

print X_scaled

#data scale using max min
min_max_scaler = preprocessing.MinMaxScaler()
X_minmax_scaled = min_max_scaler.fit_transform(X)
print X_minmax_scaled



#本函数中s为一维数组，去极值
def winsorize(s, std, have_negative=True):
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

X=np.array([1,2,3,4,999])
#print X.mean()
#print X.std()
r=winsorize(X,1)
print r