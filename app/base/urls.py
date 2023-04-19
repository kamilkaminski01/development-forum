from django.urls import path

from .views import (
    create_room_view,
    delete_room_view,
    home_view,
    login_view,
    room_view,
    update_room_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("room/<int:pk>/", room_view, name="room"),
    path("create-room/", create_room_view, name="create-room"),
    path("update-room/<int:pk>/", update_room_view, name="update-room"),
    path("delete-room/<int:pk>/", delete_room_view, name="delete-room"),
]
