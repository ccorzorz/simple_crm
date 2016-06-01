#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
import prettytable, time, random, os
#定义用户角色,登陆状态,登陆用户的全局变量
USER_STATE = False
LOGIN_STATE=False
USER_NAME = None

#装饰器,用来判断用户是否有权限进行管理员操作
def check_user_type(func):
    def inner(*args, **kwargs):
        """
        :param args: 万能参数
        :param kwargs:
        :return:
        """
        if USER_STATE:
            r = func(*args, **kwargs)
            return r
        else:
            print('\033[31;1m用户%s权限不够，管理员才可使用此功能\033[0m' % USER_NAME)
    return inner


def check_user_state(USER_NAME):
    """
    #定义判断用户角色函数
    :param USER_NAME: 登陆用户名
    :return: True:表示用户为管理员角色
    """
    with open('user_info', 'r') as f:
        for line in f:
            line = line.strip()
            #遍历文件,是否以用户名开头,并且文件行内的第一个单词为用户名,并非前若干个字幕组
            #避免用户名首字母相同时出现普通用户越权操作情况出现
            if line.startswith(USER_NAME) and USER_NAME == line.split('|')[0]:
                user_states = line.split('|')[4]
                if user_states == '1':
                    global USER_STATE   #修改全局变量,定义用户为管理员,方便判断权限
                    USER_STATE = True
                else:
                    pass
    return USER_STATE   #函数返回用户的角色状态


def user_name_list():
    """
    #定义用户列表函数,遍历用户信息文件,取用户一列生成列表
    :return: 返回用户列表
    """
    name_list = []
    with open('user_info', 'r') as f:
        for line in f:
            name_list.append(line.strip().split('|')[0])
        return name_list


def user_pwd_list():
    """
    #定义用户密码列表函数,遍历用户信息文件,取密码一列生成列表
    :return:
    """
    pwd_list = []
    with open('user_info', 'r') as f:
        for line in f:
            pwd_list.append(line.strip().split('|')[1])
        return pwd_list


def veri_code():
    """
    #定义随机验证码函数
    :return: 返回生成的随机码
    """
    li = []
    for i in range(6):  #循环6次,生成6个字符
        r = random.randrange(0, 5)  #随机生成0-4之间的数字
        if r == 1 or r == 4:    #如果随机数字是1或者4时,生成0-9的数字
            num = random.randrange(0, 9)
            li.append(str(num))
        else:   #如果不是1或者4时,生成65-90之间的数字
            temp = random.randrange(65, 91)
            char = chr(temp)    #将数字转化为ascii列表中对应的字母
            li.append(char)
    r_code = ''.join(li)    #6个字符拼接为字符串
    print('\033[31;1m%s\033[0m' % r_code)
    return r_code   #返回字符串


def find_user_line_list(USER_NAME):
    """
    #定义函数,查找用户信息文件中包含当前登录用户的文件内容,并将其转化为列表
    :param USER_NAME: 当前登录用户
    :return: line_list 返回生成的列表
    """
    with open('user_info','r') as f:
       for line in f:
            if line.strip().startswith(USER_NAME) and USER_NAME == line.strip().split('|')[0]:
                user_name=USER_NAME
                pwd=line.strip().split('|')[1]
                mail=line.strip().split('|')[2]
                tel=line.strip().split('|')[3]
                user_t=line.strip().split('|')[4]
                line_list=[user_name,pwd,mail,tel,user_t]
            else:
                pass
    return line_list


