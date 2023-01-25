import traceback

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.observations.models import ObservationDetailDeferment, ObservationDetail
from applications.observations.serializers import ObservationDetailDefermentSerializerRequest, ObservationDetailDefermentSerializerResponse
from applications.utils.resp_tools import Resp

class ObservationDetailDefermentListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            observation_detail_deferment_deferments = ObservationDetailDeferment.objects.select_related()
            
            results = self.paginate_queryset(observation_detail_deferment_deferments, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_detail_deferment_deferments.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_detail_deferment_deferments_serializer = ObservationDetailDefermentSerializerResponse(results, many=True)
            else:
                observation_detail_deferment_deferments_serializer = ObservationDetailDefermentSerializerRequest(observation_detail_deferment_deferments, many=True)

            return Resp(
                data_=observation_detail_deferment_deferments_serializer.data,
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
            observation_detail_deferment_serializer = ObservationDetailDefermentSerializerRequest(data=request.data)
            if observation_detail_deferment_serializer.is_valid():
                observation_detail_deferment_serializer.save()
                
                observation_detail = ObservationDetail.objects.get( id = observation_detail_deferment_serializer.data['observation_detail_id'] )
                observation_detail.compliance_date = observation_detail_deferment_serializer.data['cumpliance_date']
                observation_detail.save()


                return Resp(data_=observation_detail_deferment_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=observation_detail_deferment_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear observation_detail_deferment", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class ObservationDetailDefermentDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            observation_detail_deferment = ObservationDetailDeferment.objects.get(pk=pk)
            observation_detail_deferment_serializer = ObservationDetailDefermentSerializerResponse(observation_detail_deferment)
            return Resp(data_=observation_detail_deferment_serializer.data).send()
        except ObservationDetailDeferment.DoesNotExist:
            return Resp(msg="ObservationDetailDeferment no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            observation_detail_deferment = ObservationDetailDeferment.objects.get(pk=pk)
            observation_detail_deferment_serializer = ObservationDetailDefermentSerializerRequest(observation_detail_deferment, request.data, partial=True)

            if observation_detail_deferment_serializer.is_valid():
                observation_detail_deferment_serializer.save()

                # History process pending
                return Resp(data_=observation_detail_deferment_serializer.data, msg_="ObservationDetailDeferment actualizada correctamente").send()
            
            return Resp(data_=observation_detail_deferment_serializer.errors, msg_="Error al actualizar observation_detail_deferment", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except ObservationDetailDeferment.DoesNotExist:
            return Resp(msg_="ObservationDetailDeferment no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            observation_detail_deferment = ObservationDetailDeferment.objects.get(pk=pk)
            
            observation_detail_deferment.state = False
            observation_detail_deferment.save()

            # History process pending


            return Resp(msg_="ObservationDetailDeferment eliminada correctamente").send()
        except ObservationDetailDeferment.DoesNotExist:
            return Resp(msg_="ObservationDetailDeferment no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class ObservationDetailDefermentFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            observation_detail_deferment_deferments = ObservationDetailDeferment.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(observation_detail_deferment_deferments, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_detail_deferment_deferments.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_detail_deferment_deferments_serializer = ObservationDetailDefermentSerializerResponse(results, many=True)
            else:
                observation_detail_deferment_deferments_serializer = ObservationDetailDefermentSerializerRequest(observation_detail_deferment_deferments, many=True)

            return Resp(
                data_=observation_detail_deferment_deferments_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

