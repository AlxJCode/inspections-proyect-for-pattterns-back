from rest_framework import serializers

from applications.users.models import Area, Company, SystemUser, CompanyDoc

# Company serializers
class CompanySerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = Company
        fields = "__all__"

class CompanySerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = Company
        fields = "__all__"

class CompanySerializerHistory( serializers.ModelSerializer ):
    class Meta:
        model = Company
        exclude = ('created', "modified",)

# Company doc serializers
class CompanyDocSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = CompanyDoc
        fields = "__all__"

class CompanyDocSerializerResponse( serializers.ModelSerializer ):
    company_model = CompanyDocSerializerRequest( source = 'company_id' )
    class Meta:
        model = CompanyDoc
        fields = "__all__"

class CompanyDocSerializerHistory( serializers.ModelSerializer ):
    class Meta:
        model = CompanyDoc
        exclude = ('created', "modified",)

# Area serializers
class AreaSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = Area
        fields = "__all__"

class AreaSerializerResponse( serializers.ModelSerializer ):
    company_model = CompanySerializerRequest( source = 'company_id' )
    class Meta:
        model = Area
        fields = "__all__"

class AreaSerializerHistory( serializers.ModelSerializer ):
    class Meta:
        model = Area
        exclude = ('created', "modified",)

    
# SystemUser serializers
class SystemUserSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = SystemUser
        fields = "__all__"

class SystemUserSerializerResponse( serializers.ModelSerializer ):
    area_model = AreaSerializerResponse( source = 'area_id' )
    class Meta:
        model = SystemUser
        fields = "__all__"

class SystemUserSerializerHistory( serializers.ModelSerializer ):
    class Meta:
        model = SystemUser
        exclude = ('created', "modified",)
