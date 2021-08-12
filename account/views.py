from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from .services import UserActivityFromRequest


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_user_last_activity(request):
    user_activity_from_request = UserActivityFromRequest(request)
    user_id = user_activity_from_request.get_user_id()
    last_login, user_exists = user_activity_from_request.get_user_last_login()
    last_request = user_activity_from_request.get_user_last_request()

    if not user_id:
        return Response(
            {
                'status': 'error',
                'details': 'Query is incorrect, check your query parameters.'
            },
            status=HTTP_400_BAD_REQUEST
        )

    if not last_login and not user_exists:
        return Response(
            {
                'status': 'error',
                'details': f'User with id <{user_id}> does not exist.'
            },
            status=HTTP_404_NOT_FOUND
        )

    return Response(
        {
            'status': 'success',
            'user_id': user_id,
            'last_login': last_login,
            'last_request': last_request
        },
        status=HTTP_200_OK
    )
