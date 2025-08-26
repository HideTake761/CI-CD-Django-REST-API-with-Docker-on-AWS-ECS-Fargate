from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filterset_fields = ['product']
    # REST APIで特定アイテムのGET・変更・削除を商品名で行えるようにするため
    filter_backends = [DjangoFilterBackend]
    # Django REST Frameworkでfilter_fieldsを使う場合、DjangoFilterBackendが
    # フィルタリングをサポートするために設定されている必要がある。
