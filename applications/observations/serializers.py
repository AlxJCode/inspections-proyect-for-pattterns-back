from rest_framework import serializers

from applications.observations.models import *
from applications.users.serializers import SystemUserSerializerRequest

# Observation serializers
class ObservationSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = Observation
        fields = "__all__"

class ObservationSerializerResponse( serializers.ModelSerializer ):
    user_model = SystemUserSerializerRequest( source = 'user_id' )
    class Meta:
        model = Observation
        fields = "__all__"

# Observation Detail serializers
class ObservationDetailSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = ObservationDetail
        fields = "__all__"

class ObservationDetailSerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = ObservationDetail
        fields = "__all__"

# Observation responsible serializers
class ObservationResponsibleSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = ObservationResponsible
        fields = "__all__"

class ObservationResponsibleSerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = ObservationResponsible
        fields = "__all__"

# Observation evidence serializers
class ObservationEvidenceSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = ObservationEvidence
        fields = "__all__"

class ObservationEvidenceSerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = ObservationEvidence
        fields = "__all__"

# Observation assessment serializers
class ObservationAssessmentSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = ObservationAssessment
        fields = "__all__"

class ObservationAssessmentSerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = ObservationAssessment
        fields = "__all__"

class ObservationAssessmentSerializerHistory( serializers.ModelSerializer ):
    class Meta:
        model = ObservationAssessment
        exclude = ('created', "modified",)

# Observation user serializers
class ObservationUserSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = ObservationUser
        fields = "__all__"

class ObservationUserSerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = ObservationUser
        fields = "__all__"

# Observation user serializers
class ObservationAnswerSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = ObservationAnswer
        fields = "__all__"

class ObservationAnswerSerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = ObservationAnswer
        fields = "__all__"

# Observation question serializers
class ObservationQuestionSerializerRequest( serializers.ModelSerializer ):
    class Meta:
        model = ObservationQuestion
        fields = "__all__"

class ObservationQuestionSerializerResponse( serializers.ModelSerializer ):
    class Meta:
        model = ObservationQuestion
        fields = "__all__"

class ObservationQuestionSerializerHistory( serializers.ModelSerializer ):
    class Meta:
        model = ObservationQuestion
        exclude = ('created', "modified",)
