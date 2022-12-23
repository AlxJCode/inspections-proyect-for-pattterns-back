import traceback

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.observations.models import Observation
from applications.observations.serializers import ObservationSerializerRequest, ObservationSerializerResponse
from applications.utils.resp_tools import Resp

class ObservationListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            observations = Observation.objects.select_related()
            
            results = self.paginate_queryset(observations, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observations.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observations_serializer = ObservationSerializerResponse(results, many=True)
            else:
                observations_serializer = ObservationSerializerRequest(observations, many=True)

            return Resp(
                data_=observations_serializer.data,
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
            observation_serializer = ObservationSerializerRequest(data=request.data)
            if observation_serializer.is_valid():
                observation_serializer.save()
                # History process pending

                return Resp(data_=observation_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=observation_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear observation", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class ObservationDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            observation = Observation.objects.get(pk=pk)
            observation_serializer = ObservationSerializerResponse(observation)
            return Resp(data_=observation_serializer.data).send()
        except Observation.DoesNotExist:
            return Resp(msg="Observation no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            observation = Observation.objects.get(pk=pk)
            observation_serializer = ObservationSerializerRequest(observation, request.data, partial=True)

            if observation_serializer.is_valid():
                observation_serializer.save()

                # History process pending
                return Resp(data_=observation_serializer.data, msg_="Observation actualizada correctamente").send()
            
            return Resp(data_=observation_serializer.errors, msg_="Error al actualizar observation", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except Observation.DoesNotExist:
            return Resp(msg_="Observation no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            observation = Observation.objects.get(pk=pk)
            
            observation.state = "0"
            observation.save()

            # History process pending


            return Resp(msg_="Observation eliminada correctamente").send()
        except Observation.DoesNotExist:
            return Resp(msg_="Observation no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class ObservationFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            observations = Observation.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(observations, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observations.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observations_serializer = ObservationSerializerResponse(results, many=True)
            else:
                observations_serializer = ObservationSerializerRequest(observations, many=True)

            return Resp(
                data_=observations_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

