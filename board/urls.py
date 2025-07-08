from django.urls import path
from board import views
from board.views import IndexView, BoardListView, BoardReadView, BoardRegistView, BoardEditView, BoardRemoveView

app_name = 'board'

urlpatterns = [
  path('', IndexView.as_view(), name='index'),
  path('list/', BoardListView.as_view(), name='board_list'),
  path('read/<int:id>/', BoardReadView.as_view(), name='board_read'),
  path('register/', BoardRegistView.as_view(), name='board_regist'),
  path('edit/<int:id>/', BoardEditView.as_view(), name='board_edit'),
  path('remove/<int:id>/', BoardRemoveView.as_view(), name='board_remove'),
]