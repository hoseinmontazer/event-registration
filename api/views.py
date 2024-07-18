import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .models import *
import datetime
from django.utils import timezone
import json
from django.core.cache import cache
import string
import random


#logger = logging.getLogger(__name__)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from djoser.serializers import UserCreateSerializer
from rest_framework.permissions import AllowAny

class CustomUserCreateView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access the signup endpoint
    print("hiiiiiiiiii")
    def post(self, request, *args, **kwargs):
        # Check for the user_key in the headers
        print (request.headers)

        userKey = request.headers.get('userKey')
        print(userKey)
        if not userKey:
            return Response({'error': 'userKey not available'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetInvitation(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        invite_str_value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=40))
        print(invite_str_value)

        invite_str_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        print(invite_str_key)

        cache.set(invite_str_key, invite_str_value , 1800)
        print("pppppppppppp")
        print(invite_str_key,"---------",invite_str_value)
        key= cache.get(invite_str_key)
        print(key)
        return Response({"status":"200","message":"/api/invitation/"+invite_str_key+"/"+invite_str_value})
    

class CheckInvitation(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        invite_str_key = request.headers['invitestrkey']
        print("0000000")
        invite_value= cache.get(invite_str_key)
        print(invite_value)
        return Response({"status":"200","message":"/api/invitation/"})
    


class Time_Table(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        userId = request.user.id
        print("get time tabe:",userId)

        content=[]
        try:
            if 'pubDate' in request.headers:
                pubDate = request.headers['pubDate']
                print(pubDate)
                AllEvent = time_table.objects.raw('SELECT * FROM api_time_table WHERE  date(start_time) = %s AND user_id=%s ', [pubDate,userId])
                # if not pubDate :
                #     print ("not available")
                #     AllEvent = time_table.objects.raw('select * from api_time_table WHERE user_id =%s', [userId])
                #     #AllEvent = time_table.objects.raw('SELECT * FROM `api_time_table` WHERE user_id =2')
            else:
                AllEvent = time_table.objects.raw('select * from api_time_table WHERE user_id =%s', [userId])
                    #print("aaaaaaaaa", pubDate)
                    #AllEvent = time_table.objects.raw('select * from api_time_table WHERE user_id =%s AND ', [userId])
                    #AllEvent = time_table.objects.raw('SELECT * FROM api_time_table WHERE  date(start_time) = %s AND user_id=%s ', [pubDate,userId])

            for p in AllEvent:
                #print ("hi p",p)
                updateContent = {'id': p.id ,'title_event': p.title_event,'summery_event': p.summery_event, 'start_time': p.start_time,'end_time': p.end_time}
                content.append(updateContent)
            return Response(content)
        except:
            return Response({"status":"400","message":"event not found or publish date not avalable"})


class CreateEvent(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        #tz = 'Europe/Berlin'
        #print (timezone.now())
        user = request.user
        print(user)
        userId=request.user.id
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print("body",body)
        # EventTitle = body['EventTitle']
        # EventSummery = body['EventSummery']
        #print(EventSummery)


        if (len(body['EventTitle']) == 0):
            print (len(body['EventTitle']))
            EventTitle = None
        else:
            EventTitle = body['EventTitle']

        if (len(body['EventSummery']) == 0):
            print (len(body['EventSummery']))
            EventSummery = None
        else:
            EventSummery = body['EventSummery']

        if (len(body['StartTime']) == 0):
            print (len(body['StartTime']))
            StartTime = None
            print ("ssss",StartTime)
        else:
            StartTime = datetime.datetime.fromtimestamp(int(body['StartTime']))
            print("ssss2",StartTime)

        if (len(body['EndTime']) == 0):
            print (len(body['EndTime']))
            EndTime = None
        else:
            EndTime = datetime.datetime.fromtimestamp(int(body['EndTime']))
        

        #print(request.user.id)
        if (StartTime != None and EndTime != None and EventTitle!= None):
            try:
                if time_table.objects.filter(start_time=StartTime,user_id=userId) :
                    content = {'status' : '400' ,'message': 'you have a event in this time please change time or edit your event'}
                    return Response(content)
                else:
                    t = time_table.objects.create(user_id=userId, summery_event=EventSummery, start_time=StartTime, end_time=EndTime ,title_event=EventTitle)
                    content = {'status' : '200' ,'message': 'your task has been successfully created'}
                    return Response(content)
            except :
                content = {'status' : '400' ,'message': 'your task was not created, please try again'}
                return Response(content)
        elif (StartTime != None and EndTime == None and EventTitle!= None):
                if time_table.objects.filter(start_time=StartTime,user_id=userId) :
                    content = {'status' : '400' ,'message': 'you have a event in this time please change time or edit your event'}
                    return Response(content)
                else:
                    t = time_table.objects.create(user_id=userId, summery_event=EventSummery, start_time=StartTime, title_event=EventTitle)
                    content = {'status' : '200' ,'message': 'your task has been successfully created'}
                    return Response(content)
        else:
                content = {'status' : '400' ,'message': 'start time or endtime or title is empty'}
                return Response(content)            





class DeleteEvent(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            print("try delete")
            userId = request.user.id
            print ("userId is: " ,userId)
            taskId = request.headers['taskId']
            print ("taskId is: " ,taskId)
            print (len(taskId))
            # GetEventId = time_table.objects.raw('select id from api_time_table WHERE start_time=%s AND user_id =%s',[str(StartTime), userId])
            if ( len(taskId) == 0 ):
                print("lllll")
                content = {'message': 'not avaiable event'}
                return Response(content)
                print("yyy",len(taskId))
            else:
                print ("eeeeeee")
                if time_table.objects.filter(id=taskId):
                    print ("lllllll",taskId)
                    deleteTaskId = time_table.objects.filter(id=taskId).delete()
                    content = {'message': 'your task was been deleted'}
                    return Response(content)
                else:
                    content = {'message': 'task id not available'}
                    return Response(content)


        except Exception as e:
            content = {'message': 'your task was not deleted , try again'}
            return Response(content)


class EditEVENT (APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        userId = request.user.id
        try:
            print("try edit")
            userId = request.user.id
            print ("userId is: " ,userId)
            taskId = request.headers['taskId']
            print ("taskId is: " ,taskId)
            #check start time is avaliable
            if 'taskId' in request.headers:
                print("ppppp")
                selectedEvent = time_table.objects.filter(id=taskId).values()
                print("editedEvent is: ",selectedEvent)
                if selectedEvent :
                    # print("editedEvent is: ",type(selectedEvent))
                    # x = selectedEvent.get()
                    # print (x)
                    # print (x["id"])
                    # for p in editedEvent:
                    #      print (p.user_id)

                    #check start time is temporary event summery 
                    if 'TempEventSummery' in request.headers:
                        TempEventSummery = request.headers['TempEventSummery']
                        print("TempEventSummery is :",TempEventSummery)
                        editSummeryEvent = time_table.objects.filter(id=taskId).update(summery_event=TempEventSummery)
                    else:
                        TempEventSummery = None
                        print ("TempEventSummery is :",TempEventSummery)

                    #check temporary start time is avaliable
                    if 'TempStartTime' in request.headers:
                        #print (len(request.headers['TempStartTime']))
                        TempStartTime = datetime.datetime.fromtimestamp(int(request.headers['TempStartTime']))
                        print("TempStartTime is :",TempStartTime)
                        editedStartTimeEvent = time_table.objects.filter(id=taskId).update(start_time=TempStartTime)
                    else:
                        TempStartTime = None
                        print ("TempStartTime",TempStartTime)
                    #check  temporary end time is avaliable


                    if 'TempEndTime' in request.headers:
                        TempEndTime = datetime.datetime.fromtimestamp(int(request.headers['TempEndTime']))
                        print("TempEndTime is :",TempEndTime)
                        editEndTimeEvent = time_table.objects.filter(id=taskId).update(end_time=TempEndTime)

                    else:
                        TempEndTime = None
                        print ("TempEndTime",TempEndTime)


                    if 'TempEventTitle' in request.headers:
                        TempEventTitle = request.headers['TempEventTitle']
                        print("TempEventSummery is :",TempEventSummery)
                        editSummeryEvent = time_table.objects.filter(id=taskId).update(title_event=TempEventTitle)
                    else:
                        TempEventTitle = None
                        print ("TempEventTitle is :",TempEventTitle)

                    content = {'message': 'your task was sucsessfully edited , try again'}
                    return Response(content)
                else:
                    print("id not exist")
                    content = {'message': 'id not exist , try again'}
                    return Response(content)
    
            
                #editedEvent = time_table.objects.filter(id=taskId).update(summery_event='some value')
        except Exception as e:
            content = {'message': 'your task was not edited , try again'}
            return Response(content)



# class TaskHistory(APIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self, request):
#         userId = request.user.id
#         taskName = request.headers['task-name']
#         content=[]
#         try:
#             getTaskId = task.objects.raw('select id from api_task WHERE task_name=%s AND user_id =%s',[taskName, userId])
#             for p in getTaskId:
#                 taskId=p.id
#             print('hiiiiiiiii',task.objects.filter(id=taskId))
#             if task.objects.filter(id=taskId):
#                 checkTaskHistory = task.objects.raw('SELECT * FROM `api_task_detail` WHERE task_id =%s', [taskId])
#                 for p in checkTaskHistory:
#                     updateContent = {'id': p.id,'comment': p.comment, 'start_task': p.start_task,'stop_task': p.stop_task}
#                     content.append(updateContent)
#                 return Response(content)
#         except Exception as e:
#             content = {'message': 'can not find history , try again'}
#             return Response(content)



# class TaskEditHistory(APIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self, request):
#         userId = request.user.id
#         historyTaskId = request.headers['history-id']

#         tempComment = request.headers['comment']
#         tempStartTask = request.headers['start-task']
#         tempStopTask = request.headers['stop-task']
#         print(tempStopTask,tempStartTask,tempComment)
#         try:
#             if task.objects.filter(id=historyTaskId):
#                 print('hiiii')
#                 editTaskName = task_detail.objects.filter(id=historyTaskId).update(comment=tempComment, start_task=tempStartTask,
#                                                                      stop_task=tempStopTask)
#                 content = {'message': 'your history of id was been edited'}
#                 return Response(content)
#         except Exception as e:
#             content = {'message': 'can not find history id , try again'}
#             return Response(content)



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
