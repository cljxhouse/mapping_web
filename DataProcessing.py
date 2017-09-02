#-*- coding: utf-8 -*-
#本package实现KS，AR，WOE的处理
# csv 有两列，第一列是预测变量，第二列是实际变量
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *

matplotlib.use('TkAgg')

#计算AR值并绘制CAP曲线
def CAP(df):
    # df_sored=df.sort_values(by='x' ,ascending= False)
    df_sored = df.sort_values(['x', 'y'], ascending=[False, False])
    # df_sored
    # print(df_sored)
    k = 1
    N = len(df_sored)
    numdef = df_sored['y'].sum()
    # print('N',N)
    # print('numdef',numdef)
    # For i = 2 To N
    # for i in range(2,N):
    #   print (i,df_sored['x'][i-1],df_sored['x'][i-2])
    #   if df_sored['x'][i-1]!=df_sored['x'][i-2]:
    #      k = k + 1
    # print(k)
    xi = 0
    yi = 0
    area = 0
    a = 1
    # xy=pd.DataFrame({'xaxis','yaxis'})
    xy = pd.DataFrame(columns=['xi', 'yi'])
    xy.loc[0] = [0, 0]
    k = len(df_sored.groupby('x'))
    # for i in range(1,N+1):
    for i in range(len(df_sored)):
        xi = xi + 1 / N
        # yi = yi + df_sored.iloc[i-1]['y']/numdef
        yi = yi + df_sored.iloc[i]['y'] / numdef
        # print(i,xi,yi)
        # print('df_sored[''y''][i]',df_sored.iloc[i]['y'])

        # if df_sored.iloc[i-1]['x'] != df_sored.iloc[i-1+(0 if i==N else 1)]['x'] or i==N:
        if df_sored.iloc[i]['x'] != df_sored.iloc[i + (0 if i == N - 1 else 1)]['x'] or i == N - 1:
            # print('---------')
            # print('a',a)
            # print('xi',xi)
            # xy['xi'][a] = xi
            xy.loc[a, 'xi'] = xi
            # print('yi',yi)
            # xy['yi'][a] = yi
            xy.loc[a, 'yi'] = yi
            area = area + (xy['xi'][a] - xy['xi'][a - 1]) * (xy['yi'][a - 1] + xy['yi'][a]) / 2
            a = a + 1
            # print('=========')
    ar = (area - 0.5) / ((1 - numdef / N / 2) - 0.5)
    print('\r\n')
    print('ar', ar)
    print('xy', xy)
    plt.plot(xy.index.values, xy['yi'], 'r')
    plt.xticks(xy.index.values, xy['xi'], rotation=0)

    plt.legend(bbox_to_anchor=[0.3, 1])
    plt.grid()
    plt.show()
    # plt.savefig(""c:\\temp3.jpg"")
    # fig = plt.gcf()
    plt.savefig('c:\\pystudy\\tessstttyyy.png')
    plt.show()

    return


#接转换数值 WOE
x = []
y = []
xLabel = []
i = 1
for a1 in a:
    xLabel.append(a1)
    y.append(a[a1])
    x.append(i)
    i = i + 1

plt.plot(x, y, 'r', label='WOE')
plt.xticks(x, xLabel, rotation=0)

plt.legend(bbox_to_anchor=[0.3, 1])
plt.grid()
plt.show()


def compute_ks(data):
    sorted_list = data.sort_values(['predict'], ascending=[True])

    total_bad = sorted_list['label'].sum(axis=None, skipna=None, level=None, numeric_only=None)
    total_good = sorted_list.shape[0] - total_bad

    #print("total_bad = ", total_bad)
    #print(total_good = , total_good)

    x = []
    y1 = []
    y2 = []
    y3 = []
    xLabel = []
    i = 1
    max_ks = 0.0
    good_count = 0.0
    bad_count = 0.0
    for index, row in sorted_list.iterrows():
        x.append(i)
        i += 1
        xLabel.append(row['predict'])
        if row['label'] == 1:
            bad_count += 1.0
        else:
            good_count += 1.0

        val = abs(bad_count / total_bad - good_count / total_good)
        y1.append(bad_count / total_bad)
        y2.append(good_count / total_good)
        y3.append(val)
        max_ks = max(max_ks, val)

    plt.plot(x, y1, 'r', label='BAD')
    plt.plot(x, y2, 'b', label='GOOD')
    plt.plot(x, y3, 'y', label='VAL')
    plt.xticks(x, xLabel, rotation=0)

    plt.legend(bbox_to_anchor=[0.3, 1])
    plt.grid()
    plt.show()
    return max_ks, x, y1, y2, y3, xLabel

def main():
    df = pd.read_csv('C:\\pystudy\\AR\\input.csv', header=None, names=['x', 'y'])
    CAP(df)


if __name__ == ""__main__"":
    main()