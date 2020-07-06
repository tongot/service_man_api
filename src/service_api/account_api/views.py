import random
import string
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action

from .serializers import UserDetailSerializer, UserAccountSerializer, LoginSerializer
from .models import UserDetail, UserAccount, UserConfirmed
from .permissions import IsOwnerOrReadOnly

from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication


class UserAccountViewSet(viewsets.ViewSet):
    """this Handels all activities that are to do with the user registation"""
    # authentication_classes = []
    permission_classes = [IsOwnerOrReadOnly]

    def list(self, request):
        users = UserDetail.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(UserDetail.objects.all(), pk=pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer_class = UserDetailSerializer(data=request.data)

        if (request.data['user']['password'] != request.data['user']['password_confirm']):
            return Response({'password_mismatch_error': 'Password did not match'}, status.HTTP_400_BAD_REQUEST)

        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        user_detail = UserDetail.objects.get(pk=pk)
        serializer_class = UserDetailSerializer(
            instance=user_detail, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user_detail = get_object_or_404(UserDetail.objects.all(), pk=pk)
        user = get_object_or_404(
            UserAccount.objects.all(), pk=user_detail.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginViewSet(viewsets.ViewSet):
    """returns the auth token for the user"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """use the obtainauth API view to obtain the token"""
        return ObtainAuthToken().post(request)


class GetUser(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.user.is_confirmed:
            try:
                user_details = UserDetail.objects.get(user_id=request.user.id)
            except ObjectDoesNotExist:
                user = ({
                        'email': request.user.email,
                        'name': request.user.name,
                        'surname': request.user.surname,
                        'id': request.user.id})
                return Response(user)

            user = ({
                'email': request.user.email,
                'name': request.user.name,
                'surname': request.user.surname,
                'id': request.user.id,
                'user_detail_id': user_details.id,
                'address': user_details.address,
                'address2': user_details.address,
                'phone_number': user_details.phone_number,
                'phone_number2': user_details.phone_number2,
                'country': user_details.country.name,
                'country_id': user_details.country.id
            })
            return Response(user)
        else:
            return Response({'message': 'user not confirmed'}, status=status.HTTP_401_UNAUTHORIZED)


class ConfirmCode(APIView):
    def send_email(self, user_exist):
        # generate random number for confirmation
        code = random.randint(100000, 999999)
        code_owner = UserConfirmed.objects.filter(
            user_id=user_exist.id).first()
        if code_owner:
            code_owner.confirmation_number = code
            code_owner.save()
        else:
            UserConfirmed.objects.create(
                user=user_exist, confirmation_number=code)
        # send email with confirmation number
        send_mail(
            'Tshwaragano Confirm number {}'.format(code),
            'Thank you for registering with Tsharagano',
            'groovetebots@gmail.com',
            [user_exist.email],
        )
    # confirm code sent  by email

    def get(self, request, pk=None):
        code = request.query_params.get('code')
        user = request.query_params.get('user')
        print(user)
        if code and user:
            if UserAccount.objects.filter(email=user, is_confirmed=True).exists():
                return Response({'message': 'email already confirmed'}, status=status.HTTP_400_BAD_REQUEST)
            user_exist = UserConfirmed.objects.filter(
                user__email=user, confirmation_number=code).first()
            if user_exist:
                user_account = UserAccount.objects.get(pk=user_exist.user.id)
                user_account.is_confirmed = True
                user_account.save()
                user_exist.delete()
                return Response({'message': 'confirmed'})
            else:
                return Response({'message': 'code did not match'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'code not found'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if request.user.is_authenticated:
            user = request.user.email
            new_email = request.data.get('newEmail')
            if new_email:
                if new_email.lower() == user.lower():
                    return Response({'message': 'New email must differ from old email'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if UserAccount.objects.filter(email=new_email).exists():
                        return Response({"message": "Email already in use"}, status=status.HTTP_409_CONFLICT)
                    else:
                        user_exist = UserAccount.objects.filter(
                            email=user).first()
                        user_exist.email = new_email
                        user_exist.is_confirmed = False
                        user_exist.save()
                        self.send_email(user_exist)
                        return Response({'message': 'email changed'})
            else:
                return Response({'message': 'no email provided'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, pk=None):
        """Resend the code to the client """
        user = request.data.get('user')
        old_user = request.data.get('old_user')
        if user and old_user:
            print(user)
            email_changed = False
            if user.lower() != old_user.lower():
                email_changed = True
            if user:
                user_exist = UserAccount.objects.filter(
                    email=old_user, is_confirmed=False).first()

                if user_exist:
                    if email_changed:
                        if UserAccount.objects.filter(email=user).exists():
                            return Response({"message": "Email already in use"}, status=status.HTTP_409_CONFLICT)
                        else:
                            # change the email in email table
                            user_exist.email = user
                            user_exist.is_confirmed = False
                            user_exist.save()
                    self.send_email(user_exist)
                else:
                    return Response({'message': 'user not registered or already confirmed'}, status=status.HTTP_404_NOT_FOUND)
                return Response({'message': 'confirm send'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'all details are required'}, status=status.HTTP_404_NOT_FOUND)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        user = request.data.get('user')
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        password_confirm = request.data.get('password_confirm')
        if user and password and new_password and password_confirm:
            if password_confirm != new_password:
                return Response({'message': 'password did not match'})
            user_exist = UserAccount.objects.filter(email=user).first()
            if user_exist:
                if user_exist.check_password(password):
                    user_exist.set_password(new_password)
                    user_exist.save()
                    return Response({'message': 'password_changed'})
                else:
                    return Response({'message': 'Wrong Password'})
            else:
                return Response({'message': 'User not found'})
        else:
            return Response({'message': 'All fields are required'})


class ForgotPassword(APIView):

    def post(self, request, pk=None):
        user = request.data.get('user')
        if user:
            user_exist = UserAccount.objects.filter(email=user).first()
            if user_exist:
                # generate new password
                randString = string.ascii_letters
                randChar = ['#', '!', '@', '#', '%', '?', '%', '&', '*']
                password = ''.join(random.choice(randString) for i in range(6))
                getRandChar = randChar[random.randint(0, 8)]
                password = '{}{}{}'.format(
                    password, getRandChar, random.randint(0, 9))
                user_exist.set_password(password)
                user_exist.save()
                send_mail(
                    'Tshwaragano Password Reset',
                    'Your password has been reset to {}'.format(password),
                    'groovetebots@gmail.com',
                    [user_exist.email],
                )
                return Response({'message': 'Please Check Your Email'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Not found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Not found'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_confirmed:
            login(request, user)
        else:
            return Response({'message': 'not_confirmed'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, format=None)
