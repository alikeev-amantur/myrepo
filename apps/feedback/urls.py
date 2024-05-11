from django.urls import path

from .views import (
    FeedbackViewSet,
    FeedbackAnswerCreate,
    FeedbackAnswerViewSet,
    FeedbackListView,
    FeedbackCreateView,
)

urlpatterns = [
    path(
        "feedbacks/<int:pk>/",
        FeedbackViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
    ),
    path("answers/create/", FeedbackAnswerCreate.as_view()),
    path(
        "answers/<int:pk>/",
        FeedbackAnswerViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
    ),
    path("feedbacks/list/", FeedbackListView.as_view()),
    path("feedbacks/create/", FeedbackCreateView.as_view()),
]
