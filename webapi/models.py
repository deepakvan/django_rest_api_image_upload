from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class UserImages(models.Model):
    id = models.IntegerField(primary_key=True)
    name=models.CharField(max_length=200,null=False)
    path=models.ImageField(upload_to='images')
    date_created = models.DateTimeField(default=datetime.now())
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+" "+self.name+ "  "+self.path.name

    def size_check(self):
        if self.path.size<=500000:
            return True
        else:
            return False
    def type_check(self):
        parts=self.path.name.split(".")
        if parts[-1] in ['jpg','png','gif','tiff']:
            return True
        else:
            return False