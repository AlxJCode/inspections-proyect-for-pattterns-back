import traceback

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.observations.models import ObservationDetail
from applications.observations.serializers import ObservationDetailSerializerRequest, ObservationDetailSerializerResponse
from applications.utils.resp_tools import Resp

class ObservationDetailListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            observation_details = ObservationDetail.objects.select_related()
            
            results = self.paginate_queryset(observation_details, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_details.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_details_serializer = ObservationDetailSerializerResponse(results, many=True)
            else:
                observation_details_serializer = ObservationDetailSerializerRequest(observation_details, many=True)

            return Resp(
                data_=observation_details_serializer.data,
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
            observation_detail_serializer = ObservationDetailSerializerRequest(data=request.data)
            if observation_detail_serializer.is_valid():
                observation_detail_serializer.save()
                # History process pending

                return Resp(data_=observation_detail_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=observation_detail_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear observation_detail", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class ObservationDetailDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            observation_detail = ObservationDetail.objects.get(pk=pk)
            observation_detail_serializer = ObservationDetailSerializerResponse(observation_detail)
            return Resp(data_=observation_detail_serializer.data).send()
        except ObservationDetail.DoesNotExist:
            return Resp(msg="ObservationDetail no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            observation_detail = ObservationDetail.objects.get(pk=pk)
            observation_detail_serializer = ObservationDetailSerializerRequest(observation_detail, request.data, partial=True)

            if observation_detail_serializer.is_valid():
                observation_detail_serializer.save()

                # History process pending
                return Resp(data_=observation_detail_serializer.data, msg_="ObservationDetail actualizada correctamente").send()
            
            return Resp(data_=observation_detail_serializer.errors, msg_="Error al actualizar observation_detail", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except ObservationDetail.DoesNotExist:
            return Resp(msg_="ObservationDetail no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            observation_detail = ObservationDetail.objects.get(pk=pk)
            
            observation_detail.state = "0"
            observation_detail.save()

            # History process pending


            return Resp(msg_="ObservationDetail eliminada correctamente").send()
        except ObservationDetail.DoesNotExist:
            return Resp(msg_="ObservationDetail no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class ObservationDetailFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            observation_details = ObservationDetail.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(observation_details, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_details.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_details_serializer = ObservationDetailSerializerResponse(results, many=True)
            else:
                observation_details_serializer = ObservationDetailSerializerRequest(observation_details, many=True)

            return Resp(
                data_=observation_details_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

