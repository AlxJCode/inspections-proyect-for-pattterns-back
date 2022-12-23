import traceback

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.observations.models import ObservationAnswer
from applications.observations.serializers import ObservationAnswerSerializerRequest, ObservationAnswerSerializerResponse
from applications.utils.resp_tools import Resp

class ObservationAnswerListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            observation_answers = ObservationAnswer.objects.select_related()
            
            results = self.paginate_queryset(observation_answers, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_answers.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_answers_serializer = ObservationAnswerSerializerResponse(results, many=True)
            else:
                observation_answers_serializer = ObservationAnswerSerializerRequest(observation_answers, many=True)

            return Resp(
                data_=observation_answers_serializer.data,
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
            observation_answer_serializer = ObservationAnswerSerializerRequest(data=request.data)
            if observation_answer_serializer.is_valid():
                observation_answer_serializer.save()
                # History process pending

                return Resp(data_=observation_answer_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=observation_answer_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear observation_answer", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class ObservationAnswerDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            observation_answer = ObservationAnswer.objects.get(pk=pk)
            observation_answer_serializer = ObservationAnswerSerializerResponse(observation_answer)
            return Resp(data_=observation_answer_serializer.data).send()
        except ObservationAnswer.DoesNotExist:
            return Resp(msg="ObservationAnswer no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            observation_answer = ObservationAnswer.objects.get(pk=pk)
            observation_answer_serializer = ObservationAnswerSerializerRequest(observation_answer, request.data, partial=True)

            if observation_answer_serializer.is_valid():
                observation_answer_serializer.save()

                # History process pending
                return Resp(data_=observation_answer_serializer.data, msg_="ObservationAnswer actualizada correctamente").send()
            
            return Resp(data_=observation_answer_serializer.errors, msg_="Error al actualizar observation_answer", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except ObservationAnswer.DoesNotExist:
            return Resp(msg_="ObservationAnswer no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            observation_answer = ObservationAnswer.objects.get(pk=pk)
            
            observation_answer.save()

            # History process pending


            return Resp(msg_="ObservationAnswer eliminada correctamente").send()
        except ObservationAnswer.DoesNotExist:
            return Resp(msg_="ObservationAnswer no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class ObservationAnswerFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            observation_answers = ObservationAnswer.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(observation_answers, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_answers.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_answers_serializer = ObservationAnswerSerializerResponse(results, many=True)
            else:
                observation_answers_serializer = ObservationAnswerSerializerRequest(observation_answers, many=True)

            return Resp(
                data_=observation_answers_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

