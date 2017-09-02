# -*- encoding: utf-8 -*-

def gbs(a,b):
    t1=a
    t2=b
    while(t2>0):
        if t2>=t1 :
            t2=t2-t1
        else:
            t1=t1-t2
    return a*b/t1


a=1
for i in range(1,13):
    a=gbs(i,a)
    print "第",i,"次结果=",a
