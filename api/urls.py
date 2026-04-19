from django.urls import path, include
from .views import RegisterView, LoginView, KBQueryView, UsageSummaryView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('kb/query/', KBQueryView.as_view(), name='kb_query'),
    path('admin/usage-summary/', UsageSummaryView.as_view(), name='usage_summary'),
]