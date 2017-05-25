from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from . import models
from .models import UserProfile, Course
from django.contrib.auth.models import User
from website.forms import LoginForm
from django.contrib import auth
from django.db.models import Q
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import django

django.setup()


# Create your views here.
# login & logout
def login(request):
    if request.user.is_authenticated():
        user = request.user
        allcourses = models.Course.objects.filter(user_id=user.id)
        getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
        courses = []
        for i in getcourses:
            if i not in courses:
                courses.append(i)
        return render(request, 'website/platform.html', {'user': user, 'courses': courses, 'allcourses': allcourses})
    else:
        return render(request, 'website/login.html', {'form': LoginForm})


def alogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                allcourses = models.Course.objects.filter(user_id=user.id)
                getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
                courses = []
                for i in getcourses:
                    if i not in courses:
                        courses.append(i)
                return render(request, 'website/platform.html',
                              {'user': user, 'courses': courses, 'allcourses': allcourses})
            else:
                wrongpw = '1'
                form = LoginForm()
                return render(request, 'website/login.html', {'wrongpw': wrongpw, 'form': form})
    else:
        form = LoginForm()
        return render(request, 'website/login.html', {'form': form})


def alogout(request):
    auth.logout(request)
    form = LoginForm()
    return render(request, 'website/login.html', {'form': form})


# dashboard & profiles
def viewprofile(request):
    user = request.user
    courses = models.Course.objects.filter(user_id=user.id)
    return render(request, 'website/profile.html', {'user': user, 'courses': courses})


def dashboard(request):
    user = request.user
    allcourses = models.Course.objects.filter(user_id=user.id)
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    courses = []
    for i in getcourses:
        if i not in courses:
            courses.append(i)
    return render(request, 'website/platform.html', {'user': user, 'courses': courses, 'allcourses': allcourses})


def updateprofile(request):
    if request.method == 'POST':
        username = request.user.username
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phone = request.POST['phone']
        gender = request.POST['gender']
        major = request.POST['major']
        user = models.User.objects.get(username=username)
        models.User.objects.filter(username=username).update(email=email, first_name=firstname, last_name=lastname)
        models.UserProfile.objects.filter(user_id=user.id).update(phone=phone, gender=gender, major=major)
        # reget user
        user = models.User.objects.get(username=username)
        courses = models.Course.objects.filter(user_id=user.id)
        return render(request, 'website/profile.html', {'user': user, 'courses': courses})
    else:
        return HttpResponse('error occurred')


def updatepw(request):
    getuser = request.user
    courses = models.Course.objects.filter(user_id=getuser.id)
    user = User.objects.get(id=getuser.id)
    if request.method == 'POST':
        pw = request.POST['pw']
        user.set_password(pw)
        user.save()
        auth.logout(request)
        return HttpResponseRedirect(reverse('website:login'))
    return render(request, 'website/change_pw.html', {'courses': courses})


# discuss
def discuss(request, code):
    # 打开页面信息
    user = request.user
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    courses = []
    for i in getcourses:
        if i not in courses:
            courses.append(i)
    selected_courses = models.Course.objects.filter(code=code, user_id=user.id).values('coursename', 'code')
    selected_course = []
    for i in selected_courses:
        if i not in selected_course:
            selected_course.append(i)
    students = models.User.objects.all()
    # 讨论发言
    if request.method == 'POST':
        content = request.POST['sendmessage']
        if content == '':
            pass
        else:
            models.Discuss.objects.create(code=code, time=datetime.datetime.now(), content=content, user_id=user.id)
    # 内容分页
    contents_list = models.Discuss.objects.filter(code=code).order_by('time')
    paginator = Paginator(contents_list, 5)  # 默认每页显示数量
    page = request.GET.get('page', paginator.num_pages)  # 和前端互动获取page
    try:
        contents = paginator.page(page)  # 默认打开page
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        contents = paginator.page(paginator.num_pages)
    return render(request, 'website/discuss.html',
                  {'courses': courses, 'selected_course': selected_course, 'user': user, 'contents': contents,
                   'students': students, 'code': code})


