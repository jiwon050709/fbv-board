from django.urls import path
from board import views
from board.views import IndexView, BoardListRegistView, BoardReadEditRemoveView
from .views import CommentListCreateView, CommentDeleteView

app_name = 'board'

urlpatterns = [
  path('', BoardListRegistView.as_view(), name='board_list_regist'),
  path('<int:id>', BoardReadEditRemoveView.as_view(), name='board_read'),
  path('<int:board_id>/comments', CommentListCreateView.as_view(), name='board_comments'),\
  path('<int:board_id>/comments/<int:id>', CommentDeleteView.as_view(), name='board_comments'),
]