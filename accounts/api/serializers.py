from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework import exceptions

# serializer的用处： 1. 在前段渲染用户的object的时候，渲染成json格式。 2. 用来验证用户是否存在
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class SignupSerializer(serializers.ModelSerializer): #用modelserializer的话，用serializer.save的时候，会把用户创建出来，所以会新增一个class meta
    username = serializers.CharField(max_length = 20,min_length = 6)
    password = serializers.CharField(max_length = 20,min_length = 6)
    email = serializers.EmailField() #会自动有email的检测机制

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    # will be called wehn is_valid is called
    def validate(self, data):
        # TODO<HOMEWORK> 增加验证 username 是不是只由给定的字符集合构成
        if User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'This username has been occupied.'
            })
        if User.objects.filter(email=data['email'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'This email address has been occupied.'
            })
        return data

    def create(self, validated_data):
        username = validated_data['username'].lower()#存账号的时候，都换成小写
        email = validated_data['email'].lower()
        password = validated_data['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return user
