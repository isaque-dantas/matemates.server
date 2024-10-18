from api.models import Question
from api.serializers.question import QuestionSerializer


class QuestionService:
    @staticmethod
    def create_all(entry_data, entry):
        return Question.objects.create(
            [QuestionService.create(data, entry) for data in entry_data["questions"]],
        )

    @staticmethod
    def create(data, entry):
        return Question(**data, entry=entry)
