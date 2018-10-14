# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'homework.views',
    (r'^$', 'home'),
    (r'^host/', 'host'),
    (r'^operate/', 'operate'),
    # 表单下拉数据获取及渲染
    (r'^get_biz_list/$', 'get_biz_list'),
    (r'^get_ip_by_bizid/$', 'get_ip_by_bizid'),
    (r'^get_job_list/$', 'get_joblist_by_bizid'),

    # 执行作业，获取容量数据
    (r'^execute_job/$', 'execute_job'),
    (r'^get_capacity/$', 'get_capacity'),

    # 获取视图数据
    (r'^chartdata/', 'get_capacity_chartdata'),
)


