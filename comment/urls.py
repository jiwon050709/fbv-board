from django.urls import path
from .views import CommentLisCreatetView, CommentDeleteView

urlpatterns = [
    path('', CommentLisCreatetView.as_view(), name='comment_list'),
    path('<int:id>', CommentDeleteView.as_view(), name='comment_delete'),
]
