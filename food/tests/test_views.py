from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from config.settings.base import BASE_DIR
import os
import json


def read_json(path):
    with open(path, "r") as f:
        result = json.load(f)
    return result


class TestFoodWeb(TestCase):
    """templateなどのテスト"""
    # fixturesで指定すればsetUpClass()の中でファイルが読み込まれてレコードが自動で作成されます。
    fixtures = ["test_views_menu_2019_7.json"]

    def test_index_html(self):
        res = self.client.get(reverse("food:index"))
        self.assertTemplateUsed(res, "food/index.html")

    def test_form_html(self):
        res = self.client.get(reverse("food:form"))
        self.assertTemplateUsed(res, "food/form.html")


class TestFoodAPI(APITestCase):
    """food APIのテスト"""
    fixtures = ["test_views_menu_2019_7.json"]

    def setUp(self) -> None:
        self.json_data = read_json(os.path.join(BASE_DIR, "food/fixtures/test_views_menu_2019_7.json"))

    def test_get_menu_month(self):
        res = self.client.get(reverse("food:api-year-month", kwargs={"year": 2019, "month": 7}))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), len(self.json_data))

    def test_get_menu_day(self):
        res = self.client.get(reverse("food:api-year-month-day", kwargs={"year": 2019, "month": 7, "day": 1}))
        res_data_day1 = res.data[0]
        json_data_day1 = self.json_data[0]["fields"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data_day1, json_data_day1)
