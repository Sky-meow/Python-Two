#encoding:utf-8
from django.db import models
from system.models import User
from system.storage import ImageStorage
from DjangoUeditor.models import UEditorField
from easy_thumbnails.fields import ThumbnailerImageField

# Create your models here.
class MatType(models.Model):
    id          = models.BigAutoField(primary_key=True)
    code        = models.CharField(max_length=50,null=False,db_index=True,unique=True,verbose_name=u'分类编码')
    name        = models.CharField(max_length=150,null=False,db_index=True,verbose_name=u'分类名称')
    remark      = models.CharField(max_length=150,null=True,blank=True,verbose_name=u'备注')
    enable      = models.BooleanField(default=True,verbose_name=u'是否启用')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间',null=True,blank=True)
    created_by   = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,db_constraint=False,verbose_name=u'创建人',related_name='mattype_created_by')
    updated_at = models.DateTimeField(auto_now=True,verbose_name=u'修改时间',null=True,blank=True)
    updated_by   = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,db_constraint=False,verbose_name=u'修改人',related_name='mattype_updated_by')

    def __str__(self):
        return self.Name+'('+self.Code+')'

    class Meta:
        verbose_name = u'菜品类别'
        verbose_name_plural = verbose_name

class Material(models.Model):
    '''
    菜品
    '''
    id          = models.BigAutoField(primary_key=True)
    mattype     = models.ForeignKey(MatType,null=True,blank=True,on_delete=models.SET_NULL,db_constraint=False, verbose_name=u'所属类别')
    SKU         = models.CharField(max_length=50,null=False,db_index=True,verbose_name=u'SKU')
    name        = models.CharField(max_length=150,null=False,db_index=True,verbose_name=u'菜品名称')
    price       = models.FloatField(default=0,verbose_name=u'单价')
    description = UEditorField(width=600, height=300, toolbars="full", imagePath="upload/material/%(basename)s_%(datetime)s.%(extname)s", filePath="upload/material/", upload_settings={"imageMaxSize":5242880},default='',verbose_name=u'描述')
    image       = ThumbnailerImageField(upload_to=u'images/%Y/%m', null=True, blank=True, verbose_name=u'图片')
    banner      = models.BooleanField(default=False,verbose_name=u'轮播广告')
    remark      = UEditorField(width=600, height=300, toolbars="full", imagePath="ueditor/%(basename)s_%(datetime)s.%(extname)s", filePath="ueditor/", upload_settings={"imageMaxSize":1204000},default='',verbose_name=u'备注')
    created_at  = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间',null=True,blank=True)
    created_by  = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,db_constraint=False,verbose_name=u'创建人',related_name='mat_created_by')
    updated_at  = models.DateTimeField(auto_now=True,verbose_name=u'修改时间',null=True,blank=True)
    updated_by  = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,db_constraint=False,verbose_name=u'修改人',related_name='mat_updated_by')
    
    def upload_img(self):
        try:
            img = '<img src="%s" width="50px" />' % (self.image.url,)
        except Exception as e:
            img = ''
        return img
    upload_img.short_description = u'缩略图'
    upload_img.allow_tags = True

    def image_tip(self):
        return '<h4 style="color:red">%s</h4>'%(u'上传的图片路径或者名称暂不支持中文字符')
    image_tip.short_description = u'注意'
    image_tip.allow_tags = True

    
    def __str__(self):
        return '['+(self.SKU)+'] '+self.Name


    class Meta:
        verbose_name = u'堂食菜品'
        verbose_name_plural = verbose_name
