# -*- coding: utf-8 -*-
# 该示例中使用云API V1版本
from datetime import datetime
import pdb

from common.log import logger
from blueking.component.shortcuts import get_client_by_user
from homework.models import CapacityData2, CapacityData3, OperateData
import json



def get_job_instance_id(client, biz_id, ip, job_id):
    """
    执行Job作业
    """
    # 获取作业模板参数详情
    kwargs = {
        'bk_biz_id': biz_id,
        'bk_job_id': job_id,
    }
    resp = client.job.get_job_detail(**kwargs)

    steps_args = []
    if resp.get('result'):
        data = resp.get('data', {})
        steps = data.get('steps', [])
        # 组装步骤参数
        for _step in steps:
            steps_args.append(
                {
                    'step_id': int(_step.get('step_id')),
                    'ip_list': [{
                        'bk_cloud_id': 0,
                        'ip': ip,
                    }],
                }
            )

    # 执行作业
    kwargs = {
        'bk_biz_id': biz_id,
        'bk_job_id': job_id,
        'steps': steps_args,
        }
    resp = client.job.execute_job(**kwargs)
    if resp.get('result'):
        job_instance_id = resp.get('data').get('job_instance_id')
    else:
        job_instance_id = -1
    
    return resp.get('result'), job_instance_id


def get_host_capaticy(client, biz_id, job_instance_id, ip):
    """
    获取磁盘容量数据
    """
    kwargs = {
        'bk_biz_id': biz_id,
        'job_instance_id': job_instance_id,
        }
    resp = client.job.get_job_instance_log(**kwargs)

    is_finish = False
    capacity_data = []          # 作为json值返回给前端
    # index = 0
    if resp.get('result'):
        data = resp.get('data')
        logs = ''
        for _d in data:
            if _d.get('is_finished'):
                is_finish = True
                logs = _d['step_results'][0].get('ip_logs')[0].get('log_content')
                break

        logs = logs.split('\n')
        # logs = [_l.split(' ') for _l in logs]
        logs = [_l.split('|') for _l in logs]
        # 示例 [['Filesystem', 'Size', 'Used', 'Avail', 'Use%', 'Mounted', 'on'], ['/dev/mapper/centos-root', '50G', '19G', '32G', '38%', '/']

        for log in logs[0:]:
            _l_new = [_l for _l in log if _l != '']
            if _l_new and len(_l_new) >= 1:
                capacity_table_data = [ip, _l_new[1]+' '+_l_new[2]+' '+_l_new[3], _l_new[0], "公共组件", "consule", "default area", "linux centos"]
                operate_data = [ip, "admin", _l_new[0], "立即检查"]
                capacity_data.append({
                    'ip': ip,
                    'Mem/Disk/CPU': _l_new[1]+' '+_l_new[2]+' '+_l_new[3],
                    'ExecTime': _l_new[0],
                    # 'ExecTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Set': "公共组件",
                    'Module': "consule",
                    'InstName': "default area",
                    'OsName': "linux centos"
                })
                # index += 1
                # 数据入库
                _l_new.append(ip)
        #         # 示例：['/dev/mapper/centos-root', '50G', '19G', '32G', '38%', '/', '172.19.17.7']
                CapacityData2.objects.save_data(_l_new)
                CapacityData3.objects.save_data(capacity_table_data)
                OperateData.objects.save_data(operate_data)
    return is_finish, capacity_data