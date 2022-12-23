import traceback
import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.inspections.models import InspectionAssessment
from applications.history.models import History
from applications.inspections.serializers import InspectionAssessmentSerializerRequest, InspectionAssessmentSerializerResponse, InspectionAssessmentSerializerHistory
from applications.utils.resp_tools import Resp

class InspectionAssessmentListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            inspection_assessments = InspectionAssessment.objects.select_related()
            
            results = self.paginate_queryset(inspection_assessments, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_assessments.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_assessments_serializer = InspectionAssessmentSerializerResponse(results, many=True)
            else:
                inspection_assessments_serializer = InspectionAssessmentSerializerRequest(inspection_assessments, many=True)

            return Resp(
                data_=inspection_assessments_serializer.data,
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
            inspection_assessment_serializer = InspectionAssessmentSerializerRequest(data=request.data)
            if inspection_assessment_serializer.is_valid():
                inspection_assessment_serializer.save()
                # History process pending

                try:
                    new_inspection_assessment = InspectionAssessment.objects.get(id=inspection_assessment_serializer.data['id'])
                except InspectionAssessment.DoesNotExist:
                    print("No existe inspection_assessment")

                serializer_for_history = InspectionAssessmentSerializerHistory(new_inspection_assessment, data=inspection_assessment_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="InspectionAssessment",action="CREATE", table_id=inspection_assessment_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=inspection_assessment_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=inspection_assessment_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear inspection_assessment", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class InspectionAssessmentDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            inspection_assessment = InspectionAssessment.objects.get(pk=pk)
            inspection_assessment_serializer = InspectionAssessmentSerializerResponse(inspection_assessment)
            return Resp(data_=inspection_assessment_serializer.data).send()
        except InspectionAssessment.DoesNotExist:
            return Resp(msg="InspectionAssessment no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            inspection_assessment = InspectionAssessment.objects.get(pk=pk)
            inspection_assessment_serializer = InspectionAssessmentSerializerRequest(inspection_assessment, request.data, partial=True)

            if inspection_assessment_serializer.is_valid():
                inspection_assessment_serializer.save()

                # History process pending

                serializer_for_history = InspectionAssessmentSerializerHistory(inspection_assessment, data=inspection_assessment_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="InspectionAssessment",action="UPDATE", table_id=inspection_assessment_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=inspection_assessment_serializer.data, msg_="InspectionAssessment actualizada correctamente").send()
            
            return Resp(data_=inspection_assessment_serializer.errors, msg_="Error al actualizar inspection_assessment", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except InspectionAssessment.DoesNotExist:
            return Resp(msg_="InspectionAssessment no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            inspection_assessment = InspectionAssessment.objects.get(pk=pk)
            
            inspection_assessment.state = False
            inspection_assessment.save()

            # History process pending

            serializer_for_history = InspectionAssessmentSerializerHistory(inspection_assessment)
            serializer_for_history_to_json = json.dumps( serializer_for_history.data, ensure_ascii = False ).replace('"', "'")
            history= History( table_name="InspectionType", action="DELETE", table_id=serializer_for_history.data["id"], table_value=serializer_for_history_to_json )
            history.save()


            return Resp(msg_="InspectionAssessment eliminada correctamente").send()
        except InspectionAssessment.DoesNotExist:
            return Resp(msg_="InspectionAssessment no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class InspectionAssessmentFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            inspection_assessments = InspectionAssessment.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(inspection_assessments, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_assessments.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_assessments_serializer = InspectionAssessmentSerializerResponse(results, many=True)
            else:
                inspection_assessments_serializer = InspectionAssessmentSerializerRequest(inspection_assessments, many=True)

            return Resp(
                data_=inspection_assessments_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()
