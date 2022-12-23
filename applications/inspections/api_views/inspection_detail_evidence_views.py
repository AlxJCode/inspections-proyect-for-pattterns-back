import traceback

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.inspections.models import InspectionDetailEvidence
from applications.inspections.serializers import InspectionDetailEvidenceSerializerRequest, InspectionDetailEvidenceSerializerResponse
from applications.utils.resp_tools import Resp

class InspectionDetailEvidenceListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            inspection_detail_evidences = InspectionDetailEvidence.objects.select_related()
            
            results = self.paginate_queryset(inspection_detail_evidences, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_detail_evidences.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_detail_evidences_serializer = InspectionDetailEvidenceSerializerResponse(results, many=True)
            else:
                inspection_detail_evidences_serializer = InspectionDetailEvidenceSerializerRequest(inspection_detail_evidences, many=True)

            return Resp(
                data_=inspection_detail_evidences_serializer.data,
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
            inspection_serializer = InspectionDetailEvidenceSerializerRequest(data=request.data)
            if inspection_serializer.is_valid():
                inspection_serializer.save()
                # History process pending

                return Resp(data_=inspection_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=inspection_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear inspection_detail_evidence", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class InspectionDetailEvidenceDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            inspection_detail_evidence = InspectionDetailEvidence.objects.get(pk=pk)
            inspection_serializer = InspectionDetailEvidenceSerializerResponse(inspection_detail_evidence)
            return Resp(data_=inspection_serializer.data).send()
        except InspectionDetailEvidence.DoesNotExist:
            return Resp(msg="InspectionDetailEvidence no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            inspection_detail_evidence = InspectionDetailEvidence.objects.get(pk=pk)
            inspection_serializer = InspectionDetailEvidenceSerializerRequest(inspection_detail_evidence, request.data, partial=True)

            if inspection_serializer.is_valid():
                inspection_serializer.save()

                # History process pending
                return Resp(data_=inspection_serializer.data, msg_="InspectionDetailEvidence actualizada correctamente").send()
            
            return Resp(data_=inspection_serializer.errors, msg_="Error al actualizar inspection_detail_evidence", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except InspectionDetailEvidence.DoesNotExist:
            return Resp(msg_="InspectionDetailEvidence no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            inspection_detail_evidence = InspectionDetailEvidence.objects.get(pk=pk)
            
            inspection_detail_evidence.state = "0"
            inspection_detail_evidence.save()

            # History process pending


            return Resp(msg_="InspectionDetailEvidence eliminada correctamente").send()
        except InspectionDetailEvidence.DoesNotExist:
            return Resp(msg_="InspectionDetailEvidence no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class InspectionDetailEvidenceFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            inspection_detail_evidences = InspectionDetailEvidence.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(inspection_detail_evidences, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_detail_evidences.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_detail_evidences_serializer = InspectionDetailEvidenceSerializerResponse(results, many=True)
            else:
                inspection_detail_evidences_serializer = InspectionDetailEvidenceSerializerRequest(inspection_detail_evidences, many=True)

            return Resp(
                data_=inspection_detail_evidences_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()
