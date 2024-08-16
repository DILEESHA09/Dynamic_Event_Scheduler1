from django.urls import path
from .views import EventViewSet,CreateSessionView,UpdateSessionView,DeleteSessionView,ListAllSessionsView,OptimizedScheduleView

urlpatterns = [
    path('events/', EventViewSet.as_view(), name='list-create-events'),
    path('events/<int:id>/', EventViewSet.as_view(), name='retrieve-update-delete-event'),
    path('events/<int:event_id>/sessions/', CreateSessionView.as_view(), name='create-session'),
    path('events/<int:event_id>/sessions/<int:session_id>/', DeleteSessionView.as_view(), name='delete-session'),
    path('sessions/', ListAllSessionsView.as_view(), name='list-sessions'),
    path('optimized-schedule/',OptimizedScheduleView.as_view(), name='optimized-schedule'),

]
