# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from common.log import logger


class CapacityDataManager2(models.Manager):
    def save_data(self, data):
        """
        保存执行结果数据
        """
        try:
            CapacityData2.objects.create(
                ip=data[4],
                mem=data[1],
                disk=data[2],
                cpu=data[3],
                createtime=datetime.now()
            )
            result = {'result': True, 'message': u"保存成功"}
        except Exception, e:
            logger.error(u"save_data %s" % e)
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result


class CapacityData2(models.Model):
    """
    存储查询的容量数据
    """
    ip = models.CharField('ip', max_length=64, blank=True, null=True)
    mem = models.CharField('mem', max_length=64)
    disk = models.CharField('disk', max_length=64)
    cpu = models.CharField('cpu', max_length=64)
    createtime = models.DateTimeField(u"保存时间")
    objects = CapacityDataManager2()

    
    def __unicode__(self):
        return self.ip

    class Meta:
        verbose_name = u"磁盘容量数据"
        verbose_name_plural = u"磁盘容量数据"


class CapacityDataManager3(models.Manager):
    def save_data(self, data):
        """
        保存执行结果数据
        """
        try:
            CapacityData3.objects.create(
                ip=data[0],
                mem_disk_cpu=data[1],
                exec_time=data[2],
                set=data[3],
                module=data[4],
                instname=data[5],
                osname=data[6],
            )
            result = {'result': True, 'message': u"保存成功"}
        except Exception, e:
            logger.error(u"save_data %s" % e)
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result


class CapacityData3(models.Model):
    """
    存储查询的容量数据
    """
    index = models.AutoField('index', max_length=64, primary_key=True)
    ip = models.CharField('ip', max_length=64, blank=True, null=True)
    mem_disk_cpu = models.CharField('mem_disk_cpu', max_length=64)
    exec_time = models.CharField('exec_time', max_length=64)
    set = models.CharField('set', max_length=64)
    module = models.CharField('module', max_length=64)
    instname = models.CharField('instname', max_length=64)
    osname = models.CharField('osname', max_length=64)
    objects = CapacityDataManager3()


    def __unicode__(self):
        return self.ip

    class Meta:
        verbose_name = u"磁盘容量数据"
        verbose_name_plural = u"磁盘容量数据"


class OperateDataManager(models.Manager):
    def save_data(self, data):
        """
        保存操作记录数据
        """
        try:
            OperateData.objects.create(
                ip=data[0],
                operator=data[1],
                exec_time=data[2],
                operate_style=data[3],
            )
            result = {'result': True, 'message': u"保存成功"}
        except Exception, e:
            logger.error(u"save_data %s" % e)
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result


class OperateData(models.Model):
    """
    存储查询的操作记录
    """
    index = models.AutoField('index', max_length=64, primary_key=True)
    ip = models.CharField('ip', max_length=64, blank=True, null=True)
    operator = models.CharField('operator', max_length=64)
    exec_time = models.CharField('exec_time', max_length=64)
    operate_style = models.CharField('operate_style', max_length=64)
    objects = OperateDataManager()


    def __unicode__(self):
        return self.ip

    class Meta:
        verbose_name = u"操作记录数据"
        verbose_name_plural = u"操作记录数据"
        ordering = ['-index']

class TaskLogManager(models.Manager):
    def save_log(self, datalist):
        """
        保存执行结果数据
        """
        try:
            for data in datalist:
                TaskLog.objects.create(
                    operator=data.get('operator'),
                    starttime=data.get('starttime'),
                    endtime=data.get('endtime'),
                    log=data.get('log'),
                    ip=data.get('ip'),
                    result=data.get('result'),
                    stepname=data.get('stepname'),
                )
            result = {'result': True, 'message': u"保存成功"}
        except Exception, e:
            logger.error(u"save_log： %s" % e)
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result


# 定义表，存储执行历史
class TaskLog(models.Model):
    """
    执行历史日志
    """
    operator = models.CharField(u"操作人", max_length=64)
    starttime = models.DateTimeField(u"起始执行时间")
    endtime = models.DateTimeField(u"结束执行时间")
    log = models.TextField(u"执行日志", blank=True, null=True)
    ip = models.IPAddressField(u"执行IP")
    result = models.CharField(u"执行结果", max_length=64)
    stepname = models.CharField(u"步骤名", max_length=64)
    objects = TaskLogManager()

    
    def __unicode__(self):
        return self.operator

    class Meta:
        verbose_name = u"执行历史日志"
        verbose_name_plural = u"执行历史日志"


# 串行任务结果保存
class TaskResultManager(models.Manager):
    def save_result(self, datalist):
        """
        保存会议记录
        """
        try:
            for data in datalist:
                TaskResult.objects.create(
                    func=data.get('func'),
                    result=data.get('result'),
                )
            result = {'result': True, 'message': u"保存成功"}
        except Exception, e:
            logger.error(u"save_result %s" % e)
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result
    

class TaskResult(models.Model):
    """
    任务执行结果
    """
    # taskid = models.DateTimeField(u"任务时间戳")
    func = models.CharField(u"执行函数", max_length=64)
    result = models.TextField(u"函数返回结果", max_length=64)
    objects = TaskResultManager()

    
    def __unicode__(self):
        return self.func

    class Meta:
        verbose_name = u"任务执行结果"
        verbose_name_plural = u"任务执行结果"