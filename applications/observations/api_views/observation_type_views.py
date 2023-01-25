import traceback
import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.observations.models import ObservationType
from applications.history.models import History
from applications.observations.serializers import ObservationTypeSerializerRequest, ObservationTypeSerializerResponse, ObservationTypeSerializerHistory
from applications.utils.resp_tools import Resp

class ObservationTypeListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            observation_types = ObservationType.objects.select_related()
            
            results = self.paginate_queryset(observation_types, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_types.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_types_serializer = ObservationTypeSerializerResponse(results, many=True)
            else:
                observation_types_serializer = ObservationTypeSerializerRequest(observation_types, many=True)

            return Resp(
                data_=observation_types_serializer.data,
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
            observation_type_serializer = ObservationTypeSerializerRequest(data=request.data)
            if observation_type_serializer.is_valid():
                observation_type_serializer.save()
                # History process pending

                try:
                    new_observation_question = ObservationType.objects.get(id=observation_type_serializer.data['id'])
                except ObservationType.DoesNotExist:
                    print("No existe inspection_affected")

                serializer_for_history = ObservationTypeSerializerHistory(new_observation_question, data=observation_type_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="ObservationType",action="CREATE", table_id=observation_type_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()


                return Resp(data_=observation_type_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=observation_type_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear observation_type", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class ObservationTypeDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            observation_type = ObservationType.objects.get(pk=pk)
            observation_type_serializer = ObservationTypeSerializerResponse(observation_type)
            return Resp(data_=observation_type_serializer.data).send()
        except ObservationType.DoesNotExist:
            return Resp(msg="ObservationType no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            observation_type = ObservationType.objects.get(pk=pk)
            observation_type_serializer = ObservationTypeSerializerRequest(observation_type, request.data, partial=True)

            if observation_type_serializer.is_valid():
                observation_type_serializer.save()

                # History process pending

                serializer_for_history = ObservationTypeSerializerHistory(observation_type, data=observation_type_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="ObservationType",action="UPDATE", table_id=observation_type_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=observation_type_serializer.data, msg_="ObservationType actualizada correctamente").send()
            
            return Resp(data_=observation_type_serializer.errors, msg_="Error al actualizar observation_type", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except ObservationType.DoesNotExist:
            return Resp(msg_="ObservationType no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            observation_type = ObservationType.objects.get(pk=pk)
            observation_type.delete()

            # History process pending

            serializer_for_history = ObservationTypeSerializerHistory(observation_type)
            serializer_for_history_to_json = json.dumps( serializer_for_history.data, ensure_ascii = False ).replace('"', "'")
            history= History( table_name="ObservationType", action="DELETE", table_id=serializer_for_history.data["id"], table_value=serializer_for_history_to_json )
            history.save()


            return Resp(msg_="ObservationType eliminada correctamente").send()
        except ObservationType.DoesNotExist:
            return Resp(msg_="ObservationType no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class ObservationTypeFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            observation_types = ObservationType.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(observation_types, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_types.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_types_serializer = ObservationTypeSerializerResponse(results, many=True)
            else:
                observation_types_serializer = ObservationTypeSerializerRequest(observation_types, many=True)

            return Resp(
                data_=observation_types_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

