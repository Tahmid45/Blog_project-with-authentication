from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('add/',views.add_post, name='addpost'),
    path('add/',views.AddPostCreateView.as_view(), name='addpost'),
    # path('edit/<int:id>',views.edit_post, name='editpost'),
    path('edit/<int:id>',views.EditPostView.as_view(), name='editpost'),
    # path('delete/<int:id>',views.delete_post, name='deletepost'),
    path('delete/<int:id>',views.DeletePostView.as_view(), name='deletepost'),
    path('details/<int:id>',views.DetailPostView.as_view(), name='detailsPost'),
]
