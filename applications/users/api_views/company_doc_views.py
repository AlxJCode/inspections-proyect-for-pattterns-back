import traceback
import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.users.models import CompanyDoc
from applications.history.models import History
from applications.users.serializers import CompanyDocSerializerRequest, CompanyDocSerializerResponse, CompanyDocSerializerHistory
from applications.utils.resp_tools import Resp

class CompanyDocListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            company_docs = CompanyDoc.objects.select_related()
            
            results = self.paginate_queryset(company_docs, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = company_docs.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                company_docs_serializer = CompanyDocSerializerResponse(results, many=True)
            else:
                company_docs_serializer = CompanyDocSerializerRequest(company_docs, many=True)

            return Resp(
                data_=company_docs_serializer.data,
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
            company_doc_serializer = CompanyDocSerializerRequest(data=request.data)
            if company_doc_serializer.is_valid():
                company_doc_serializer.save()
                # History process pending

                try:
                    new_company_doc = CompanyDoc.objects.get(id=company_doc_serializer.data['id'])
                except CompanyDoc.DoesNotExist:
                    print("No existe company_doc")

                serializer_for_history = CompanyDocSerializerHistory(new_company_doc, data=company_doc_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="CompanyDoc",action="CREATE", table_id=company_doc_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=company_doc_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=company_doc_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear company_doc", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class CompanyDocDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            company_doc = CompanyDoc.objects.get(pk=pk)
            company_doc_serializer = CompanyDocSerializerResponse(company_doc)
            return Resp(data_=company_doc_serializer.data).send()
        except CompanyDoc.DoesNotExist:
            return Resp(msg="CompanyDoc no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            company_doc = CompanyDoc.objects.get(pk=pk)
            company_doc_serializer = CompanyDocSerializerRequest(company_doc, request.data, partial=True)

            if company_doc_serializer.is_valid():
                company_doc_serializer.save()

                # History process pending
                serializer_for_history = CompanyDocSerializerHistory(company_doc, data=company_doc_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="CompanyDoc",action="UPDATE", table_id=company_doc_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                
                return Resp(data_=company_doc_serializer.data, msg_="CompanyDoc actualizada correctamente").send()
            
            return Resp(data_=company_doc_serializer.errors, msg_="Error al actualizar company_doc", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except CompanyDoc.DoesNotExist:
            return Resp(msg_="CompanyDoc no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            company_doc = CompanyDoc.objects.get(pk=pk)
            
            company_doc.state = False
            company_doc.save()

            # History process pending

            serializer_for_history = CompanyDocSerializerHistory(company_doc)
            serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
            history= History(table_name="CompanyDoc",action="DELETE", table_id=serializer_for_history.data["id"],table_value=serializer_for_history_to_json)
            history.save()

            return Resp(msg_="CompanyDoc eliminada correctamente").send()
        except CompanyDoc.DoesNotExist:
            return Resp(msg_="CompanyDoc no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class CompanyDocFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            company_docs = CompanyDoc.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(company_docs, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = company_docs.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                company_docs_serializer = CompanyDocSerializerResponse(results, many=True)
            else:
                company_docs_serializer = CompanyDocSerializerRequest(company_docs, many=True)

            return Resp(
                data_=company_docs_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()
