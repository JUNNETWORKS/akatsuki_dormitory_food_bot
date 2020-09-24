from django.shortcuts import render, redirect, HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .app.Menu_DataFrame import Menu_data
from .models import FoodMenu
import pandas as pd
import datetime
import os
import json
import django_filters
from rest_framework import viewsets, filters
from .serializer import FoodSerializer
from rest_framework import generics
import logging

logger = logging.getLogger(__name__)


def index(request):
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    # 今月登録されているデータ
    data = FoodMenu.objects.filter(year=year, month=month)
    return render(request, "food/index.html", {
        "data": data,
        "month": month,
    })


UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/image/'


@csrf_exempt
def form(request):
    now_month = datetime.datetime.now().month
    now_year = datetime.datetime.now().year
    if FoodMenu.objects.filter(year=now_year, month=now_month):  # 今月分のデータが有るか
        return render(request, "food/form.html", {
            "msg": "{}年{}月のデータは登録済みです".format(now_year, now_month)
        })

    if request.method != 'POST':
        c = {}
        c.update(csrf(request))
        return render(request, 'food/form.html')

    logger.info("received post request")

    file = request.FILES['file']

    # path = os.path.join(settings.BASE_DIR, file.name)
    path = os.path.join(UPLOADE_DIR, file.name)
    destination = open(path, 'wb')

    for chunk in file.chunks():
        destination.write(chunk)

    file_name = file.name
    if os.path.splitext(file_name)[1] != ".jpg":  # splitext でファイル名と拡張子を分割
        HttpResponse("拡張子が\".jpg\"のものを選択してください", status=400)

    # ここからデータベースの作成
    img_path = os.path.join(UPLOADE_DIR, file_name)
    save_path = os.path.join(UPLOADE_DIR, "akatsuki_menu.jpg")  # トリミングした画像のパス
    dir_path = os.path.join(UPLOADE_DIR, "split_img/")  # 分割した画像の保存場所
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    now_month = datetime.datetime.now().month
    now_year = datetime.datetime.now().year
    df = Menu_data(img_path, save_path, dir_path)  # DataFrame型で作成
    for index_num, row in df.iterrows():
        index_num = index_num + 1
        insert_data = FoodMenu(year=now_year, month=now_month, day=index_num, breakfast=row["Breakfast"],
                               lunch=row["Lunch"], dinner=row["Dinner"])
        insert_data.save()

    logger.info("Done registration of data of menu")

    return redirect("/food/")


class AkatsukiViewSet(viewsets.ModelViewSet):
    queryset = FoodMenu.objects.all()
    serializer_class = FoodSerializer


class AkatsukiYearMonthDay(generics.ListAPIView):
    serializer_class = FoodSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """

        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        return FoodMenu.objects.filter(year=year, month=month, day=day)


class AkatsukiYearMonth(generics.ListAPIView):
    serializer_class = FoodSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        return FoodMenu.objects.filter(year=year, month=month)


class AkatsukiYear(generics.ListAPIView):
    serializer_class = FoodSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        year = self.kwargs["year"]
        return FoodMenu.objects.filter(year=year)
