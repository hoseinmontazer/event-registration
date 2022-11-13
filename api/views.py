from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
import datetime
import time
import pytz
from django.utils import timezone

class Time_Table(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        userId = request.user.id
        content=[]
        try:
            print("hi try")
            checkTaskName = task.objects.raw('select * from api_time_table WHERE user_id =%s', [userId])
            for p in checkTaskName:
                print ("hi p",p)
                updateContent = {'summery_event': p.summery_event, 'start_time': p.start_time,'end_time': p.end_time}
                content.append(updateContent)
            return Response(content)
        except:
            return Response({"status":"400","mesage":"event not found"})


class CreateEvent(APIView):
    permission_classes = (IsAuthenticated,)
    print("ooooo")
    def post(self, request):
        #tz = 'Europe/Berlin'
        #print (timezone.now())
        user = request.user
        print(user)
        userId=request.user.id
        EventSummery = request.headers['EventSummery']
        #print(EventSummery)
        if (len(request.headers['StartTime']) == 0):
            print (len(request.headers['StartTime']))
            StartTime = None
            print ("ssss",StartTime)
        else:
            StartTime = datetime.datetime.fromtimestamp(int(request.headers['StartTime']))
        #print(StartTime)
        if (len(request.headers['EndTime']) == 0):
            print (len(request.headers['EndTime']))
            EndTime = None
        else:
            EndTime = datetime.datetime.fromtimestamp(int(request.headers['EndTime']))
        
        #print(request.user.id)
        if (StartTime != None and EndTime != None):
            try:
                if time_table.objects.filter(start_time=StartTime,user_id=userId) :
                    content = {'message': 'you have a event in this time please change time or edit your event'}
                    return Response(content)
                else:
                    t = time_table.objects.create(user_id=userId, summery_event=EventSummery, start_time=StartTime, end_time=EndTime)
                    content = {'message': 'your task has been successfully created'}
                    return Response(content)
            except :
                content = {'message': 'your task was not created, please try again'}
                return Response(content)
        elif (StartTime != None and EndTime == None):
                if time_table.objects.filter(start_time=StartTime,user_id=userId) :
                    content = {'message': 'you have a event in this time please change time or edit your event'}
                    return Response(content)
                else:
                    t = time_table.objects.create(user_id=userId, summery_event=EventSummery, start_time=StartTime)
                    content = {'message': 'your task has been successfully created'}
                    return Response(content)
        else:
                content = {'message': 'start time or endtime is empty'}
                return Response(content)            



class DeleteEvent(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        userId = request.user.id
        if (len(request.headers['StartTime']) == 0):
            print (len(request.headers['StartTime']))
            StartTime = None
            print ("ssss",StartTime)
        else:
            StartTime = datetime.datetime.fromtimestamp(int(request.headers['StartTime']))
            print(StartTime, userId)

        try:
            print("aaaa")
            GetEventId = time_table.objects.raw('select id from api_time_table WHERE start_time=%s AND user_id =%s',[str(StartTime), userId])
            if ( len(GetEventId) == 0 ):
                print("lllll")
                content = {'message': 'not avaiable event'}
                return Response(content)
                print("yyy",len(GetEventId))
            else:
                for p in GetEventId:
                    EventId=p.id
                    print("qqqqqq", EventId)
                    #print(p)
                if time_table.objects.filter(id=EventId):
                    print (EventId)
                    deleteTaskName = time_table.objects.filter(id=EventId).delete()
                    content = {'message': 'your task was been deleted'}
                    return Response(content)

        except Exception as e:
            content = {'message': 'your task was not deleted , try again'}
            return Response(content)


class EditEVENT (APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        userId = request.user.id
        EventSummery = request.headers['EventSummery']
        #print(EventSummery)
        if (len(request.headers['StartTime']) == 0):
            print (len(request.headers['StartTime']))
            StartTime = None
            print ("ssss",StartTime)
        else:
            StartTime = datetime.datetime.fromtimestamp(int(request.headers['StartTime']))
        #print(StartTime)
        if (len(request.headers['EndTime']) == 0):
            print (len(request.headers['EndTime']))
            EndTime = None
        else:
            EndTime = datetime.datetime.fromtimestamp(int(request.headers['EndTime']))
        try:
            print (userId,EventSummery,StartTime,EndTime)
            GetEventId = time_table.objects.raw('select id from api_time_table WHERE start_time=%s AND user_id =%s',[StartTime, userId])
            for p in GetEventId:
                EventId=p
                print("qqqqqq", EventId)
            if time_table.objects.filter(id=EventId) :
                editTaskName = task.objects.filter(id=EventId).update(summery_event=EventSummery,start_time=StartTime  ,end_time=EndTime)
                content = {'message': 'your task was been edited'}
                return Response(content)
            else:
                content = {'message': 'not editeable task'}
                return Response(content)
        except Exception as e:
            content = {'message': 'your task was not edited , try again'}
            return Response(content)


class TaskHistory(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        userId = request.user.id
        taskName = request.headers['task-name']
        content=[]
        try:
            getTaskId = task.objects.raw('select id from api_task WHERE task_name=%s AND user_id =%s',[taskName, userId])
            for p in getTaskId:
                taskId=p.id
            print('hiiiiiiiii',task.objects.filter(id=taskId))
            if task.objects.filter(id=taskId):
                checkTaskHistory = task.objects.raw('SELECT * FROM `api_task_detail` WHERE task_id =%s', [taskId])
                for p in checkTaskHistory:
                    updateContent = {'id': p.id,'comment': p.comment, 'start_task': p.start_task,'stop_task': p.stop_task}
                    content.append(updateContent)
                return Response(content)
        except Exception as e:
            content = {'message': 'can not find history , try again'}
            return Response(content)



class TaskEditHistory(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        userId = request.user.id
        historyTaskId = request.headers['history-id']

        tempComment = request.headers['comment']
        tempStartTask = request.headers['start-task']
        tempStopTask = request.headers['stop-task']
        print(tempStopTask,tempStartTask,tempComment)
        try:
            if task.objects.filter(id=historyTaskId):
                print('hiiii')
                editTaskName = task_detail.objects.filter(id=historyTaskId).update(comment=tempComment, start_task=tempStartTask,
                                                                     stop_task=tempStopTask)
                content = {'message': 'your history of id was been edited'}
                return Response(content)
        except Exception as e:
            content = {'message': 'can not find history id , try again'}
            return Response(content)



class TaskDeletHistory(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        userId = request.user.id
        historyTaskId = request.headers['history-id']
        #print(tempStopTask,tempStartTask,tempComment)
        try:
            if task.objects.filter(id=historyTaskId):
                print('hiiii')
                deleteTaskName = task_detail.objects.filter(id=historyTaskId).delete()
                content = {'message': 'your history of id was been deleted'}
                return Response(content)
        except Exception as e:
            content = {'message': 'can not find history id , try again'}
            return Response(content)