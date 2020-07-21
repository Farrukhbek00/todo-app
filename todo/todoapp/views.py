from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer

from .models import Task


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        "Task List": '/todoapp/task-list/',
        'Task Detail': '/todoapp/task-detail/<str:pk>/',
        'Task Create': '/todoapp/task-create/',
        'Task Update': '/todoapp/task-update/<str:pk>/',
        'Task Delete': '/todoapp/task-delete/<str:pk>/'
    }

    return Response(api_urls)


@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all().order_by('-id')
    serializer = TaskSerializer(tasks, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def task_detail(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(task, many=False)

    return Response(serializer.data)

@api_view(['POST'])
def task_create(request):

    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def task_update(request, pk):
    old_task = Task.objects.get(id=pk)

    serializer = TaskSerializer(instance=old_task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def task_delete(request, pk):
    task = Task.objects.get(id=pk)

    task.delete()

    return Response('Deleted')
