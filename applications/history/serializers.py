
from rest_framework import serializers

from applications.history.models import *

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"