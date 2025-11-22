from django.contrib.auth.models import User
from .models import Category, Expense
from .serializers import UserRegistrationSerializer, UserSerializer, ExpenseSerializer, CategorySerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

# --------------------------------------------------
#  USER REGISTRATION VIEW
# --------------------------------------------------

class UserRegistrationViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be registered"""
    query_set = User.objects.all()
    serializer_class = UserRegistrationSerializer

    # Set permission to AllowAny, so anyone (include unauthenticated users) can create a new account
    permission_classes = [AllowAny]

# --------------------------------------------------
#  CATEGORY VIEW
# --------------------------------------------------

class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint that allows categories to be viewed or edited"""
    serializer_class = CategorySerializer

    # Only a logged-in user can access this endpoint
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """This view should return a list of all categories for the currently authenticated user"""

        # Filtered to only return catgories that owned by the user making the request
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically assign the new create category to the currently authenticated user"""

        serializer.save(user=self.request.user)

# --------------------------------------------------
#  EXPENSE VIEW
# --------------------------------------------------

class ExpenseViewSet(viewsets.ModelViewSet):
    """API endpoint that allows expenses to be viewed or edited"""
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """This view should return a list of all expenses for the currently authenticated user"""
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically assign the new create expense to the currently authenticated user"""

        serializer.save(user=self.request.user)

# --------------------------------------------------
#  PROFILE VIEW
# --------------------------------------------------
class UserProfileView(APIView):
    """API endpoint to get the current user's details"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    