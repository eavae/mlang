#coding:utf-8
from sae.storage import Bucket
from PIL import Image
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class AvatarManager(object):
    def __init__(self,app):
        self.app = app
        self.bucket = Bucket(app.config['STORAGE_NAME'])
        self.bucket.put()
        self.bucket.post(acl='.r:.sinaapp.com,.r:sae.sina.com.cn', metadata={'expires': '1d'})

    def _saveAvatar(self,file,filename,size,sizecode):
        filetype = file.mimetype.split('/')[1]
        img = Image.open(StringIO(file.read()))
        file.seek(0)
        ratio = float(img.size[0]) / img.size[1]
        if ratio > 1:
            length = int(img.size[1]/2)
        else:
            length = int(img.size[0]/2)
        x0,y0 = int(img.size[0]/2),int(img.size[1]/2)
        img = img.crop((x0-length,y0-length,x0+length,y0+length))
        img = img.resize((size,size),Image.ANTIALIAS)

        output = StringIO()
        img.save(output,filetype)
        content = output.getvalue()
        output.close()
        self.bucket.put_object('avatar/'+filename, content, content_type=file.mimetype)

    def saveAvatar(self,file,id):
        filename = str(id)
        self._saveAvatar(file,filename,self.app.config['AVATAR_SIZE_S'],'s')
        self._saveAvatar(file,filename,self.app.config['AVATAR_SIZE_M'],'m')
        self._saveAvatar(file,filename,self.app.config['AVATAR_SIZE_L'],'l')

    def getAvatarUrl(self,id,sizecode):
        try:
            self.bucket.stat_object('avatar/'+str(id)+sizecode)
        except :
            return self.app.config['DEFAULT_AVATAR_URL']+'/'+sizecode
        return self.bucket.generate_url('avatar/'+str(id)+sizecode)