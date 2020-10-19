from django.shortcuts import render, HttpResponse, redirect
from app01 import models

# Create your views here.


def login(request):
    '''
    get请求和post请求，应该有不同的处理机制
    :param request:  请求相关的数据对象，里面有很多的简易方法
    :return:
    '''
    # if request.method == 'GET':
    #     print(request.method)  # 返回请求方式并且是全大写的字符串形式  <class 'str'>
    #     return render(request, "login.html")
    # elif request.method == 'POST':
    #     return HttpResponse("I'm a post request")

    if request.method == 'POST':
        # print(request.POST)  # 获取用户提交的POST请求数据（不包含文件）
        # # < QueryDict: {'password': ['passworf'], 'username': ['username']} >
        # # 字典的键取决于前端 input框的name值
        # username = request.POST.get('username')
        # print(username, type(username))   # ada <class 'str'>
        # # hobby = request.POST.get("hobby")
        # # print(hobby, type(hobby)) # 333 <class 'str'>
        # '''
        # get只会获取列表最后一个元素
        # getlist 获取整个列表的数据'''
        # hobby = request.POST.getlist("hobby")
        # print(hobby, type(hobby))   # ['111', '222', '333'] <class 'list'>
        # 获取url后面携带的数据
        # print(request.GET)
        # 获取用户的用户名和密码，利用orm 操作数据校验数据是否正确
        username = request.POST.get('username')
        password = request.POST.get('password')
        #  select * from User where username = "mxxx"
        user_obj = models.User.objects.filter(username=username).first()
        # <QuerySet [<User: User object>]> [数据对象1 ，数据对象2]
        # [17/Oct/2020 11:57:31] "GET /login/?usernam
        # e=sdasd&password=asdasds&hobby=111&hobby=222&hobby=333 HTTP/1.1" 200 1185
        if user_obj:
            # 比对密码是否一致
            if password == user_obj.password:
                return HttpResponse('登陆成功')
            else:
                return HttpResponse('密码错误')
        else:
            return HttpResponse("用户不存在")
    return render(request, "login.html")


def reg(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 直接获取用户数据存入数据库
        # 第一种增加数据的方法
        # res = models.User.objects.create(username=username, password=password)
        # 返回值就是当前被创建的对象本身  User object www 123
        # print(res, res.username, res.password)
        # 第二种增加数据的方法
        user_obj = models.User(username=username, password=password)
        user_obj.save()  # 保存数据

    # 先给用户返回一个注册页面
    return render(request, "reg.html")


def user_list(request):
    # 查询出用户表里的所有数据
    # 方式1
    # data = models.User.objects.filter()
    # print(data)
    user_queryset = models.User.objects.all()
    # print(user_queryset)
    # return HttpResponse('hello world')
    # <QuerySet [<User: User object>, <User: User object>,
    # <User: User object>, <User: User object>]>
    # return render(request, 'user_list.html', {'user_queryset':user_queryset})
    return render(request, 'user_list.html', locals())


def edit_list(request):
    # 获取url后面的参数
    edit_id = request.GET.get('user_id')
    # 查询当前用户想要编辑的数据对象
    edit_obj = models.User.objects.filter(id=edit_id).first()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 去数据中修改对应的数据内容
        # 修改数据方式1
        # models.User.objects.filter(id=edit_id).update(username=username, password=password)
        '''
        将filter查询出来的列表中的所有的对象全部更新     批量更新操作
        '''
        # 修改数据方式2
        edit_obj.username = username
        edit_obj.password = password
        edit_obj.save()
        # 跳转到数据的展示页面
        return redirect('/user_list')

    # 查询当前用户想要编辑的数据对象
    # edit_obj = models.User.objects.filter(id=edit_id).first()
    # 将数据对象展示到页面上
    return render(request, 'edit_user.html', locals())


def delete_user(request):
    # 获取用户想要删除的数据的id值
    delete_id = request.GET.get('user_id')
    # 直接去数据库中找到对应的数据删除即可
    models.User.objects.filter(id=delete_id).delete()
    '''
    批理删除
    '''
    # 跳转到展示页面

    return redirect('/user_list/')