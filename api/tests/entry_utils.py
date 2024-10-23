from api.models.entry import Entry
from api.serializers.entry import EntrySerializer
from api.services.entry import EntryService
from api.tests import base64_encoded_files
from api.tests.knowledge_area_utils import KnowledgeAreaUtils


# TODO: add some knowledge areas by default in the constructor method (__init__)

class EntryUtils:
    entry_datas = {
        'angulo-reto': {
            "content": "*ân.gu.lo* re.to",
            "main_term_gender": "M",
            "main_term_grammatical_category": "substantivo",
            "definitions": [
                {"content": "Ângulo cuja medida é de 90°.", "knowledge_area__content": "álgebra"},
                {"content": "Alguma outra definição.", "knowledge_area__content": "álgebra"},
            ],
            "images": [
                {"caption": "ângulo reto na imagem", "format": "jpg", "base64_image": base64_encoded_files.ANGULO_RETO},
                {"caption": "outro ângulo reto", "format": "jpg", "base64_image": base64_encoded_files.ANGULO_RETO},
            ],
            "questions": [
                {"statement": "Um quadrado tem ângulos retos?", "answer": "Sim.", "explanation": "Porque sim."},
            ],
        },

        'calculadora': {
            "content": "cal.cu.la.do.ra",
            "main_term_gender": "F",
            "main_term_grammatical_category": "substantivo",
            "definitions": [
                {"content": "Dispositivo eletrônico usado para efetuar cálculos matemáticos.",
                 "knowledge_area__content": "álgebra"},
                {"content": "Um homem, uma máquina, um fantástico espetáculo.",
                 "knowledge_area__content": "estatística"},
            ],
            "images": [
                {"caption": "ângulo reto na imagem", "format": "jpg", "base64_image": base64_encoded_files.CALCULADORA},
                {"caption": "outro ângulo reto", "format": "jpg", "base64_image": base64_encoded_files.ANGULO_RETO},
            ],
            "questions": [
                {"statement": "Quantas galinhas um ovo consegue pôr?",
                 "answer": "Aproximadamente o que uma calculadora pode computar.", "explanation": "Porque sim."},
            ],
        }
    }

    @staticmethod
    def get_data(data_identifier: str):
        data = EntryUtils.entry_datas[data_identifier].copy()
        copied_data = {}
        for key in data:
            if data[key] is list:
                copied_data[key] = [dict_in_list.copy() for dict_in_list in data[key]]
            else:
                copied_data[key] = data[key]

        return copied_data

    def set_database_environment(self, environment: dict[str, bool]):
        environment = environment or {'angulo_reto': False, 'calculadora': False}
        actions = {
            True: lambda e: self.create(e),
            False: lambda e: self.delete(e),
        }

        KnowledgeAreaUtils.create_all()

        for content, must_create in environment.items():
            actions[must_create](content)

    def retrieve(self, content: str):
        content = self.parse_content(content)
        return Entry.objects.get(content=content)

    def exists(self, content: str) -> bool:
        content = self.parse_content(content)
        return Entry.objects.filter(content=content).exists()

    def create(self, content: str):
        content = self.parse_content(content)
        if self.exists(content):
            return None

        serializer = EntrySerializer(data=self.get_data(content))
        serializer.is_valid(raise_exception=True)
        EntryService.create(serializer)

    def delete(self, content: str):
        content = self.parse_content(content)
        if not self.exists(content):
            return None

        Entry.objects.filter(content=content).delete()

    @staticmethod
    def parse_content(content: str) -> str:
        return content.replace("*", "").replace(".", "").replace(" ", "_")