def change_pwd(USER_NAME):
    """
    定义修改当前用户密码的函数
    :param USER_NAME:
    :return:
    """
    new_pwd=input('请输入新的密码:')
    with open('user_info','r') as f,open('user_info_new','w') as new_f:
       for line in f:
            if line.strip().startswith(USER_NAME) and USER_NAME == line.strip().split('|')[0]:
                line_list=find_user_line_list(USER_NAME)    #调用查找并生成列表的函数并赋值变量
                line_list[1]=new_pwd    #修改其中的值
                new_line='|'.join(line_list)    #拼接为字符串
                new_f.write('%s\n'%new_line)    #写入新文件
            else:
                new_f.write(line)   #如果非匹配内容,直接写入新文件
    os.rename('user_info','user_info.bak')  #修改文件名称
    os.rename('user_info_new','user_info')
    os.remove('user_info.bak')  #删除旧文件
    return True


def change_mail(USER_NAME):
    """
    定义修改当前用户邮箱的函数,和上一个函数相同,不同的是将新的邮箱赋值到邮箱的下标位置
    :param USER_NAME: 当前登录用户
    :return: 如果修改成功,返回True,
    """
    new_mail=input('请输入新邮箱:')
    with open('user_info','r') as f,open('user_info_new','w') as new_f:
       for line in f:
            if line.strip().startswith(USER_NAME) and USER_NAME == line.strip().split('|')[0]:
                line_list=find_user_line_list(USER_NAME)
                line_list[2]=new_mail
                new_line='|'.join(line_list)
                new_f.write('%s\n'%new_line)
            else:
                new_f.write(line)
    os.rename('user_info','user_info.bak')
    os.rename('user_info_new','user_info')
    os.remove('user_info.bak')
    return True


def change_tel(USER_NAME):
    """
    修改当前登录用户电话号码函数,方法同上
    :param USER_NAME: 当前登录用户
    :return: 修改成功,返回Ture
    """
    new_tel=input('请输入新的电话号码:')
    with open('user_info','r') as f,open('user_info_new','w') as new_f:
       for line in f:
            if line.strip().startswith(USER_NAME) and USER_NAME == line.strip().split('|')[0]:
                line_list=find_user_line_list(USER_NAME)
                line_list[3]=new_tel
                new_line='|'.join(line_list)
                new_f.write('%s\n'%new_line)
            else:
                new_f.write(line)
    os.rename('user_info','user_info.bak')
    os.rename('user_info_new','user_info')
    os.remove('user_info.bak')
    return True


def modify_user_info(USER_NAME):
    """
    修改当前用户信息函数
    :param USER_NAME: 当前用户账号
    :return: 修改成功,返回True
    """
    row=prettytable.PrettyTable()
    row.field_names=['修改密码','修改邮箱','修改联系电话']
    row.add_row([1,2,3])
    print(row)
    while True:
        inp=input('请选择功能菜单,\033[32;1m返回主菜单请输入b或者back\033[0m:')
        if inp == '1':
            res=change_pwd(USER_NAME)
            if res:
                print('密码修改成功')
                break
        elif inp == '2':
            res=change_mail(USER_NAME)
            if res:
                print('邮箱修改成功')
                break
        elif inp == '3':
            res=change_tel(USER_NAME)
            if res:
                print('电话修改成功')
                break
        elif inp == 'back' or inp == 'b':
            break
        else:
            print('输入有误,请重新输入!')
    return True

def no_pwd_file():
    """
    依据用户信息文件,去除密码一列生成新文件,避免模糊搜索时将密码也匹配
    :return: None
    """
    with open('user_info', 'r') as f, open('no_pwd', 'w') as new_f:
        for line in f:
            line = line.strip().lower().split('|')
            del line[1]
            line = '|'.join(line)
            new_f.write('%s\n' % line)

@check_user_type
def show_all_user():
    """
    装饰器做权限判断,显示所有用户的信息,显示时将密码以*代替
    :return: 成功生成后,返回True
    """
    no_pwd_file()
    row = prettytable.PrettyTable()
    row.field_names = ['用户名', '密码', '邮箱', '电话', '账户类型']
    with open('no_pwd','r') as f:
        for line in f:
            line = line.strip()
            if line.split('|')[3]=='1':
                user_type='管理员'
            elif line.split('|')[3]=='0':
                user_type='普通用户'
            row.add_row([line.split('|')[0],'***',line.split('|')[1],
                         line.split('|')[2],user_type])
    print(row)
    os.remove('no_pwd')
    return True

