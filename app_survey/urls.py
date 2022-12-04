from django.urls import path
from . import views


urlpatterns = [
    path('', views.SurveysListView.as_view(), name='surveys_list'),
    path('<int:pk>', views.SurveyDetailView.as_view(), name='survey_detail'),

]