from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer
from drf_yasg.utils import swagger_auto_schema

class CommentLisCreatetView(APIView):
    @swagger_auto_schema(responses={200: CommentSerializer(many=True)})
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
      
    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDeleteView(APIView):
    @swagger_auto_schema(operation_description="댓글 삭제", responses={204: 'No Content', 404: 'Not Found'})
    def delete(self, request, id):
        try:
            comment = Comment.objects.get(pk=id)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)