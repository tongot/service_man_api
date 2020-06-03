from rest_framework import serializers
from .models import UserAccount, UserDetail


class UserAccountSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=255,required=False,allow_blank=True)
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField(max_length=255,required=False)

    class Meta:
        model =  UserAccount
        fields = ['id','name','surname','email','password','password_confirm']
        extra_kwargs ={'password':{'write_only':True,'required':False}}
        validators = []

    def validate(self,validate_data):
        user_id = validate_data['id'] if 'id' in validate_data  else 0
        user_email = validate_data['email']
        if user_email==None:
            raise serializers.ValidationError("Email is required")

        if user_id and user_email != None:
            if UserAccount.objects.exclude(pk=user_id).filter(email__iexact=user_email):
                raise serializers.ValidationError("This email is already in use")

        if user_email != None and user_id==0:
            if UserAccount.objects.filter(email=user_email).exists():
                raise serializers.ValidationError("This email is already in use")

        return validate_data

class UserDetailSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()
    class Meta:
        model=UserDetail
        fields = ['id','user','phone_number', 'phone_number2','address','address2']

    def create(self, validated_data):
        user1 = validated_data.pop('user')
        user = UserAccount(
        email=user1['email'],
        name=user1['name'],
        surname= user1['surname']
        )
        user.set_password(user1['password'])
        user.save()

        user_detail = UserDetail.objects.create(user=user,**validated_data)
        return user_detail

    def update(self,instance,validate_data ):
        user = validate_data.pop('user')
        instance.user.name=user['name']
        instance.user.surname=user['surname']
        instance.user.email=user['email']
        user_update=instance.user

        instance.phone_number= validate_data['phone_number']
        instance.phon_number2 = validate_data['phone_number2']
        instance.address = validate_data['address']
        instance.address2 = validate_data['address2']

        user_update.save()
        instance.save()
        return instance

    