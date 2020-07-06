import random

from django.contrib.auth import authenticate
from django.apps import apps
from django.core.mail import send_mail

from rest_framework import serializers
from .models import UserAccount, UserDetail, UserConfirmed

Country = apps.get_model('business', 'Country')


class UserAccountSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField(max_length=255, required=False)

    class Meta:
        model = UserAccount
        fields = ['id', 'name', 'surname', 'email',
                  'password', 'password_confirm']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}
        validators = []

    def validate(self, validate_data):
        user_id = validate_data['id'] if 'id' in validate_data else 0
        user_email = validate_data.get('email')
        if user_email == None:
            raise serializers.ValidationError("Email is required")

        if user_id and user_email != None:
            if UserAccount.objects.exclude(pk=user_id).filter(email__iexact=user_email):
                raise serializers.ValidationError(
                    "This email is already in use")

        if user_email != None and user_id == 0:
            if UserAccount.objects.filter(email=user_email).exists():
                raise serializers.ValidationError(
                    "This email is already in use")

        return validate_data


class UserDetailSerializer(serializers.ModelSerializer):
    country_detail = serializers.SerializerMethodField(read_only=True)
    user = UserAccountSerializer()

    class Meta:
        model = UserDetail
        fields = ['id', 'user', 'phone_number', 'phone_number2',
                  'address', 'address2', 'country', 'country_detail']

    def get_country_detail(self, user):

        detail = user.country
        data = {'id': detail.id, 'name': detail.name,
                'code': detail.country_code}
        return data

    def create(self, validated_data):
        user1 = validated_data.pop('user')
        user = UserAccount(
            email=user1['email'],
            name=user1['name'],
            surname=user1['surname'],
        )
        user.set_password(user1['password'])
        user.save()

        user_detail = UserDetail.objects.create(user=user, **validated_data)
        # generate random number for confirmation
        code = random.randint(100000, 999999)
        UserConfirmed.objects.create(user=user, confirmation_number=code)
        # send email with confirmation number
        send_mail(
            'Tshwaragano Confirm number {}'.format(code),
            'Thank you for registering with Tsharagano',
            'groovetebots@gmail.com',
            [user1['email']],
        )
        return user_detail

    def update(self, instance, validate_data):
        user = validate_data.pop('user')
        instance.user.name = user['name']
        instance.user.surname = user['surname']
        instance.user.email = user['email']

        user_update = instance.user

        instance.phone_number = validate_data['phone_number']
        instance.phone_number2 = validate_data['phone_number2']
        instance.address = validate_data['address']
        instance.address2 = validate_data['address2']
        instance.country = validate_data['country']

        user_update.save()
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['email', 'name', 'surname', 'is_confirmed']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = '__all__'
        read_only_fields = ['password']

    def validate(self, validate_data):
        email = validate_data.get('email')
        password = validate_data.get('password')

        if email and password:
            if UserAccount.objects.filter(email=email).exists():
                user = authenticate(request=self.context.get(
                    'request'), email=email, password=password)
            else:
                msg = {
                    "message": "user does not exist",
                    'status': False
                }
                raise serializers.ValidationError(msg)
            if not user:
                msg = {
                    "message": "invalid username or password",
                    'status': False
                }
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = {
                "message": "All details are required",
                'status': False
            }
            raise serializers.ValidationError(msg, code='authorization')
        validate_data['user'] = user
        return validate_data
