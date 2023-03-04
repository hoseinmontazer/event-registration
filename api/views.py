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
            pubDate = request.headers['pubDate']
            if pubDate == "null":
                print ("notavalable")
                AllEvent = time_table.objects.raw('select * from api_time_table WHERE user_id =%s', [userId])
                #AllEvent = time_table.objects.raw('SELECT * FROM `api_time_table` WHERE user_id =2')
            else:
                #print("aaaaaaaaa", pubDate)
                #AllEvent = time_table.objects.raw('select * from api_time_table WHERE user_id =%s AND ', [userId])
                AllEvent = time_table.objects.raw('SELECT * FROM api_time_table WHERE  date(start_time) = %s ', [pubDate])

            for p in AllEvent:
                #print ("hi p",p)
                updateContent = {'summery_event': p.summery_event, 'start_time': p.start_time,'end_time': p.end_time}
                content.append(updateContent)
            return Response(content)
        except:
            return Response({"status":"400","message":"event not found or publish date not avalable"})


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
            print("ssss2",StartTime)
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

        #check start time is avaliable
        if (len(request.headers['StartTime']) == 0):
            print (len(request.headers['StartTime']))
            StartTime = None
            print ("StartTime is :",StartTime)
        else:
            StartTime = datetime.datetime.fromtimestamp(int(request.headers['StartTime']))
            print("StartTime is :",StartTime)


        #check start time is temporary event summery 
        if (len(request.headers['TempEventSummery']) == 0):
            print (len(request.headers['TempEventSummery']))
            TempEventSummery = None
            print ("TempEventSummery is :",TempEventSummery)
        else:
            TempEventSummery = request.headers['TempEventSummery']
            print("TempEventSummery is :",TempEventSummery)

        #check temporary start time is avaliable
        if (len(request.headers['TempStartTime']) == 0):
            print (len(request.headers['TempStartTime']))
            TempStartTime = None
            print ("ssss",TempStartTime)
        else:
            TempStartTime = datetime.datetime.fromtimestamp(int(request.headers['TempStartTime']))
            print("TempStartTime is :",TempStartTime)

        #check  temporary end time is avaliable
        if (len(request.headers['TempEndTime']) == 0):
            print (len(request.headers['TempEndTime']))
            TempEndTime = None
        else:
            TempEndTime = datetime.datetime.fromtimestamp(int(request.headers['TempEndTime']))
            print("TempEndTime is :",TempEndTime)



        try:
            if ( StartTime == None ):
                    content = {'message': 'start time can not be empty or null'}
                    return Response(content) 
            else:
                print ("alll parameters is :",userId,TempEventSummery,TempStartTime,TempEndTime,StartTime)
                GetEventId = time_table.objects.raw('select * from api_time_table WHERE start_time=%s AND user_id =%s',[StartTime, userId])
                if len(GetEventId) == 0 :
                    content = {'message': 'query is not valid'}
                    return Response(content)
                else:
                    print("get event id:", GetEventId)
                    for p in GetEventId:
                        EventId=p.id
                        EventSummery=p.summery_event
                        StartTime=p.start_time                    
                        EndTime=p.end_time
                        print("qqqqqq", EventId ,EventSummery, StartTime, EndTime )
                    if time_table.objects.filter(id=EventId) and TempEventSummery == None and TempStartTime == None and TempEndTime == None:
                        editTaskName = time_table.objects.filter(id=EventId).update(summery_event=EventSummery,start_time=StartTime  ,end_time=EndTime)
                        content = {'message': 'your task was been edited without any change'}
                        return Response(content)
                    elif time_table.objects.filter(id=EventId) and TempEventSummery != None and TempStartTime != None and TempEndTime != None:
                        editTaskName = time_table.objects.filter(id=EventId).update(summery_event=TempEventSummery,start_time=TempStartTime  ,end_time=TempEndTime)
                        content = {'message': 'your task was been edited with change the start time and end amd summery'}
                        return Response(content) 
                    elif time_table.objects.filter(id=EventId) and TempEventSummery == None and TempStartTime != None and TempEndTime != None:
                        editTaskName = time_table.objects.filter(id=EventId).update(summery_event=EventSummery,start_time=TempStartTime  ,end_time=TempEndTime)
                        content = {'message': 'your task was been edited with change start and end time'}
                        return Response(content)
                    elif time_table.objects.filter(id=EventId) and TempEventSummery == None and TempStartTime == None and TempEndTime != None:
                        editTaskName = time_table.objects.filter(id=EventId).update(summery_event=EventSummery,start_time=StartTime  ,end_time=TempEndTime)
                        content = {'message': 'your task was been edited with change the end time'}
                        return Response(content) 

                    elif time_table.objects.filter(id=EventId) and TempEventSummery == None and TempStartTime != None and TempEndTime == None:
                        editTaskName = time_table.objects.filter(id=EventId).update(summery_event=EventSummery,start_time=TempStartTime  ,end_time=EndTime)
                        content = {'message': 'your task was been edited with change the start time'}
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