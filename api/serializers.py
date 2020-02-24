import json

from django_redis import get_redis_connection
from rest_framework import serializers

from common.models import District, Agent, Estate, HouseType, Tag, HouseInfo, HousePhoto


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
        exclude = ('estates', )


class AgentDetailSerializer(serializers.ModelSerializer):
    """经理人详情序列化器"""
    estates = serializers.SerializerMethodField()

    @staticmethod
    def get_estates(agent):
        queryset = agent.estates.all()[:5]
        return EstateSimpleSerializer(queryset, many=True).data

    class Meta:
        model = Agent
        fields = '__all__'


class EstateSimpleSerializer(serializers.ModelSerializer):
    """楼盘简单序列化器"""

    class Meta:
        model = Estate
        fields = ('estateid', 'name')


class EstateCreateSerializer(serializers.ModelSerializer):
    """创建楼盘序列化器"""

    class Meta:
        model = Estate
        fields = '__all__'


class EstateDetailSerializer(serializers.ModelSerializer):
    """楼盘详情序列化器"""
    district = serializers.SerializerMethodField()

    @staticmethod
    def get_district(estate):
        return DistrictSimpleSerializer(estate.district).data

    class Meta:
        model = Estate
        fields = '__all__'


class HouseTypeSerializer(serializers.ModelSerializer):
    """户型序列化器"""

    class Meta:
        model = HouseType
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """房源标签序列化器"""

    class Meta:
        model = Tag
        fields = '__all__'


class HouseInfoSimpleSerializer(serializers.ModelSerializer):
    """房源基本信息序列化器"""
    mainphoto = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    @staticmethod
    def get_mainphoto(houseinfo):
        return '/media/images/' + houseinfo.mainphoto

    @staticmethod
    def get_district(houseinfo):
        return DistrictSimpleSerializer(houseinfo.district_level3).data

    @staticmethod
    def get_type(houseinfo):
        return HouseTypeSerializer(houseinfo.type).data

    @staticmethod
    def get_tags(houseinfo):
        return TagSerializer(houseinfo.tags, many=True).data

    class Meta:
        model = HouseInfo
        fields = ('houseid', 'title', 'area', 'floor', 'totalfloor', 'price', 'priceunit',
                  'mainphoto', 'street', 'district', 'type', 'tags')


class HouseInfoCreateSerializer(serializers.ModelSerializer):
    """创建房源序列化器"""

    class Meta:
        model = HouseInfo
        fields = '__all__'


class HouseInfoDetailSerializer(serializers.ModelSerializer):
    """房源详情序列化器"""
    district = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    estate = serializers.SerializerMethodField()
    agent = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()

    @staticmethod
    def get_district(houseinfo):
        return DistrictSimpleSerializer(houseinfo.district_level3).data

    @staticmethod
    def get_type(houseinfo):
        return HouseTypeSerializer(houseinfo.type).data

    @staticmethod
    def get_tags(houseinfo):
        return TagSerializer(houseinfo.tags, many=True).data

    @staticmethod
    def get_estate(houseinfo):
        return EstateSimpleSerializer(houseinfo.estate).data

    @staticmethod
    def get_agent(houseinfo):
        return AgentSimpleSerializer(houseinfo.agent).data

    @staticmethod
    def get_photos(houseinfo):
        queryset = HousePhoto.objects.filter(house=houseinfo)
        return HousePhotoSerializer(queryset, many=True).data

    class Meta:
        model = HouseInfo
        exclude = ('district_level2', 'district_level3', 'user')


class HousePhotoSerializer(serializers.ModelSerializer):
    """房源照片序列化器"""

    class Meta:
        model = HousePhoto
        fields = ('photoid', 'path')