# Consult
def consult(request, code):
    # 打开页面信息
    user = request.user
    selected_courses = models.Course.objects.filter(code=code, user_id=user.id).values('coursename', 'code',
                                                                                       'is_teacher')
    selected_course = []
    for i in selected_courses:
        if i not in selected_course:
            selected_course.append(i)
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    courses = []
    for i in getcourses:
        if i not in courses:
            courses.append(i)
    code = code
    # function
    for selectcourse in selected_course:
        if selectcourse['is_teacher'] == '1':
            gettitles = models.Consult.objects.filter(code=code).values('title')
            titles = []
            isteacher = True
            for i in gettitles:
                if i not in titles:
                    titles.append(i)
            return render(request, 'website/consult-main.html',
                          {'courses': courses, 'selected_course': selected_course, 'titles': titles, 'code': code,
                           'isteacher': isteacher})
        else:
            gettitles = models.Consult.objects.filter(user_id=user.id, code=code).values('title')
            titles = []
            isteacher = False
            for i in gettitles:
                if not i in titles:
                    titles.append(i)
            return render(request, 'website/consult-main.html',
                          {'courses': courses, 'selected_course': selected_course, 'titles': titles, 'code': code,
                           'isteacher': isteacher})


def consult_talk(request, code, title):
    # 打开页面信息
    user = request.user
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    courses = []
    for i in getcourses:
        if i not in courses:
            courses.append(i)
    selected_courses = models.Course.objects.filter(code=code, user_id=user.id).values('coursename', 'code')
    selected_course = []
    for i in selected_courses:
        if i not in selected_course:
            selected_course.append(i)
    students = models.User.objects.all()
    title = title
    code = code
    # comments
    if request.method == 'POST':
        content = request.POST['sendmessage']
        if content == '':
            pass
        else:
            models.Consult.objects.create(code=code, time=datetime.datetime.now(), content=content, user_id=user.id,
                                          title=title)
    # 内容分页
    consults_list = models.Consult.objects.filter(title=title, code=code)
    paginator = Paginator(consults_list, 5)  # 默认每页显示数量
    page = request.GET.get('page', paginator.num_pages)  # 和前端互动获取page
    try:
        consults = paginator.page(page)  # 默认打开page
    except PageNotAnInteger:
        consults = paginator.page(1)
    except EmptyPage:
        consults = paginator.page(paginator.num_pages)
    return render(request, 'website/consult-talk.html',
                  {'courses': courses, 'selected_course': selected_course, 'consults': consults, 'students': students,
                   'title': title, 'code': code})


def consult_new(request, code):
    # 打开页面信息
    user = request.user
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    courses = []
    for i in getcourses:
        if i not in courses:
            courses.append(i)
    selected_courses = models.Course.objects.filter(code=code, user_id=user.id).values('coursename', 'code')
    selected_course = []
    for i in selected_courses:
        if i not in selected_course:
            selected_course.append(i)
    students = models.User.objects.all()
    code = code
    # new consult
    if request.method == 'POST':
        content = request.POST['content']
        title = request.POST['title']
        if content == '' or title == '':
            pass
        else:
            models.Consult.objects.create(code=code, time=datetime.datetime.now(), content=content, user_id=user.id,
                                          title=title)
            consults = models.Consult.objects.filter(title=title, code=code)
            return render(request, 'website/consult-talk.html',
                          {'courses': courses, 'selected_course': selected_course, 'consults': consults,
                           'students': students,
                           'title': title, 'code': code})
    return render(request, 'website/consult_new.html',
                  {'courses': courses, 'selected_courses': selected_course, 'code': code})


# Message
def message(request):
    # 打开页面信息
    user = request.user
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    courses = []
    for i in getcourses:
        if i not in courses:
            courses.append(i)
    # function
    alluser = models.User.objects.all()
    getreceiver = models.Message.objects.filter(Q(user_id=user.id) | Q(receive_id=user.id)).values('receive_id', 'user_id', 'first')
    receivers = []
    for i in getreceiver:
        if not i in receivers:
            receivers.append(i)
    return render(request, 'website/message-main.html',
                  {'courses': courses, 'receivers': receivers, 'alluser': alluser, 'user': user})


