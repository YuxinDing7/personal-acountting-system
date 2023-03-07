"""
accountClass.py
author:Ding Yuxin
date:2022-05-25
description:Account函数，实现基本的创建账户，记账查账功能。
"""
# -*- coding:UTF-8 -*-
import decimal
import os
import time
from matplotlib import pyplot as plt
import matplotlib
from matplotlib.ticker import Locator
import numpy as np
from decimal import Decimal

path = os.getcwd()

class Account():
    users = open(path + '\\usersFiles\\users.csv', 'r')
    userslist = users.readlines()
    users.close()
    usersDict = {}
    for i in range(len(userslist)):
        user = userslist[i].split(',')
        user[1] = user[1].replace('\n','')
        usersDict[user[0]] = user[1]

    def __init__(self, userName, password):
        self.userName = userName #用户名
        self.password = password #密码
        self.totalAssets = 0.0 #总资产
        self.billFileName = path + "\\usersFiles\\" + userName + 'billFile.csv' #账单文件名
        if userName in Account.usersDict:
            self.bill = open(self.billFileName, 'r') #账单
            billsAllType = self.bill.readlines()
            for i in range(3,len(billsAllType)):
                billAllType = billsAllType[i].split(',')
                if billAllType[2]=='+':
                    self.totalAssets += eval(billAllType[3])
                else:
                    self.totalAssets -= eval(billAllType[3])
            self.bill.close()
        else:
            self.bill = open(self.billFileName, 'w') #账单
            self.bill.write('用户名：' + ',' + userName + '\n')
            self.bill.write('密码：' + ',' + password + '\n')
            self.bill.write('账户创建时间：' + ',' + time.ctime() + '\n')
            self.bill.close()
           

    #收入函数
    def addMoney(self, money, type = '未归类', time = time.ctime(), remark = 'null'):
        moneyFloat = eval(money)
        self.totalAssets += moneyFloat
        with open(self.billFileName, 'a') as b:
            b.write(time +','+ type + ',' + '+' + ','+ money + ',' + remark + '\n')

    #支出函数
    def spendMoney(self, money, type = '未归类', time = time.ctime(), remark = 'null'):
        moneyFloat = eval(money)
        if(moneyFloat > self.totalAssets):
            return False
        else:
            self.totalAssets -= moneyFloat
        with open(self.billFileName, 'a') as b:
            b.write(time +','+ type + ',' + '-' + ',' + money + ',' + remark + '\n')
            return True

    #查询当前总资产
    def getTotalAssets(self):
        return self.totalAssets
    
    #得到所有账单
    def getAllBills(self):
        with open(self.billFileName, 'r') as b:
            billsAllType = b.readlines()
        allBills = [];
        for i in range(3, len(billsAllType)):
            bill = billsAllType[i].split(',')
            bill[4] = bill[4].replace('\n', '')
            monthToNum = {'Jan':' 1','Feb':' 2','Mar':' 3','Apr':' 4','May':' 5','Jun':' 6','Jul':' 7','Aug':' 8','Sep':' 9','Oct':'10','Nov':'11','Dec':'12'}
            yearin = bill[0][20:24]
            monthin = bill[0][4:7]
            dayin = bill[0][8:10]
            date = yearin+'年'+monthToNum[monthin]+'月'+dayin+'日'
            aBillList = [date, bill[1], bill[2], '￥'+bill[3], bill[4]]
            allBills.append(aBillList)
        return allBills

    #查询不同类型/年度/月度/天总 收入 的函数
    def getin(self, type = 'all', year = 'all', month = 'all', day = 'all'):
        with open(self.billFileName, 'r') as b:
            billsAllType = b.readlines()
        allinmoney = 0
        allinbills = []
        bills = []
        #处理类型
        if type != 'all':
            for i in range(3, len(billsAllType)):
                billAllType = billsAllType[i].split(',')
                billAllType[4] = billAllType[4].replace('\n', '')
                if billAllType[1] == type:
                    bills.append(billsAllType[i])
        else:
            bills = billsAllType[3:len(billsAllType)]
        #查询记账本内的全部支出
        if year == 'all':
            for i in range(0,len(bills)):
                bill = bills[i].split(',')
                bill[4] = bill[4].replace('\n', '')
                if bill[2] == '+':
                    allinbills.append(bill)
                    allinmoney += eval(bill[3])
                    allinmoney = round(allinmoney, 2)
        #查询年度支出
        elif month == 'all':
            for i in range(0,len(bills)):
                bill = bills[i].split(',')
                bill[4] = bill[4].replace('\n', '')
                if bill[0][20:24] == year and bill[2] == '+':
                    allinbills.append(bill)
                    allinmoney += eval(bill[3])
                    allinmoney = round(allinmoney, 2)
        #查询月度支出
        elif day == 'all':
            for i in range(0,len(bills)):
                bill = bills[i].split(',')
                bill[4] = bill[4].replace('\n', '')
                if bill[0][20:24] == year and bill[0][4:7] == month and bill[2] == '+':
                    allinbills.append(bill)
                    allinmoney += eval(bill[3])
                    allinnmoney = round(allinmoney, 2)
        #查询一天的支出
        else:
            for i in range(0,len(bills)):
                bill = bills[i].split(',')
                bill[4] = bill[4].replace('\n', '')
                md = month + ' ' + day
                if bill[0][20:24] == year and bill[0][4:10] == md and bill[2] == '+':
                    allinbills.append(bill)
                    allinmoney += eval(bill[3])
                    allinmoney = round(allinmoney, 2)           
        allinmoney = str(allinmoney)
        #返回一个支出的金额总和(string)，一个支出的账单(list包list包string)
        return allinmoney, allinbills

    #查询不同类型/年度/月度/天总 支出 的函数
    def getout(self, type = 'all', year = 'all', month = 'all', day = 'all'):
        with open(self.billFileName, 'r') as b:
            billsAllType = b.readlines()
        alloutmoney = 0
        alloutbills = []
        bills = []
        #处理类型
        if type != 'all':
            for i in range(3, len(billsAllType)):
                billAllType = billsAllType[i].split(',')
                billAllType[4] = billAllType[4].replace('\n', '')
                if billAllType[1] == type:
                    bills.append(billsAllType[i])
        else:
            bills = billsAllType[3:len(billsAllType)]
        #查询记账本内的全部支出
        if year == 'all':
            for i in range(0,len(bills)):
                bill = bills[i].split(',')
                bill[4] = bill[4].replace('\n', '')
                if bill[2] == '-':
                    alloutbills.append(bill)
                    alloutmoney += eval(bill[3])
                    alloutmoney = round(alloutmoney, 2)
        #查询年度支出
        elif month == 'all':
            for i in range(0,len(bills)):
                bill = bills[i].split(',')
                bill[4] = bill[4].replace('\n', '')
                if bill[0][20:24] == year and bill[2] == '-':
                    alloutbills.append(bill)
                    alloutmoney += eval(bill[3])
                    alloutmoney = round(alloutmoney, 2)
        #查询月度支出
        elif day == 'all':
            for i in range(0,len(bills)):
                bill = bills[i].split(',')
                bill[4] = bill[4].replace('\n', '')
                if bill[0][20:24] == year and bill[0][4:7] == month and bill[2] == '-':
                    alloutbills.append(bill)
                    alloutmoney += eval(bill[3])
                    alloutmoney = round(alloutmoney, 2)
        #查询一天的支出
        else:
            for i in range(0,len(bills)):
                bill = bills[i].split(',')
                bill[4] = bill[4].replace('\n', '')
                md = month + ' ' + day
                if bill[0][20:24] == year and bill[0][4:10] == md and bill[2] == '-':
                    alloutbills.append(bill)
                    alloutmoney += eval(bill[3])
                    alloutmoney = round(alloutmoney, 2)           
        alloutmoney = str(alloutmoney)
        #返回一个支出的金额总和(string)，一个支出的账单(list包list包string)
        return alloutmoney, alloutbills

    #删除某条账单
    def delete(self, type, year, month, day, inout, money, comment):
        with open(self.billFileName, 'r') as b:
            billsOrigin = b.readlines()       
        bills_delete = []
        for i in range(3, len(billsOrigin)):
            bill = billsOrigin[i].split(',')
            bill[4] = bill[4].replace('\n', '')
            md = month + ' ' + day
            money = money.replace('￥','')
            if bill[0][20:24] == year and bill[0][4:10] == md and bill[2]==inout and bill[3]==money and bill[4]==comment:
                continue
            else:
                bills_delete.append(billsOrigin[i])
        with open(self.billFileName, 'w') as b:
            for i in range(3):
                billStr = billsOrigin[i]
                b.write(billStr)
            for j in bills_delete:
                b.write(j)

    #年收支统计图
    def makeAYearGraph(self, yearG):
        allYearinmoney, allYearinbills = self.getin('all', yearG)
        allYearoutmoney, allYearoutbills = self.getout('all', yearG)
        monthsList = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
        monthsEnList = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        dataIn = []
        dataOut = []
        for month in monthsEnList:
            allMonthinMoney, allMonthinBills = self.getin('all', yearG, month)
            dataIn.append(Decimal(allMonthinMoney))
            allMonthoutMoney, allMonthoutBills = self.getout('all', yearG, month)
            dataOut.append(Decimal(allMonthoutMoney))
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False
        x = np.arange(12)
        rects1 = plt.bar(x, dataIn, width=0.4, alpha=0.8, color='pink', label="收入")
        rects2 = plt.bar([i + 0.4 for i in x], dataOut, width=0.4, color='lightskyblue', label="支出")
        plt.ylim(0, 10000)
        plt.ylabel('金额')
        plt.xticks([index + 0.2 for index in x], monthsList)
        plt.xlabel('月份')
        hoistTitle = self.userName+'的'+yearG+'年收支情况统计'
        plt.xlabel(hoistTitle)
        plt.legend()
        for rect in rects1:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height+1, str(height), ha="center", va="bottom")
        for rect in rects2:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height+1, str(height), ha="center", va="bottom")
        plt.show()
    
    #月收入构成图
    def makeAmonthInGraph(self, yearM, monthM):
        monthDict = {'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6','Jul':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}
        allMonthinmoney, allMonthinbills = self.getin('all', yearM, monthM)
        allMonthoutmoney, allMonthoutbills = self.getout('all', yearM, monthM)
        typeInList = ["工资奖金", "人情红包","收转帐","其他收入"]
        datasIn = []
        typesIn = []
        for i in range(4):
            allMonthTypeinmoney, allMonthTypeinBills = self.getin(typeInList[i], yearM, monthM)
            if(eval(allMonthTypeinmoney) > 0):
                datasIn.append(eval(allMonthTypeinmoney))
                typesIn.append(typeInList[i])
        color = ['orange','lightgreen','tomato', 'violet', 'lightskyblue', 'pink','gold','lightgreen']
        colors = []
        for i in range(len(typesIn)):
            colors.append(color[i])
        plt.rcParams['font.sans-serif'] = ['SimHei']
        fig, ax = plt.subplots()
        ax.pie(datasIn, colors=colors,labels = typesIn, wedgeprops={"linewidth": 1, "edgecolor": "white"},autopct="%1.1f%%",frame=True)
        ax.axis('equal')
        ax.axis('off')
        inPieTitle = self.userName+'的'+yearM+'年'+monthDict[monthM]+'月收入构成'
        plt.title(inPieTitle)
        ax.legend()
        plt.show()

    #月支出构成图
    def makeAmonthOutGraph(self, yearM, monthM):
        monthDict = {'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6','Jul':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}
        allMonthoutmoney, allMonthoutbills = self.getout('all', yearM, monthM)
        typeOutList = ["餐饮支出","服饰支出","交通支出","购物支出","教育支出","娱乐支出","医疗支出","其他支出"]
        datasOut = []
        typesOut = []
        for i in range(8):
            allMonthTypeOutmoney, allMonthTypeOutBills = self.getout(typeOutList[i], yearM, monthM)
            if(eval(allMonthTypeOutmoney) > 0):
                datasOut.append(eval(allMonthTypeOutmoney))
                typesOut.append(typeOutList[i])
        color = ['orange','lightgreen','tomato','violet', 'lightskyblue', 'pink','gold','lightgreen']
        colors = []
        for i in range(len(typesOut)):
            colors.append(color[i])
        plt.rcParams['font.sans-serif'] = ['SimHei']
        fig, ax = plt.subplots()
        ax.pie(datasOut, colors=colors,labels = typesOut, wedgeprops={"linewidth": 1, "edgecolor": "white"},autopct="%1.1f%%",frame=True)
        ax.axis('equal')
        ax.axis('off')
        inPieTitle = self.userName+'的'+yearM+'年'+monthDict[monthM]+'月支出构成'
        plt.title(inPieTitle)
        ax.legend()
        plt.show()

 #核实用户信息
def checkUser(userName, password):
    if userName in Account.usersDict:
        return Account.usersDict[userName] == password
    else:
        return False

 #创建账号
def MakeAccount(userName, password):
    if userName in Account.usersDict:
        return False
    else:
        obj = Account(userName, password)
        with open(path + '\\usersFiles\\users.csv', 'a') as u:
            u.write(userName + ',' + password + '\n') #写入users文件，储存用户信息
        return True