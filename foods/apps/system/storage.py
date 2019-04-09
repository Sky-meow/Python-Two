#encoding:utf-8
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


class FileStorage(FileSystemStorage):
    from django.conf import settings
    
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        super(FileStorage, self).__init__(location, base_url)

    # 重写 _save方法        
    def _save(self, name, content):
        import os, time, random, string
        # 文件扩展名
        #self.logged('1')
        ext = os.path.splitext(name)[1]
        # 文件目录
        # if settings.MEDIA_URL not in name and settings.MEDIA_ROOT not name:
        #     name = settings.MEDIA_ROOT + name
        d = os.path.dirname(name)
        # 定义文件名，年月日时分秒随机数
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%s' % ''.join(random.sample(string.ascii_letters + string.digits, 30)) #随机产生30位字符串
        # 重写合成文件名
        name = os.path.join(d, fn + ext)
        super(FileStorage, self)._save(name, content)

class ImageStorage(FileSystemStorage):
    '''
    重写保存图片方法
    给上传的图片重新生成随机名称
    '''
    from django.conf import settings
    
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        super(ImageStorage, self).__init__(location, base_url)

    def exists(self, name):
        import os
        # if type(name) == str:
        #     name = name.encode('utf8').decode('utf8','replace')
        return os.path.exists(self.path(name))

    # 重写 _save方法        
    def _save(self, name, content):
        import os, time, random, string
        from PIL import Image
        from django.conf import settings
        # 文件扩展名
        #self.logged('1')
        ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件名，年月日时分秒随机数
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%s' % ''.join(random.sample(string.ascii_letters + string.digits, 30)) #随机产生30位字符串
        # 重写合成文件名
        name = os.path.join(d, fn + ext)
        #self.logged(name)
        #content.name = name
        # 调用父类方法
        #image = content.image
        #print(type(image))
        #(width, height) = image.size  
        # if width / height != 3/2:
        #     size = ( 3000, 2000)
        #     #re = image.crop()
        #     image = image.resize(size, Image.ANTIALIAS)
        #     #content.image = image
        super(ImageStorage, self)._save(name, content)
        #self.logged('3')

        image = Image.open(settings.MEDIA_ROOT+name)
        (width, height) = image.size   
        if width / height != 3/2:  
            size = ( 3000, 2000)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(settings.MEDIA_ROOT+name)
            return name.replace('\\', '/')

    def logged(self,content):
        '''
        保存日志
        '''
        import os
        import logging
        from django.conf import settings
        logging.basicConfig(filename=os.path.join(settings.BASE_DIR+'/logs/','debug.txt'),level=logging.DEBUG)
        filename = settings.BASE_DIR+'/logs/log.txt'
        f = open(filename,'a',encoding='utf-8')
        f.write(content)
        f.write('\n')
        f.close()