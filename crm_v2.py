#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz

import prettytable, time, random, os

USER_STATE = False
LOGIN_STATE=False
USER_NAME = None

def check_user_type(func):
    def inner(*args, **kwargs):
        if USER_STATE:
            r = func(*args, **kwargs)
            return r
        else:
            print('\033[31;1m用户%s权限不够，管理员才可使用此功能\033[0m' % USER_NAME)
    return inner


def check_user_state(USER_NAME):
    with open('user_info', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(USER_NAME) and USER_NAME == line.split('|')[0]:
                user_states = line.split('|')[4]
                if user_states == '1':
                    global USER_STATE
                    USER_STATE = True
                else:
                    pass
    return USER_STATE

def user_name_list():
    name_list = []
    with open('user_info', 'r') as f:
        for line in f:
            name_list.append(line.strip().split('|')[0])
        return name_list

def user_pwd_list():
    pwd_list = []
    with open('user_info', 'r') as f:
        for line in f:
            pwd_list.append(line.strip().split('|')[1])
        # print(pwd_list)
        return pwd_list

def veri_code():
    li = []
    for i in range(6):
        r = random.randrange(0, 5)
        if r == 1 or r == 4:
            num = random.randrange(0, 9)
            li.append(str(num))
        else:
            temp = random.randrange(65, 91)
            char = chr(temp)
            li.append(char)
    r_code = ''.join(li)
    print('\033[31;1m%s\033[0m' % r_code)
    return r_code

def find_user_line_list(USER_NAME):
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
    new_pwd=input('请输入新的密码:')
    with open('user_info','r') as f,open('user_info_new','w') as new_f:
       for line in f:
            if line.strip().startswith(USER_NAME) and USER_NAME == line.strip().split('|')[0]:
                line_list=find_user_line_list(USER_NAME)
                line_list[1]=new_pwd
                new_line='|'.join(line_list)
                new_f.write('%s\n'%new_line)
            else:
                new_f.write(line)
    os.rename('user_info','user_info.bak')
    os.rename('user_info_new','user_info')
    os.remove('user_info.bak')
    return True

def change_mail(USER_NAME):
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
    with open('user_info', 'r') as f, open('no_pwd', 'w') as new_f:
        for line in f:
            line = line.strip().lower().split('|')
            del line[1]
            line = '|'.join(line)
            new_f.write('%s\n' % line)

@check_user_type
def show_all_user():
    # print('USER_NAME:%s'%USER_NAME)
    # print('USER_STATE:%s'%USER_STATE)
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
    user_info_list = []
    with open('user_info', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(USER_NAME) and USER_NAME == line.split('|')[0]:
                user_info_list.extend(line.split('|'))
        if len(user_info_list) == 0:
            print('无此用户或者没有相关权限')
        else:
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
            info = [name, pwd, mail, tel, '0']
            new_line = '|'.join(info)
            with open('user_info', 'a') as f:
                f.write('%s\n' % new_line)
            break
    return True,name

def login():
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
                            global LOGIN_STATE
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
    no_pwd_file()
    res = []
    search_res_list = []
    user_type = None
    with open('no_pwd', 'r') as f:
        for line in f:
            line = line.strip()
            if keywords in line:
                res.append(line)
    if len(res) == 0:
        print('通过关键字查询,无结果.')
    else:
        for line in res:
            if line.split('|')[3] == '0':
                user_type = '普通用户'
            elif line.split('|')[3] == '1':
                user_type = '管理员'
            li = [line.split('|')[0], line.split('|')[1],
                  line.split('|')[2], user_type, ]
            search_res_list.append(li)
        row = prettytable.PrettyTable()
        row.field_names = ['用户名', '邮箱', '电话', '用户类型']
        for line in search_res_list:
            row.add_row([line[0], line[1], line[2], line[3], ])
        print(row)
    os.remove('no_pwd')

@check_user_type
def update_user(account):
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
    show_all_user()
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
    row=prettytable.PrettyTable()
    row.field_names=['增加用户','删除用户']
    row.add_row([1,2])
    print(row)
    while True:
        inp=input('请选择功能\033[32;1m返回输入back或b\033[0m:')
        if inp == '1':
            res,name=regis()
            if res:
                print('新增用户%s'%name)
                break
        elif inp == '2':
            dele_user()
            break
        elif inp == 'b' or inp == 'back':
            break
        else:
            print('输入有误,请重新输入')

def logout():
    global USER_STATE,LOGIN_STATE,USER_NAME
    USER_STATE, LOGIN_STATE, USER_NAME=False,False,None
    exit('程序已退出！！')

def show_menu():
    row=prettytable.PrettyTable()
    row.field_names=['\033[31;1m模糊查询\033[0m','\033[31;1m查看所有用户\033[0m',
                     '\033[31;1m提升指定用户为管理员\033[0m',
                     '\033[31;1m重置成员密码\033[0m',
                     '\033[31;1m增删成员\033[0m']
    row.add_row([3,4,5,6,7])
    # print('\033[32;1m欢迎来到大牛逼CRM系统\033[0m'.center(75))
    print(row)

def show_menu_2():
    row=prettytable.PrettyTable()
    row.field_names=['查看%s账户信息'%USER_NAME,'修改%s帐户信息'%USER_NAME,
                     '\033[31;1m退出\033[0m']
    row.add_row([1,2,'q&quit'])
    print('\033[32;1m欢迎来到大牛逼CRM系统\033[0m'.center(50))
    print(row)

def main():
    row = prettytable.PrettyTable()
    row.field_names = ['功能', '登录' , '注册用户']
    row.add_row(['快捷键','1','2'])
    print(row)
    inp = input('请输入菜单序列号:')
    if inp == '1':
        global LOGIN_STATE, USER_NAME
        LOGIN_STATE, USER_NAME = login()
        global USER_STATE
        USER_STATE = check_user_state(USER_NAME)
        print('USER_STATE:%s'%USER_STATE)
        if LOGIN_STATE:
            while True:
                show_menu_2()
                if USER_STATE:
                    show_menu()
                else:pass
                inp=input('输入相应序列号,选择相应功能,'
                          '\033[31;1m红色字体为管理员操作,请慎选\033[0m:')
                if inp == '1':
                    show_user_info(USER_NAME)
                    time.sleep(1)
                elif inp == '2':
                    modify_user_info(USER_NAME)
                    time.sleep(1)
                elif inp == '4':
                    show_all_user()
                    time.sleep(1)
                elif inp == '3':
                    keywords = input('请输入您要查询的关键字')
                    res = search(keywords)
                    time.sleep(1)
                elif inp == '5':
                    res=show_all_user()
                    if res:
                        account=input('请输入您要提升的用户账号名称:')
                        name_list=user_name_list()
                        if account in name_list:
                            res=update_user(account)
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
                elif inp == '6':
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
                elif inp == '7':
                    edit_user()
                    time.sleep(1)
                elif inp == 'q' or inp == 'quit':
                    logout()
                else:
                    print('输入有误,请重新输入!')
        else:
            exit('登陆有误,程序退出')
    elif inp == '2':
        res,name=regis()
        if res:
            print('用户%s注册成功' % name)
        else:
            pass
    else:
        exit('选择错误,程序退出')

main()
