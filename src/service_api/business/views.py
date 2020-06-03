from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from .models import ProductCategory,BusinessCategory, Location, Business, Product,ProductImages,Order,Message
from .serializers import BusinessCategorySerializer,ProductImageSerializer,OwnProductSerializer,OrdersSerializer,MessageSerializer, ProductCategorySerializer, LocationSerializer, ProductSerializer, BusinessSerializer
from .permissions import IsTheirOrder

class OwnBusinessView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,format=None):
        queryset= Business.objects.filter(owner=request.user.id)
        serializer = BusinessSerializer(queryset,many=True, context={'request':request})
        return Response(serializer.data)


class OwnBusinessOrderView(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None):
        business_id = request.query_params.get('businessId')
        if business_id != None:
            business = Business.objects.filter(owner_id=request.user.id, id=business_id).first()
            if business!=None:
                queryset= Order.objects.filter(business_id=business_id)
                serializer = OrdersSerializer(queryset,many=True, context={'request':request})
                return Response(serializer.data)
            return Response({'error':'Not authorized'},status.HTTP_400_BAD_REQUEST) 
        return Response({'error':'orders not found'},status.HTTP_400_BAD_REQUEST)
        

    def create(self,request):
        pass

class ProductImagesViewSet(viewsets.ViewSet):
    """upload multiple images"""
    def create(self,request):
        images = request.data.pop('images')
        product_id = request.data['product']
        product = get_object_or_404(Product, pk=product_id)
        for image in images:
            product_pic = ProductImages.objects.create(product=product, image=image)
            product_pic.save()
        return Response(request.data,status.HTTP_201_CREATED)

    def destroy(self,request,pk=None):
        image = get_object_or_404(ProductImages,pk=pk)
        image.delete()
        return Response({'message':'deleted'})


class LocationView(viewsets.ModelViewSet):
    queryset= Location.objects.all()
    serializer_class = LocationSerializer


class ProductCategoryView(viewsets.ModelViewSet):
    queryset= ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class BusinessCategoryView(viewsets.ModelViewSet):
    queryset = BusinessCategory.objects.all()
    serializer_class = BusinessCategorySerializer
class BusinessView(viewsets.ModelViewSet):
    queryset= Business.objects.all()
    serializer_class = BusinessSerializer


class ProductView(viewsets.ModelViewSet):
    queryset= Product.objects.all()
    serializer_class = ProductSerializer


class ProductCoverView(viewsets.ModelViewSet): 
    queryset= ProductImages.objects.all()
    serializer_class = ProductImageSerializer
    

class OrderView(viewsets.ModelViewSet): 
    queryset= Order.objects.all()
    serializer_class = OrdersSerializer    


class MessageView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
   

class OwnProductViewSet(viewsets.ViewSet):
    """get own business product"""
    def get(self,request,format=None):
        if 'businessId' in request.query_params:
            businessId = request.query_params['businessId']
            if businessId is not None:
                queryset = Product.objects.filter(business_id= businessId)
                serializer = ProductSerializer(queryset,many=True, context={'request':request})
                return Response(serializer.data)
            return Response({'error':'product not found'},status.HTTP_404_BAD_REQUEST)
        return Response({'error':'product not found'},status.HTTP_400_BAD_REQUEST)  
        
    def create(self,request):
        pass