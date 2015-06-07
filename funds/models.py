from django.db import models
from django.contrib.auth.models import User
# Create your models here.
SEX_CHOICES=(('Male','male'),('Female','female'))

#个人信息
class Me(models.Model):
    user = models.OneToOneField(User)
    realname = models.CharField(max_length=20,verbose_name="真实姓名",)
    sex = models.CharField(max_length=10,verbose_name="性别",
                           choices=SEX_CHOICES)
    birth = models.DateField(verbose_name="生日",)
    cash = models.FloatField(verbose_name="现金额",)

    def __unicode__(self):
        return u'%s %s'%(self.user, self.realname)

class Record(models.Model):
    ID = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Me)
    date = models.DateField(verbose_name='时间')
    place = models.CharField(max_length=50,verbose_name='地点')

    class Meta:
        ordering = ['-date','ID']

    def __unicode__(self):
        return u'%d'%(self.ID)

#支出
class Assumption(Record):
    amount = models.FloatField(verbose_name='金额')
    items = models.CharField(max_length=50,verbose_name='条目')

    def __unicode__(self):
        return u'%s %s'%(self.date,self.items)

#收入
class Income(Record):
    amount = models.FloatField(verbose_name='金额')
    source = models.CharField(max_length=20,verbose_name='来源')

    def __unicode__(self):
        return u'%s %s'%(self.date,self.source)

#其他事务
class Other(Record):
    details = models.TextField(verbose_name='详细')

    def __unicode__(self):
        return u'%s %s'%(self.date,self.details)

#存款账户
class Deposit(models.Model):
    name = models.CharField(max_length=20,primary_key=True,verbose_name='账户名')
    owner = models.ForeignKey(Me)
    balance = models.FloatField(verbose_name='余额')
    deposit_type = models.CharField(max_length=20,verbose_name='账户类型')
    bank = models.CharField(max_length=20,verbose_name='银行')
    opening_date = models.DateField(verbose_name='开户日期')

    def __unicode__(self):
        return u'%s'%(self.name)

#贷款账户
class Loan(models.Model):
    name = models.CharField(max_length=20,primary_key=True,verbose_name='账户名')
    owner = models.ForeignKey(Me)
    amount = models.FloatField(verbose_name='金额')
    loan_type = models.CharField(max_length=20,verbose_name='账户类型')
    bank = models.CharField(max_length=20,verbose_name='银行')
    opening_date = models.DateField(verbose_name='贷款日期')

    def __unicode__(self):
        return u'%s'%(self.name)

