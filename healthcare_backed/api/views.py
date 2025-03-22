from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from .models import *
from .serializers import PatientSerializer, DoctorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from api.models import Patient
from api.serializers import PatientSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import PatientDoctorMappingSerializer


class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

class PatientCreateView(generics.CreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class DoctorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]


# User Registration View
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login View
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]


# Assign a doctor to a patient & List all mappings
class PatientDoctorMappingListCreateView(generics.ListCreateAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

# Retrieve all doctors assigned to a specific patient
class PatientDoctorMappingByPatientView(generics.ListAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return PatientDoctorMapping.objects.filter(patient_id=patient_id)

# Remove a doctor from a patient
class PatientDoctorMappingDeleteView(generics.DestroyAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
