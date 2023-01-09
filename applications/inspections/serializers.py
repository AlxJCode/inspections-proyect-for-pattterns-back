from rest_framework import serializers

from applications.inspections.models import InspectionAssessment, InspectionDetail, Inspection, InspectionDetailEvidence, InspectionDetailResponsible, InspectionAffected, InspectionType, InspectionUser, Inspection
from applications.users.serializers import SystemUserSerializerRequest

# Inpection serializers
class InspectionSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = Inspection
        fields = "__all__"

class InspectionSerializerResponse( serializers.ModelSerializer ):
    user_model = SystemUserSerializerRequest( source = 'user_id' )
    class Meta:
        model = Inspection
        fields = "__all__"

# Inpection user serializers
class InspectionUserSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = InspectionUser
        fields = "__all__"

class InspectionUserSerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = InspectionUser
        fields = "__all__"

# Inpection detail serializers
class InspectionDetailSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = InspectionDetail
        fields = "__all__"

class InspectionDetailSerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = InspectionDetail
        fields = "__all__"

# Inpection type serializers
class InspectionTypeSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = InspectionType
        fields = "__all__"

class InspectionTypeSerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = InspectionType
        fields = "__all__"

class InspectionTypeSerializerHistory( serializers.ModelSerializer ):
    class Meta:
        model = InspectionType
        exclude = ('created', "modified",)

# Inpection detail evidence serializers
class InspectionDetailEvidenceSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = InspectionDetailEvidence
        fields = "__all__"

class InspectionDetailEvidenceSerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = InspectionDetailEvidence
        fields = "__all__"

# Inpection detail responsible serializers
class InspectionDetailResponsibleSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = InspectionDetailResponsible
        fields = "__all__"

class InspectionDetailResponsibleSerializerResponse( serializers.ModelSerializer ):
    inspection_detail_model = InspectionDetailSerializerRequest( source = "inpection_detail_id" )
    class Meta:
        model = InspectionDetailResponsible
        fields = "__all__"

# Inpection affected serializers
class InspectionAffectedSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = InspectionAffected
        fields = "__all__"

class InspectionAffectedSerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = InspectionAffected
        fields = "__all__"
    
class InspectionAffectedSerializerHistory( serializers.ModelSerializer ):
    class Meta:
        model = InspectionAffected
        exclude = ('created', "modified",)

# Inpection assessment serializers
class InspectionAssessmentSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = InspectionAssessment
        fields = "__all__"

class InspectionAssessmentSerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = InspectionAssessment
        fields = "__all__"

class InspectionAssessmentSerializerHistory( serializers.ModelSerializer ):
    class Meta:
        model = InspectionAssessment
        exclude = ('created', "modified",)