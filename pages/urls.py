# page/urls.py

from django.urls import path, register_converter
from .views import message, homePageView, predictPageView, resultPageView, reportPageView, predictPost, results


class FloatUrlParameterConverter:
    regex = '[0-9]+\.?[0-9]+'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)


register_converter(FloatUrlParameterConverter, 'float')

urlpatterns = [
    path('', homePageView, name='home'),
    path('predict/', predictPageView, name='predict'),
    path('report/', reportPageView, name='report'),
    path('predictPost/', predictPost, name='predictPost'),
    path("message/<str:msg>/<str:title>", message, name="message"),
    path(
        'results/<int:temp>/<str:luminosity>/<str:radius>/<str:magnitude>/<int:colour>/<int:spectral_class>',
        results, name='results'),
]
