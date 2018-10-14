# -*- coding: utf-8 -*-
import Tkinter
import sys

import json
import datetime
import pdb
import tkMessageBox
from django.http import HttpResponse
from django.shortcuts import redirect
from common.mymako import render_mako_context, render_json
from blueking.component.shortcuts import get_client_by_request
from homework.models import CapacityData2, CapacityData3, OperateData
from homework.utils import get_job_instance_id, get_host_capaticy
from homework.celery_tasks import async_task, celery_chain_task, custom_func1, save_task_log


def home(request):
    ip = request.GET.get("ip", "")
    ips = ["172.50.19.24", "172.50.19.25", "172.50.19.26"]
    if ip in ips:
        capacitydatas = CapacityData3.objects.filter(ip=ip)
        return render_mako_context(request, '/homework/home.html', {"capacitydatas": capacitydatas, "ip": ip})
    elif ip == "":
        capacitydatas = CapacityData3.objects.all()
        return render_mako_context(request, '/homework/home.html', {"capacitydatas": capacitydatas, "ip": u"仅支持内网IP查询"})
    else:
        top = Tkinter.Tk()
        top.withdraw()
        tkMessageBox.showinfo(title="输入的ip不正确", message="请输入正确的IP地址")
        return redirect('/homework/')
        # return render_mako_context(request, '/homework/')


def host(request):
    return render_mako_context(request, '/homework/host.html')


def operate(request):
    operatedatas = OperateData.objects.all()
    return render_mako_context(request, '/homework/operate.html', {"operatedatas": operatedatas})



# ------------------------------------
# 执行参数表单数据获取，业务、ip、作业
# ------------------------------------
def get_biz_list(request):
    """
    获取所有业务
    """
    biz_list = []
    client = get_client_by_request(request)
    kwargs = {
        'fields': ['bk_biz_id', 'bk_biz_name']
    }
    resp = client.cc.search_business(**kwargs)

    if resp.get('result'):
        data = resp.get('data', {}).get('info', {})
        for _d in data:
            biz_list.append({
                'name': _d.get('bk_biz_name'),
                'id': _d.get('bk_biz_id'),
            })

    result = {'result': resp.get('result'), 'data': biz_list}
    return render_json(result)


def get_ip_by_bizid(request):
    """
    获取业务下IP
    """
    biz_id = int(request.GET.get('biz_id'))
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')
    kwargs = {'bk_biz_id': biz_id,
              'condition': [
                {
                    'bk_obj_id': 'biz',
                    'fields': ['bk_biz_id'],
                    'condition': [
                        {
                            'field': 'bk_biz_id',
                            'operator': '$eq',
                            'value': biz_id
                        }
                    ]
                }
            ]
        }

    resp = client.cc.search_host(**kwargs)

    ip_list = []
    if resp.get('result'):
        data = resp.get('data', {}).get('info', {})
        for _d in data:
            _hostinfo = _d.get('host', {})
            if _hostinfo.get('bk_host_innerip') not in ip_list:
                ip_list.append(_hostinfo.get('bk_host_innerip'))

    ip_all = [{'ip': _ip} for _ip in ip_list]
    result = {'result': resp.get('result'), 'data': ip_all}
    return render_json(result)


def get_joblist_by_bizid(request):
    """
    获取业务下的作业列表
    """
    biz_id = request.GET.get('biz_id')
    client = get_client_by_request(request)
    # client.set_bk_api_ver('v2')
    kwargs = {'bk_biz_id': biz_id}
    resp = client.job.get_job_list(**kwargs)
    job_list = []
    if resp.get('result'):
        data = resp.get('data', [])
        for _d in data:
            # 获取作业信息
            job_list.append({
                'job_id': _d.get('bk_job_id'),
                'job_name': _d.get('name'),
            })
    result = {'result': resp.get('result'), 'data': job_list}
    return render_json(result)


#------------------------------------
# 执行作业，获取实时磁盘容量数据
#------------------------------------
def execute_job(request):
    """
    执行磁盘容量查询作业
    """
    biz_id = request.POST.get('biz_id')
    ip = request.POST.get('ip')
    job_id = request.POST.get('job_id')

    # 调用作业平台API，或者作业执行实例ID 
    client = get_client_by_request(request)
    # client.set_bk_api_ver('v2')
    result, job_instance_id = get_job_instance_id(client, biz_id, ip, job_id)

    result = {'result': result, 'data': job_instance_id}
    return render_json(result)


def get_capacity(request):
    """
    获取作业执行结果，并解析执行结果展示
    """
    job_instance_id = request.GET.get('job_instance_id')
    biz_id = request.GET.get('biz_id')
    ip = request.GET.get('ip')

    # 调用作业平台API，或者作业执行详情，解析获取磁盘容量信息
    client = get_client_by_request(request)
    # client.set_bk_api_ver('v2')
    is_finish, capacity_data = get_host_capaticy(client, biz_id, job_instance_id, ip)

    return render_json({'code': 0, 'message': 'success', 'data': capacity_data})


# ------------------------------------
# 获取视图数据
# ------------------------------------
def get_capacity_chartdata(request):
    """  获取视图数据，Mounted为：/data的磁盘容量，ip为1.1.1.1
    """
    ip = request.GET.get('ip')
    # pdb.set_trace()
    # ip = "172.50.19.24"
    capacitydatas = CapacityData2.objects.filter(ip=ip)
    times = []
    data_mem = []
    data_disk = []
    data_cpu = []
    # pdb.set_trace()
    for capacity in capacitydatas:
        times.append(capacity.createtime.strftime('%Y-%m-%d %H:%M:%S'))
        data_mem.append(capacity.mem.strip('%'))
        data_disk.append(capacity.disk.strip('%'))
        data_cpu.append(capacity.cpu.strip('%'))
    result = {
            'code': 0,
            'result': True,
            'messge': 'success',
            'data': {
                'xAxis': times,
                'series': [
                    {
                        'name': '内存利用率',
                        'type': 'line',
                        'data': data_mem
                    },
                    {
                        'name': '磁盘利用率',
                        'type': 'line',
                        'data': data_disk
                    },
                    {
                        'name': 'cpu利用率',
                        'type': 'line',
                        'data': data_cpu
                    }
                ]
            }
        }
    return render_json(result)




