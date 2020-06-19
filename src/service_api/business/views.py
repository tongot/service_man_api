from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Max

import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Country,BusinessProfile, BusinessReviews, BusinessComment, BusinessCommentReply, ProductCategory,BusinessCategory, Location, Business, Product,ProductImages,Order,Message
from .serializers import CountrySerializer,BusinessProfileSerializer, BusinessCommentSerializer, BusinessReviewSerializer,BusinessCommentReplySerializer,BusinessCategorySerializer,ProductImageSerializer,OwnProductSerializer,OrdersSerializer,MessageSerializer, ProductCategorySerializer, LocationSerializer, ProductSerializer, BusinessSerializer
from .permissions import IsTheirOrder, IsOwnerOrReadOnly

class OwnBusinessView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,format=None):
        queryset= Business.objects.filter(owner=request.user.id)
        serializer = BusinessSerializer(queryset,many=True, context={'request':request})
        return Response(serializer.data)

class BusinessProfileView(viewsets.ModelViewSet):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer

class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class OwnBusinessOrderView(viewsets.ViewSet):
    """Order processing for business owners"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def isOwnerOfOder(self,req):
        business_id = req.query_params.get('businessId')
        if business_id != None:
            business = Business.objects.filter(owner_id=req.user.id, id=business_id).first()
            if business!=None:
                return True
            return False
        return False

    def get(self,request,format=None):
        """get order for a particular business"""
        if self.isOwnerOfOder(request):
            business_id = request.query_params.get('businessId')
            queryset= Order.objects.filter(business_id=business_id)
            serializer = OrdersSerializer(queryset,many=True, context={'request':request})
            return Response(serializer.data)
        return Response({'error':'Not authorized'},status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False,methods=['get'])
    def orderViewed(self,request,format=None):
        """mark orders as viewed"""
        if self.isOwnerOfOder(request):
            orderId = request.query_params.get('orderId')
            if(orderId != None):
                order = get_object_or_404(Order,pk = orderId)
                if order.business.id == int(request.query_params.get('businessId')):
                    order.viewed = True
                    order.save()
                    return Response({'updated':'message openned'},status.HTTP_202_ACCEPTED)
                return Response({'error':'business order mismatch'},status.HTTP_400_BAD_REQUEST)
            return Response({'error':'get order failed'},status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Not authorized'},status.HTTP_400_BAD_REQUEST)
        

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
    serializer_class = BusinessSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['location__city','name']

    def get_queryset(self):
        categoryParams = self.request.query_params.get('businessCategory')
        category=[]

        if categoryParams !=None:
            category = categoryParams.split(',')
            if(all(i.isdigit() for i in category))==False:
                category=[]
            if len(category)>0:
                return Business.objects.filter(category__in=category)
        return Business.objects.all()


class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['name','description','business__name','product_category__name']

    def filterPrice(self,query,maxPrice,minPrice):
        try:
            if maxPrice!= None and minPrice!= None and minPrice!='' and maxPrice!='':
                return query.filter(price__gte=minPrice,price__lte=maxPrice)
            elif minPrice!= None and minPrice!='':
                return query.filter(price__gte=minPrice)
            elif maxPrice!= None  and maxPrice!='':
                return query.filter(price__lte=maxPrice)
            else:
                return query
        except:
            return query

    def get_queryset(self):
        
        categories= []
        businesses=[]
        returnQuery={}

        paramsCategory = self.request.query_params.get('productCategory')
        paramsBusiness = self.request.query_params.get('sellers')
        maxPrice = self.request.query_params.get('maxPrice')
        minPrice = self.request.query_params.get('minPrice')
        businesses = []
        categories = []

        if paramsCategory!=None:
            categories= paramsCategory.split(',')
            if all(i.isdigit() for i in categories)==False:
                categories = []

        if paramsBusiness!=None:
            businesses= paramsBusiness.split(',')
            if all(i.isdigit() for i in businesses)==False:
                businesses = []


        if len(businesses)>0:
            businessResult = Product.objects.filter(business_id__in=businesses)
            returnQuery = businessResult
            if len(categories)>0:
                if returnQuery != None:
                    categoryResults=returnQuery.filter(product_category__in=categories)
                    returnQuery=categoryResults
                    return self.filterPrice(returnQuery,maxPrice,minPrice)
                return self.filterPrice(returnQuery,maxPrice,minPrice)
            return self.filterPrice(returnQuery,maxPrice,minPrice)
        elif len(categories)>0:
            categoryResults = Product.objects.filter(product_category__in=categories)
            return  self.filterPrice(categoryResults,maxPrice,minPrice)
        return self.filterPrice(Product.objects.all(),maxPrice,minPrice)

    @action(detail=False, methods=['get'])
    def getHomeProducts(self,request):
        pagestring = request.query_params.get('page')
        page_lengthstring = request.query_params.get('pageLength')
        category = request.query_params.get('category')
        if pagestring != None and page_lengthstring != None and category != None:
            if pagestring.isdigit() and page_lengthstring.isdigit() and category.isdigit():
                page = int(pagestring)-1
                page_length = int(page_lengthstring)
                products_count =  Product.objects.filter(product_category=category).count()
                product= Product.objects.filter(product_category=category)[page*page_length:page*page_length+page_length]
                serializer = ProductSerializer(product,many=True, context={'request':request})
                return Response({'count':products_count,'items':serializer.data})
            return Response({'message':'parameter shot'})
        return Response({'message':'parameter shot'})

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

class BusinessRatingView(viewsets.ModelViewSet):
    """Business comment and ratings """

    queryset = BusinessReviews.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    serializer_class = BusinessReviewSerializer

class BusinessCommentView(viewsets.ModelViewSet):
    """Business comment """

    queryset = BusinessComment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    serializer_class = BusinessCommentSerializer


class BusinessCommentReplyView(viewsets.ModelViewSet):
    """Business comment and ratings """

    queryset = BusinessCommentReply.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    serializer_class = BusinessCommentReplySerializer



