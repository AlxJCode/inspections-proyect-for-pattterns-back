import traceback

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.observations.models import ObservationResponsible
from applications.observations.serializers import ObservationResponsibleSerializerRequest, ObservationResponsibleSerializerResponse
from applications.utils.resp_tools import Resp

class ObservationResponsibleListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            observation_responsibles = ObservationResponsible.objects.select_related()
            
            results = self.paginate_queryset(observation_responsibles, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_responsibles.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_responsibles_serializer = ObservationResponsibleSerializerResponse(results, many=True)
            else:
                observation_responsibles_serializer = ObservationResponsibleSerializerRequest(observation_responsibles, many=True)

            return Resp(
                data_=observation_responsibles_serializer.data,
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
            observation_responsible_serializer = ObservationResponsibleSerializerRequest(data=request.data)
            if observation_responsible_serializer.is_valid():
                observation_responsible_serializer.save()
                # History process pending

                return Resp(data_=observation_responsible_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=observation_responsible_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear observation_responsible", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class ObservationResponsibleDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            observation_responsible = ObservationResponsible.objects.get(pk=pk)
            observation_responsible_serializer = ObservationResponsibleSerializerResponse(observation_responsible)
            return Resp(data_=observation_responsible_serializer.data).send()
        except ObservationResponsible.DoesNotExist:
            return Resp(msg="ObservationResponsible no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            observation_responsible = ObservationResponsible.objects.get(pk=pk)
            observation_responsible_serializer = ObservationResponsibleSerializerRequest(observation_responsible, request.data, partial=True)

            if observation_responsible_serializer.is_valid():
                observation_responsible_serializer.save()

                # History process pending
                return Resp(data_=observation_responsible_serializer.data, msg_="ObservationResponsible actualizada correctamente").send()
            
            return Resp(data_=observation_responsible_serializer.errors, msg_="Error al actualizar observation_responsible", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except ObservationResponsible.DoesNotExist:
            return Resp(msg_="ObservationResponsible no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            observation_responsible = ObservationResponsible.objects.get(pk=pk)
            
            observation_responsible.delete()

            # History process pending


            return Resp(msg_="ObservationResponsible eliminada correctamente").send()
        except ObservationResponsible.DoesNotExist:
            return Resp(msg_="ObservationResponsible no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class ObservationResponsibleFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            observation_responsibles = ObservationResponsible.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(observation_responsibles, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_responsibles.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_responsibles_serializer = ObservationResponsibleSerializerResponse(results, many=True)
            else:
                observation_responsibles_serializer = ObservationResponsibleSerializerRequest(observation_responsibles, many=True)

            return Resp(
                data_=observation_responsibles_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

