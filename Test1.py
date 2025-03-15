import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

'''текущая дата'''
my_date=datetime(2022,12,8)

os.chdir('C:/Users/rasta/Downloads/DA/DA/task_2_data (2)/task_2_data')

df_orders=pd.read_csv('orders.csv')
df_pay_fact=pd.read_csv('payments.csv')
df_plan=pd.read_csv('plan.csv')

'''список сумм платежей нарастающих'''

def plan_summ(ord_id):
    plan_sum=[]
    DF=df_plan[df_plan['order_id'] == ord_id]
    for i in DF.loc[:,'plan_sum_total'].values[:]:
        plan_sum.append(round(i, 2))
    return plan_sum

'''список суммы платежей необходимых для внесения'''

def plan_summ_dif(ord_id):
    plan_sum = plan_summ(ord_id)
    plan_sum_dif=[plan_sum[0]]
    for i,j in enumerate(plan_sum):
        try:
            plan_sum_dif.append(round(plan_sum[i+1] - plan_sum[i], 2))
        except:
            IndexError

    return plan_sum_dif


'''график платежей'''

def pays_d(ord_id):
    dates = df_plan[df_plan['order_id'] == ord_id]['plan_at'].values[:]
    pays = plan_summ_dif(ord_id)
    plt.bar(dates, pays)
    for i, count in enumerate(pays):
        plt.text(i, count + 1, str(count), ha='center')
    plt.show()


'''id не закрытых кредитов на текущую дату'''

def not_closed(d_f):
    orders_not_pay = []
    df_np=df_orders[df_orders['closed_at'].isna()]
    for orders in df_np['order_id']:
        orders_not_pay.append(orders)

    return orders_not_pay

orders_not_pay = not_closed(df_orders)



"""id не закрытых кредитов, у которых дата последнего платежа просрочена"""

debtors=[]
for orders in orders_not_pay:
    dfp=df_plan[df_plan['order_id'] == orders].tail(1)
    if datetime.strptime(dfp['plan_at'].values[0], '%Y-%m-%d') < my_date:
        debtors.append(orders)


'число записей платежей'
n_w = df_pay_fact[df_pay_fact['order_id'] == debtors[6]]['paid_at'].count()

(df_plan[df_plan['order_id'] == debtors[6]][:n_w])
(df_pay_fact[df_pay_fact['order_id'] == debtors[6]])


'внесено ноль платежей среди id, которые должны быть закрыты на текущую дату'

def zer_pay(arr1):
    dict0 = {}
    for i in arr1:
        if (df_pay_fact[df_pay_fact['order_id'] == i]).empty:
            zzz = my_date - datetime.strptime(df_plan[df_plan['order_id'] == i]['plan_at'].values[0], '%Y-%m-%d')
            dict0.update({i:zzz.days})
    return dict0

zer = zer_pay(debtors)

print(debtors)

df_plan['plan_at'] = pd.to_datetime(df_plan['plan_at'])

df_pay_fact['paid_at'] = pd.to_datetime(df_pay_fact['paid_at'])


plan_s = df_plan[df_plan['order_id'] == 400039450]

paid_s = df_pay_fact[df_pay_fact['order_id'] == 400039450]

print(plan_s)
print(paid_s)

# платежи уплаченные по месяцам

paid_sum_m = paid_s.groupby(paid_s['paid_at'].dt.to_period('M'))['paid_sum'].sum()

# разбиваем нарастающий итог на дифферинцированные платежи

#список нарастающий значений платежей из фрейма
arr_plan_sum = plan_s['plan_sum_total'].tolist()

def plan_sum_dif(arr0):
    plan_sum0 = arr0
    plan_sum_dif=[plan_sum0[0]]
    for i,j in enumerate(plan_sum0):
        try:
            plan_sum_dif.append(round(plan_sum0[i+1] - plan_sum0[i], 2))
        except:
            IndexError

    return plan_sum_dif

arr_plan_dif = plan_sum_dif(arr_plan_sum)
print(arr_plan_dif)


# копия для добавления столбца с дифф-ми платежами

plan_sum_with_dif = plan_s.copy()
plan_sum_with_dif['plan_sum_dif'] = arr_plan_dif

#платежи необходимые к уплате по месяцам

p_mounth = plan_sum_with_dif.groupby(plan_sum_with_dif['plan_at'].dt.to_period('M'))['plan_sum_dif'].sum()

print(p_mounth)
print(paid_sum_m)
print(paid_sum_m.subtract(p_mounth))









