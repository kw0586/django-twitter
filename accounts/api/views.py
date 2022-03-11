from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from accounts.api.serializers import UserSerializer

#提供一个user的api，能够读取user的具体内容
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined') #从哪去获取数据
    serializer_class = UserSerializer #数据怎么变成json
    permission_classes = [permissions.IsAuthenticated] #
