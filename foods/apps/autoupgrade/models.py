# encoding:utf-8
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from system.storage import FileStorage

# Create your models here.


class AndroidVersion(models.Model):
    '''
    安卓Apk版本管理
    '''
    version = models.BigAutoField(primary_key=True)
    #type    = models.CharField(max_length=25, default='seller', choices=TYPE_CHOICE, null=False, verbose_name=u'apk类型')
    path = models.FileField(upload_to='apks', verbose_name=u'apk地址')

    def __str__(self):

        return '版本号: %d' % (self.version)

    class Meta:
        verbose_name = u'安卓app更新'
        verbose_name_plural = verbose_name


@receiver(post_delete, sender=AndroidVersion)
def androidversion_post_delete_receiver(sender, instance, **kwargs):
    '''
    删除用户后执行
    同时删除文件
    '''
    import os
    import shutil
    from django.conf import settings
    path = os.sep.join([settings.MEDIA_ROOT, str(instance.path)])
    if os.path.exists(path):
        shutil.rmtree(path)


@receiver(post_save, sender=AndroidVersion)
def androidversion_post_save_receiver(sender, created, instance, **kwargs):
    '''
    删除用户后执行
    同时删除文件
    '''
    import os
    import stat
    from django.conf import settings
    path = os.sep.join([settings.MEDIA_ROOT, str(instance.path)])
    if os.path.exists(path):
        os.chmod(path, stat.S_IRWXU+stat.S_IROTH)