def message_talk(request, receiveid, first):
    # 打开页面信息
    user = request.user
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    courses = []
    for i in getcourses:
        if i not in courses:
            courses.append(i)
    # function comments
    alluser = models.User.objects.all()
    receiveid = receiveid
    if request.method == 'POST':
        content = request.POST['sendmessage']
        if first == '1':
            models.Message.objects.filter(user_id=receiveid).update(first='0')
        if content == '':
            pass
        else:
            models.Message.objects.create(time=datetime.datetime.now(), content=content, receive_id=receiveid,
                                          user_id=user.id, first='0')
    # 内容分页
    message_list = models.Message.objects.filter(
        Q(user_id=user.id, receive_id=receiveid) | Q(user_id=receiveid, receive_id=user.id)).order_by('time')
    paginator = Paginator(message_list, 5)  # 默认每页显示数量
    page = request.GET.get('page', paginator.num_pages)  # 和前端互动获取page
    try:
        messages = paginator.page(page)  # 默认打开page
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)

    return render(request, 'website/message-talk.html',
                  {'courses': courses, 'alluser': alluser, 'messages': messages, 'user': user, 'receiveid': receiveid, 'first': first})


def message_new(request):
    # 打开页面信息
    user = request.user
    courses = models.Course.objects.filter(user_id=user.id)
    alluser = models.User.objects.all()
    first = '1'
    # new message
    if request.method == 'POST':
        content = request.POST['content']
        receiveid = request.POST['receiver']
        if content == '':
            pass
        else:
            models.Message.objects.create(time=datetime.datetime.now(), content=content, receive_id=receiveid,
                                          user_id=user.id, first='1')
            messages = models.Message.objects.filter(
                Q(user_id=user.id, receive_id=receiveid) | Q(user_id=receiveid, receive_id=user.id)).order_by('time')
            return render(request, 'website/message-talk.html',
                          {'courses': courses, 'alluser': alluser, 'messages': messages, 'user': user,
                           'receiveid': receiveid, 'first': first})
    return render(request, 'website/message-new.html', {'courses': courses, 'alluser': alluser})


# Bulletin
def bulletin(request):
    # 打开页面信息
    user = request.user
    courses = models.Course.objects.filter(user_id=user.id)
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    dashboardcourse = []
    for i in getcourses:
        if i not in dashboardcourse:
            dashboardcourse.append(i)
    alluser = models.User.objects.all()
    # 获取公告
    bulletins = []
    isteacher = False
    for course in courses:
        if course.is_teacher == '1':  # 教师权限发布公告
            isteacher = True
        bulletins_add = models.Bulletin.objects.filter(
            Q(code=course.code, classes=course.classes) | Q(code=course.code, classes='0')).order_by('time')
        for i in bulletins_add:
            if not i in bulletins:
                bulletins.append(i)
    return render(request, 'website/bulletin-main.html',
                  {'courses': courses, 'alluser': alluser, 'bulletins': bulletins, 'isteacher': isteacher,
                   'dcourse': dashboardcourse})


def bulletin_get(request, bulletinid):
    # 打开页面信息
    user = request.user
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    courses = []
    for i in getcourses:
        if i not in courses:
            courses.append(i)
    # 获取打开的公告
    bulletins = models.Bulletin.objects.get(id=bulletinid)
    return render(request, 'website/bulletin-get.html', {'courses': courses, 'bulletins': bulletins})


def bulletin_new(request):
    # 打开页面信息
    user = request.user
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    courses = []
    for i in getcourses:
        if i not in courses:
            courses.append(i)
    alluser = models.User.objects.all()
    # 新建公告
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        code = request.POST['code']
        classes = request.POST['classes']
        if content == '' or title == '':
            pass
        else:
            models.Bulletin.objects.create(title=title, code=code, classes=classes, time=datetime.datetime.now(),
                                           content=content, user_id=user.id)
            bulletins = models.Bulletin.objects.get(content__contains=content)
            return render(request, 'website/bulletin-get.html', {'courses': courses, 'bulletins': bulletins})
    return render(request, 'website/bulletin-new.html', {'courses': courses, })


