from datetime import datetime
import json

from django.core.mail import BadHeaderError, send_mail

from rest_framework import serializers
from .models import BusinessProfile, BusinessComment, BusinessProfile, Country, BusinessDirectors, BusinessContactPerson, BusinessReviews, BusinessCommentReply, BusinessCategory, ProductCategory, Location, Order, TypeOfGoodsSold, OtherProductProperty, Message, Business, Product, ProductImages


class ProductCategorySerializer(serializers.ModelSerializer):
    selected = serializers.BooleanField(
        required=False, default=True, read_only=True)

    class Meta:
        model = ProductCategory
        fields = '__all__'


class BusinessProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = '__all__'


class BusinessCategorySerializer(serializers.ModelSerializer):
    selected = serializers.BooleanField(
        required=False, default=True, read_only=True)

    class Meta:
        model = BusinessCategory
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = '__all__'


class BusinessContactPersonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = BusinessContactPerson
        fields = ['id', 'first_name', 'last_name', 'phone']


class BusinessDirectorsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = BusinessDirectors
        fields = ['id', 'first_name', 'last_name',
                  'about_director', 'social_links']


class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = '__all__'


class BusinessSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location_detail = serializers.SerializerMethodField(read_only=True)
    category_detail = serializers.SerializerMethodField(read_only=True)
    contact_person = BusinessContactPersonSerializer(many=True, required=False)
    directors = BusinessDirectorsSerializer(many=True, required=False)
    profile = serializers.SerializerMethodField(read_only=True)

    # dammies to represent json in text form from form data
    directorJ = serializers.CharField(required=False)
    contactJ = serializers.CharField(required=False)

    class Meta:
        model = Business
        fields = ['directorJ', 'contactJ', 'id', 'articles_number', 'business_logo', 'owner', 'name', 'description', 'email', 'address', 'location',
                  'phone', 'location', 'date_created', 'category', 'category_detail', 'location_detail', 'contact_person', 'directors', 'profile']
        extra_kwargs = {'date_created': {'read_only': True}}

    def get_profile(self, business):
        detail = BusinessProfile.objects.filter(business=business).first()
        data = {}
        if detail != None:
            data = {'id': detail.id, 'about': detail.about,
                    'main_color': detail.main_color}
        return data

    def get_location_detail(self, business):
        detail = business.location
        data = {'country': detail.country.name,
                'city': detail.city, 'id': detail.id}
        return data

    def get_category_detail(self, business):
        detail = business.category
        data = {'name': detail.name,
                'description': detail.description, 'id': detail.id}
        return data

    def create(self, validated_data):
        print(validated_data)
        contact_person = None
        directors = None

        hasDammyContact = validated_data.get('contactJ')
        hasDammyDirector = validated_data.get('directorJ')
        if hasDammyContact != None:
            validated_data.pop('contactJ')
            contact_person = json.loads(hasDammyContact)
        if hasDammyDirector != None:
            validated_data.pop('directorJ')
            directors = json.loads(hasDammyDirector)
        if validated_data.get('contact_person') != None:
            contact_person = validated_data.pop('contact_person')
        if validated_data.get('directors') != None:
            directors = validated_data.pop('directors')

        if contact_person == None or directors == None:
            raise serializers.ValidationError(
                "Needs at least 1 director and 1 contact person")

        business = Business.objects.create(**validated_data)
        business.save()
        for person in contact_person:
            contact = BusinessContactPerson.objects.create(
                first_name=person['first_name'],
                last_name=person['last_name'],
                phone=person['phone'],
                business=business)
            contact.save()
        for director in directors:
            direct = BusinessDirectors.objects.create(
                first_name=director['first_name'],
                last_name=director['last_name'],
                about_director=director['about_director'],
                social_links=director.get('social_links'),
                business=business)
            direct.save()
        return business

    def update(self, instance, validated_data):
        contact_person = None
        directors = None

        hasDammyContact = validated_data.get('contactJ')
        hasDammyDirector = validated_data.get('directorJ')
        if hasDammyContact != None:
            validated_data.pop('contactJ')
            contact_person = json.loads(hasDammyContact)
        if hasDammyDirector != None:
            validated_data.pop('directorJ')
            directors = json.loads(hasDammyDirector)
        if validated_data.get('contact_person') != None:
            contact_person = validated_data.pop('contact_person')
        if validated_data.get('directors') != None:
            directors = validated_data.pop('directors')

        if contact_person == None or directors == None:
            raise serializers.ValidationError(
                "Needs at least 1 director and 1 contact person")

        business = super().update(instance, validated_data)

        for person in contact_person:
            if person['id'] == 0:
                new_contact = BusinessContactPerson.objects.create(
                    first_name=person['first_name'],
                    last_name=person['last_name'],
                    phone=person['phone'],
                    business=business)
                new_contact.save()
            elif person['id'] < 0:
                p = BusinessContactPerson.objects.get(pk=(person['id']*-1))
                p.delete()
            elif person['id'] > 0:
                BusinessContactPerson.objects.filter(pk=person['id']).update(
                    first_name=person['first_name'],
                    last_name=person['last_name'],
                    phone=person['phone'],)

            else:
                pass

        for person in directors:
            if person['id'] == 0:
                new_director = BusinessDirectors.objects.create(
                    first_name=person['first_name'],
                    last_name=person['last_name'],
                    about_director=person['about_director'],
                    social_links=person.get('social_links'),
                    business=business)
                new_director.save()
            elif person['id'] < 0:
                p = BusinessDirectors.objects.get(pk=person['id']*-1)
                p.delete()
            elif person['id'] > 0:
                BusinessDirectors.objects.filter(pk=person['id']).update(
                    first_name=person['first_name'],
                    last_name=person['last_name'],
                    about_director=person['about_director'],
                    social_links=person.get('social_links'),
                )
            else:
                pass

        return business


class ProductImageSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(source='product.id', required=False)

    class Meta:
        model = ProductImages
        fields = '__all__'

    def create(self, validate_data):
        print(validate_data)
        product = validate_data.pop('product')
        old_cover = ProductImages.objects.filter(
            product_id=product['id'], is_cover=True)
        if old_cover is not None:
            old_cover.delete()
        image = ProductImages(
            product_id=product['id'], image=validate_data['image'], is_cover=True)
        image.save()

        return image


class OtherProductPropertySerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(source='product.id', required=False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = OtherProductProperty
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    other_properties = OtherProductPropertySerializer(
        many=True, required=False)
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
                                                           property_name=prop['property_name'],
                                                           description=prop['description']
                                                           )
            proparty.save()

        """ handling type of goods sold by a business"""
        category_of_product_sold = TypeOfGoodsSold.objects.create(
            product_category=product.product_category, business=product.business)
        category_of_product_sold.save()

        return product

    def update(self, instance, validate_data):
        other_properties = []
        if 'other_properties' in validate_data:
            other_properties = validate_data.pop('other_properties')

        product = super().update(instance, validate_data)
        OtherProductProperty.objects.filter(product=product).delete()

        for other_property in other_properties:
            other_p = OtherProductProperty.objects.create(
                product=product,
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

    def get_product_detail(self, order):
        try:
            detail = order.product
            return {'name': detail.name, 'id': detail.id}
        except:
            return {}

    def update(self, validate_data):
        pass

    def create(self, validate_data):
        order = Order.objects.create(**validate_data)
        try:
            send_mail(
                'New order on tshwaragano, order number {}'.format(
                    order.id),
                'New order from {}'.format(validate_data.get('email_address')),
                'Tswaragano@groovetek.co.bw',
                [order.business.email]
            )
        except BadHeaderError:
            raise serializers.ValidationError('Invalid header found')
        return order


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        product_id = validated_data.get('product')
        product = Product.objects.filter(id=product_id).first()
        if product:
            try:
                send_mail(
                    '{}product request message (product id {})'.format(
                        product.name, product.id),
                    '{}'.format(validated_data.get('text')),
                    'Tswaragano@groovetek.co.bw',
                    [product.business.email]
                )
            except BadHeaderError:
                raise serializers.ValidationError('Invalid header found')

            Message.objects.create(**validated_data)
        else:
            raise serializers.ValidationError('Product not found')
        return validated_data


class BusinessReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessReviews
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data['business'].id)
        rated_already = BusinessReviews.objects.filter(
            user_id=validated_data['user'].id, business_id=validated_data['business'].id).first()
        print(rated_already)
        if rated_already != None:
            rated_already.comment = validated_data['comment']
            rated_already.stars = validated_data['stars']
            rated_already.date_posted = datetime.now()
            rated_already.save()
            return rated_already
        rating = BusinessReviews.objects.create(**validated_data)
        return rating


class BusinessCommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCommentReply
        fields = '__all__'

    def create(self, validated_data):
        bussiness_original_comment = BusinessComment.objects.get(
            pk=validated_data['business_comment'].id)
        if bussiness_original_comment.business.owner.id == validated_data['user'].id:
            reply = BusinessCommentReply.objects.create(
                comment=validated_data['comment'],
                business_comment=validated_data['business_comment'],
                user=validated_data['user'],
                business=bussiness_original_comment.business
            )
            return reply
        reply = BusinessCommentReply.objects.create(**validated_data)
        return reply


class BusinessCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)
    id = serializers.IntegerField(required=False)
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BusinessComment
        fields = ['id', 'comment', 'date_posted',
                  'username', 'user', 'business', 'replies']

    def get_username(self, comment):
        return comment.user.name+" "+comment.user.surname

    def get_replies(self, comment):
        result = []
        replies = BusinessCommentReply.objects.filter(
            business_comment=comment.id)
        if replies != None:
            for reply in replies:
                result.append({'id': reply.id, 'reply': reply.comment, 'user_id': reply.user.id,
                               'user_email': reply.user.email, 'username': reply.user.name+" "+reply.user.surname,
                               'date_posted': reply.date_posted
                               })
            return result
        return result
