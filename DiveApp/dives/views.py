from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from dives.DiveSerializers import DiveSerializer
from services.dive_service import DiveService


@api_view(['POST'])
def create_Dive(request):
    if request.method == 'POST':
        data = request.data
        dive =DiveService.create_dive(user, data)

        serializer = DiveSerializer(dive)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_Dives(request):
    if request.method == 'GET':
        dives = DiveService.list_user_dives(request.user)
        serializer = DiveSerializer(dives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)