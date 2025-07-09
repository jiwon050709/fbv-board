from django.urls import path
from .views import CommentListCreateView, CommentDeleteView

urlpatterns = [
    path('', CommentListCreateView.as_view(), name='comment_list'),
    path('<int:id>', CommentDeleteView.as_view(), name='comment_delete'),
]
