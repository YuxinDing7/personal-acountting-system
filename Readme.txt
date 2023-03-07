###  “小谢记账本” 简介###
“小谢记账本”是一个基本的个人记账系统，拥有账户注册登录系统，可以实现记录账单，删除某条账单，查询某一特定类型的账单，查询某日，某月，某年账单，并根据账单数据生成对应图表的功能。

### 项目运行方法 ###
需要将本项目文件personal_accounting_system在python编译器中打开。将pyFiles中的main.py文件设为启动文件。Script path为……personal_accounting_system\pyFiles\main.py，working directory为personal_accounting_system文件夹所在地址。需要额外安装matplotlib库。

### 注意事项 ###
在第一次注册新账号后，需要重新打开程序再登录。

###文件目录###
personal_accounting_system
│
│  Readme.txt
│  
├─picture
│      background.gif
│      
├─pyFiles
│      accountClass.py
│      main.py  
│                   
├─usersFiles
        sample2billFile.csv
        users.csv