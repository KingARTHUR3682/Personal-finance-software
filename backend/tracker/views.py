from django.contrib.auth.models import User
from .models import Category, Expense
from .serializers import UserRegistrationSerializer, UserSerializer, ExpenseSerializer, CategorySerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status

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
    
class RequestPasswordResetEmail(APIView):
    """
    Step 1: User POSTs email. We generate a link and send it via email.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # For security, don't reveal that the user doesn't exist.
            # Just say "If account exists, email sent."
            return Response({'message': 'If an account exists, a reset link has been sent.'})

        # Generate token and ID
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Create the link pointing to your VUE Frontend
        # It must match the route in your Vue router: /reset-password/:uidb64/:token
        resetSF_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

        # Send Email
        subject = "Password Reset Request"
        message = f"Click the link below to reset your password:\n\n{resetSF_link}"
        
        send_mail(subject, message, 'noreply@financeapp.com', [email])

        return Response({'message': 'Password reset link sent.'})


class PasswordResetConfirmView(APIView):
    """
    Step 2: User POSTs uid, token, and new passwords to reset.
    """
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')

        if not new_password1 or not new_password2:
            return Response({'error': 'Both password fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password1 != new_password2:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.getzk(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid UID'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.set_password(new_password1)
        user.save()

        return Response({'message': 'Password reset successful'})