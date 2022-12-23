import traceback
import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.users.models import Company
from applications.history.models import History
from applications.users.serializers import CompanySerializerRequest, CompanySerializerResponse, CompanySerializerHistory
from applications.utils.resp_tools import Resp

class CompanyListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            companies = Company.objects.select_related()
            
            results = self.paginate_queryset(companies, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = companies.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                companies_serializer = CompanySerializerResponse(results, many=True)
            else:
                companies_serializer = CompanySerializerRequest(companies, many=True)

            return Resp(
                data_=companies_serializer.data,
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
            company_serializer = CompanySerializerRequest(data=request.data)
            if company_serializer.is_valid():
                company_serializer.save()
                # History process pending

                try:
                    new_area = Company.objects.get(id=company_serializer.data['id'])
                except Company.DoesNotExist:
                    print("No existe empresa")

                serializer_for_history = CompanySerializerHistory(new_area, data=company_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="Company",action="CREATE", table_id=company_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                return Resp(data_=company_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=company_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear empresa", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class CompanyDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            company_serializer = CompanySerializerResponse(company)
            return Resp(data_=company_serializer.data).send()
        except Company.DoesNotExist:
            return Resp(msg="Empresa no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            company_serializer = CompanySerializerRequest(company, request.data, partial=True)

            if company_serializer.is_valid():
                company_serializer.save()

                # History process pending

                serializer_for_history = CompanySerializerHistory(company, data=company_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="Company",action="UPDATE", table_id=company_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()
                
                return Resp(data_=company_serializer.data, msg_="Empresa actualizada correctamente").send()
            
            return Resp(data_=company_serializer.errors, msg_="Error al actualizar empresa", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except Company.DoesNotExist:
            return Resp(msg_="Empresa no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            
            company.state = False
            company.save()

            # History process pending

            serializer_for_history = CompanySerializerHistory(company)
            serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
            history= History(table_name="Company",action="DELETE", table_id=serializer_for_history.data["id"],table_value=serializer_for_history_to_json)
            history.save()

            return Resp(msg_="Empresa eliminada correctamente").send()
        except Company.DoesNotExist:
            return Resp(msg_="Empresa no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class CompanyFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            companies = Company.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(companies, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = companies.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                companies_serializer = CompanySerializerResponse(results, many=True)
            else:
                companies_serializer = CompanySerializerRequest(companies, many=True)

            return Resp(
                data_=companies_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()
