import traceback
import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.inspections.models import InspectionType
from applications.history.models import History
from applications.inspections.serializers import InspectionTypeSerializerRequest, InspectionTypeSerializerResponse, InspectionTypeSerializerHistory
from applications.utils.resp_tools import Resp

class InspectionTypeListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            inspection_types = InspectionType.objects.select_related()
            
            results = self.paginate_queryset(inspection_types, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_types.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_types_serializer = InspectionTypeSerializerResponse(results, many=True)
            else:
                inspection_types_serializer = InspectionTypeSerializerRequest(inspection_types, many=True)

            return Resp(
                data_=inspection_types_serializer.data,
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
            inspection_type_serializer = InspectionTypeSerializerRequest(data=request.data)
            if inspection_type_serializer.is_valid():
                inspection_type_serializer.save()
                # History process pending

                try:
                    new_inspection_type = InspectionType.objects.get(id=inspection_type_serializer.data['id'])
                except InspectionType.DoesNotExist:
                    print("No existe inspection_type")

                serializer_for_history = InspectionTypeSerializerHistory(new_inspection_type, data=inspection_type_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="InspectionType",action="CREATE", table_id=inspection_type_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()


                return Resp(data_=inspection_type_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=inspection_type_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear inspection_type", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class InspectionTypeDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            inspection_type = InspectionType.objects.get(pk=pk)
            inspection_type_serializer = InspectionTypeSerializerResponse(inspection_type)
            return Resp(data_=inspection_type_serializer.data).send()
        except InspectionType.DoesNotExist:
            return Resp(msg="InspectionType no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            inspection_type = InspectionType.objects.get(pk=pk)
            inspection_type_serializer = InspectionTypeSerializerRequest(inspection_type, request.data, partial=True)

            if inspection_type_serializer.is_valid():
                inspection_type_serializer.save()

                # History process pending

                serializer_for_history = InspectionTypeSerializerHistory(inspection_type, data=inspection_type_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="InspectionType",action="UPDATE", table_id=inspection_type_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=inspection_type_serializer.data, msg_="InspectionType actualizada correctamente").send()
            
            return Resp(data_=inspection_type_serializer.errors, msg_="Error al actualizar inspection_type", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except InspectionType.DoesNotExist:
            return Resp(msg_="InspectionType no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            inspection_type = InspectionType.objects.get(pk=pk)
            inspection_type.delete()

            # History process pending

            serializer_for_history = InspectionTypeSerializerHistory(inspection_type)
            serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
            history= History(table_name="InspectionType", action="DELETE", table_id=serializer_for_history.data["id"], table_value=serializer_for_history_to_json)
            history.save()


            return Resp(msg_="InspectionType eliminada correctamente").send()
        except InspectionType.DoesNotExist:
            return Resp(msg_="InspectionType no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class InspectionTypeFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            inspection_types = InspectionType.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(inspection_types, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_types.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_types_serializer = InspectionTypeSerializerResponse(results, many=True)
            else:
                inspection_types_serializer = InspectionTypeSerializerRequest(inspection_types, many=True)

            return Resp(
                data_=inspection_types_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()
