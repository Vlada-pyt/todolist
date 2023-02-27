from typing import Any

from django.contrib.auth import login, logout
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from core.models import User
from core.serializers import CoreSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        login(request, user=serializer.save())
        return Response(serializer.data)


class UserCreateView(CreateAPIView):
    serializer_class = CoreSerializer
    permission_classes = [AllowAny]


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class: Serializer = ProfileSerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance: User):
        logout(self.request)


class PasswordUpdateView(UpdateAPIView):
    serializer_class: Serializer = UpdatePasswordSerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
