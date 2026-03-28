from accounts.api.v1.serializers.otp_serializers import SendOTPSerializer, VerifyOTPSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
    

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # ✅ New User
        if data["is_new_user"]:
            return Response({
                "is_new_user" : True,
                "temp_token" : data["temp_token"]
            }, status=status.HTTP_200_OK)

        # ✅ Existing User (Login)
        return Response({
            "is_new_user" : False,
            "user" : {
                "uuid" : data["user"].uuid,
                "full_name" : data["user"].full_name,
                "phone_number" : data["user"].phone_number,
                "email" : data["user"].email if data["user"].email else None,
                "profile_photo" : data["user"].profile_photo.url if data["user"].profile_photo else None,
            },
            "token" : {
                "access" : data["access"],
                "refresh" : data["refresh"]
            }
        },status=status.HTTP_200_OK)
