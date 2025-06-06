from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from UserProfile.models import UserProfile


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])

    if not user.check_password(request.data['password']):
        return Response({"error" : 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user = user)


    serializer = UserSerializer(instance=user)

    return Response({"token" : token.key}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])  
        user.save()

        # Verifica si el UserProfile ya existe
        UserProfile.objects.get_or_create(user=user)  # Esto creará el UserProfile si no existe

        token = Token.objects.create(user=user)
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):

    print(request.user)
    return Response("You are login with {}".format(request.user.username), status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    # Eliminar el token del usuario
    request.user.auth_token.delete()
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