def show_user_info(USER_NAME):
    """
    显示当前登录用户的信息
    :param USER_NAME: 当前登录用户
    :return: None
    """
    user_info_list = []     #定义一个空列表
    with open('user_info', 'r') as f:
        for line in f:  #遍历文件,匹配到当前用户,并将内容分割为列表,添加入空列表
            line = line.strip()
            if line.startswith(USER_NAME) and USER_NAME == line.split('|')[0]:
                user_info_list.extend(line.split('|'))
        if len(user_info_list) == 0:    #如果为空,说明无匹配内容
            print('无此用户或者没有相关权限')
        else:    #如果非空,将内容打印,密码做加密处理
            user_type = None
            if user_info_list[4] == '1':
                user_type = '管理员'
            elif user_info_list[4] == '0':
                user_type = '普通用户'
            row = prettytable.PrettyTable()
            row.field_names = ['用户名', '密码', '邮箱', '电话', '账户类型']
            row.add_row([user_info_list[0], '****', user_info_list[2],
                         user_info_list[3], user_type])
            print(row)

def regis():
    """
    定义注册函数,注册时,角色默认为普通用户
    :return: 注册成功返回True,如果已经有此用户名,返回False,name为注册用户名
    """
    name_list = user_name_list()
    i = 0
    while i < 3:
        name = input('请输入用户名:')
        if name in name_list:
            print('用户名%s已被注册' % name)
            i += 1
            return False,name
        else:
            pwd = input('请输入密码:')
            mail = input('请输入邮箱:')
            tel = input('请输入电话:')
            info = [name, pwd, mail, tel, '0']  #默认注册时,角色为普通用户
            new_line = '|'.join(info)   #将列表元素拼接为字符串
            with open('user_info', 'a') as f:
                f.write('%s\n' % new_line)
            break
    return True,name

def login():
    """
    登陆函数,有3次输入用户,密码机会,并且加入了随机验证码功能
    验证校验码有3次机会
    :return: LOGIN_STATE:登陆状态 USER_NAME:登陆用户名
    """
    name_list = user_name_list()
    pwd_list = user_pwd_list()
    exit_flag = 0
    i_a = 0
    i_b = 0
    i_c = 0
    while i_a < 3 and exit_flag == 0:
        USER_NAME= input('请输入用户名:')
        if USER_NAME in name_list:
            while i_b < 3 and exit_flag == 0:
                pwd = input('请输入%s的密码:' % USER_NAME)
                if pwd == pwd_list[name_list.index(USER_NAME)]:
                    while i_c < 3 and exit_flag == 0:
                        r_code = veri_code()
                        c_cod = input('请输入红色字体显示的校验码:')
                        if c_cod.lower() == r_code.lower():
                            global LOGIN_STATE  #修改全局变量登陆状态
                            LOGIN_STATE = True
                            print("登陆成功")
                            exit_flag = 1
                        elif i_c == 2:
                            exit_flag = 1
                            print('验证次数超过三次,登陆退出...')
                        else:
                            i_c += 1
                            '校验码不正确,请重新验证'
                elif i_b == 2:
                    exit_flag = 1
                    print('尝试次数过多,退出登陆系统.')
                else:
                    i_b += 1
                    print('密码不正确,请重新输入..')
        else:
            i_a += 1
            print('无此账户,请确认用户名')
    return LOGIN_STATE, USER_NAME

