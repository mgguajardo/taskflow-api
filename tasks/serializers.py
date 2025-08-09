from rest_framework import serializers
from .models import Task, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tags_id = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        source="tags",
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "completed",
            "created_at",
            "tags",
            "tags_id",
        ]
        read_only_fields = ["id", "created_at", "tags", "user"]

    def validate_title(self, value):
        """
        Evitar titulos duplicados para el mismo usuario
        """
        user = self.context["request"].user
        # si estas actualizando, exclude la instancia actual
        task_id = self.instance.id if self.instance else None
        if Task.objects.filter(user=user, title=value).exclude(id=task_id).exists():
            raise serializers.ValidationError("ya existe una tarea con este titulo.")
        return value

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        task = Task.objects.create(**validated_data)
        task.tags.set(tags_data)
        return task

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags_data is not None:
            instance.tags.set(tags_data)
        return instance
