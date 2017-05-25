from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.alogout, name='logout'),
    url(r'^submit/$', views.alogin, name='alogin'),
    url(r'^profile/$', views.viewprofile, name='profile'),
    url(r'^profile/submit/$', views.updateprofile, name='updateprofile'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^test/$', views.test, name='test'),
    url(r'^discuss/(\d+)/$', views.discuss, name='discuss'),
    url(r'^consult/(\d+)/$', views.consult, name='consult'),
    url(r'^consult/new/(\d+)/$', views.consult_new, name='consult_new'),
    url(r'^consult/talk/(\d+)/(.*)/$', views.consult_talk, name='consult_talk'),
    url(r'^message/$', views.message, name='message'),
    url(r'^message/talk/(\d+)/(\d+)/$', views.message_talk, name='message_talk'),
    url(r'^message/new/$', views.message_new, name='message_new'),
    url(r'^bulletin/$', views.bulletin, name='bulletin'),
    url(r'^bulletin/get/(\d+)/$', views.bulletin_get, name='bulletin_get'),
    url(r'^bulletin/new/$', views.bulletin_new, name='bulletin_new'),
    url(r'^file/$', views.uploaded_file, name='file'),
    url(r'^file/upload/$', views.file_upload, name='file_upload'),
    url(r'^file/delete/(.*)/$', views.file_delete, name='file_delete'),
    url(r'^assignment/$', views.assignment, name='assignment'),
    url(r'^assignment/new/(.*)/$', views.assignment_new, name='assignment_new'),
    url(r'^assignment/detail/(.*)/(\d+)/$', views.assignment_detail, name='assignment_detail'),
    url(r'^assignment/upload/(.*)/(\d+)/$', views.assignment_upload, name='assignment_upload'),
    url(r'^assignment/deletefile/(.*)/(.*)/(\d+)/$', views.assignmentfile_delete, name='assignmentfile_delete'),
    url(r'^assignment/delete/(\d+)/$', views.assignment_delete, name='assignment_delete'),
    url(r'^assignment/comment/$', views.assignment_comment, name='assignment_comment'),
    url(r'^assignment/checkcomment/(\d+)/$', views.check_comment, name='check_comment'),
    url(r'^changepw/$', views.updatepw, name='changepw'),
]
