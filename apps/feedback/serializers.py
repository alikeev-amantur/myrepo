from rest_framework import serializers

from apps.partner.models import Establishment

from .models import FeedbackAnswer, Feedback


class FeedbackAnswerSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FeedbackAnswer
        fields = (
            "id",
            "feedback",
            "user",
            "created_at",
            "text",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = instance.user.email
        return representation


class FeedbackSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    feedback_answers = FeedbackAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = (
            "id",
            "user",
            "created_at",
            "establishment",
            "text",
            "feedback_answers",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = instance.user.email
        representation["establishment"] = instance.establishment.name
        return representation


class FeedbackCreateUpdateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Feedback
        fields = (
            "id",
            "created_at",
            "text",
        )

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        establishment = self.context.get("request").resolver_match.kwargs["pk"]
        validated_data["establishment"] = Establishment.objects.get(pk=establishment)
        feedback = Feedback.objects.create(**validated_data)
        return feedback


class FeedbackAnswerCreateUpdateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FeedbackAnswer
        fields = (
            "id",
            "created_at",
            "text",
        )

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        feedback = self.context.get("request").resolver_match.kwargs["pk"]
        validated_data["feedback"] = Feedback.objects.get(pk=feedback)
        feedback_answer = FeedbackAnswer.objects.create(**validated_data)
        return feedback_answer