# file sharing
def uploaded_file(request):
    # 打开页面信息
    user = request.user
    courses = models.Course.objects.filter(user_id=user.id)
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    dashboardcourse = []
    for i in getcourses:
        if i not in dashboardcourse:
            dashboardcourse.append(i)
    alluser = models.User.objects.all()
    # 文件卡片
    isteacher = False
    filelist = []
    for course in courses:
        if course.is_teacher == '1':  # 是否教师
            isteacher = True
        files = models.Uploaded_files.objects.filter(
            Q(code=course.code, classes=course.classes) | Q(code=course.code, classes='0'))
        for file in files:
            if not file in filelist:
                filelist.append(file)

    return render(request, 'website/file-main.html',
                  {'courses': courses, 'alluser': alluser, 'isteacher': isteacher, 'filelist': filelist,
                   'dcourse': dashboardcourse})


def file_upload(request):
    # 打开页面信息
    user = request.user
    courses = models.Course.objects.filter(user_id=user.id)
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    dashboardcourse = []
    for i in getcourses:
        if i not in dashboardcourse:
            dashboardcourse.append(i)
    alluser = models.User.objects.all()
    # upload file
    if request.method == 'POST':
        code = request.POST['code']
        classes = request.POST['classes']
        file = request.FILES['file']
        if code == '' or not file:
            pass
        else:
            models.Uploaded_files.objects.create(user_id=user.id, classes=classes, code=code,
                                                 time=datetime.datetime.now(), file=file)
            isteacher = True
            filelist = []
            for course in courses:
                files = models.Uploaded_files.objects.filter(
                    Q(code=course.code, classes=course.classes) | Q(code=course.code, classes='0'))
                for file in files:
                    if not file in filelist:
                        filelist.append(file)
            return render(request, 'website/file-main.html',
                          {'courses': courses, 'alluser': alluser, 'isteacher': isteacher, 'filelist': filelist})
    return render(request, 'website/file-upload.html', {'courses': courses, 'alluser': alluser, 'dcourse': dashboardcourse})


def file_delete(request, path):
    # 删除文件
    path = path
    models.Uploaded_files.objects.filter(file=path).delete()
    return HttpResponseRedirect(reverse('website:file'))


# assignment
def assignment(request):
    # 打开页面信息
    user = request.user
    courses = models.Course.objects.filter(user_id=user.id)
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    dashboardcourse = []
    for i in getcourses:
        if i not in dashboardcourse:
            dashboardcourse.append(i)
    alluser = models.User.objects.all()
    # 显示作业
    assignments = []
    isteacher = False
    for course in courses:
        if course.is_teacher == '1':
            isteacher = True
        assignment_add = models.Assignment.objects.filter(code=course.code, classes=course.classes)
        for i in assignment_add:
            if not i in assignments:
                assignments.append(i)

    return render(request, 'website/assignment-main.html',
                  {'courses': courses, 'alluser': alluser, 'assignments': assignments, 'isteacher': isteacher,
                   'dcourse': dashboardcourse})


