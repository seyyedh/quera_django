from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsCharityOwner, IsBenefactor
from charities.models import Task
from charities.serializers import (
    TaskSerializer, CharitySerializer, BenefactorSerializer
)


class BenefactorRegistration(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        serializer_name = BenefactorSerializer(data = request.data)
        if serializer_name.is_valid():
            serializer_name.save(user = request.user)
            return Response({'message': 'this is ok'})
        return Response({'message': serializer_name.errors})

class CharityRegistration(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        charity_user = CharitySerializer(data = request.data)
        if charity_user.is_valid():
            charity_user.save(user = request.user)
            return Response({'message':'this is OK'})
        return Response({'message': charity_user.errors})

class Tasks(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all_related_tasks_to_user(self.request.user)

    def post(self, request, *args, **kwargs):
        data = {
            **request.data,
            "charity_id": request.user.charity.id
        }
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsCharityOwner, ]

        return [permission() for permission in self.permission_classes]

    def filter_queryset(self, queryset):
        filter_lookups = {}
        for name, value in Task.filtering_lookups:
            param = self.request.GET.get(value)
            if param:
                filter_lookups[name] = param
        exclude_lookups = {}
        for name, value in Task.excluding_lookups:
            param = self.request.GET.get(value)
            if param:
                exclude_lookups[name] = param

        return queryset.filter(**filter_lookups).exclude(**exclude_lookups)

class TaskRequest(APIView):
     permission_classes = (IsAuthenticated,)
     def get(self,task_id):
         task = get_object_or_404(Task,task_id = task_id)
         if task.state != 'PENDING':
             return Response(data={'detail': 'This task is not pending.'},
                             status=status.HTTP_404_NOT_FOUND)
         else:
             task_benefactor = Task.objects.filter(assigned_benefactor__task__charity_id=task_id)
             task_benefactor.state = 'W'
             Task.assigned_benefactor = task_benefactor
             task_benefactor.save()
             return Response(data={'detail': 'Request sent.'},
                             status=status.HTTP_200_OK)




class TaskResponse(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,task_id):
        response = TaskSerializer(data = request.data)

        status_id_task = Task.objects.filter(assigned_benefactor__task__charity_id=task_id)
        statuss = Task.objects.filter(assigned_benefactor__task__charity_id=task_id).values("state")
        if response == 'A':
            status_id_task.state = "ASSIGNED"
            status_id_task.save()
            return Response(status=status.HTTP_200_OK,
                     data={'detail': 'Response sent.'})
        elif response == 'R':
            status_id_task.state = "PENDING"
            status_id_task.assigned_benefactor = 'None'
            status_id_task.save()
            return Response(status=status.HTTP_200_OK,
                     data={'detail': 'Response sent.'})
        elif statuss != 'WAITING':
            return Response(status=status.HTTP_404_NOT_FOUND,
                     data={'detail': 'This task is not waiting.'})
        else:
            return Response(status= status.HTTP_400_BAD_REQUEST,
                     data={'detail': 'Required field ("A" for accepted / "R" for rejected)'})


class DoneTask(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        task_name = get_object_or_404(Task,task_id = request.task_id)
        # task_id_model = Task.objects.filter(assigned_benefactor__task__charity_id=task_id).values("state")
        if task_name.state != 'ASSIGNED':
            return Response(status = status.HTTP_404_NOT_FOUND,
                            data={'detail': 'Task is not assigned yet.'})
        else:
            task_name.state = 'DONE'
            task_name.save()
            return Response(status=status.HTTP_200_OK,
                            data={'detail': 'Task has been done successfully.'})

