import traceback
import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.observations.models import ObservationAssessment
from applications.history.models import History
from applications.observations.serializers import ObservationAssessmentSerializerRequest, ObservationAssessmentSerializerResponse, ObservationAssessmentSerializerHistory
from applications.utils.resp_tools import Resp

class ObservationAssessmentListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            observation_assessments = ObservationAssessment.objects.select_related()
            
            results = self.paginate_queryset(observation_assessments, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_assessments.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_assessments_serializer = ObservationAssessmentSerializerResponse(results, many=True)
            else:
                observation_assessments_serializer = ObservationAssessmentSerializerRequest(observation_assessments, many=True)

            return Resp(
                data_=observation_assessments_serializer.data,
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
            observation_assessment_serializer = ObservationAssessmentSerializerRequest(data=request.data)
            if observation_assessment_serializer.is_valid():
                observation_assessment_serializer.save()
                # History process pending

                try:
                    new_observation_assessment = ObservationAssessment.objects.get(id=observation_assessment_serializer.data['id'])
                except ObservationAssessment.DoesNotExist:
                    print("No existe observation_assessment")

                serializer_for_history = ObservationAssessmentSerializerHistory(new_observation_assessment, data=observation_assessment_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="ObservationAssessment",action="CREATE", table_id=observation_assessment_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=observation_assessment_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=observation_assessment_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear observation_assessment", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class ObservationAssessmentDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            observation_assessment = ObservationAssessment.objects.get(pk=pk)
            observation_assessment_serializer = ObservationAssessmentSerializerResponse(observation_assessment)
            return Resp(data_=observation_assessment_serializer.data).send()
        except ObservationAssessment.DoesNotExist:
            return Resp(msg="ObservationAssessment no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            observation_assessment = ObservationAssessment.objects.get(pk=pk)
            observation_assessment_serializer = ObservationAssessmentSerializerRequest(observation_assessment, request.data, partial=True)

            if observation_assessment_serializer.is_valid():
                observation_assessment_serializer.save()

                # History process pending

                serializer_for_history = ObservationAssessmentSerializerHistory(observation_assessment, data=observation_assessment_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="ObservationAssessment",action="UPDATE", table_id=observation_assessment_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=observation_assessment_serializer.data, msg_="ObservationAssessment actualizada correctamente").send()
            
            return Resp(data_=observation_assessment_serializer.errors, msg_="Error al actualizar observation_assessment", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except ObservationAssessment.DoesNotExist:
            return Resp(msg_="ObservationAssessment no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            observation_assessment = ObservationAssessment.objects.get(pk=pk)
            
            observation_assessment.state = False
            observation_assessment.save()

            # History process pending

            serializer_for_history = ObservationAssessmentSerializerHistory(observation_assessment)
            serializer_for_history_to_json = json.dumps( serializer_for_history.data, ensure_ascii = False ).replace('"', "'")
            history= History( table_name="ObservationAssessment", action="DELETE", table_id=serializer_for_history.data["id"], table_value=serializer_for_history_to_json )
            history.save()


            return Resp(msg_="ObservationAssessment eliminada correctamente").send()
        except ObservationAssessment.DoesNotExist:
            return Resp(msg_="ObservationAssessment no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class ObservationAssessmentFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            observation_assessments = ObservationAssessment.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(observation_assessments, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_assessments.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_assessments_serializer = ObservationAssessmentSerializerResponse(results, many=True)
            else:
                observation_assessments_serializer = ObservationAssessmentSerializerRequest(observation_assessments, many=True)

            return Resp(
                data_=observation_assessments_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()
