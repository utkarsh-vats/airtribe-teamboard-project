from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q, Count
from django.db import transaction
from .permissions import IsAdminUser
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

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = authenticate(username=username, password=password)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        company = Company.objects.get(user=user)
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response(
                {
                    'access': access,
                    'company_name': company.company_name,
                    'api_key': company.api_key,
                }, 
                status=status.HTTP_200_OK
            )

class KBQueryView(APIView):
    def post(self, request):
        company = Company.objects.get(user=request.user)
        search = request.data.get('search')

        if not search:
            return Response({'error': 'Search term is required'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            entries = KBEntry.objects.filter(Q(question__icontains=search) | Q(answer__icontains=search))
            serialize = KBEntrySerializer(entries, many=True)

            count = entries.count()
            query_log = QueryLog.objects.create(company=company, search_term=search, results_count=count)

        return Response({
            'search': search,
            'count': count,
            'results': serialize.data,
        }, status=status.HTTP_200_OK)

class UsageSummaryView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        total_queries = QueryLog.objects.aggregate(total = Count('id'))['total']
        active_companies = QueryLog.objects.values('company').distinct().count()
        top_search_terms = QueryLog.objects.values('search_term').annotate(count=Count('id')).order_by('-count')[:5]

        return Response({
            'total_queries': total_queries,
            'active_companies': active_companies,
            'top_search_terms': top_search_terms,
        }, status=status.HTTP_200_OK)