from django.db import models

# Create your models here.
class Register(models.Model):
    reg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tel = models.CharField(max_length=20)
    des = models.TextField()
    pay = models.CharField(max_length=20)
    current_time = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    remain_day = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.user_id} {self.name} {self.tel} {self.des} {self.pay} {self.current_time} {self.start_date} {self.end_date} {self.remain_day}'

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    des = models.TextField()
    pay = models.CharField(max_length=20)
    current_time = models.CharField(max_length=20)
    date = models.DateField()
    
    def __str__(self) -> str:
        return f'{self.user_id} {self.name} {self.des} {self.pay} {self.current_time} {self.date}'

class Member_checkin(models.Model):
    name = models.CharField(max_length=100)
    tel = models.CharField(max_length=15)
    des = models.TextField()
    reg_current_time = models.CharField(max_length=20)
    date = models.DateField()
    
    def __str__(self) -> str:
        return f'{self.name} {self.tel} {self.des} {self.pay} {self.reg_current_time} {self.date}'
