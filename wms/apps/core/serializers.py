from rest_framework import serializers
from .models import User, Warehouse, Supplier, Customer, Product, ActivityLog, FileAttachment
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    # this will be used for API resource (serialisation) and create a new object (deserialisation) 
    # write_only is true such that it will not be returned in the response
    password = serializers.CharField(write_only=True)
    warehouse_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'warehouse_id']
    
    def validate_warehouse_id(self, value):
        try:
            warehouse = Warehouse.objects.get(id=value, is_active=True)
            return value
        except Warehouse.DoesNotExist:
            raise serializers.ValidationError("Invalid warehouse ID")
    
    def create(self, validated_data):
        warehouse_id = validated_data.pop('warehouse_id')
        password = validated_data.pop('password')
        validated_data['is_staff'] = True
        validated_data['role'] = 'operator' 
        
        # Create user
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        
        # Assign warehouse
        warehouse = Warehouse.objects.get(id=warehouse_id)
        user.warehouse = warehouse
        user.save()
        
        return user

class UserSerializer(serializers.ModelSerializer):
    # this will be used for API resource (serialisation) and create a new object (deserialisation) 
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    warehouse_code = serializers.CharField(source='warehouse.code', read_only=True)
    class Meta:
        model = User
        # this will be similar to what received from the front end and what is returned except overwritten by extra_kwargs
        fields = ['id', 'username', 'role', 'password', 'warehouse_name', 'warehouse_code']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    # def create(self, validated_data):
    #     # validated will be dictionary, hence thats why we have to destructure it for create_user
    #     password = validated_data.pop('password')
    #     # for MVP, all user is a staff
    #     # this is kinda like Laravel mutator where you want to add stuff before adding to database
    #     # alternative method is putting it at the save method in model
    #     validated_data['is_staff'] = True
    #     user = User.objects.create_user(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user
    
class LoginSerializer(serializers.Serializer):
    # this will be used to validate data (similar to laravel validator) since we are using Serializer instead of ModelSerializer

    # has to explicitly declare the field to be extracted
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
               raise serializers.ValidationError('Username or password inputted is incorrect')
            if not user.is_active:
                raise serializers.ValidationError('User account is not active.')
            data['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
        return data

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"
        # so that the timestamps are not shown in the API response
        exclude = ['created_at', 'updated_at']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"
        # so that the timestamps are not shown in the API response
        exclude = ['created_at', 'updated_at']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        # so that the timestamps are not shown in the API response
        exclude = ['created_at', 'updated_at']

class ActivityLogSerializer(serializers.ModelSerializer):
    # user here refers to the user variable in the model
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ActivityLog
        fields = '__all__'
        exclude = ['created_at']

class FileAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = FileAttachment
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    total_stock = serializers.SerializerMethodField()
    available_stock = serializers.SerializerMethodField()
    is_low_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_at', 'updated_at']
    
    def get_total_stock(self, obj):
        return obj.get_total_quantity_across_warehouses()
    
    def get_available_stock(self, obj):
        return obj.get_available_quantity_across_warehouses()
    
    def get_is_low_stock(self, obj):
        total_stock = self.get_total_stock(obj)
        return total_stock <= obj.low_stock_threshold




             