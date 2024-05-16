from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from expenses.serializers import ExpenseSerializer
from authentication.models import CustomUser
from expenses.models import Expense
from expenses.permissions import IsOwner
from rest_framework import permissions

class ExpeneseListAPIView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serialiser):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class ExpeneseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
