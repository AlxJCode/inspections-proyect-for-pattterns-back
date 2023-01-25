import traceback
import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.observations.models import ObservationAffected
from applications.history.models import History
from applications.observations.serializers import ObservationAffectedSerializerRequest, ObservationAffectedSerializerResponse, ObservationAffectedSerializerHistory
from applications.utils.resp_tools import Resp

class ObservationAffectedListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            observation_affecteds = ObservationAffected.objects.select_related()
            
            results = self.paginate_queryset(observation_affecteds, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_affecteds.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_affecteds_serializer = ObservationAffectedSerializerResponse(results, many=True)
            else:
                observation_affecteds_serializer = ObservationAffectedSerializerRequest(observation_affecteds, many=True)

            return Resp(
                data_=observation_affecteds_serializer.data,
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
            observation_affected_serializer = ObservationAffectedSerializerRequest(data=request.data)
            if observation_affected_serializer.is_valid():
                observation_affected_serializer.save()
                # History process pending

                try:
                    new_observation_question = ObservationAffected.objects.get(id=observation_affected_serializer.data['id'])
                except ObservationAffected.DoesNotExist:
                    print("No existe inspection_affected")

                serializer_for_history = ObservationAffectedSerializerHistory(new_observation_question, data=observation_affected_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="ObservationAffected",action="CREATE", table_id=observation_affected_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=observation_affected_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=observation_affected_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear observation_affected", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class ObservationAffectedDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            observation_affected = ObservationAffected.objects.get(pk=pk)
            observation_affected_serializer = ObservationAffectedSerializerResponse(observation_affected)
            return Resp(data_=observation_affected_serializer.data).send()
        except ObservationAffected.DoesNotExist:
            return Resp(msg="ObservationAffected no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            observation_affected = ObservationAffected.objects.get(pk=pk)
            observation_affected_serializer = ObservationAffectedSerializerRequest(observation_affected, request.data, partial=True)

            if observation_affected_serializer.is_valid():
                observation_affected_serializer.save()

                # History process pending

                serializer_for_history = ObservationAffectedSerializerHistory(observation_affected, data=observation_affected_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="ObservationAffected",action="UPDATE", table_id=observation_affected_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=observation_affected_serializer.data, msg_="ObservationAffected actualizada correctamente").send()
            
            return Resp(data_=observation_affected_serializer.errors, msg_="Error al actualizar observation_affected", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except ObservationAffected.DoesNotExist:
            return Resp(msg_="ObservationAffected no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            observation_affected = ObservationAffected.objects.get(pk=pk)
            observation_affected.state = False
            observation_affected.save()

            # History process pending

            serializer_for_history = ObservationAffectedSerializerHistory(observation_affected)
            serializer_for_history_to_json = json.dumps( serializer_for_history.data, ensure_ascii = False ).replace('"', "'")
            history= History( table_name="ObservationAffected", action="DELETE", table_id=serializer_for_history.data["id"], table_value=serializer_for_history_to_json )
            history.save()


            return Resp(msg_="ObservationAffected eliminada correctamente").send()
        except ObservationAffected.DoesNotExist:
            return Resp(msg_="ObservationAffected no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class ObservationAffectedFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            observation_affecteds = ObservationAffected.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(observation_affecteds, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_affecteds.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_affecteds_serializer = ObservationAffectedSerializerResponse(results, many=True)
            else:
                observation_affecteds_serializer = ObservationAffectedSerializerRequest(observation_affecteds, many=True)

            return Resp(
                data_=observation_affecteds_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

