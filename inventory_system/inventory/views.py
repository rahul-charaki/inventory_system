# inventory/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import Item
from .serializers import ItemSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    serializer = ItemSerializer(data=request.data)
    if Item.objects.filter(name=request.data['name']).exists():
        logger.error(f"Item '{request.data['name']}' already exists.")
        return Response({"error": "Item already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    if serializer.is_valid():
        serializer.save()
        logger.info(f"Item '{serializer.data['name']}' created.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_item(request, item_id):
    cache_key = f"item_{item_id}"
    cached_item = cache.get(cache_key)
    
    if cached_item:
        logger.info(f"Item '{item_id}' fetched from cache.")
        return Response(cached_item)

    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        logger.error(f"Item '{item_id}' not found.")
        return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(item)
    cache.set(cache_key, serializer.data, timeout=60 * 15)  # Cache for 15 minutes
    logger.info(f"Item '{item_id}' fetched from database and cached.")
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        logger.error(f"Item '{item_id}' not found.")
        return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete(f"item_{item_id}")  # Invalidate cache
        logger.info(f"Item '{item_id}' updated.")
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        item.delete()
        cache.delete(f"item_{item_id}")  # Invalidate cache
        logger.info(f"Item '{item_id}' deleted.")
        return Response({"success": "Item deleted."}, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        logger.error(f"Item '{item_id}' not found.")
        return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
