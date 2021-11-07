# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Canteen(models.Model):
    canteen_id = models.AutoField(primary_key=True, verbose_name='食堂编号')
    canteen_name = models.CharField(max_length=10, verbose_name='食堂名称')
    canteen_photo = models.ImageField(upload_to='images/canteen', null=True, blank=True, verbose_name='食堂照片')
    sanitation_level = models.CharField(max_length=1, choices=[("A", 'A'), ("B", 'B'), ("C", 'C')], verbose_name='卫生等级')
    canteen_active = models.CharField(max_length=10, choices=[("营业中", '营业中'), ("歇业中", '歇业中')], verbose_name='食堂状态')

    class Meta:
        ordering = ['canteen_id']
        db_table = 'canteen'
        verbose_name = "食堂信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.canteen_name


class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True, verbose_name='窗口编号')
    canteen = models.ForeignKey(Canteen, models.CASCADE, verbose_name='食堂')
    manager = models.ForeignKey('ShopManager', models.SET_NULL, null=True, verbose_name='窗口经营者')
    shop_name = models.CharField(max_length=20, verbose_name='窗口名称')
    shop_detail = models.CharField(max_length=200, blank=True, null=True, verbose_name='窗口描述')
    shop_photo = models.ImageField(upload_to='images/shop', null=True, blank=True, verbose_name='窗口照片')
    shop_active = models.IntegerField(choices=[(1, '营业中'), (0, '歇业中')], verbose_name='窗口状态')

    class Meta:
        ordering = ['shop_id']
        db_table = 'shop'
        verbose_name = "窗口信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.shop_name


class ShopManager(models.Model):
    manager_id = models.AutoField(primary_key=True, verbose_name='经营者编号')
    manager_name = models.CharField(max_length=20, verbose_name='经营者昵称')
    manager_password = models.CharField(max_length=20, verbose_name='经营者密码')
    manager_tel = models.CharField(max_length=11, verbose_name="经营者电话")
    manager_status = models.IntegerField(choices=[(0, '离线'), (1, '在线')], default=0, verbose_name="经营者状态")
    manage_shop_num = models.IntegerField(verbose_name='经营窗口数')

    class Meta:
        ordering = ['manager_id']
        db_table = 'shop_manager'
        verbose_name = "窗口经营者信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.manager_name
