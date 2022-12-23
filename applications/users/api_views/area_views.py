import traceback
import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.users.models import Area
from applications.history.models import History
from applications.users.serializers import AreaSerializerRequest, AreaSerializerResponse, AreaSerializerHistory
from applications.utils.resp_tools import Resp

class AreaListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            areas = Area.objects.select_related()
            
            results = self.paginate_queryset(areas, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = areas.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                areas_serializer = AreaSerializerResponse(results, many=True)
            else:
                areas_serializer = AreaSerializerRequest(areas, many=True)

            return Resp(
                data_=areas_serializer.data,
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
            area_serializer = AreaSerializerRequest(data=request.data)
            if area_serializer.is_valid():
                area_serializer.save()
                # History process pending

                try:
                    new_area = Area.objects.get(id=area_serializer.data['id'])
                except Area.DoesNotExist:
                    print("No existe area")

                serializer_for_history = AreaSerializerHistory(new_area, data=area_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="Area",action="CREATE", table_id=area_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=area_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=area_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear area", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class AreaDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            area = Area.objects.get(pk=pk)
            area_serializer = AreaSerializerResponse(area)
            return Resp(data_=area_serializer.data).send()
        except Area.DoesNotExist:
            return Resp(msg="Area no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            area = Area.objects.get(pk=pk)
            area_serializer = AreaSerializerRequest(area, request.data, partial=True)

            if area_serializer.is_valid():
                area_serializer.save()

                # History process pending
                serializer_for_history = AreaSerializerHistory(area, data=area_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="Area",action="UPDATE", table_id=area_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                
                return Resp(data_=area_serializer.data, msg_="Area actualizada correctamente").send()
            
            return Resp(data_=area_serializer.errors, msg_="Error al actualizar area", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except Area.DoesNotExist:
            return Resp(msg_="Area no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            area = Area.objects.get(pk=pk)
            
            area.state = False
            area.save()

            # History process pending

            serializer_for_history = AreaSerializerHistory(area)
            serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
            history= History(table_name="Area",action="DELETE", table_id=serializer_for_history.data["id"],table_value=serializer_for_history_to_json)
            history.save()

            return Resp(msg_="Area eliminada correctamente").send()
        except Area.DoesNotExist:
            return Resp(msg_="Area no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class AreaFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            areas = Area.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(areas, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = areas.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                areas_serializer = AreaSerializerResponse(results, many=True)
            else:
                areas_serializer = AreaSerializerRequest(areas, many=True)

            return Resp(
                data_=areas_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()
