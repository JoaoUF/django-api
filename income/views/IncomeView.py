from income.models import Income
from income.permissions import IsOwner
from income.serializers import IncomeSerializer
from authentication.models import CustomUser
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class IncomeListAPIView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serialiser):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class IncomeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
