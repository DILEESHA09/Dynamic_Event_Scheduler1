from django.urls import path
from .views import EventViewSet,CreateSessionView,UpdateSessionView,DeleteSessionView,ListAllSessionsView,OptimizedScheduleView,register,LoginView,Logout

urlpatterns = [
    path('events/', EventViewSet.as_view(), name='list-create-events'),
    path('events/<int:id>/', EventViewSet.as_view(), name='retrieve-update-delete-event'),
    path('events/<int:event_id>/sessions/', CreateSessionView.as_view(), name='create-session'),
    path('events/<int:event_id>/sessions/<int:session_id>/', UpdateSessionView.as_view(), name='update-session'),
    path('events/<int:event_id>/sessions/<int:session_id>/', DeleteSessionView.as_view(), name='delete-session'),
    path('sessions/', ListAllSessionsView.as_view(), name='list-sessions'),
    path('optimized-schedule/',OptimizedScheduleView.as_view(), name='optimized-schedule'),
    path('register/',register.as_view() ,name='register' ),
    path('login/',LoginView.as_view(), name='login'),
    path('logout/',Logout.as_view(), name='logout'),

]
