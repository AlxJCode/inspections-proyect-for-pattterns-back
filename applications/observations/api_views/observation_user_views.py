import traceback

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.observations.models import ObservationUser
from applications.observations.serializers import ObservationUserSerializerRequest, ObservationUserSerializerResponse
from applications.utils.resp_tools import Resp

class ObservationUserListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            observation_users = ObservationUser.objects.select_related()
            
            results = self.paginate_queryset(observation_users, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_users.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_users_serializer = ObservationUserSerializerResponse(results, many=True)
            else:
                observation_users_serializer = ObservationUserSerializerRequest(observation_users, many=True)

            return Resp(
                data_=observation_users_serializer.data,
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
            observation_user_serializer = ObservationUserSerializerRequest(data=request.data)
            if observation_user_serializer.is_valid():
                observation_user_serializer.save()
                # History process pending

                return Resp(data_=observation_user_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=observation_user_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            return Resp(msg_="Ocurrió un error al crear observation_user", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class ObservationUserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            observation_user = ObservationUser.objects.get(pk=pk)
            observation_user_serializer = ObservationUserSerializerResponse(observation_user)
            return Resp(data_=observation_user_serializer.data).send()
        except ObservationUser.DoesNotExist:
            return Resp(msg="ObservationUser no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            observation_user = ObservationUser.objects.get(pk=pk)
            observation_user_serializer = ObservationUserSerializerRequest(observation_user, request.data, partial=True)

            if observation_user_serializer.is_valid():
                observation_user_serializer.save()

                # History process pending
                return Resp(data_=observation_user_serializer.data, msg_="ObservationUser actualizada correctamente").send()
            
            return Resp(data_=observation_user_serializer.errors, msg_="Error al actualizar observation_user", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except ObservationUser.DoesNotExist:
            return Resp(msg_="ObservationUser no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            observation_user = ObservationUser.objects.get(pk=pk)
            observation_user.save()

            # History process pending


            return Resp(msg_="ObservationUser eliminada correctamente").send()
        except ObservationUser.DoesNotExist:
            return Resp(msg_="ObservationUser no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class ObservationUserFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            observation_users = ObservationUser.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(observation_users, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = observation_users.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                observation_users_serializer = ObservationUserSerializerResponse(results, many=True)
            else:
                observation_users_serializer = ObservationUserSerializerRequest(observation_users, many=True)

            return Resp(
                data_=observation_users_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

