# -*- coding: utf-8 -*-

from django.conf.urls import patterns

# 提供磁盘容量历史数据查询API
urlpatterns = patterns('get_capacity.api_views',
    (r'^history_data/$', 'get_history_data'),
)