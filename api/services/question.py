from api.models import Question
from api.serializers.question import QuestionSerializer


class QuestionService:
    @staticmethod
    def create_all(entry_data, entry):
        return Question.objects.create(
            [QuestionService.get_instance_from_data(data, entry) for data in entry_data["questions"]],
        )

    @staticmethod
    def get_instance_from_data(data, entry):
        return Question(statement=data["statement"], answer=data["answer"], entry=entry)

    @staticmethod
    def get(pk):
        return Question.objects.get(pk=pk)

    @staticmethod
    def exists(pk):
        return Question.objects.filter(pk=pk).exists()

    @staticmethod
    def delete(pk):
        Question.objects.filter(id=pk).delete()

    @staticmethod
    def is_parent_validated(pk):
        return QuestionService.get(pk).entry.is_validated

    @staticmethod
    def update(serializer):
        data = serializer.validated_data
        instance: Question = serializer.instance

        instance.statement = data["statement"]
        instance.answer = data["answer"]
        instance.save()

    @classmethod
    def create(cls, serializer):
        data = serializer.validated_data
        question = cls.get_instance_from_data(data, data["entry"])
        question.save()

        return question
