from typing import ByteString
from rest_framework import response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.shortcuts import render
from .models import RecordMaster
from .serializers import *

def index(request):
    return render(request, "build/index.html")

class UserRegistrationView(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            if user:
                return Response("success", status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# def generate_key():
#     """
#     Generates a key and save it into a file
#     """
#     key = Fernet.generate_key()
#     with open("secret.key", "wb") as key_file:
#         key_file.write(key)

def load_key():
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()

class RecordListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=RecordSerializer

    def perform_create(self, serializer):
        key=load_key()
        fernet = Fernet(key)
        website_password=self.request.data.get('website_password')
        encrypted_website_password = fernet.encrypt(website_password.encode())
        serializer.save(created_by=self.request.user,website_password=encrypted_website_password)

    def get_queryset(self):
        records=RecordMaster.objects.filter(created_by=self.request.user.id) 
        output_data=[]
        key=load_key()
        fernet = Fernet(key)
        for record in records.iterator():
            password=bytes(record.website_password.split("'")[1],"utf-8")
            website_password=fernet.decrypt(password).decode()   
            output_data.append({'id':record.id,'website_name':record.website_name,"website_url":record.website_url,"website_username":record.website_username,"website_password":website_password})
        return output_data

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_delete_record(request, pk):
    try: 
        record = RecordMaster.objects.get(pk=pk) 
    except RecordMaster.DoesNotExist: 
        return Response({'message': 'The record does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'PUT': 
        record_serializer = RecordSerializer(data=request.data) 
        if record_serializer.is_valid(): 
            record_serializer.save() 
            return Response(record_serializer.data) 
        return Response(record_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'DELETE': 
        record.delete() 
        return Response({'message': 'Record was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    