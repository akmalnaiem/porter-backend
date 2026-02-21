from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.api.v1.serializers.auth_serializers import RegisterSerializer, LoginSerializer, ResetPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# Register View-
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "message" : "User registered successfully",
                "user": {
                    "id" : user.id,
                    "full_name" : user.full_name,
                    "phone_number" : user.phone_number,
                    "email" : user.email
                },
            },
            status = status.HTTP_201_CREATED
        )
    

# Login View-
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        # Generate JWT Token
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message" : "Login Successful",
                "user" : {
                    "id" : user.id,
                    "full_name" : user.full_name,
                    "phone_number" : user.phone_number,
                    "email" : user.email,
                },
                "tokens" : {
                    "refresh" : str(refresh),
                    "access" : str(refresh.access_token),
                },
            },
            status = status.HTTP_200_OK
        )
    

# Reset Password View-
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Password reset successful"},
            status=status.HTTP_200_OK,
        )