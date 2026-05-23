from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.api.v1.serializers.auth_serializers import RegisterSerializer
import jwt
from django.conf import settings


class PublicTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


# Register View-
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        token = request.data.get("temp_token")

        if not token:
            return Response({"error" : "Token missing"}, status=status.HTTP_404_NOT_FOUND)
        else:
            token = token.strip()
            
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )
            phone_number = payload["phone_number"]
            
        except jwt.ExpiredSignatureError:
            return Response({"error" : "Token expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.InvalidTokenError:
            return Response({"error" : "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RegisterSerializer(
            data = request.data,
            context = {"phone_number" : phone_number}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response({
            "user" : {
                "uuid" : data["user"].uuid,
                "full_name" : data["user"].full_name,
                "phone_number" : data["user"].phone_number,
                "email" : data["user"].email if data["user"].email else None,
                "profile_photo" : data["user"].profile_photo.url if data["user"].profile_photo else None
            },
            "tokens" : {
                "access" : data["access"],
                "refresh" : data["refresh"],
            }
        }, status=status.HTTP_201_CREATED
        )
