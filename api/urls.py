from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('patients/', PatientListCreateView.as_view(), name='patients'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('doctors/', DoctorListCreateView.as_view(), name='doctors'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('mappings/', PatientDoctorMappingListCreateView.as_view(), name='mappings'),
    path('mappings/<int:patient_id>/', PatientDoctorMappingByPatientView.as_view(), name='patient-mappings'),
    path('mappings/delete/<int:pk>/', PatientDoctorMappingDeleteView.as_view(), name='mapping-delete'),
]
