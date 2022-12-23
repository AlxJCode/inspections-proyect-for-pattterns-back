import traceback

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.inspections.models import Inspection
from applications.inspections.serializers import InspectionSerializerRequest, InspectionSerializerResponse
from applications.utils.resp_tools import Resp

class InspectionListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            inspections = Inspection.objects.select_related()
            
            results = self.paginate_queryset(inspections, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspections.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspections_serializer = InspectionSerializerResponse(results, many=True)
            else:
                inspections_serializer = InspectionSerializerRequest(inspections, many=True)

            return Resp(
                data_=inspections_serializer.data,
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
            inspection_serializer = InspectionSerializerRequest(data=request.data)
            if inspection_serializer.is_valid():
                inspection_serializer.save()
                # History process pending

                return Resp(data_=inspection_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=inspection_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear inspection", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class InspectionDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            inspection = Inspection.objects.get(pk=pk)
            inspection_serializer = InspectionSerializerResponse(inspection)
            return Resp(data_=inspection_serializer.data).send()
        except Inspection.DoesNotExist:
            return Resp(msg="Inspection no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            inspection = Inspection.objects.get(pk=pk)
            inspection_serializer = InspectionSerializerRequest(inspection, request.data, partial=True)

            if inspection_serializer.is_valid():
                inspection_serializer.save()

                # History process pending
                return Resp(data_=inspection_serializer.data, msg_="Inspection actualizada correctamente").send()
            
            return Resp(data_=inspection_serializer.errors, msg_="Error al actualizar inspection", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except Inspection.DoesNotExist:
            return Resp(msg_="Inspection no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            inspection = Inspection.objects.get(pk=pk)
            
            inspection.state = "0"
            inspection.save()

            # History process pending


            return Resp(msg_="Inspection eliminada correctamente").send()
        except Inspection.DoesNotExist:
            return Resp(msg_="Inspection no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class InspectionFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            inspections = Inspection.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(inspections, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspections.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspections_serializer = InspectionSerializerResponse(results, many=True)
            else:
                inspections_serializer = InspectionSerializerRequest(inspections, many=True)

            return Resp(
                data_=inspections_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()
