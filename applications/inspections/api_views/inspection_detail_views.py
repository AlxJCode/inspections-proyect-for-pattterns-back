import traceback

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.inspections.models import InspectionDetail
from applications.inspections.serializers import InspectionDetailSerializerRequest, InspectionDetailSerializerResponse
from applications.utils.resp_tools import Resp

class InspectionDetailListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            inspection_details = InspectionDetail.objects.select_related()
            
            results = self.paginate_queryset(inspection_details, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_details.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_details_serializer = InspectionDetailSerializerResponse(results, many=True)
            else:
                inspection_details_serializer = InspectionDetailSerializerRequest(inspection_details, many=True)

            return Resp(
                data_=inspection_details_serializer.data,
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
            inspection_detail_serializer = InspectionDetailSerializerRequest(data=request.data)
            if inspection_detail_serializer.is_valid():
                inspection_detail_serializer.save()
                # History process pending

                return Resp(data_=inspection_detail_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=inspection_detail_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear inspection_detail", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class InspectionDetailDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            inspection_detail = InspectionDetail.objects.get(pk=pk)
            inspection_detail_serializer = InspectionDetailSerializerResponse(inspection_detail)
            return Resp(data_=inspection_detail_serializer.data).send()
        except InspectionDetail.DoesNotExist:
            return Resp(msg="InspectionDetail no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            inspection_detail = InspectionDetail.objects.get(pk=pk)
            inspection_detail_serializer = InspectionDetailSerializerRequest(inspection_detail, request.data, partial=True)

            if inspection_detail_serializer.is_valid():
                inspection_detail_serializer.save()

                # History process pending
                return Resp(data_=inspection_detail_serializer.data, msg_="InspectionDetail actualizada correctamente").send()
            
            return Resp(data_=inspection_detail_serializer.errors, msg_="Error al actualizar inspection_detail", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except InspectionDetail.DoesNotExist:
            return Resp(msg_="InspectionDetail no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            inspection_detail = InspectionDetail.objects.get(pk=pk)
            inspection_detail.delete()

            # History process pending


            return Resp(msg_="InspectionDetail eliminada correctamente").send()
        except InspectionDetail.DoesNotExist:
            return Resp(msg_="InspectionDetail no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class InspectionDetailFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            inspection_details = InspectionDetail.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(inspection_details, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_details.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_details_serializer = InspectionDetailSerializerResponse(results, many=True)
            else:
                inspection_details_serializer = InspectionDetailSerializerRequest(inspection_details, many=True)

            return Resp(
                data_=inspection_details_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()
