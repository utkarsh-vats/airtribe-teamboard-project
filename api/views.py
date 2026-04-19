from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q, Count
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistrationSerializer, KBEntrySerializer
from .models import Company, KBEntry, QueryLog

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        company_name = serializer.validated_data['company_name']
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        company = Company.objects.get(user=user)
        company.company_name = company_name
        company.save()

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response(
                {
                    'username': user.username, 
                    'company_name': company.company_name,
                    'api_key': company.api_key,
                    'access': access,
                }, 
                status=status.HTTP_201_CREATED
            )






