from django.urls import path, include
from Petstagram.common import views


urlpatterns = [
    path('', views.index, name='index'),
    path("like/<int:photo_id>/", views.like_functionality, name='like'),
    path("share/<int:photo_id>/", views.copy_link_clipboard, name='share'),
    path("comment/<int:photo_id>/", views.add_comment, name='comment'),
]