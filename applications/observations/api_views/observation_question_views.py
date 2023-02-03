import traceback
import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.observations.models import ObservationQuestion
from applications.history.models import History
from applications.observations.serializers import ObservationQuestionSerializerRequest, ObservationQuestionSerializerResponse, ObservationQuestionSerializerHistory
from applications.utils.resp_tools import Resp

class ObservationQuestionListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            observation_questions = ObservationQuestion.objects.select_related().order_by('order')
            
            results = self.paginate_queryset(observation_questions, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_questions.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_questions_serializer = ObservationQuestionSerializerResponse(results, many=True)
            else:
                observation_questions_serializer = ObservationQuestionSerializerRequest(observation_questions, many=True)

            return Resp(
                data_=observation_questions_serializer.data,
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
            observation_question_serializer = ObservationQuestionSerializerRequest(data=request.data)
            if observation_question_serializer.is_valid():
                observation_question_serializer.save()
                # History process pending

                try:
                    new_observation_question = ObservationQuestion.objects.get(id=observation_question_serializer.data['id'])
                except ObservationQuestion.DoesNotExist:
                    print("No existe inspection_affected")

                serializer_for_history = ObservationQuestionSerializerHistory(new_observation_question, data=observation_question_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="ObservationQuestion",action="CREATE", table_id=observation_question_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=observation_question_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=observation_question_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear observation_question", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class ObservationQuestionDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            observation_question = ObservationQuestion.objects.get(pk=pk)
            observation_question_serializer = ObservationQuestionSerializerResponse(observation_question)
            return Resp(data_=observation_question_serializer.data).send()
        except ObservationQuestion.DoesNotExist:
            return Resp(msg="ObservationQuestion no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            observation_question = ObservationQuestion.objects.get(pk=pk)
            observation_question_serializer = ObservationQuestionSerializerRequest(observation_question, request.data, partial=True)

            if observation_question_serializer.is_valid():
                observation_question_serializer.save()

                # History process pending

                serializer_for_history = ObservationQuestionSerializerHistory(observation_question, data=observation_question_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="ObservationQuestion",action="UPDATE", table_id=observation_question_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=observation_question_serializer.data, msg_="ObservationQuestion actualizada correctamente").send()
            
            return Resp(data_=observation_question_serializer.errors, msg_="Error al actualizar observation_question", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except ObservationQuestion.DoesNotExist:
            return Resp(msg_="ObservationQuestion no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            observation_question = ObservationQuestion.objects.get(pk=pk)
            
            observation_question.state = "0"
            observation_question.save()

            # History process pending

            serializer_for_history = ObservationQuestionSerializerHistory(observation_question)
            serializer_for_history_to_json = json.dumps( serializer_for_history.data, ensure_ascii = False ).replace('"', "'")
            history= History( table_name="ObservationQuestion", action="DELETE", table_id=serializer_for_history.data["id"], table_value=serializer_for_history_to_json )
            history.save()


            return Resp(msg_="ObservationQuestion eliminada correctamente").send()
        except ObservationQuestion.DoesNotExist:
            return Resp(msg_="ObservationQuestion no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class ObservationQuestionFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            observation_questions = ObservationQuestion.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('order')
            
            results = self.paginate_queryset(observation_questions, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_questions.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_questions_serializer = ObservationQuestionSerializerResponse(results, many=True)
            else:
                observation_questions_serializer = ObservationQuestionSerializerRequest(observation_questions, many=True)

            return Resp(
                data_ = observation_questions_serializer.data,
                pagination_ = is_paginated, 
                previous_link_ = previous_link, 
                next_link_ = next_link,
                count_ = count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

