import traceback

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.inspections.models import InspectionUser
from applications.inspections.serializers import InspectionUserSerializerRequest, InspectionUserSerializerResponse
from applications.utils.resp_tools import Resp

class InspectionUserListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            inpection_users = InspectionUser.objects.select_related()
            
            results = self.paginate_queryset(inpection_users, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inpection_users.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inpection_users_serializer = InspectionUserSerializerResponse(results, many=True)
            else:
                inpection_users_serializer = InspectionUserSerializerRequest(inpection_users, many=True)

            return Resp(
                data_=inpection_users_serializer.data,
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
            inpection_user_serializer = InspectionUserSerializerRequest(data=request.data)
            if inpection_user_serializer.is_valid():
                inpection_user_serializer.save()
                # History process pending

                return Resp(data_=inpection_user_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=inpection_user_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear inpection_user", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class InspectionUserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            inpection_user = InspectionUser.objects.get(pk=pk)
            inpection_user_serializer = InspectionUserSerializerResponse(inpection_user)
            return Resp(data_=inpection_user_serializer.data).send()
        except InspectionUser.DoesNotExist:
            return Resp(msg="InspectionUser no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            inpection_user = InspectionUser.objects.get(pk=pk)
            inpection_user_serializer = InspectionUserSerializerRequest(inpection_user, request.data, partial=True)

            if inpection_user_serializer.is_valid():
                inpection_user_serializer.save()

                # History process pending
                return Resp(data_=inpection_user_serializer.data, msg_="InspectionUser actualizada correctamente").send()
            
            return Resp(data_=inpection_user_serializer.errors, msg_="Error al actualizar inpection_user", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except InspectionUser.DoesNotExist:
            return Resp(msg_="InspectionUser no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            inpection_user = InspectionUser.objects.get(pk=pk)
            inpection_user.delete()

            # History process pending


            return Resp(msg_="InspectionUser eliminada correctamente").send()
        except InspectionUser.DoesNotExist:
            return Resp(msg_="InspectionUser no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class InspectionUserFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            inspection_users = InspectionUser.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(inspection_users, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_users.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inpection_users_serializer = InspectionUserSerializerResponse(results, many=True)
            else:
                inpection_users_serializer = InspectionUserSerializerRequest(inspection_users, many=True)

            return Resp(
                data_=inpection_users_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()
