import json

from django.core.cache import caches
from django.db.models import Q
from django.db.transaction import atomic
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.models import *
from common.utils import to_md5_hex
from common.validators import USERNAME_PATTERN, TEL_PATTERN, EMAIL_PATTERN


class DistrictSimpleSerializer(serializers.ModelSerializer):
    """地区简单序列化器"""

    class Meta:
        model = District
        fields = ('distid', 'name')


class DistrictDetailSerializer(serializers.ModelSerializer):
    """地区详情序列化器"""
    cities = serializers.SerializerMethodField()

    @staticmethod
    def get_cities(district):
        redis_cli = get_redis_connection()
        data = redis_cli.get(f'tiaotiaoche:district:{district.distid}:cities')
        if data:
            data = json.loads(data)
        else:
            queryset = District.objects.filter(parent=district).only('name')
            data = DistrictSimpleSerializer(queryset, many=True).data
            redis_cli.set(f'tiaotiaoche:district:{district.distid}:cities', json.dumps(data), ex=900)
        return data

    class Meta:
        model = District
        exclude = ('parent', )


class AgentSimpleSerializer(serializers.ModelSerializer):
    """经理人简单序列化器"""

    class Meta:
        model = Agent
        fields = ('agentid', 'name', 'tel', 'servstar')


class AgentCreateSerializer(serializers.ModelSerializer):
    """创建经理人序列化器"""

    class Meta:
        model = Agent
        exclude = ('car_shops', )


class AgentDetailSerializer(serializers.ModelSerializer):
    """经理人详情序列化器"""
    car_shops = serializers.SerializerMethodField()

    @staticmethod
    def get_car_shops(agent):
        queryset = agent.car_shops.all()[:5]
        return CarShopSimpleSerializer(queryset, many=True).data

    class Meta:
        model = Agent
        fields = '__all__'


class CarShopSimpleSerializer(serializers.ModelSerializer):
    """店铺简单序列化器"""

    class Meta:
        model = CarShop
        fields = ('car_shopid', 'name')


class CarShopCreateSerializer(serializers.ModelSerializer):
    """创建店铺序列化器"""

    class Meta:
        model = CarShop
        fields = '__all__'


class CarShopDetailSerializer(serializers.ModelSerializer):
    """店铺详情序列化器"""
    district = serializers.SerializerMethodField()

    @staticmethod
    def get_district(car_shop):
        return DistrictSimpleSerializer(car_shop.district).data

    class Meta:
        model = CarShop
        fields = '__all__'


class CarTypeSerializer(serializers.ModelSerializer):
    """车型序列化器"""

    class Meta:
        model = CarType
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """车源标签序列化器"""

    class Meta:
        model = Tag
        fields = '__all__'


class CarInfoSimpleSerializer(serializers.ModelSerializer):
    """车源基本信息序列化器"""
    mainphoto = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    @staticmethod
    def get_mainphoto(carinfo):
        return '/media/images/' + carinfo.mainphoto

    @staticmethod
    def get_district(carinfo):
        return DistrictSimpleSerializer(carinfo.district_level3).data

    @staticmethod
    def get_type(carinfo):
        return CarTypeSerializer(carinfo.type).data

    @staticmethod
    def get_tags(carinfo):
        return TagSerializer(carinfo.tags, many=True).data

    class Meta:
        model = CarInfo
        fields = ('carid', 'title', 'area', 'floor', 'totalfloor', 'price', 'priceunit',
                  'mainphoto', 'street', 'district', 'type', 'tags')


class CarInfoCreateSerializer(serializers.ModelSerializer):
    """创建车源序列化器"""

    class Meta:
        model = CarInfo
        fields = '__all__'


class CarInfoDetailSerializer(serializers.ModelSerializer):
    """车源详情序列化器"""
    district = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    car_shop = serializers.SerializerMethodField()
    agent = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()

    @staticmethod
    def get_district(carinfo):
        return DistrictSimpleSerializer(carinfo.district_level3).data

    @staticmethod
    def get_type(carinfo):
        return CarTypeSerializer(carinfo.type).data

    @staticmethod
    def get_tags(carinfo):
        return TagSerializer(carinfo.tags, many=True).data

    @staticmethod
    def get_car_shop(carinfo):
        return CarShopSimpleSerializer(carinfo.car_shop).data

    @staticmethod
    def get_agent(carinfo):
        return AgentSimpleSerializer(carinfo.agent).data

    @staticmethod
    def get_photos(carinfo):
        queryset = CarPhoto.objects.filter(car=carinfo)
        return CarPhotoSerializer(queryset, many=True).data

    class Meta:
        model = CarInfo
        exclude = ('district_level2', 'district_level3', 'user')


class CarPhotoSerializer(serializers.ModelSerializer):
    """车源照片序列化器"""

    class Meta:
        model = CarPhoto
        fields = ('photoid', 'path')


class UserSimpleSerializer(serializers.ModelSerializer):
    """用户简单序列化器"""

    class Meta:
        model = User
        exclude = ('password', 'roles')


class UserUpdateSerializer(serializers.ModelSerializer):
    """更新用户序列化器"""

    class Meta:
        model = User
        fields = ('realname', 'tel', 'email', 'sex')


class UserCreateSerializer(serializers.ModelSerializer):
    """创建用户序列化器"""
    username = serializers.RegexField(regex=USERNAME_PATTERN)
    password = serializers.CharField(min_length=6)
    realname = serializers.RegexField(regex=r'[\u4e00-\u9fa5]{2,20}')
    tel = serializers.RegexField(regex=TEL_PATTERN)
    email = serializers.RegexField(regex=EMAIL_PATTERN)
    code = serializers.CharField(write_only=True, min_length=6, max_length=6)

    def validate(self, attrs):
        code_from_user = attrs['code']
        code_from_redis = caches['default'].get(f'{attrs["tel"]}:valid')
        if code_from_redis != code_from_user:
            raise ValidationError('请输入有效的手机验证码', 'invalid')
        user = User.objects.filter(Q(username=attrs['username']) |
                                   Q(tel=attrs['tel']) |
                                   Q(email=attrs['email']))
        if user:
            raise ValidationError('用户名、手机或邮箱已被注册', 'invalid')
        return attrs

    def create(self, validated_data):
        del validated_data['code']
        caches['default'].delete(f'{validated_data["tel"]}:valid')
        validated_data['password'] = to_md5_hex(validated_data['password'])
        with atomic():
            user = User.objects.create(**validated_data)
            role = Role.objects.get(roleid=1)
            UserRole.objects.create(user=user, role=role)
        return user

    class Meta:
        model = User
        exclude = ('userid', 'regdate', 'point', 'lastvisit', 'roles')


class RoleSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('roleid', )
