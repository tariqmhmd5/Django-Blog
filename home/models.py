from django.db import models

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    content = models.TextField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return('Message from: ' + self.fname + ' ' +  self.lname)
