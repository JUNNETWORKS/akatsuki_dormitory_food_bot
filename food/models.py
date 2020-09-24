from django.db import models
import datetime


# Create your models here.

class FoodMenu(models.Model):
    class Meta(object):
        db_table = "food_menu"
    year = models.IntegerField(blank=True)  # 年
    month = models.IntegerField(blank=True)  # 月
    day = models.IntegerField()  # 日
    breakfast = models.CharField(max_length=200)  # 朝飯
    lunch = models.CharField(max_length=200)  # 昼飯
    dinner = models.CharField(max_length=200)  # 晩飯

    def __str__(self):
        return "{}/{}/{}".format(self.year, self.month, self.day)
