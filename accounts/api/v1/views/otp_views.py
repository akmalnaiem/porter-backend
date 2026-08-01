from accounts.api.v1.serializers.otp_serializers import SendOTPSerializer, VerifyOTPSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({
            "message": "OTP sent successfully",
            "retry_after": 60
            },
            status=status.HTTP_200_OK
        )


class BaseVerifyOTPView(APIView):
    permission_classes = [AllowAny]
    role = None

    def post(self, request):
        serializer = VerifyOTPSerializer(
            data=request.data,
            context={"role": self.role}
            )

        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # ✅ New User
        if data["user_status"] == "NEW":
            return Response({
                "user_status" : data["user_status"],
                "temp_token" : data["temp_token"],
            }, status=status.HTTP_200_OK)

        else:
            # ✅ Existing User (Login)
            return Response({
                "user_status" : data["user_status"],
                "user" : {
                    "uuid" : data["user"].uuid,
                    "full_name" : data["user"].full_name,
                    "phone_number" : data["user"].phone_number,
                    "email" : data["user"].email if data["user"].email else None,
                    "profile_photo" : data["user"].profile_photo.url if data["user"].profile_photo else None,
                    "role": data["user"].role,
                    "language": data["user"].language.code if data["user"].language else None,
                    "gender": data["user"].gender,

                    # Traveller
                    "city": data["user"].city if data["user"].role == "user" else None
                },
                "token" : {
                    "access" : data["access"],
                    "refresh" : data["refresh"]
                }
            },
            status=status.HTTP_200_OK)



class UserVerifyOTPView(BaseVerifyOTPView):
    role = "user"

class PorterVerifyOTPView(BaseVerifyOTPView):
    role = "porter"
