import traceback

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.inspections.models import InspectionDetailDeferment, InspectionDetail
from applications.inspections.serializers import InspectionDetailDefermentSerializerRequest, InspectionDetailDefermentSerializerResponse
from applications.utils.resp_tools import Resp

class InspectionDetailDefermentListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            inspection_detail_deferments = InspectionDetailDeferment.objects.select_related()
            
            results = self.paginate_queryset(inspection_detail_deferments, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_detail_deferments.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_detail_deferments_serializer = InspectionDetailDefermentSerializerResponse(results, many=True)
            else:
                inspection_detail_deferments_serializer = InspectionDetailDefermentSerializerRequest(inspection_detail_deferments, many=True)

            return Resp(
                data_=inspection_detail_deferments_serializer.data,
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
            inspection_serializer = InspectionDetailDefermentSerializerRequest(data=request.data)
            if inspection_serializer.is_valid():
                inspection_serializer.save()

                inspection_detail = InspectionDetail.objects.get( id = inspection_serializer.data['id'] )
                inspection_detail.compliance_date = inspection_serializer.data['cumpliance_date']
                inspection_detail.save()

                # History process pending

                return Resp(data_=inspection_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=inspection_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            print( traceback.format_exc() )
            return Resp(msg_="Ocurrió un error al crear inspection_detail_deferment", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class InspectionDetailDefermentDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            inspection_detail_deferment = InspectionDetailDeferment.objects.get(pk=pk)
            inspection_serializer = InspectionDetailDefermentSerializerResponse(inspection_detail_deferment)
            return Resp(data_=inspection_serializer.data).send()
        except InspectionDetailDeferment.DoesNotExist:
            return Resp(msg="InspectionDetailDeferment no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            inspection_detail_deferment = InspectionDetailDeferment.objects.get(pk=pk)
            inspection_serializer = InspectionDetailDefermentSerializerRequest(inspection_detail_deferment, request.data, partial=True)

            if inspection_serializer.is_valid():
                inspection_serializer.save()

                # History process pending
                return Resp(data_=inspection_serializer.data, msg_="InspectionDetailDeferment actualizado correctamente").send()
            
            return Resp(data_=inspection_serializer.errors, msg_="Error al actualizar inspection_detail_deferment", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except InspectionDetailDeferment.DoesNotExist:
            return Resp(msg_="InspectionDetailDeferment no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            inspection_detail_deferment = InspectionDetailDeferment.objects.get(pk=pk)
            
            inspection_detail_deferment.state = "0"
            inspection_detail_deferment.save()

            # History process pending


            return Resp(msg_="InspectionDetailDeferment eliminado correctamente").send()
        except InspectionDetailDeferment.DoesNotExist:
            return Resp(msg_="InspectionDetailDeferment no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class InspectionDetailDefermentFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            inspection_detail_deferments = InspectionDetailDeferment.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(inspection_detail_deferments, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_detail_deferments.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_detail_deferments_serializer = InspectionDetailDefermentSerializerResponse(results, many=True)
            else:
                inspection_detail_deferments_serializer = InspectionDetailDefermentSerializerRequest(inspection_detail_deferments, many=True)

            return Resp(
                data_=inspection_detail_deferments_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

