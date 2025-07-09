from django.urls import path
from board import views
from board.views import IndexView, BoardListRegistView, BoardReadEditRemoveView

app_name = 'board'

urlpatterns = [
  path('', BoardListRegistView.as_view(), name='board_list_regist'),
  path('<int:id>', BoardReadEditRemoveView.as_view(), name='board_read'),
]