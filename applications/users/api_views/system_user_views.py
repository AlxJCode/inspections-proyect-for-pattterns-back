import traceback
import json

from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction
from rest_framework.pagination import PageNumberPagination

from applications.users.models import SystemUser
from applications.history.models import History

from applications.users.serializers import SystemUserSerializerRequest, SystemUserSerializerResponse, SystemUserSerializerHistory
from applications.utils.resp_tools import Resp
from applications.utils.token_auth import TokenSimpleJWTAuth
from django.contrib.auth.hashers import check_password

class SystemUserListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            system_users = SystemUser.objects.select_related()
            
            results = self.paginate_queryset(system_users, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = system_users.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                system_users_serializer = SystemUserSerializerResponse(results, many=True)
            else:
                system_users_serializer = SystemUserSerializerRequest(system_users, many=True)

            return Resp(
                data_=system_users_serializer.data,
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
            # we encapsulate the request if there is an exception remove all executed process
            with transaction.atomic():
                dni = request.data.get('dni')
                existing_auth_user = User.objects.filter(username=dni)
                existing_system_user = SystemUser.objects.filter(dni=dni)
                
                if len(existing_auth_user) > 0 or len(existing_system_user) > 0:
                    return Resp(data_={"dni":dni}, msg="Usuario ya existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

                # we created a new auth user
                auth_user = User(username=request.data["dni"])
                auth_user.set_password(str(request.data["dni"]) + '0')
                auth_user.save()
                
                # we added created user to the information data
                request.data["auth_user"] = auth_user.pk

                system_user_serializer = SystemUserSerializerRequest(data=request.data)

                if system_user_serializer.is_valid():
                    system_user_serializer.save()
                    # History process pending

                    try:
                        new_systemuser = SystemUser.objects.get(id=system_user_serializer.data['id'])
                    except SystemUser.DoesNotExist:
                        print("No existe systemuser")

                    serializer_for_history = SystemUserSerializerHistory(new_systemuser, data=system_user_serializer.data, partial=True)
                    if serializer_for_history.is_valid():
                        serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                        history= History(table_name="Users",action="CREATE", table_id=system_user_serializer.data["id"],table_value=serializer_for_history_to_json)
                        history.save()


                    return Resp(data_=system_user_serializer.data, code_=status.HTTP_201_CREATED).send()
                # If system user serializer is not valid throw exception and remove the previous process
                raise Exception('System user serializer is not valid')
        except Exception:
            return Resp(msg_="Error al crear al usuario, verfique que todos los datos enviados sean los requeridos.", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

class SystemUserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            system_user = SystemUser.objects.get(pk=pk)
            system_user_serializer = SystemUserSerializerResponse(system_user)
            return Resp(data_=system_user_serializer.data).send()
        except SystemUser.DoesNotExist:
            return Resp(msg="Usuario no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            system_user = SystemUser.objects.get(pk=pk)
            system_user_serializer = SystemUserSerializerRequest(system_user, request.data, partial=True)

            if system_user_serializer.is_valid():
                system_user_serializer.save()

                # History process pending

                serializer_for_history = SystemUserSerializerHistory(system_user, data=system_user_serializer.data, partial=True)
                if serializer_for_history.is_valid():
                    serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
                    history= History(table_name="Users",action="UPDATE", table_id=system_user_serializer.data["id"],table_value=serializer_for_history_to_json)
                    history.save()

                
                return Resp(data_=system_user_serializer.data, msg_="Usuario actualizado correctamente").send()
            
            return Resp(data_=system_user_serializer.errors, msg_="Error al actualizar usuario", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except SystemUser.DoesNotExist:
            return Resp(msg_="Usuario no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            system_user = SystemUser.objects.get(pk=pk)
            
            system_user.state = False
            system_user.save()

            # History process pending

            serializer_for_history = SystemUserSerializerHistory(system_user)
            serializer_for_history_to_json = json.dumps(serializer_for_history.data, ensure_ascii=False).replace('"', "'")
            history= History(table_name="Users",action="DELETE", table_id=serializer_for_history.data["id"],table_value=serializer_for_history_to_json)
            history.save()


            return Resp(msg_="Usuario eliminado correctamente").send()
        except SystemUser.DoesNotExist:
            return Resp(msg_="Usuario no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class SystemUserFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            system_users = SystemUser.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(system_users, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = system_users.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                system_users_serializer = SystemUserSerializerResponse(results, many=True)
            else:
                system_users_serializer = SystemUserSerializerRequest(system_users, many=True)

            return Resp(
                data_=system_users_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()


class SystemUserPasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        type = TokenSimpleJWTAuth.get_type_systemuser_from_auth_id( request.user.pk )

        if type == "SA":
            try:
                system_user = SystemUser.objects.get( pk = request.data['system_user_id'] )
                auth_user = User.objects.get( pk = system_user.auth_user.pk )
                auth_user.set_password( request.data['new_password'] )
                auth_user.save()
                return Resp( msg_ = "Se actualizó la constraseña correctamente" ).send()
            except:
                tb = traceback.format_exc()
                print( tb )
                return Resp(
                    msg_ = "Ocurrió un error al actualizar contraseña, revise los campos.", 
                    status_= False,
                    code_ = status.HTTP_400_BAD_REQUEST,
                ).send()

        try:
            system_user = SystemUser.objects.get( pk = request.data['system_user_id'] )
            if system_user.auth_user.pk is not request.user.pk:
                return Resp(
                    msg_ = "No puede cambiar la contraseña de una usuario que no sea usted.", 
                    status_= False,
                    code_ = status.HTTP_400_BAD_REQUEST,
                ).send()

            value = check_password( request.data['current_password'], request.user.password )
            if not value:
                return Resp(
                    msg_ = "La contraseña actual no coincide", 
                    status_= True,
                    code_ = status.HTTP_202_ACCEPTED,
                ).send()

            auth_user = User.objects.get( pk = system_user.auth_user.pk )
            auth_user.set_password( request.data['new_password'] )
            auth_user.save()
            return Resp( msg_ = "Se actualizó la constraseña correctamente" ).send()
        except:
            tb = traceback.format_exc()
            print( tb )
            return Resp(
                msg_ = "Ocurrió un error al actualizar contraseña, revise los campos.", 
                status_= False,
                code_ = status.HTTP_400_BAD_REQUEST,
            ).send()