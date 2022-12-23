import traceback
import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.inspections.models import InspectionAffected
from applications.history.models import History
from applications.inspections.serializers import InspectionAffectedSerializerRequest, InspectionAffectedSerializerResponse, InspectionAffectedSerializerHistory
from applications.utils.resp_tools import Resp

class InspectionAffectedListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            inspection_affecteds = InspectionAffected.objects.select_related()
            
            results = self.paginate_queryset(inspection_affecteds, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_affecteds.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_affecteds_serializer = InspectionAffectedSerializerResponse(results, many=True)
            else:
                inspection_affecteds_serializer = InspectionAffectedSerializerRequest(inspection_affecteds, many=True)

            return Resp(
                data_=inspection_affecteds_serializer.data,
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
            inspection_affected_serializer = InspectionAffectedSerializerRequest(data=request.data)
            if inspection_affected_serializer.is_valid():
                inspection_affected_serializer.save()
                # History process pending


                try:
                    new_inspection_affected = InspectionAffected.objects.get(id=inspection_affected_serializer.data['id'])
                except InspectionAffected.DoesNotExist:
                    print("No existe inspection_affected")

                serializer_for_history = InspectionAffectedSerializerHistory(new_inspection_affected, data=inspection_affected_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="InspectionAffected",action="CREATE", table_id=inspection_affected_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=inspection_affected_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=inspection_affected_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear inspection_affected", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class InspectionAffectedDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            inspection_affected = InspectionAffected.objects.get(pk=pk)
            inspection_affected_serializer = InspectionAffectedSerializerResponse(inspection_affected)
            return Resp(data_=inspection_affected_serializer.data).send()
        except InspectionAffected.DoesNotExist:
            return Resp(msg="InspectionAffected no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            inspection_affected = InspectionAffected.objects.get(pk=pk)
            inspection_affected_serializer = InspectionAffectedSerializerRequest(inspection_affected, request.data, partial=True)

            if inspection_affected_serializer.is_valid():
                inspection_affected_serializer.save()

                # History process pending

                serializer_for_history = InspectionAffectedSerializerHistory(inspection_affected, data=inspection_affected_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="InspectionAffected",action="UPDATE", table_id=inspection_affected_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=inspection_affected_serializer.data, msg_="InspectionAffected actualizada correctamente").send()
            
            return Resp(data_=inspection_affected_serializer.errors, msg_="Error al actualizar inspection_affected", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except InspectionAffected.DoesNotExist:
            return Resp(msg_="InspectionAffected no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            inspection_affected = InspectionAffected.objects.get(pk=pk)
            
            inspection_affected.state = False
            inspection_affected.save()

            # History process pending

            serializer_for_history = InspectionAffectedSerializerHistory(inspection_affected)
            serializer_for_history_to_json = json.dumps( serializer_for_history.data, ensure_ascii = False ).replace('"', "'")
            history= History( table_name="InspectionAffected", action="DELETE", table_id=serializer_for_history.data["id"], table_value=serializer_for_history_to_json )
            history.save()


            return Resp(msg_="InspectionAffected eliminada correctamente").send()
        except InspectionAffected.DoesNotExist:
            return Resp(msg_="InspectionAffected no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class InspectionAffectedFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            inspection_affecteds = InspectionAffected.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(inspection_affecteds, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_affecteds.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_affecteds_serializer = InspectionAffectedSerializerResponse(results, many=True)
            else:
                inspection_affecteds_serializer = InspectionAffectedSerializerRequest(inspection_affecteds, many=True)

            return Resp(
                data_=inspection_affecteds_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()
