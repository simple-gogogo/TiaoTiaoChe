import json

from django_redis import get_redis_connection
from rest_framework import serializers

from common.models import District, Agent, car_shop, carType, Tag, carInfo, carPhoto


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
        return car_shopSimpleSerializer(queryset, many=True).data

    class Meta:
        model = Agent
        fields = '__all__'


class car_shopSimpleSerializer(serializers.ModelSerializer):
    """楼盘简单序列化器"""

    class Meta:
        model = car_shop
        fields = ('car_shopid', 'name')


class car_shopCreateSerializer(serializers.ModelSerializer):
    """创建楼盘序列化器"""

    class Meta:
        model = car_shop
        fields = '__all__'


class car_shopDetailSerializer(serializers.ModelSerializer):
    """楼盘详情序列化器"""
    district = serializers.SerializerMethodField()

    @staticmethod
    def get_district(car_shop):
        return DistrictSimpleSerializer(car_shop.district).data

    class Meta:
        model = car_shop
        fields = '__all__'


class carTypeSerializer(serializers.ModelSerializer):
    """户型序列化器"""

    class Meta:
        model = carType
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """房源标签序列化器"""

    class Meta:
        model = Tag
        fields = '__all__'


class carInfoSimpleSerializer(serializers.ModelSerializer):
    """房源基本信息序列化器"""
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
        return carTypeSerializer(carinfo.type).data

    @staticmethod
    def get_tags(carinfo):
        return TagSerializer(carinfo.tags, many=True).data

    class Meta:
        model = carInfo
        fields = ('carid', 'title', 'area', 'floor', 'totalfloor', 'price', 'priceunit',
                  'mainphoto', 'street', 'district', 'type', 'tags')


class carInfoCreateSerializer(serializers.ModelSerializer):
    """创建房源序列化器"""

    class Meta:
        model = carInfo
        fields = '__all__'


class carInfoDetailSerializer(serializers.ModelSerializer):
    """房源详情序列化器"""
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
        return carTypeSerializer(carinfo.type).data

    @staticmethod
    def get_tags(carinfo):
        return TagSerializer(carinfo.tags, many=True).data

    @staticmethod
    def get_car_shop(carinfo):
        return car_shopSimpleSerializer(carinfo.car_shop).data

    @staticmethod
    def get_agent(carinfo):
        return AgentSimpleSerializer(carinfo.agent).data

    @staticmethod
    def get_photos(carinfo):
        queryset = carPhoto.objects.filter(car=carinfo)
        return carPhotoSerializer(queryset, many=True).data

    class Meta:
        model = carInfo
        exclude = ('district_level2', 'district_level3', 'user')


class carPhotoSerializer(serializers.ModelSerializer):
    """房源照片序列化器"""

    class Meta:
        model = carPhoto
        fields = ('photoid', 'path')
