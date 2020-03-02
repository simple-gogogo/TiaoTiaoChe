# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Agent(models.Model):
    agentid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    tel = models.CharField(max_length=20)
    servstar = models.IntegerField()
    realstar = models.IntegerField()
    profstar = models.IntegerField()
    certificated = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_agent'


class AgentCarShop(models.Model):
    agent_shopid = models.AutoField(primary_key=True)
    agentid = models.IntegerField()
    shopid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_agent_car_shop'
        unique_together = (('agentid', 'shopid'),)


class CarInfo(models.Model):
    carid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    priceunit = models.CharField(max_length=10)
    detail = models.CharField(max_length=511, blank=True, null=True)
    mainphoto = models.CharField(max_length=255)
    pubdate = models.DateTimeField(blank=True, null=True)
    mileage = models.CharField(max_length=255)
    time = models.DateTimeField(blank=True, null=True)
    gear = models.CharField(max_length=255)
    allowremove = models.CharField(max_length=255)
    hasagentfees = models.IntegerField(blank=True, null=True)
    typeid = models.IntegerField()
    userid = models.IntegerField()
    distid2 = models.IntegerField()
    distid3 = models.IntegerField()
    car_shopid = models.IntegerField(blank=True, null=True)
    agentid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_car_info'


class CarPhoto(models.Model):
    photoid = models.AutoField(primary_key=True)
    carid = models.IntegerField()
    path = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tb_car_photo'


class CarShop(models.Model):
    shopid = models.AutoField(primary_key=True)
    distid = models.IntegerField()
    name = models.CharField(max_length=255)
    hot = models.IntegerField(blank=True, null=True)
    intro = models.CharField(max_length=511, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_car_shop'


class CarTag(models.Model):
    car_tag_id = models.AutoField(primary_key=True)
    carid = models.IntegerField()
    tagid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_car_tag'
        unique_together = (('carid', 'tagid'),)


class CarType(models.Model):
    typeid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tb_car_type'


class District(models.Model):
    distid = models.IntegerField(primary_key=True)
    pid = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    ishot = models.IntegerField(blank=True, null=True)
    intro = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_district'


class LoginLog(models.Model):
    logid = models.BigAutoField(primary_key=True)
    userid = models.IntegerField()
    ipaddr = models.CharField(max_length=255)
    logdate = models.DateTimeField(blank=True, null=True)
    devcode = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_login_log'


class Privilege(models.Model):
    privid = models.AutoField(primary_key=True)
    method = models.CharField(max_length=15)
    url = models.CharField(max_length=1024)
    detail = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_privilege'


class Record(models.Model):
    recordid = models.BigAutoField(primary_key=True)
    userid = models.IntegerField()
    carid = models.IntegerField()
    recorddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tb_record'
        unique_together = (('userid', 'carid'),)


class Role(models.Model):
    roleid = models.AutoField(primary_key=True)
    rolename = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tb_role'


class RolePrivilege(models.Model):
    role_priv_id = models.AutoField(primary_key=True)
    roleid = models.IntegerField()
    privid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_role_privilege'
        unique_together = (('roleid', 'privid'),)


class Tag(models.Model):
    tagid = models.AutoField(primary_key=True)
    content = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tb_tag'


class User(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=32)
    realname = models.CharField(max_length=20)
    sex = models.IntegerField(blank=True, null=True)
    tel = models.CharField(unique=True, max_length=20)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    regdate = models.DateTimeField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)
    lastvisit = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_user'


class UserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    userid = models.IntegerField()
    roleid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_user_role'
        unique_together = (('userid', 'roleid'),)
