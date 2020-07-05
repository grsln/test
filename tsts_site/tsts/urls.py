from django.urls import path
from . import views

app_name = 'tsts'
urlpatterns = [
    path("tstng/", views.tstng, name='tstng'),
    path("<int:pk>/<int:question_id>/", views.TstQuestionView.as_view(), name='tst_questions'),
    path("<int:pk>/quit/", views.TstQuitView.as_view(), name='tst_quit'),
    path("", views.index, name='index'),
    path("api/t/<int:pk>/", views.TView.as_view()),
    path("api/t/create/", views.TCreateView.as_view())
]
