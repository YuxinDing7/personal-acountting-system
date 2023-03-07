"""
main.py
author:Ding Yuxin
date:2022-05-25
description:GUI窗口实现
"""
# -*- coding:UTF-8 -*-
import tkinter
from tkinter.constants import LEFT
import os
from matplotlib import pyplot as plt
from matplotlib.pyplot import show
import accountClass
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from accountClass import MakeAccount
from accountClass import checkUser
import time

name=""
pwd=""
path = os.getcwd()
#主窗口
def rootFun(name, pwd):
    obj = accountClass.Account(name, pwd)
    root = Tk()
    root.geometry('540x360+300+150')
    root.title("小谢记账本")
    root.config(background = "#fff8d3")
    #菜单栏
    mn = Menu(root)
    root.config(menu = mn)

    #类型筛选选项
    typeDict = {1:"餐饮支出",2:"服饰支出",3:"交通支出",4:"购物支出",5:"教育支出",6:"娱乐支出",7:"医疗支出",8:"其他支出",9:"工资奖金",10:"人情红包",\
                11:"收转帐",12:"其他收入", 13:"全部支出", 14:"全部收入"}

    def chooseType(i):
        typeChosen = typeDict[i]

        #筛选出的类型账单窗口
        typeWin = Tk()
        typeWin.title(typeChosen)
        typeWin.geometry('290x260+400+200')
        typeWin.config(background = "#fff8d3")
        if i<=8 or i==13:
            Label(typeWin, text = "总支出：",width=10,background = "#fff8d3").grid(row=0,column=0)
            if i == 13:
                allIn, Allinbills = obj.getout()
            else:
                allIn, Allinbills = obj.getout(typeChosen)
            Label(typeWin, text = '￥' + allIn,width=10,background = "#fff8d3").grid(row=0,column=1)

        else:
            Label(typeWin, text = "总收入：",width=10,background = "#fff8d3").grid(row=0,column=0)
            if i == 14:
                allIn, Allinbills = obj.getin()
            else:
                allIn, Allinbills = obj.getin(typeChosen)
            Label(typeWin, text = '￥' + allIn,width=10,background = "#fff8d3").grid(row=0,column=1)

        #单一类型账单显示
        typeFrame = Frame(typeWin)
        typeFrame.grid(row=2, column=0, rowspan=30, columnspan=3,padx=5,pady=5)

        sb1 = Scrollbar(typeFrame)
        sb1.pack(side=RIGHT, fill=Y)
        inListBox = Listbox(typeFrame, yscrollcommand=sb1.set,width=35)
        monthToNum = {'Jan':' 1','Feb':' 2','Mar':' 3','Apr':' 4','May':' 5','Jun':' 6','Jul':' 7','Aug':' 8','Sep':' 9','Oct':'10','Nov':'11','Dec':'12'}
        for i in Allinbills:
            yearin = i[0][20:24]
            monthin = i[0][4:7]
            dayin = i[0][8:10]
            billin = yearin+'年'+monthToNum[monthin]+'月'+dayin+'日 '+i[1]+' '+i[2]+i[3]+' '+i[4]
            inListBox.insert(END, billin)
        inListBox.pack(ipadx=3,ipady=2)
        sb1.config(command = inListBox.yview)

        typeWin.mainloop()


    select_menu = Menu(mn)
    mn.add_cascade(label = '全部类型', menu = select_menu)
    select_menu.add_command(label = '全部支出', command = lambda:chooseType(13))
    select_menu.add_command(label = '餐饮支出', command = lambda:chooseType(1))
    select_menu.add_command(label = '服饰支出', command = lambda:chooseType(2))
    select_menu.add_command(label = '交通支出', command = lambda:chooseType(3))
    select_menu.add_command(label = '购物支出', command = lambda:chooseType(4))
    select_menu.add_command(label = '教育支出', command = lambda:chooseType(5))
    select_menu.add_command(label = '娱乐支出', command = lambda:chooseType(6))
    select_menu.add_command(label = '医疗支出', command = lambda:chooseType(7))
    select_menu.add_command(label = '其他支出', command = lambda:chooseType(8))
    select_menu.add_separator()
    select_menu.add_command(label = '全部收入', command = lambda:chooseType(14))
    select_menu.add_command(label = '工资奖金', command = lambda:chooseType(9))
    select_menu.add_command(label = '人情红包', command = lambda:chooseType(10))
    select_menu.add_command(label = '收转账', command = lambda:chooseType(11))
    select_menu.add_command(label = '其他收入', command = lambda:chooseType(12))

    #收支情况统计选项
    def getYearSum():
        yearRoot = Toplevel(root)
        yearRoot.geometry('320x60+450+300')
        yearRoot.title('年账单')
        Label(yearRoot, text='请选择您想查询的年份：').grid(row=0,column=0)
        yearrVar = StringVar()
        yearComb1 = Combobox(yearRoot, textvariable=yearrVar, values=['2016','2017','2018','2019','2020','2021','2022','2023'])
        yearComb1.grid(row=0,column=1)
        Label(yearRoot,text="年").grid(row=0,column=2)

        def qr():
            year1 = yearrVar.get() 
            allYearIn, allYearBills = obj.getin('all', yearrVar.get())
            allYearOut, allYearOutbills = obj.getout('all', yearrVar.get())
            showSum = Toplevel(yearRoot)
            showSum.geometry('240x60+450+300')
            title = obj.userName + '的'+ yearrVar.get() +'年收支情况'
            showSum.title(title)
            Label(showSum, text='总收入：').grid(row=0,column=0)
            Label(showSum, text = '￥' + allYearIn).grid(row=0,column=1)
            Label(showSum, text = "总支出：").grid(row=0,column=2)
            Label(showSum, text = '￥' + allYearOut).grid(row=0,column=3)
            bt = Button(showSum, text = '查看收支情况统计图',command=lambda:obj.makeAYearGraph(year1))
            bt.grid(row=1,column=1,columnspan=2)
            showSum.mainloop()

        bt1 = Button(yearRoot, text = '确认',command = qr)
        bt1.grid(row=1, column=0,columnspan=2)
        yearRoot.mainloop()

    #月收支统计报告
    def getmonthSum():
        monthWin = Toplevel(root)
        monthWin.geometry('640x60+450+300')
        monthWin.title('月账单')
        Label(monthWin, text='请选择您想查询的年份：').grid(row=0,column=0)
        year2Var = StringVar()
        yearComb2 = Combobox(monthWin, textvariable=year2Var, values=['2016','2017','2018','2019','2020','2021','2022','2023'])
        yearComb2.grid(row=0,column=1)
        Label(monthWin,text="年").grid(row=0,column=2)
        Label(monthWin, text='请选择您想查询的月份：').grid(row=0,column=3)
        monthhVar = StringVar()
        monthhComb1 = Combobox(monthWin, textvariable=monthhVar,values=[' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9','10','11','12'] )
        monthhComb1.grid(row=0,column=4)
        Label(monthWin,text="月").grid(row=0,column=5)
        def qr2():
            monthDict = {' 1':'Jan',' 2':'Feb',' 3':'Mar',' 4':'Apr',' 5':'May',' 6':'Jun',' 7':'Jul',' 8':'Aug',' 9':'Sep','10':'Oct','11':'Nov','12':'Dec'}
            year2 = year2Var.get()
            month2 = monthhVar.get()
            allMonthIn, allMonthBills = obj.getin('all', year2, monthDict[month2])
            allMonthOut, allMonthOutbills = obj.getout('all', year2, monthDict[month2])
            showSum = Toplevel(monthWin)
            showSum.geometry('245x60+450+300')
            title = obj.userName + '的'+ year2 +'年'+ month2 +'月收支情况统计'
            showSum.title(title)
            Label(showSum, text='总收入：').grid(row=0,column=0)
            Label(showSum, text = '￥' + allMonthIn).grid(row=0,column=1)
            Label(showSum, text = "总支出：").grid(row=0,column=2)
            Label(showSum, text = '￥' + allMonthOut).grid(row=0,column=3)
            btIn = Button(showSum, text = '查看收入构成图',command=lambda:obj.makeAmonthInGraph(year2, monthDict[month2]))
            btIn.grid(row=1,column=1,columnspan=2)
            btOut = Button(showSum, text = '查看支出构成图',command=lambda:obj.makeAmonthOutGraph(year2, monthDict[month2]))
            btOut.grid(row=1,column=3,columnspan=2)
            showSum.mainloop()

        bt2 = Button(monthWin, text = '确认',command = qr2)
        bt2.grid(row=1, column=3)
        monthWin.mainloop()
    
    #单日账单显示
    def getDaySum():
        def daySum(allDayInMoney, allDayInBills, allDayOutMoney, allDayOutBills):
            dayWIn = Tk()
            dayWIn.geometry('540x300+300+150')
            dayWIn.title("日账单")
            dayWIn.config(background = "#fff8d3")

            Label(dayWIn, text = "总收入：",width=10,background = "#fff8d3").grid(row=0,column=0)
            Label(dayWIn, text = '￥' + allDayInMoney,width=10,background = "#fff8d3").grid(row=0,column=1)

            Label(dayWIn, text = "总支出：",width=10,background = "#fff8d3").grid(row=0,column=2)
            Label(dayWIn, text = '￥' + allDayOutMoney,width=10,background = "#fff8d3").grid(row=0,column=3)

            Label(dayWIn, text = "总结余：",width=10,background = "#fff8d3").grid(row=0,column=4)
            allBalance = str(round((eval(allDayInMoney) - eval(allDayOutMoney)), 2))
            Label(dayWIn, text = '￥' + allBalance,width=10,background = "#fff8d3").grid(row=0,column=5)   

            #python 3.8 bug 必须有这个配置才能显示颜色
            def fixed_map(option):
                return [elm for elm in style.map("Treeview", query_opt=option) if elm[:2] != ("!disabled", "!selected")]

            style = Style()
            style.map("Treeview", foreground=fixed_map("foreground"), background=fixed_map("background"))

            #账单显示
            table_frame = Frame(dayWIn)
            table_frame.grid(row=2, column=0, rowspan=30, columnspan=6, padx=10,pady=5)
            columns = ['时间', '类型', '收支', '金额','备注']
            xscroll = Scrollbar(table_frame, orient=HORIZONTAL)
            yscroll = Scrollbar(table_frame, orient=VERTICAL)
            billTable = Treeview(table_frame, height = 10, columns = columns, show='headings', xscrollcommand=xscroll.set, yscrollcommand=yscroll.set) 
            for column in columns:
                billTable.heading(column=column, text=column, anchor = 'center')  
                billTable.column(column=column, width=100, minwidth=100, anchor=CENTER, )
            xscroll.config(command=billTable.xview)
            xscroll.pack(side=BOTTOM, fill=X)
            yscroll.config(command=billTable.yview)
            yscroll.pack(side=RIGHT, fill=Y)
            billTable.pack(fill=BOTH, expand=True)
            def makeBills(bills):
                allBills = []
                for bill in bills:
                    monthToNum = {'Jan':' 1','Feb':' 2','Mar':' 3','Apr':' 4','May':' 5','Jun':' 6','Jul':' 7','Aug':' 8','Sep':' 9','Oct':'10','Nov':'11','Dec':'12'}
                    yearin = bill[0][20:24]
                    monthin = bill[0][4:7]
                    dayin = bill[0][8:10]
                    date = yearin+'年'+monthToNum[monthin]+'月'+dayin+'日'
                    aBillList = [date, bill[1], bill[2], '￥'+bill[3], bill[4]]
                    allBills.append(aBillList)
                return allBills
            allInBills = makeBills(allDayInBills)
            allOutBills = makeBills(allDayOutBills)

            for i in allInBills:
                billTable.insert('', END, values = i,tags = 'pinkColor')
                billTable.tag_configure('pinkColor', background = 'pink')
            for i in allOutBills:
                billTable.insert('', END, values = i, tags = 'blueColor')
                billTable.tag_configure('blueColor', background = 'lightskyblue')

        #选择日期窗口
        chooseTimeWin = Toplevel(root)
        chooseTimeWin.title("选择日期")
        chooseTimeWin.geometry('300x90+360+190')

        #选择年份
        yearVar = StringVar()
        yearComb = Combobox(chooseTimeWin, textvariable=yearVar,values=['2016','2017','2018','2019','2020','2021','2022','2023'] )
        yearComb.place(x=10, y=20, width=60, height=20)
        Label(chooseTimeWin,text="年").place(x=80,y=20)
        #选择月份
        monthVar = StringVar()
        monthComb = Combobox(chooseTimeWin, textvariable=monthVar,values=[' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9','10','11','12'] )
        monthComb.place(x=110, y=20, width=50, height=20)
        Label(chooseTimeWin,text="月").place(x=170,y=20)
        #选择日期
        dayVar = StringVar()
        dayComb = Combobox(chooseTimeWin, textvariable=dayVar,values=[' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9','10','11','12','13','14','15',\
            '16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'] )
        dayComb.place(x=200, y=20, width=50, height=20)
        Label(chooseTimeWin,text="日").place(x=260,y=20)

        #确认按钮函数，关闭日期选择窗口
        def confirm():
            monthDict = {' 1':'Jan',' 2':'Feb',' 3':'Mar',' 4':'Apr',' 5':'May',' 6':'Jun',' 7':'Jul',' 8':'Aug',' 9':'Sep','10':'Oct','11':'Nov','12':'Dec'}
            allDayInMoney, allDayInBills = obj.getin('all', yearVar.get(), monthDict[monthVar.get()], dayVar.get())
            allDayOutMoney, allDayOutBills = obj.getout('all', yearVar.get(), monthDict[monthVar.get()], dayVar.get())
            chooseTimeWin.destroy()
            daySum(allDayInMoney, allDayInBills,allDayOutMoney, allDayOutBills)

        #确认按钮
        confirmButton = Button(chooseTimeWin, text="确认", command=confirm)
        confirmButton.place(x=100, y=50)
        chooseTimeWin.mainloop()

        allDayInMoney, allDayInBills = obj.getin('all', )


    #收支情况统计菜单
    inout_menu = Menu(mn)
    mn.add_cascade(label='收支情况统计', menu = inout_menu)
    inout_menu.add_command(label = '日账单', command = getDaySum)
    inout_menu.add_command(label = '月账单', command = getmonthSum)
    inout_menu.add_command(label = '年账单', command = getYearSum)

    #总收入总支出总结余显示
    Label(root, text = "总收入：",width=10,background = "#fff8d3").grid(row=0,column=0)
    allIn, Allinbills = obj.getin()
    Label(root, text = '￥' + allIn,width=10,background = "#fff8d3").grid(row=0,column=1)

    Label(root, text = "总支出：",width=10,background = "#fff8d3").grid(row=0,column=2)
    allOut, AllOutbills = obj.getout()
    Label(root, text = '￥' + allOut,width=10,background = "#fff8d3").grid(row=0,column=3)

    Label(root, text = "总结余：",width=10,background = "#fff8d3").grid(row=0,column=4)
    allBalance = str(round((eval(allIn) - eval(allOut)), 2))
    Label(root, text = '￥' + allBalance,width=10,background = "#fff8d3").grid(row=0,column=5)   
    
    #python 3.8 bug 必须有这个配置才能显示颜色
    def fixed_map(option):
        return [elm for elm in style.map("Treeview", query_opt=option) if elm[:2] != ("!disabled", "!selected")]

    style = Style()
    style.map("Treeview", foreground=fixed_map("foreground"), background=fixed_map("background"))


    #账单显示
    table_frame = Frame(root)
    table_frame.grid(row=2, column=0, rowspan=30, columnspan=6,padx=10,pady=5)
    columns = ['时间', '类型', '收支', '金额','备注']
    xscroll = Scrollbar(table_frame, orient=HORIZONTAL)
    yscroll = Scrollbar(table_frame, orient=VERTICAL)
    billTable = Treeview(table_frame, height = 10, columns = columns, show='headings', xscrollcommand=xscroll.set, yscrollcommand=yscroll.set) 
    for column in columns:
        billTable.heading(column=column, text=column, anchor = 'center')  
        billTable.column(column=column, width=100, minwidth=100, anchor=CENTER, )
    
    xscroll.config(command=billTable.xview)
    xscroll.pack(side=BOTTOM, fill=X)
    yscroll.config(command=billTable.yview)
    yscroll.pack(side=RIGHT, fill=Y)
    billTable.pack(fill=BOTH, expand=True)

    for i in obj.getAllBills():
        if i[2]=='+':
            billTable.insert('', END, values = i, tags = 'pinkColor')
            billTable.tag_configure('pinkColor', background = 'pink')
        else:
            billTable.insert('', END, values = i, tags = 'blueColor')
            billTable.tag_configure('blueColor', background = 'lightskyblue')

    #记一笔功能
    def recordABill():
        recordWin = Toplevel(root)
        recordWin.geometry('350x250+350+180')
        recordWin.title("记一笔")

        #获取账单时间timestring
        Label(recordWin, text='日期：').grid(row=0, column=0, sticky ='E')
        timeVar = IntVar()

        timestring = ''
        #选择当前日期或重新选择日期
        def decideTime():
            if timeVar.get():
                chooseTime()
            else:
                global timestring
                timestring = time.ctime()

        timeCur = Radiobutton(recordWin, text="当前日期", variable=timeVar, value=0, command=decideTime)
        timeCur.grid(row=0, column=1, sticky='W')
        
        #重新选择日期
        def chooseTime():
            chooseTimeWin = Toplevel(recordWin)
            chooseTimeWin.title("选择日期")
            chooseTimeWin.geometry('300x90+360+190')

            #选择年份
            yearVar = StringVar()
            yearComb = Combobox(chooseTimeWin, textvariable=yearVar,values=['2016','2017','2018','2019','2020','2021','2022','2023'] )
            yearComb.place(x=10, y=20, width=60, height=20)
            Label(chooseTimeWin,text="年").place(x=80,y=20)
            #选择月份
            monthVar = StringVar()
            monthComb = Combobox(chooseTimeWin, textvariable=monthVar,values=[' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9','10','11','12'] )
            monthComb.place(x=110, y=20, width=50, height=20)
            Label(chooseTimeWin,text="月").place(x=170,y=20)
            #选择日期
            dayVar = StringVar()
            dayComb = Combobox(chooseTimeWin, textvariable=dayVar,values=[' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9','10','11','12','13','14','15',\
               '16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'] )
            dayComb.place(x=200, y=20, width=50, height=20)
            Label(chooseTimeWin,text="日").place(x=260,y=20)

            #确认按钮函数，关闭日期选择窗口
            def confirm():
                monthDict = {' 1':'Jan',' 2':'Feb',' 3':'Mar',' 4':'Apr',' 5':'May',' 6':'Jun',' 7':'Jul',' 8':'Aug',' 9':'Sep','10':'Oct','11':'Nov','12':'Dec'}
                global timestring
                timestring = 'Non ' + monthDict[monthVar.get()] + ' ' + dayVar.get() + ' 12:00:00 ' + yearVar.get()
                chooseTimeWin.destroy()


            #确认按钮
            confirmButton = Button(chooseTimeWin, text="确认", command=confirm)
            confirmButton.place(x=100, y=50)
            chooseTimeWin.mainloop()

        timeCho = Radiobutton(recordWin, text="选择其他日期", variable=timeVar, value=1, command=decideTime)
        timeCho.grid(row=0,column=2, columnspan=2, sticky='W')

        #获取账单类型typestring
        typestring = ''
        typeDict = {1:"餐饮支出",2:"服饰支出",3:"交通支出",4:"购物支出",5:"教育支出",6:"娱乐支出",7:"医疗支出",8:"其他支出",9:"工资奖金",10:"人情红包",\
            11:"收转帐",12:"其他收入"}
        Label(recordWin, text='类型：').grid(row=1, column=0, sticky ='E')
        Label(recordWin,text='          支出          ', background='lightgray').grid(row=1,column=1,columnspan=4, sticky='W')
        typeVar = IntVar()
        eatDrink = Radiobutton(recordWin, text="餐饮支出", variable=typeVar, value=1).grid(row=2,column=1,sticky='W')
        clothes = Radiobutton(recordWin, text="服饰支出", variable=typeVar, value=2).grid(row=2,column=2,sticky='W')
        transportation = Radiobutton(recordWin, text="交通支出", variable=typeVar, value=3).grid(row=2,column=3,sticky='W')
        shopping = Radiobutton(recordWin, text="购物支出", variable=typeVar, value=4).grid(row=2,column=4,sticky='W')
        education = Radiobutton(recordWin, text="教育支出", variable=typeVar, value=5).grid(row=3,column=1,sticky='W')
        entertainment = Radiobutton(recordWin, text="娱乐支出", variable=typeVar, value=6).grid(row=3,column=2,sticky='W')
        medicine = Radiobutton(recordWin, text="医疗支出", variable=typeVar, value=7).grid(row=3,column=3,sticky='W')
        otherout = Radiobutton(recordWin, text="其他支出", variable=typeVar, value=8).grid(row=3,column=4,sticky='W')
        Label(recordWin,text='          收入          ', background='lightgray').grid(row=4,column=1,columnspan=4, sticky='W')
        salary = Radiobutton(recordWin, text="工资奖金", variable=typeVar, value=9).grid(row=5, column=1,sticky='W')
        redPacket = Radiobutton(recordWin, text="人情红包", variable=typeVar, value=10).grid(row=5, column=2,sticky='W')
        transfer = Radiobutton(recordWin, text="收转帐", variable=typeVar, value=11).grid(row=5,column=3,sticky='W')
        otherin = Radiobutton(recordWin, text="其他收入", variable=typeVar, value=12).grid(row=5,column=4,sticky='W')
        typestring = typeVar.get()

        #选择金额moneystring
        Label(recordWin, text='金额：').grid(row=6, column=0, sticky='E')
        Label(recordWin, text='￥').grid(row=6, column=1, sticky='E')
        moneyEntry = Entry(recordWin,width=20)
        moneyEntry.grid(row=6, column=2,columnspan=2, sticky='W')

        
        #留备注commentstring
        Label(recordWin, text='备注：').grid(row=7, column=0, sticky='E')
        commentEntry = Entry(recordWin,width=20)
        commentEntry.grid(row=7, column=2,columnspan=2, sticky='W')

        Label(recordWin, text=' ').grid(row=8, column=0, sticky='E')

        def confirmRecord():
            global timestring
            if timeVar.get() == 0:
                timestring = time.ctime()
            typestring = typeDict[typeVar.get()]
            moneystring = moneyEntry.get()
            allNum = True
            for i in moneystring:
                if (ord(i)>=48 and ord(i)<=57) or ord(i)==46:
                    continue
                else:
                    messagebox.showerror('记录失败', "金额中包含了数字以外的字符，请重新输入格式正确的金额。")
                    allNum = False
                    break
            if allNum == True:
                commentstring = commentEntry.get()
                if typeVar.get() <= 8:
                    if obj.spendMoney(moneystring, typestring, timestring, commentstring) == False:
                        messagebox.showerror('记录失败', "金额超出当前总资产，请重新输入正确的金额。")
                        recordABill()
                else:
                    obj.addMoney(moneystring, typestring, timestring, commentstring)
                recordWin.destroy()
                root.destroy()
                rootFun(name, pwd)
            else:
                recordABill()

        #确认记录按钮
        confirmRecordButton = Button(recordWin, text='确认', command = confirmRecord).grid(row=9, column=2,columnspan=3, sticky='W')

        recordWin.mainloop
    record = Button(root, text = "记一笔", command=recordABill)
    record.grid(row=50, column=1, columnspan=2,ipady=10)

    #删除一条账单
    def delABill():
        toDel = billTable.set(billTable.focus())
        year = toDel['时间'][0:4]
        monthDict = {' 1':'Jan',' 2':'Feb',' 3':'Mar',' 4':'Apr',' 5':'May',' 6':'Jun',' 7':'Jul',' 8':'Aug',' 9':'Sep','10':'Oct','11':'Nov','12':'Dec'}
        monthNum = toDel['时间'][5:7]
        month = monthDict[monthNum]
        day = toDel['时间'][8:10]
        obj.delete(toDel['类型'], year,month,day,toDel['收支'], toDel['金额'], toDel['备注'])
        root.destroy()
        rootFun(name, pwd)

    del_bt = Button(root, text='删一笔', command=delABill)
    del_bt.grid(row=50, column=3, columnspan=2,ipady=10,pady=10)
    root.mainloop()

