from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response #返回的都是response格式
from rest_framework import permissions
from rest_framework.decorators import action
from accounts.api.serializers import (
    UserSerializer,
    LoginSerializer,
    SignupSerializer,
)

from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
    authenticate as django_authenticate,

)
#提供一个user的api，能够读取user的具体内容
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined') #从哪去获取数据
    serializer_class = UserSerializer #数据怎么变成json
    permission_classes = [permissions.IsAuthenticated] #

class AccountViewSet(viewsets.ViewSet): #不用内置的accountviewset，自己定义，所以继承一个空的viewset
    serializer_class = SignupSerializer
    @action(methods = ['GET'], detail = False)
    # 指定是get的request
    # viewset里自带的操作是增删查改，这边我们自己定义一个action，叫login_status
        #定义在某个object上的动作，detail=False要取掉。如果是定义在整个根目录上的动作，detail = False 例如api/accounts/login_status (定义在根目录accounts上的动作);
        #api/accouns/123/login_status 是定义在object123上的动作
    def login_status(self,request):
        data = {'has_logged_in': request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)

    @action(methods = ['POST'],detail =False)
    def logout(self,request):
        django_logout(request)
        return Response(({'success':True}))

    @action(methods = ['POST'], detail = False)
    def login(self,request):
        # get user name and password from request
        serializer = LoginSerializer(data=request.data) #通过loginserializer 获取用户输入的数据
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input",
                "errors": serializer.errors,
            }, status=400)
        # validation ok, login
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        #如果user不存在的话
        '''
        下面这段queryset的代码常用于debug，看django里面的语句对应的sql语句是什么
        '''
        # queryset= User.objects.filter(username=username)
        # print(queryset.query)

        if not User.objects.filter(username=username).exists():
            return Response({
                "success": False,
                "message": "username and password does not match",
            }, status=400)

        user = django_authenticate(username=username, password=password) # authenticate后的user才是能够使用的user
        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "username and password does not match",
            }, status=400)

        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(instance=user).data,
        })

    @action(methods = ['POST'], detail = False)
    def signup(self,request):
        serializer = SignupSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input",
                "errors": serializer.errors,
            }, status=400)

        user = serializer.save()
        django_login(request, user)
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
        },status  =201)