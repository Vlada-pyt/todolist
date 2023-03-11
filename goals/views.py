from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions
from rest_framework.pagination import LimitOffsetPagination
from goals.filters import GoalDateFilter
from goals.models import Goal, GoalCategory, GoalComment, BoardParticipant, Board
from goals.permissions import BoardPermissions, GoalCategoryPermissions, GoalPermissions, GoalCommentsPermissions
from goals.serializers import (
    GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCommentCreateSerializer, GoalCommentSerializer,
    GoalCreateSerializer, GoalSerializer, BoardCreateSerializer, BoardSerializer, BoardListSerializer,
)


class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        query = GoalCategory.objects.filter(
            is_deleted=False,
            board__participants__user_id=self.request.user.id
        )
        return query


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermissions]

    def get_queryset(self):
        if self.request.method == "GET":
            return GoalCategory.objects.filter(
                is_deleted=False,
                board__participants__user=self.request.user.id
            )
        return GoalCategory.objects.filter(
            user=self.request.user.id, is_deleted=False
        ).exclude(board__participants__role=BoardParticipant.Role.reader)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)


class GoalListView(generics.ListAPIView):
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user_id=self.request.user.id,
            category__is_deleted=False
        ).exclude(status=Goal.Status.archived)


class GoalCreateView(generics.CreateAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]

    def get_queryset(self):
        return Goal.objects.filter(
                category__board__participants__user_id=self.request.user.id,
                category__is_deleted=False
            ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance: Goal):
        instance.is_deleted = True
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status', 'is_deleted',))


class GoalCommentListView(generics.ListAPIView):
    permission_classes = [GoalCommentsPermissions]
    serializer_class = GoalCommentSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user_id=self.request.user.id
        ).exclude(
            goal__status=Goal.Status.archived
        )


class GoalCommentCreateView(generics.CreateAPIView):
    model = GoalComment
    permission_classes = [GoalCommentsPermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCommentSerializer
    permission_classes = [GoalCommentsPermissions]

    def get_queryset(self):
        return GoalComment.objects.filter(
            user=self.request.user
        ).exclude(
            goal__status=Goal.Status.archived
        )

class BoardCreateView(generics.CreateAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer

    def perform_create(self, serializer):
        BoardParticipant.objects.create(user=self.request.user, board=serializer.save())


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)


class BoardListView(generics.ListAPIView):
    permission_classes = [BoardPermissions]
    serializer_class = BoardListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.filter(
            participants__user_id=self.request.user.id,
            is_deleted=False
        )