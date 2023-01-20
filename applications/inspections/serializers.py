from rest_framework import serializers

from applications.inspections.models import InspectionAssessment, InspectionDetail, Inspection, InspectionDetailEvidence, InspectionDetailResponsible, InspectionAffected, InspectionType, InspectionUser, Inspection, InspectionDetailDeferment
from applications.users.serializers import SystemUserSerializerRequest

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

# Inpection serializers
class InspectionSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = Inspection
        fields = "__all__"

class InspectionSerializerResponse( serializers.ModelSerializer ):
    user_model = SystemUserSerializerRequest( source = 'user_id' )
    type_model = InspectionTypeSerializerRequest( source = 'type' )
    class Meta:
        model = Inspection
        fields = "__all__"

# Inpection user serializers
class InspectionUserSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = InspectionUser
        fields = "__all__"

class InspectionUserSerializerResponse( serializers.ModelSerializer ):
    user_model = SystemUserSerializerRequest( source = "user_id" )
    class Meta:
        model = InspectionUser
        fields = "__all__"

# Inpection detail evidence serializers
class InspectionDetailEvidenceSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = InspectionDetailEvidence
        fields = "__all__"

# Inpection detail responsible serializers
class InspectionDetailResponsibleSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = InspectionDetailResponsible
        fields = "__all__"

# Inpection detail serializers
class InspectionDetailSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = InspectionDetail
        fields = "__all__"

class InspectionDetailSerializerResponse( serializers.ModelSerializer ):
    assessment_model    = InspectionAssessmentSerializerRequest( source = "assesment_id" )
    affected_model      = InspectionAffectedSerializerRequest( source = "affected_id" )
    inspection_model    = InspectionSerializerRequest( source = "inspection_id" )
    evidences           = InspectionDetailEvidenceSerializerRequest ( source = "ide", many = True )
    responsible_users   = InspectionDetailResponsibleSerializerRequest ( source = "idr", many = True )

    class Meta:
        model = InspectionDetail
        fields = "__all__"


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
    inspection_detail_model = InspectionDetailSerializerRequest( source = "inspection_detail_id" )
    class Meta:
        model = InspectionDetailResponsible
        fields = "__all__"

# Inpection detail deferment serializers
class InspectionDetailDefermentSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = InspectionDetailDeferment
        fields = "__all__"

class InspectionDetailDefermentSerializerResponse( serializers.ModelSerializer ):
    inspection_detail_model = InspectionDetailSerializerRequest( source = "inspection_detail_id" )
    class Meta:
        model = InspectionDetailDeferment
        fields = "__all__"

