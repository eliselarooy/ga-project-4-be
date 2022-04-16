from jwt_auth.serializers import UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import *
from .serializers import *

# Create your views here.


class SingleDonationList(ListAPIView):
    queryset = SingleDonation.objects.all()
    serializer_class = SingleDonationSerializer


class MonthlyDonationList(ListAPIView):
    queryset = MonthlyDonation.objects.all()
    serializer_class = MonthlyDonationSerializer


class SingleDonationCreate(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        request.data['user'] = request.user.id

        single_donation_serializer = SingleDonationSerializer(
            data=request.data)

        if single_donation_serializer.is_valid():
            single_donation_serializer.save()
            return Response(data=single_donation_serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=single_donation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleDonationRetrieveUpdateDelete(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        single_donation = self.get_single_donation(pk=pk)
        serialized_donation = SingleDonationSerializer(single_donation)

        return Response(data=serialized_donation.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        donation_to_update = self.get_single_donation(pk=pk)
        request.data['user'] = request.user.id

        if request.user != donation_to_update.user:
            raise PermissionDenied({'message': 'Invalid credentials'})

        updated_donation = SingleDonationSerializer(
            donation_to_update, data=request.data)

        if updated_donation.is_valid():
            updated_donation.save()
            return Response(updated_donation.data, status=status.HTTP_200_OK)

        return Response(data=updated_donation.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_single_donation(self, pk):
        try:
            return SingleDonation.objects.get(pk=pk)

        except SingleDonation.DoesNotExist:
            raise NotFound(detail="Cannot find that donation")


class MonthlyDonationCreate(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        request.data['user'] = request.user.id

        monthly_donation_serializer = MonthlyDonationSerializer(
            data=request.data)

        if monthly_donation_serializer.is_valid():
            monthly_donation_serializer.save()
            return Response(data=monthly_donation_serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=monthly_donation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
