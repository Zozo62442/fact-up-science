from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),

    path('subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),

    path('<slug:slug>/edit_comment/<int:comment_id>',
         views.comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>',
         views.comment_delete, name='comment_delete'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
