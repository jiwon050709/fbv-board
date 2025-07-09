# board/views.py
from django.shortcuts import render, redirect, reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Board
from comment.models import Comment
from .serializers import BoardSerializer
from comment.serializers import CommentSerializer


class IndexView(APIView):
    def get(self, request):
        return Response({'message': 'Index page'}, status=status.HTTP_200_OK)

class BoardListRegistView(APIView):
    @swagger_auto_schema(responses={200: BoardSerializer, 404: 'Board not found'})
    def get(self, request):
        boards = Board.objects.all().order_by('-id')
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=BoardSerializer, responses={201: BoardSerializer, 404: 'Board not found'})
    def post(self, request):
        title = request.data.get('title')
        writer = request.data.get('writer')
        content = request.data.get('content')
        if title and writer and content:
            board = Board.objects.create(title=title, writer=writer, content=content)
            serializer = BoardSerializer(board)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class BoardReadEditRemoveView(APIView):
    @swagger_auto_schema(responses={200: BoardSerializer, 404: 'Board not found'})
    def get(self, request, id):
        try:
            board = Board.objects.get(pk=id)
            board.incrementReadCount()
            serializer = BoardSerializer(board)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(request_body=BoardSerializer, responses={200: BoardSerializer, 404: 'Board not found'})
    def put(self, request, id):
        try:
            board = Board.objects.get(pk=id)
            board.title = request.data.get('title', board.title)
            board.writer = request.data.get('writer', board.writer)
            board.content = request.data.get('content', board.content)
            board.save()
            return Response({'message': 'Board updated successfully'}, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, id):
        try:
            board = Board.objects.get(pk=id)
            board.delete()
            return Response({'message': 'Board deleted successfully'}, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)

class CommentListCreateView(APIView):
    @swagger_auto_schema(responses={200: CommentSerializer(many=True)})
    def get(self, request, board_id):
        comments = Comment.objects.filter(board_id=board_id) 
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CommentSerializer,responses={201: CommentSerializer})
    def post(self, request, board_id):
        data = request.data.copy()
        data['board'] = board_id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentDeleteView(APIView):
    @swagger_auto_schema(operation_description="댓글 삭제", responses={204: 'No Content', 404: 'Not Found'})
    def delete(self, request, board_id, id):
        try:
            comment = Comment.objects.get(pk=id)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)