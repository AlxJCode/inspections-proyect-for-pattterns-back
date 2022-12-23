import traceback

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.observations.models import ObservationEvidence
from applications.observations.serializers import ObservationEvidenceSerializerRequest, ObservationEvidenceSerializerResponse
from applications.utils.resp_tools import Resp

class ObservationEvidenceListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            observation_evidences = ObservationEvidence.objects.select_related()
            
            results = self.paginate_queryset(observation_evidences, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_evidences.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_evidences_serializer = ObservationEvidenceSerializerResponse(results, many=True)
            else:
                observation_evidences_serializer = ObservationEvidenceSerializerRequest(observation_evidences, many=True)

            return Resp(
                data_=observation_evidences_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()
    
    def post(self, request, format=None):
        try:
            observation_evidence_serializer = ObservationEvidenceSerializerRequest(data=request.data)
            if observation_evidence_serializer.is_valid():
                observation_evidence_serializer.save()
                # History process pending

                return Resp(data_=observation_evidence_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=observation_evidence_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear observation_evidence", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class ObservationEvidenceDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            observation_evidence = ObservationEvidence.objects.get(pk=pk)
            observation_evidence_serializer = ObservationEvidenceSerializerResponse(observation_evidence)
            return Resp(data_=observation_evidence_serializer.data).send()
        except ObservationEvidence.DoesNotExist:
            return Resp(msg="ObservationEvidence no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            observation_evidence = ObservationEvidence.objects.get(pk=pk)
            observation_evidence_serializer = ObservationEvidenceSerializerRequest(observation_evidence, request.data, partial=True)

            if observation_evidence_serializer.is_valid():
                observation_evidence_serializer.save()

                # History process pending
                return Resp(data_=observation_evidence_serializer.data, msg_="ObservationEvidence actualizada correctamente").send()
            
            return Resp(data_=observation_evidence_serializer.errors, msg_="Error al actualizar observation_evidence", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except ObservationEvidence.DoesNotExist:
            return Resp(msg_="ObservationEvidence no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            observation_evidence = ObservationEvidence.objects.get(pk=pk)
            
            observation_evidence.delete()

            # History process pending


            return Resp(msg_="ObservationEvidence eliminada correctamente").send()
        except ObservationEvidence.DoesNotExist:
            return Resp(msg_="ObservationEvidence no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class ObservationEvidenceFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            observation_evidences = ObservationEvidence.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(observation_evidences, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_evidences.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_evidences_serializer = ObservationEvidenceSerializerResponse(results, many=True)
            else:
                observation_evidences_serializer = ObservationEvidenceSerializerRequest(observation_evidences, many=True)

            return Resp(
                data_=observation_evidences_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()
