from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions

from goals.filters import GoalDateFilter
from goals.models import Goal, GoalCategory, GoalComment, BoardParticipant, Board
from goals.permissions import IsOwnerOrReadOnly, BoardPermissions, GoalCategoryPermissions, GoalPermissions, \
    GoalCommentsPermissions
from goals.serializers import (
    GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCommentCreateSerializer, GoalCommentSerializer,
    GoalCreateSerializer, GoalSerializer, BoardCreateSerializer, BoardSerializer,
)


class BoardCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer

    def perform_create(self, serializer):
        BoardParticipant.objects.create(user=self.request.user, board=serializer.save())


class BoardListView(generics.ListAPIView):
    permission_classes = [BoardPermissions]
    serializer_class = BoardCreateSerializer

    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(is_deleted=False)


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user_id=self.request.user.id, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)


class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user_id=self.request.user.id,
                                           is_deleted=False)


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user_id=self.request.user.id,
                                           is_deleted=False)


    def perform_destroy(self, instance: GoalCategory):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)
        return instance


class GoalCreateView(generics.CreateAPIView):
    serializer_class = GoalCreateSerializer
    permission_classes = [GoalPermissions]


class GoalListView(generics.ListAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer
    filterset_class = GoalDateFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user_id=self.request.user.id,
                                   category__is_deleted=False).exclude(status=Goal.Status.archived)


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user_id=self.request.user, category__is_deleted=False).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))



class GoalCommentCreateView(generics.CreateAPIView):
    serializer_class = GoalCommentCreateSerializer
    permission_classes = [GoalCommentsPermissions]


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    permission_classes = [GoalCommentsPermissions]
    serializer_class = GoalCommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user_id=self.request.user.id)


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = [GoalCommentsPermissions]
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)
