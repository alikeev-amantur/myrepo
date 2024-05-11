from drf_spectacular.utils import extend_schema
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from happyhours.permissions import IsAdmin

from .models import Feedback, FeedbackAnswer
from .serializers import (
    FeedbackSerializer,
    FeedbackAnswerSerializer,
)
from .views_services import FeedbackViewSetService


@extend_schema(tags=["Feedbacks"])
class FeedbackListView(ListAPIView):
    """
    Feedback's list view

    ### Fields:
    - `user`: Owner of the feedback
    - `created_at`: Time of creation
    - `establishment`: Establishment of the feedback
    - `text`: Content of the feedback
    - `feedback_answers`: Answers to the feedback

    ### Access Control:
    - Everyone

    """

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


@extend_schema(tags=["Feedbacks"])
class FeedbackCreateView(CreateAPIView):
    """
    Feedback's creation view

    ### Fields:
    - `user`: Owner of the feedback
    - `created_at`: Time of creation
    - `establishment`: Establishment of the feedback
    - `text`: Content of the feedback
    - `feedback_answers`: Answers to the feedback

    ### Access Control:
    - Authenticated user

    """

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["Feedbacks"])
class FeedbackViewSet(FeedbackViewSetService):
    """
    Feedback's CRUD

    ### Fields:
    - `user`: Owner of the feedback
    - `created_at`: Time of creation
    - `establishment`: Establishment of the feedback
    - `text`: Content of the feedback
    - `feedback_answers`: Answers to the feedback

    ### Access Control:
    - Retrieve - anonymous user
    - Updating or deleting - Owner of feedback or admin and superuser

    """

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


@extend_schema(tags=["Feedbacks"])
class FeedbackAnswerCreate(CreateAPIView):
    """
    Feedback's answers' creation view

    ### Fields:
    - `feedback`: Feedback of the answer
    - `user`: Owner of the answer
    - `created_at`: Time of creation
    - `text`: Content of the feedback

    ### Access Control:
    - Admin or superuser

    """

    queryset = FeedbackAnswer.objects.all()
    serializer_class = FeedbackAnswerSerializer
    permission_classes = [IsAdmin]


@extend_schema(tags=["Feedbacks"])
class FeedbackAnswerViewSet(FeedbackViewSetService):
    """
    Feedback's answers' CRUD

    ### Fields:
    - `feedback`: Feedback of the answer
    - `user`: Owner of the answer
    - `created_at`: Time of creation
    - `text`: Content of the feedback

    ### Access Control:
    - Retrieve - anonymous user
    - Updating or deleting - Owner of feedback or admin and superuser

    """

    queryset = FeedbackAnswer.objects.all()
    serializer_class = FeedbackAnswerSerializer