@check_user_type
def search(keywords):
    """
    装饰器做权限判断,定义搜索函数,文件为no_pwd文件,避免匹配密码字段
    :param keywords: 搜索时的关键字
    :return: None
    """
    no_pwd_file()
    res = []
    search_res_list = []
    user_type = None    #定义用户角色变量
    with open('no_pwd', 'r') as f:
        for line in f:  #遍历文件,匹配关键字,并将结果添加进空列表
            line = line.strip()
            if keywords in line:
                res.append(line)
    if len(res) == 0:
        print('通过关键字查询,无结果.')
    else:
        for line in res:
            #判断用户角色,如果为0赋值为普通用户,如果为1赋值为管理员
            if line.split('|')[3] == '0':
                user_type = '普通用户'
            elif line.split('|')[3] == '1':
                user_type = '管理员'
            #列表中元素拆分,加入空列表
            li = [line.split('|')[0], line.split('|')[1],
                  line.split('|')[2], user_type, ]
            search_res_list.append(li)
        #打印列表中的元素
        row = prettytable.PrettyTable()
        row.field_names = ['用户名', '邮箱', '电话', '用户类型']
        for line in search_res_list:
            row.add_row([line[0], line[1], line[2], line[3], ])
        print(row)
    os.remove('no_pwd') #删除no_pwd文件

@check_user_type
def update_user(account):
    """
    装饰器判断权限,管理员指定用户提升权限
    :param account: 指定的用户账号
    :return: 修改成功,返回True,如果已经为管理员,返回False
    """
    with open('user_info','r') as f,open('user_info_new','w') as new_f:
        for line in f:
            if line.strip().startswith(account) and account == line.strip().split('|')[0]:
                new_line_list=line.strip().split('|')
                if new_line_list[4] == '1':
                    return False
                else:
                    new_line_list[4]='1'
                    new_line='|'.join(new_line_list)
                    new_f.write('%s\n'%new_line)
            else:
                new_f.write(line)
    os.rename('user_info','user_info.bak')
    os.rename('user_info_new','user_info')
    os.remove('user_info.bak')
    return True

@check_user_type
def reset_pwd(account,new_pwd):
    """
    管理员充值用户密码
    :param account: 指定用户账号
    :param new_pwd: 新密码
    :return: 修改成功,返回True
    """
    with open('user_info','r') as f,open('user_info_new','w') as new_f:
        for line in f:
            if line.strip().startswith(account) and account == line.strip().split('|')[0]:
                new_line_list=line.strip().split('|')
                new_line_list[1]=new_pwd
                new_line='|'.join(new_line_list)
                new_f.write('%s\n'%new_line)
            else:
                new_f.write(line)
    os.rename('user_info','user_info.bak')
    os.rename('user_info_new','user_info')
    os.remove('user_info.bak')
    return True

@check_user_type
def dele_user():
    """
    管理员权限,删除用户函数
    :return: None
    """
    show_all_user() #调用显示所有用户信息函数
    name=input('输入您要删除的用户')
    name_list=user_name_list()
    if name in name_list:
        with open('user_info','r') as f,open('user_info_new','w') as new_f:
            for line in f:
                if line.strip().startswith(name) and name == line.strip().split('|')[0]:
                     pass
                else:
                    new_f.write(line)
        os.rename('user_info','user_info.bak')
        os.rename('user_info_new','user_info')
        os.remove('user_info.bak')
        print('账户%s删除完毕'%name)
    else:
        print('无%s的账户信息,请确认后再操作'%name)

@check_user_type
def edit_user():
    """
    管理员权限,编辑用户信息
    :return: None
    """
    #显示选择菜单
    row=prettytable.PrettyTable()
    row.field_names=['增加用户','删除用户']
    row.add_row([1,2])
    print(row)
    while True:
        inp=input('请选择功能\033[32;1m返回输入back或b\033[0m:')
        if inp == '1':  #新增用户调用注册函数
            res,name=regis()
            if res:
                print('新增用户%s'%name)
                break
        elif inp == '2':    #删除用户调用删除用户函数
            dele_user()
            break
        elif inp == 'b' or inp == 'back':
            break
        else:
            print('输入有误,请重新输入')

