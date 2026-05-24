import jwt

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.api.v1.serializers.auth_serializers import RegisterSerializer



class PublicTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


# Register View-
class BaseRegisterView(APIView):
    permission_classes = [AllowAny]

    role = None

    def post(self, request):

        token = request.data.get("temp_token")

        if not token:
            return Response({"error" : "Temp token required"}, status=status.HTTP_404_NOT_FOUND)
        else:
            token = token.strip()
            
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )
            phone_number = payload.get("phone_number")

            if not phone_number:
                raise AuthenticationFailed("Phone number missing in token")

        except jwt.ExpiredSignatureError:
            return Response({"error" : "Token expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.InvalidTokenError:
            return Response({"error" : "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RegisterSerializer(
            data = request.data,
            context = {
                "phone_number" : phone_number,
                "role": self.role
                }
        )

        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response({
            "user" : {
                "uuid" : data["user"].uuid,
                "full_name" : data["user"].full_name,
                "phone_number" : data["user"].phone_number,
                "email" : data["user"].email if data["user"].email else None,
                "profile_photo" : data["user"].profile_photo.url if data["user"].profile_photo else None,
                "role" : data["user"].role
            },
            "tokens" : {
                "access" : data["access"],
                "refresh" : data["refresh"],
            }
        }, status=status.HTTP_201_CREATED
        )


class UserRegisterView(BaseRegisterView):
    role = "user"

class PorterRegisterView(BaseRegisterView):
    role = "porter"
