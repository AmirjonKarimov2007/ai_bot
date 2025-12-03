from django.shortcuts import render

# Create your views here.
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import User, Promocode, PromocodeUsage
from .serializers import UserSerializer, PromocodeSerializer, PromocodeUsageSerializer
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import PromocodeUsage
from .serializers import PromocodeUsageSerializer



class PromocodeViewSet(viewsets.ModelViewSet):
    queryset = Promocode.objects.all()
    serializer_class = PromocodeSerializer

    # Promo-kodni faollashtirish
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        promocode = self.get_object()

        # Promo-kodni faollashtirishni tekshirish
        if not promocode.is_valid():
            return Response({"detail": "Promo code is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Foydalanuvchining ID'si
        user = request.user

        # Promo-kodni foydalanuvchiga qo'llash
        promocode_usage, created = PromocodeUsage.objects.get_or_create(user=user, promocode=promocode)

        if not created:
            return Response({"detail": "This promo code has already been used by this user."}, status=status.HTTP_400_BAD_REQUEST)

        # Promo-kodni foydalanuvchiga qo'llash
        promocode.used_count += 1
        promocode.save()

        return Response({"detail": "Promo code successfully applied."}, status=status.HTTP_200_OK)

class PromocodeUsageViewSet(viewsets.ModelViewSet):
    queryset = PromocodeUsage.objects.all()
    serializer_class = PromocodeUsageSerializer
