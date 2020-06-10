from rest_framework import serializers
from .models import BusinessCategory, ProductCategory, Location,Order, TypeOfGoodsSold,OtherProductProperty,Message, Business, Product, ProductImages


class ProductCategorySerializer(serializers.ModelSerializer):
    selected = serializers.BooleanField(required=False,default=True,read_only=True)
    class Meta:
        model = ProductCategory
        fields = '__all__'


class BusinessCategorySerializer(serializers.ModelSerializer):
    selected = serializers.BooleanField(required=False,default=True,read_only=True)
    class Meta:
        model = BusinessCategory
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','country', 'city',]
       

class BusinessSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location_detail= serializers.SerializerMethodField(read_only=True)
    category_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Business
        fields = ['id','business_logo','location_detail','owner','name','description','email','address','location','phone','location','contact_persona_name','contact_persona_phone','date_created','category','category_detail']
        extra_kwargs={'date_created':{'read_only':True}}

    def get_location_detail(self,business):
        detail = business.location
        data = {'country':detail.country,'city':detail.city,'id':detail.id}
        return data

    def get_category_detail(self,business):
        detail = business.category
        data = {'name':detail.name,'description':detail.description,'id':detail.id}
        return data


class ProductImageSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(source='product.id',required=False)

    class Meta:
        model = ProductImages
        fields = '__all__'
        
    def create(self, validate_data):
        print(validate_data)
        product = validate_data.pop('product')
        old_cover = ProductImages.objects.filter(product_id=product['id'], is_cover=True)
        if old_cover is not None:
            old_cover.delete()
        image = ProductImages(product_id=product['id'],image=validate_data['image'],is_cover=True)
        image.save()

        return image


class OtherProductPropertySerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(source='product.id',required=False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = OtherProductProperty
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    other_properties = OtherProductPropertySerializer(many=True, required= False)
    product_images = ProductImageSerializer(required=False, many=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['product_images']


    def create(self, validate_data):
        other_properties = validate_data.pop('other_properties')
        
        product = Product.objects.create(**validate_data)
        product.save()
 
        """"put all otherproperties of the product"""
        for prop in other_properties:
            proparty = OtherProductProperty.objects.create(product=product,
            property_name = prop['property_name'],
            description = prop['description']
            )
            proparty.save()

        """ handling type of goods sold by a business"""
        category_of_product_sold = TypeOfGoodsSold.objects.create(product_category=product.product_category, business=product.business)
        category_of_product_sold.save()

        return product

    def update(self,instance,validate_data):
        other_properties = []
        if 'other_properties' in validate_data:
            other_properties = validate_data.pop('other_properties')

        product = super().update(instance,validate_data)
        OtherProductProperty.objects.filter(product=product).delete()

        for other_property in other_properties:
            other_p = OtherProductProperty.objects.create(
                    product = product, 
                    property_name=other_property['property_name'],
                    description=other_property['description'])
            other_p.save()
        return product


class OwnProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

class OrdersSerializer(serializers.ModelSerializer):

    product_detail = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
    
    def get_product_detail(self,order):
        detail = order.product
        return {'name':detail.name,'id':detail.id}

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