def assignment_new(request, assignments_id):
    # 打开页面信息
    user = request.user
    courses = models.Course.objects.filter(user_id=user.id)
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    dashboardcourse = []
    for i in getcourses:
        if i not in dashboardcourse:
            dashboardcourse.append(i)
    # new assignment
    if assignments_id == '0':
        if request.method == 'POST':
            title = request.POST['title']
            content = request.POST['content']
            code = request.POST['code']
            # get classes
            classes = request.POST['classes']
            # formating deadline
            gettime = request.POST['deadline']  # get time
            # if deadline doesn't set
            if gettime == '':
                models.Assignment.objects.create(title=title, code=code, classes=classes, time=datetime.datetime.now(),
                                                 content=content, user_id=user.id)
                return HttpResponseRedirect(reverse('website:assignment'))
            strtime = ''.join(gettime)  # change to string
            strampm = strtime[16:19]  # get ampm
            if strampm == 'AM':
                # split time by '/'
                strtime = strtime.replace(' AM', '')
                strtime = strtime.replace(' ', '/')
                strtime = strtime.replace(':', '/')
                strtime = strtime.split('/')
                # combine new time
                if strtime[3] == '12':
                    strtime[3] = str(int(strtime[3]) - 12)
                    deadline = strtime[2] + '-' + strtime[0] + '-' + strtime[1] + ' ' + strtime[3] + ':' + strtime[
                        4] + ':00'
                else:
                    deadline = strtime[2] + '-' + strtime[0] + '-' + strtime[1] + ' ' + strtime[3] + ':' + strtime[
                        4] + ':00'
            else:
                strtime = strtime.replace(' PM', '')
                strtime = strtime.replace(' ', '/')
                strtime = strtime.replace(':', '/')
                strtime = strtime.split('/')
                if strtime[3] == '12':
                    deadline = strtime[2] + '-' + strtime[0] + '-' + strtime[1] + ' ' + strtime[3] + ':' + strtime[
                        4] + ':00'
                else:
                    strtime[3] = str(int(strtime[3]) + 12)
                    deadline = strtime[2] + '-' + strtime[0] + '-' + strtime[1] + ' ' + strtime[3] + ':' + strtime[
                        4] + ':00'
            if content == '' or title == '':
                pass
            else:
                models.Assignment.objects.create(title=title, code=code, classes=classes, time=datetime.datetime.now(),
                                                 content=content, user_id=user.id, deadline=deadline)
                return HttpResponseRedirect(reverse('website:assignment'))
    else:
        if request.method == 'POST':
            title = request.POST['title']
            content = request.POST['content']
            code = request.POST['code']
            # get classes
            classes = request.POST['classes']
            # formating deadline
            gettime = request.POST['deadline']  # get time
            # if deadline doesn't change
            if gettime == '':
                models.Assignment.objects.filter(id=assignments_id).update(title=title, code=code, classes=classes,
                                                                           content=content)
                return HttpResponseRedirect(reverse('website:assignment'))
            strtime = ''.join(gettime)  # change to string
            strampm = strtime[16:19]  # get ampm
            if strampm == 'AM':
                # split time by '/'
                strtime = strtime.replace(' AM', '')
                strtime = strtime.replace(' ', '/')
                strtime = strtime.replace(':', '/')
                strtime = strtime.split('/')
                # combine new time
                if strtime[3] == '12':
                    strtime[3] = '00'
                    deadline = strtime[2] + '-' + strtime[0] + '-' + strtime[1] + ' ' + strtime[3] + ':' + strtime[
                        4] + ':00'
                else:
                    deadline = strtime[2] + '-' + strtime[0] + '-' + strtime[1] + ' ' + strtime[3] + ':' + strtime[
                        4] + ':00'
            else:
                strtime = strtime.replace(' PM', '')
                strtime = strtime.replace(' ', '/')
                strtime = strtime.replace(':', '/')
                strtime = strtime.split('/')
                if strtime[3] == '12':
                    deadline = strtime[2] + '-' + strtime[0] + '-' + strtime[1] + ' ' + strtime[3] + ':' + strtime[
                        4] + ':00'
                else:
                    strtime[3] = str(int(strtime[3]) + 12)
                    deadline = strtime[2] + '-' + strtime[0] + '-' + strtime[1] + ' ' + strtime[3] + ':' + strtime[
                        4] + ':00'
            if content == '' or title == '':
                pass
            else:
                models.Assignment.objects.filter(id=assignments_id).update(title=title, code=code, classes=classes,
                                                                           content=content, deadline=deadline)
                return HttpResponseRedirect(reverse('website:assignment'))
    return render(request, 'website/assignment-new.html', {'courses': courses, 'dcourse': dashboardcourse})


