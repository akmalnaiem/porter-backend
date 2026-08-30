from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from accounts.api.v1.serializers.profile_serializer import ProfileSerializer, ProfileUpdateSerializer
import logging

logger = logging.getLogger(__name__)


class ProfileView(APIView):
    def get(self, request):
        try:
            user = request.user
            serializer = ProfileSerializer(user)

            return Response(
                {
                    "Success": True,
                    "message": "Profile Fetched Successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "Success": False,
                    "message": "Requested resource does not exist"
                }, status=status.HTTP_404_NOT_FOUND
            )
        except DatabaseError as db_err:
            return Response(
                {
                    "Success": False,
                    "message": "Something went wrong while accessing the database"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Unexpected error in ProfileView: {e}")
            return Response(
                {
                    "Success": False,
                    "message": "An unexcepted error occured. Please try again later"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class ProfileUpdateView(APIView):

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
