import json
import traceback
from rest_framework.views import APIView
from rest_framework import status
from applications.history.serializers import *
from applications.utils.resp_tools import Resp
from rest_framework.pagination import PageNumberPagination


class HistoryListView(APIView, PageNumberPagination):
    serializer_class = HistorySerializer


    def get(self, request, format=None):
        self.page_size = 100
        histories = History.objects.all()
        results = self.paginate_queryset(histories, request, view=self)
        previous_link = self.get_previous_link()
        next_link = self.get_next_link()
        
  
        serializer = HistorySerializer(results, many=True)

        return Resp(data_=serializer.data, msg_="Historiales Recuperados Exitosamente.", status_=True, pagination_=True, next_link_=next_link, previous_link_=previous_link,
                    code_=status.HTTP_200_OK).send()

    def post(self, request, format=None):
        try:
            serializer = HistorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Resp(data_=serializer.data, msg_="Historial creado exitosamente.",
                            status_=True,
                            code_=status.HTTP_201_CREATED).send()
            return Resp(data_=serializer.errors, msg_="Error al guardar Historial", status_=False,
                        code_=status.HTTP_200_OK).send()
        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class HistoryDetailView(APIView):
    serializer_class = HistorySerializer

    def get(self, request, pk, format=None):
        try:
            history = History.objects.get(pk=pk)
            serializer = HistorySerializer(history)
            return Resp(data_=serializer.data, msg_="Historial recuperado exitosamente", status_=True).send()
        except History.DoesNotExist:
            return Resp(data_="No existe la Historial", status_=False, code_=status.HTTP_404_NOT_FOUND).send()

    def put(self, request, pk, format=None):
        try:
            history = History.objects.get(pk=pk)
            serializer = HistorySerializer(
                history, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Resp(data_=serializer.data, status_=True, msg_="Historial actualizada correctamente").send()

            return Resp(data_=serializer.errors, msg_="Error en actualizar Historial", status_=False, code_=status.HTTP_200_OK).send()

        except:
            return Resp(msg_="Historial no existe", status_=False,  code_=status.HTTP_404_NOT_FOUND).send()

    def delete(self, request, pk, format=None):
        try:
            history = History.objects.get(pk=pk)
            history.delete()
            return Resp(data_="Historial eliminado Exitosamente", status_=True).send()
        except History.DoesNotExist:
            return Resp(msg_="Historial no existe", status_=False, code_=status.HTTP_404_NOT_FOUND).send


class HistoryFilterView(APIView, PageNumberPagination):
    """
        Get, update or delete a specific History.
    """
    serializer_class = HistorySerializer

    def get(self, request, format=None):
        return Resp(data_={}, msg_="", status_=False, code_=status.HTTP_405_METHOD_NOT_ALLOWED).send()

    def post(self, request, format=None):
        try:

            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            histories = History.objects.filter( **filter ).exclude( **exclude )

            results = self.paginate_queryset(histories, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = histories.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                histories_serializer = HistorySerializer(results, many=True)
            else:
                histories_serializer = HistorySerializer(histories, many=True)

            return Resp(
                data_=histories_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except Exception as e:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=str(e), status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()


class GetGreatHistoryById(APIView): 


    def post(self, request, foramt=None):
        try:
            history_id = request.data.get("id")
           

            histories = History.objects.filter(id__gt=history_id)
            serializer = HistorySerializer(histories, many=True)

            return Resp(data_=serializer.data, msg_="Historiales recuperados exitosamente",
                 status_=True, code_=status.HTTP_200_OK).send()

        except Exception as e:
            return Resp(msg_=str(e), status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()