def assignment_detail(request, isteacher, assignments_id):
    # 打开页面信息
    user = request.user
    getcourses = models.Course.objects.filter(user_id=user.id).values('coursename', 'code', 'is_teacher')
    courses = []
    for i in getcourses:
        if i not in courses:
            courses.append(i)
    # 区分页面
    if isteacher == 'True':
        # teacher page
        alluser = models.User.objects.all()
        nofile = ''
        assignments = models.Assignment.objects.get(id=assignments_id)
        filelist = models.Assignment_file.objects.filter(assignments_id=assignments_id)
        if not filelist:
            nofile = '还没有人提交作业！'
        return render(request, 'website/assignment-teacher.html',
                      {'courses': courses, 'assignments': assignments, 'filelist': filelist,
                       'assignments_id': assignments_id, 'isteacher': isteacher, 'nofile': nofile, 'alluser': alluser})
    else:
        # student page
        # get assignment
        assignments = models.Assignment.objects.get(id=assignments_id)
        # get file
        isuploaded = False
        filelist = models.Assignment_file.objects.filter(user_id=user.id, assignments_id=assignments_id)
        if filelist:
            isuploaded = True
        return render(request, 'website/assignment-student.html',
                      {'courses': courses, 'assignments': assignments, 'isuploaded': isuploaded, 'filelist': filelist,
                       'assignments_id': assignments_id, 'isteacher': isteacher})


def assignment_upload(request, isteacher, assignments_id):
    # 打开页面信息
    user = request.user
    # upload file
    if request.method == 'POST':
        file = request.FILES['file']
        if not file:
            pass
        else:
            models.Assignment_file.objects.create(user_id=user.id, assignments_id=assignments_id,
                                                  time=datetime.datetime.now(), file=file)
            return HttpResponseRedirect(reverse('website:assignment_detail', args=[isteacher, assignments_id]))
    return render(request, 'website/file-upload.html')


def assignmentfile_delete(request, path, isteacher, assignments_id):
    # 删除文件
    path = path
    models.Assignment_file.objects.filter(file=path).delete()

    return HttpResponseRedirect(reverse('website:assignment_detail', args=[isteacher, assignments_id]))


def assignment_delete(request, assignments_id):
    # delete comments
    fileid = models.Assignment_file.objects.filter(assignments_id=assignments_id).values('id')
    for id in fileid:
        models.Assignment_comment.objects.filter(assignment_file_id=id['id']).delete()
    # delete assignment files
    models.Assignment_file.objects.filter(assignments_id=assignments_id).delete()
    # delete assignment
    models.Assignment.objects.get(id=assignments_id).delete()
    return HttpResponseRedirect(reverse('website:assignment'))


def assignment_comment(request):
    # get user and his name
    user = request.user
    first_name = models.User.objects.get(id=user.id).first_name
    last_name = models.User.objects.get(id=user.id).last_name
    # get comment and file id
    aid = request.GET.get('id', None)
    comment = request.GET.get('comment', None)
    # create comment
    models.Assignment_comment.objects.create(assignment_file_id=aid, user_id=user.id, first_name=first_name,
                                             last_name=last_name, comment=comment)
    # response
    data = {'success': '留言成功!'}
    return JsonResponse(data)


def check_comment(request, file_id):
    # 打开页面信息
    user = request.user
    courses = models.Course.objects.filter(user_id=user.id)
    # get comments
    comments = models.Assignment_comment.objects.filter(assignment_file_id=file_id)
    return render(request, 'website/assignment-comment.html',
                  {'comments': comments, 'courses': courses, 'file_id': file_id})


# create users
def test(request):
    user = request.user
    getreceiver = models.Message.objects.filter(Q(receive_id=user.id) | Q(user_id=user.id)).values('receive_id', 'user_id')
    receivers = []
    for i in getreceiver:
        if not i in receivers:
            receivers.append(i)

    return render(request, 'website/test.html', {'receivers': receivers})
