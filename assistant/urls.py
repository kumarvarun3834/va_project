from django.urls import path
from .views import assistant_view, home , get_sessions, get_history, delete_session, update_session

urlpatterns = [
    path("", home, name="home"),
    path("ask/", assistant_view, name="ask-assistant"),
    path("ask/<int:session_id>/", assistant_view, name="ask_existing"),  # continue session
    path("sessions/", get_sessions, name="sessions"),
    path("history/<int:session_id>/", get_history, name="history"),
    path("delete-session/<int:session_id>/", delete_session, name="delete-session"),
    path("update-session/<int:session_id>/", update_session, name="update-session"),
]
