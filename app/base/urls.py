from django.urls import path

from .views import (
    activity_view,
    create_room_view,
    delete_message_view,
    delete_room_view,
    home_view,
    login_view,
    logout_view,
    register_view,
    room_view,
    topics_view,
    update_room_view,
    update_user,
    user_profile_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/<int:pk>/", user_profile_view, name="user-profile"),
    path("create-room/", create_room_view, name="create-room"),
    path("room/<int:pk>/", room_view, name="room"),
    path("update-room/<int:pk>/", update_room_view, name="update-room"),
    path("delete-room/<int:pk>/", delete_room_view, name="delete-room"),
    path("delete-message/<int:pk>/", delete_message_view, name="delete-message"),
    path("update-user/", update_user, name="update-user"),
    path("topics/", topics_view, name="topics"),
    path("activity/", activity_view, name="activity"),
]