#登录界面
def entryWinFun():
    entryWin = Tk()
    entryWin.title('小谢记账本')
    entryWin.geometry('300x230+480+250')
    picPath = path + "\\picture\\background.gif"
    bg = PhotoImage(file = picPath)
    bgl = Label(entryWin, image = bg)
    bgl.pack()
    Label(entryWin, text = 'User Name:', background='#fff8d3').place(x=35, y=65, width=80, height=20)
    Label(entryWin, text = 'Password:', background='#fff8d3').place(x=35, y=90, width=80, height=20)
    entryName = Entry(entryWin, width=120)
    entryName.place(x=150, y=65, width=120, height=20)
    entryPwd = Entry(entryWin, width=120)
    entryPwd['show'] = '*'
    entryPwd.place(x=150, y=90, width=120, height=20)

    #登录函数
    def login():
        if checkUser(entryName.get().lower(), entryPwd.get()):
            name = entryName.get().lower()
            pwd = entryPwd.get()
            entryWin.destroy()
            rootFun(name, pwd)
        else:
            messagebox.showerror('用户名或密码错误', "请更改用户名或密码，重新登录；；")

    #注册成功与否提示
    def MakeAccountRoot():
        if MakeAccount(entryName.get().lower(), entryPwd.get()):
            messagebox.showinfo("创建成功！", "您已成功注册账号，请重新打开程序进行登录。\n小谢记账本，陪伴您的每一天(^_^)/")
            entryWin.destroy()
        else:
            messagebox.showerror('创建失败', "此用户名已被使用，请尝试其他的用户名；；")

    loginButton = Button(entryWin, text = "登录", command=login)
    loginButton.place(x=45, y=130, width = 220, height=30)
    Label(entryWin, text="若之前未注册账号，请先选择“创建新账号”", background='#fff8d3').place(x=45, y=170, width=240, height=20)
    makeAccountButton = Button(entryWin, text = "创建新账号", command=MakeAccountRoot)
    makeAccountButton.place(x=45, y=190, width = 220, height=30)
    entryWin.mainloop()
entryWinFun()
