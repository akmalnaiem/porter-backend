from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from accounts.api.v1.serializers.profile_serializer import ProfileUpdateSerializer


class ProfileView(APIView):

    def patch(self, request):
        try:
            serializer = ProfileUpdateSerializer(
                request.user,
                data=request.data,
                partial=True
            )

            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            return Response(
                {
                    "message": "Profile updated successfully.",
                    "user": {
                        "uuid": user.uuid,
                        "full_name": user.full_name,
                        "phone_number": user.phone_number,
                        "email": user.email,
                        "profile_photo": (
                            user.profile_photo.url
                            if user.profile_photo
                            else None
                        ),
                        "language": user.language.code if user.language else None,
                        "gender": user.gender,
                        "city": (
                            user.city
                            if user.role == "user"
                            else None
                        ),
                        "role": user.role,
                    }
                }, status=status.HTTP_200_OK
            )

        except ValidationError as e:
            return Response(
                {
                    "message": "Validation failed",
                    "error": e.detail
                }, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {
                    "message": "Something went wrong while updating profile",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
