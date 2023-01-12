import traceback

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from applications.inspections.models import InspectionDetailResponsible
from applications.users.models import SystemUser
from applications.inspections.serializers import InspectionDetailResponsibleSerializerRequest, InspectionDetailResponsibleSerializerResponse
from applications.utils.resp_tools import Resp
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

class InspectionDetailResponsibleListView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            inspection_detail_responsibles = InspectionDetailResponsible.objects.select_related()
            
            results = self.paginate_queryset(inspection_detail_responsibles, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_detail_responsibles.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_detail_responsibles_serializer = InspectionDetailResponsibleSerializerRequest(results, many=True)
            else:
                inspection_detail_responsibles_serializer = InspectionDetailResponsibleSerializerResponse(inspection_detail_responsibles, many=True)

            return Resp(
                data_=inspection_detail_responsibles_serializer.data,
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
            inspection_detail_responsible_serializer = InspectionDetailResponsibleSerializerRequest(data=request.data)
            if inspection_detail_responsible_serializer.is_valid():
                inspection_detail_responsible_serializer.save()
                
                inspection = InspectionDetailResponsible.objects.filter( id = inspection_detail_responsible_serializer.data['id'] ).values( 'id', 'created' ).last()
                responsible = SystemUser.objects.filter( dni = inspection_detail_responsible_serializer.data['user_dni'] ).values('auth_user').last( )

                devices_to_send = FCMDevice.objects.filter(
                    user__in = responsible
                )

                try:
                    devices_to_send.send_message(
                        Message(
                            notification = Notification(
                                title = "FUE ASIGNADO COMO RESPONSABLE DE UNA INSPECCIÓN",
                                body = """Fecha: {0}""".format(
                                    inspection.created,  
                                ),
                            ),
                            data = {
                                "id": str( inspection.id ),
                                "module": "inspections",
                                "type": "assigned",
                            },
                            
                        )
                    )
                    print( "Notificación enviada" )
                except:
                    print("Error al enviar notificación")
                    print( traceback.format_exc() )

                return Resp(data_=inspection_detail_responsible_serializer.data, code_=status.HTTP_201_CREATED).send()
            
            return Resp(msg_=inspection_detail_responsible_serializer.errors, code_=status.HTTP_400_BAD_REQUEST, status_=False).send()

        except Exception:
            print( traceback.format_exc() )
            return Resp(msg_="Ocurrió un error al crear inspection_detail_responsible", status_=False, code_=status.HTTP_500_INTERNAL_SERVER_ERROR).send()

class InspectionDetailResponsibleDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            inspection_detail_responsible = InspectionDetailResponsible.objects.get(pk=pk)
            inspection_detail_responsible_serializer = InspectionDetailResponsibleSerializerResponse(inspection_detail_responsible)
            return Resp(data_=inspection_detail_responsible_serializer.data).send()
        except InspectionDetailResponsible.DoesNotExist:
            return Resp(msg="InspectionDetailResponsible no existente", status_=False, code_=status.HTTP_400_BAD_REQUEST).send()

    def put(self, request, pk):
        try:
            inspection_detail_responsible = InspectionDetailResponsible.objects.get(pk=pk)
            inspection_detail_responsible_serializer = InspectionDetailResponsibleSerializerRequest(inspection_detail_responsible, request.data, partial=True)

            if inspection_detail_responsible_serializer.is_valid():
                inspection_detail_responsible_serializer.save()

                # History process pending
                return Resp(data_=inspection_detail_responsible_serializer.data, msg_="InspectionDetailResponsible actualizada correctamente").send()
            
            return Resp(data_=inspection_detail_responsible_serializer.errors, msg_="Error al actualizar inspection_detail_responsible", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        except InspectionDetailResponsible.DoesNotExist:
            return Resp(msg_="InspectionDetailResponsible no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()
        
    def delete(self, request, pk):
        try:
            inspection_detail_responsible = InspectionDetailResponsible.objects.get(pk=pk)
            inspection_detail_responsible.delete()

            # History process pending


            return Resp(msg_="InspectionDetailResponsible eliminada correctamente").send()
        except InspectionDetailResponsible.DoesNotExist:
            return Resp(msg_="InspectionDetailResponsible no existente", status=False, code_=status.HTTP_400_BAD_REQUEST).send()

class InspectionDetailResponsibleFiltersView(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            filter = request.data.get("filter", {})
            exclude = request.data.get("exclude", {})

            inspection_detail_responsibles = InspectionDetailResponsible.objects.filter( **filter ).exclude( **exclude ).select_related().order_by('-created')
            
            results = self.paginate_queryset(inspection_detail_responsibles, request, view=self)
            previous_link = self.get_previous_link()
            next_link = self.get_next_link()
            count = inspection_detail_responsibles.count()

            is_paginated = bool(request.GET.get('page', None))

            if is_paginated:
                inspection_detail_responsibles_serializer = InspectionDetailResponsibleSerializerResponse(results, many=True)
            else:
                inspection_detail_responsibles_serializer = InspectionDetailResponsibleSerializerRequest(inspection_detail_responsibles, many=True)

            return Resp(
                data_=inspection_detail_responsibles_serializer.data,
                pagination_=is_paginated, 
                previous_link_=previous_link, 
                next_link_=next_link,
                count_=count,
            ).send()

        except:
            tb = traceback.format_exc()
            print(tb)
            return Resp(msg_=tb, status_=False, code_=status.HTTP_400_BAD_REQUEST).send()