def logout():
    """
    退出程序函数,将全局变量修改回初始值
    :return: None
    """
    global USER_STATE,LOGIN_STATE,USER_NAME
    USER_STATE, LOGIN_STATE, USER_NAME=False,False,None
    exit('程序已退出！！')

def show_menu():
    """
    显示主菜单函数
    :return: None
    """
    row=prettytable.PrettyTable()
    row.field_names=['查看%s账户信息'%USER_NAME,'修改%s帐户信息'%USER_NAME,
                     '\033[31;1m模糊查询\033[0m','\033[31;1m查看所有用户\033[0m',
                     '\033[31;1m提升指定用户为管理员\033[0m',
                     '\033[31;1m重置成员密码\033[0m',
                     '\033[31;1m增删成员\033[0m','退出']
    row.add_row([1,2,3,4,5,6,7,'q&quit'])
    print('\033[32;1m欢迎来到大牛逼CRM系统\033[0m'.center(120))
    print(row)

def main():
    """
    定义主函数
    :return: None
    """
    row = prettytable.PrettyTable()
    row.field_names = ['功能', '登录' , '注册用户']
    row.add_row(['快捷键','1','2'])
    print(row)
    inp = input('请输入菜单序列号:')
    if inp == '1':
        global LOGIN_STATE, USER_NAME   #修改全局变量,重新赋值
        LOGIN_STATE, USER_NAME = login()
        global USER_STATE   #修改全局变量,调用判断用户角色函数,并赋值
        USER_STATE = check_user_state(USER_NAME)
        if LOGIN_STATE: #如果登陆成功,执行以下
            while True:
                show_menu() #调用显示主菜单函数,
                inp=input('输入相应序列号,选择相应功能,'
                          '\033[31;1m红色字体为管理员操作,请慎选\033[0m:')
                if inp == '1':
                    show_user_info(USER_NAME)   #显示本账号信息
                    time.sleep(1)
                elif inp == '2':    #修改本账号信息
                    modify_user_info(USER_NAME)
                    time.sleep(1)
                elif inp == '4':    #管理员权限,显示所有用户
                    show_all_user()
                    time.sleep(1)
                elif inp == '3':    #管理员权限,关键字模糊查询
                    keywords = input('请输入您要查询的关键字')
                    res = search(keywords)
                    time.sleep(1)
                elif inp == '5':    #管理员提升指定用户权限
                    res=show_all_user()
                    if res:
                        account=input('请输入您要提升的用户账号名称:')
                        name_list=user_name_list()  #调用用户列表函数
                        if account in name_list:    #如果指定用户在用户列表中
                            res=update_user(account)    #调用提升权限函数
                            if res:
                                print('权限提升成功')
                            else:
                                print('\033[31;1m%s已经是管理员,'
                                      '无需提升权限!\033[0m'%account)
                            time.sleep(1)
                        else:
                            print('\033[31;1m无此账户:%s信息\033[0m'%account)
                    else:
                        pass
                    time.sleep(1)
                elif inp == '6':    #管理员重置用户密码
                    res=show_all_user()
                    if res:
                        account=input('请输入您要修改用户账号名称:')
                        name_list=user_name_list()
                        if account in name_list:
                            new_pwd=input('请输入账户的新密码:')
                            res=reset_pwd(account,new_pwd)
                            if res:
                                print('密码已重置成功')
                        else:
                            print('\033[31;1m无此账户:%s信息\033[0m'%account)
                        time.sleep(1)
                    else:
                        pass
                        time.sleep(1)
                elif inp == '7':    #管理员编辑用户信息
                    edit_user()
                    time.sleep(1)
                if inp == 'q' or inp == 'quit': #退出
                    logout()    #调用退出函数
                else:
                    print('输入有误,请重新输入!')
        else:
            exit('登陆有误,程序退出')
    elif inp == '2':    #调用注册函数
        res,name=regis()
        if res:
            print('用户%s注册成功' % name)
        else:
            pass
    else:
        exit('选择错误,程序退出')

#调用主函数
main()
