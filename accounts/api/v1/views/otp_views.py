from accounts.api.v1.serializers.otp_serializers import SendOTPSerializer, VerifyOTPSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "OTP sent"}, status=status.HTTP_200_OK)
    

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #LOGIN RESPONSE
        if serializer.validated_data["purpose"] == "login":
            user = serializer.validated_data["user"]

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
                        "refresh" : serializer.validated_data["refresh"],
                        "access" : serializer.validated_data["access"]
                    },
                },
                status = status.HTTP_200_OK
            )
        
        # RESET PASSWORD RESPONSE
        return Response({
            "message" : "OTP verified. You can reset password now.",
            "uid" : serializer.validated_data["uid"],
            "reset_token" : serializer.validated_data["reset_token"],
        })

