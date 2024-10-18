from api.models.entry import Entry
from api.tests.knowledge_area_utils import KnowledgeAreaUtils


# TODO: add some knowledge areas by default in the constructor method (__init__)

class EntryUtils:
    right_angle_entry_data = {
        "content": "*ân.gu.lo* re.to",
        "main_term_gender": "M",
        "main_term_grammatical_category": "substantivo",
        "definitions": [
            {"content": "Ângulo cuja medida é de 90°.", "knowledge_area__content": "álgebra"},
            {"content": "Alguma outra definição.", "knowledge_area__content": "estatística"},
        ],
        "images": [
            {"caption": "ângulo reto na imagem", "base64_encoded_string": ""},
            {"caption": "outro ângulo reto", "base64_encoded_string": ""},
        ],
        "questions": [
            {"statement": "Um quadrado tem ângulos retos?", "answer": "Sim.", "explanation": "Porque sim."},
        ],
    }

    calculator_entry_data = {
        "content": "cal.cu.la.do.ra",
        "main_term_gender": "F",
        "main_term_grammatical_category": "substantivo",
        "definitions": [
            {"content": "Dispositivo eletrônico usado para efetuar cálculos matemáticos.",
             "knowledge_area__content": "álgebra"},
            {"content": "Um homem, uma máquina, um fantástico espetáculo.", "knowledge_area__content": "estatística"},
        ],
        "images": [
            {"caption": "ângulo reto na imagem", "base64_encoded_string": ""},
            {"caption": "outro ângulo reto", "base64_encoded_string": ""},
        ],
        "questions": [
            {"statement": "Quantas galinhas um ovo consegue pôr?",
             "answer": "Aproximadamente o que uma calculadora pode computar.", "explanation": "Porque sim."},
        ],
    }

    def __init__(self):
        KnowledgeAreaUtils.create_all()

    def set_database_environment(self, environment: dict[str, bool]):
        environment = environment or {'angulo_reto': False, 'calculadora': False}
        actions = {
            True: lambda e: self.create(e),
            False: lambda e: self.delete(e),
        }

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

        Entry.objects.create(**self._get_data_by_content(content))

    def delete(self, content: str):
        content = self.parse_content(content)
        if not self.exists(content):
            return None

        Entry.objects.filter(content=content).delete()

    @staticmethod
    def parse_content(content: str) -> str:
        return content.replace("*", "").replace(".", "").replace(" ", "_")

    def _get_data_by_content(self, content: str):
        if content == 'calculadora':
            return self.calculator_entry_data
        elif content == 'ângulo_reto':
            return self.right_angle_entry_data
