from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from .models import Events,Sessions,registermodel
from .serializers import EventsSerializer,SessionsSerializer,register_serializer

class EventViewSet(generics.GenericAPIView):
    serializer_class = EventsSerializer

    def get_object(self, id):
        return get_object_or_404(Events, id=id)

    def get(self, request, id=None):
        if id:
            # Retrieve a specific event
            event = self.get_object(id)
            serializer = self.serializer_class(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # List all events
            events = Events.objects.all()
            serializer = self.serializer_class(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        event = self.get_object(id)
        serializer = self.serializer_class(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        print(f"Attempting to delete event with ID: {id}")  # Debug output
        event = get_object_or_404(Events, id=id)
        serializer = EventsSerializer(event)
        event.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class CreateSessionView(APIView):
    def post(self, request, event_id):
        # Retrieve the event object
        event = get_object_or_404(Events, id=event_id)
        
        # Add the event to the session data
        session_data = request.data.copy()
        session_data['event_id'] = event.id
        
        # Serialize and validate the session data
        serializer = SessionsSerializer(data=session_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UpdateSessionView(APIView):
    def put(self, request, event_id, session_id):
        # Retrieve the session object
        session = get_object_or_404(Sessions, id=session_id, event_id=event_id)
        
        # Create a serializer instance with the updated data
        serializer = SessionsSerializer(session, data=request.data)
        
        if serializer.is_valid():
            # Validate the session to ensure no time conflicts
            updated_session = serializer.validated_data
            
            # Check for time conflicts
            conflicting_sessions = Sessions.objects.filter(
                event_id=event_id
            ).exclude(id=session_id).filter(
                start_time__lt=updated_session['end_time'],
                end_time__gt=updated_session['start_time']
            )
            
            if conflicting_sessions.exists():
                return Response(
                    {"detail": "Time conflict detected with another session."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Save the updated session data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteSessionView(APIView):
    def delete(self, request, event_id, session_id):
        session = get_object_or_404(Sessions, id=session_id, event_id=event_id)
        serializer = SessionsSerializer(session)  # Serialize the session data
        session.delete()  # Delete the session
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data of deleted session 

class ListAllSessionsView(APIView):
    def get(self, request):
        sessions = Sessions.objects.all()
        serializer = SessionsSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class OptimizedScheduleView(APIView):
    def get(self, request):
        # Retrieve all sessions with related event information
        sessions = Sessions.objects.select_related('event_id').all()
        
        # Serialize the data
        serializer = SessionsSerializer(sessions, many=True)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class register(APIView):
    def post(self,request):
        serializer = register_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response({'result':'register success'})
        
    
        return Response ({'result':'register failed'})
    
    
class LoginView(APIView):
   def post(self, request):
        serializer = register_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            try:
                user = registermodel.objects.filter(email=email, password=password)

                if user.exists():
                    request.session['id'] = user[0].id
                    request.session['email'] = user[0].email
                    if not request.session.session_key:
                        request.session.create()  # Create the session if it doesn't exist
                        session_id = request.session.session_key  # Get the session ID
                        print(session_id)
                        print(request.session['email'])

                    return Response({'message': 'User logged in successfully','session_id':session_id,'id':user[0].id}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            except registermodel.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class Logout(APIView):
    def post(self, request):
        print(request)
        session_key = request.data.get('sessionKey')

        if not session_key:
            return Response({'error': 'Session key not provided'}, status=status.HTTP_400_BAD_REQUEST)

        # if session_key == request.session.session_key:
        #     # Remove specific session data
        #     request.session.pop('candidate_id', None)
        #     request.session.pop('candidate_email', None)

        request.session.flush()    
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        # else:
        #     return Response({'error': 'Invalid session key'}, status=status.HTTP_400_BAD_REQUEST)