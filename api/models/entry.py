from django.db import models

# import api
import api.models


# TODO: refactor "save.*" methods to models.Manager inherited classes of each database entity

class EntryManager(models.Manager):
    def create(self, **kwargs):
        entry = Entry(content=self.parse_content(kwargs['content']))
        entry.save()
        self.save_terms(entry, kwargs['main_term_gender'], kwargs['main_term_grammatical_category'])
        self.save_definitions(entry, kwargs['definitions'])
        self.save_questions(entry, kwargs['questions'])

        print('created entry:', entry.__repr__())

    @staticmethod
    def parse_content(content: str):
        return content.replace("*", "").replace(" ", "_").replace(".", "")

    def save_terms(self, entry, main_term_gender: str, main_term_grammatical_category: str):
        for i, term_content in enumerate(entry.content.split(" ")):
            term_data = dict()
            term_data.update({"content": self.parse_content(term_content)})
            term_data.update({"order": i})

            is_main_term = term_content.startswith("*") and term_content.endswith("*")
            term_data.update({"is_main_term": is_main_term})
            if is_main_term:
                term_data.update({"gender": main_term_gender})
                term_data.update({"grammatical_category": main_term_grammatical_category})

            term = api.models.Term(**term_data)
            term.entry = entry
            term.save()

            self.save_syllables(term, term_content)



    @staticmethod
    def save_definitions(entry, definitions: list[dict]):
        for i, definition_incoming_data in enumerate(definitions):
            definition_data = dict()
            definition_data.update({"content": definition_incoming_data["content"]})
            definition_data.update({"order": i})

            definition = api.models.Definition(**definition_data)
            definition.entry = entry

            knowledge_area = api.models.KnowledgeArea.objects.get(
                content=definition_incoming_data["knowledge_area__content"])
            definition.knowledge_area = knowledge_area

            definition.save()

    @staticmethod
    def save_questions(entry, questions: list[dict]):
        for i, question in enumerate(questions):
            question_data = dict()
            question_data.update({"statement": question["statement"]})
            question_data.update({"answer": question["answer"]})
            question_data.update({"explanation": question["explanation"]})
            question_data.update({"order": i})

            question = api.models.Question(**question_data)
            question.entry = entry
            question.save()


class Entry(models.Model):
    content = models.CharField(max_length=128, blank=False, unique=True)
    is_validated = models.BooleanField(default=False, blank=False)

    objects = EntryManager()

    def __repr__(self):
        return f'<Entry {self.content}>'
