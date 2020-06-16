from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .serializers import UserDetailSerializer,UserAccountSerializer
from .models import UserDetail, UserAccount
from .permissions import IsOwnerOrReadOnly


class UserAccountViewSet(viewsets.ViewSet):
    """this Handels all activities that are to do with the user registation"""
    authentication_classes = []
    permission_classes = [IsOwnerOrReadOnly]

    def list(self,request):
        users = UserDetail.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self,request,pk=None):
        user = get_object_or_404(UserDetail.objects.all(), pk=pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    def create(self,request):
        serializer_class = UserDetailSerializer(data=request.data)

        if (request.data['user']['password'] != request.data['user']['password_confirm']):
            return Response({'password_mismatch_error':'Password did not match'},status.HTTP_400_BAD_REQUEST)

        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk=None):
        user_detail = UserDetail.objects.get( pk = pk)

        serializer_class = UserDetailSerializer(instance=user_detail,data=request.data)

        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        user_detail = get_object_or_404(UserDetail.objects.all(), pk = pk)
        user =  get_object_or_404(UserAccount.objects.all(), pk = user_detail.user.id)
        user.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


class LoginViewSet(viewsets.ViewSet):
    """returns the auth token for the user"""

    serializer_class = AuthTokenSerializer

    def create(self,request):
        """use the obtainauth API view to obtain the token"""
        return ObtainAuthToken().post(request)

class GetUser(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request, format=None):
        try:
            user_details = UserDetail.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            user =({
                    'email':request.user.email,
                    'name':request.user.name,
                    'surname':request.user.surname,
                    'id':request.user.id})
            return Response(user)

        user =({
                    'email':request.user.email,
                    'name':request.user.name,
                    'surname':request.user.surname,
                    'id':request.user.id,
                    'address':user_details.address,
                    'address2':user_details.address,
                    'phone_number':user_details.phone_number
            })
        return Response(user)

        
 