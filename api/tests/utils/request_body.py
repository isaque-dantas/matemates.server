from api.tests.utils import base64_encoded_files
from matemates_server import settings


class RequestBody:
    __data = {
        "entry": {
            "angulo-reto": {
                "content": "*ân.gu.lo* re.to",
                "main_term_gender": "M",
                "main_term_grammatical_category": "substantivo",
                "definitions": [
                    {"content": "Ângulo cuja medida é de 90°.", "knowledge_area__content": "álgebra"},
                    {"content": "Alguma outra definição.", "knowledge_area__content": "álgebra"},
                ],
                "images": [
                    {"caption": "ângulo reto na imagem", "base64_image": base64_encoded_files.ANGULO_RETO, "id": None},
                    {"caption": "outro ângulo reto", "base64_image": base64_encoded_files.ANGULO_RETO, "id": None},
                ],
                "questions": [
                    {"statement": "Um quadrado tem ângulos retos?", "answer": "Sim."},
                ],
            },
            "calculadora": {
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
                    {"caption": "ângulo reto na imagem", "base64_image": base64_encoded_files.CALCULADORA, "id": None},
                    {"caption": "outro ângulo reto", "base64_image": base64_encoded_files.ANGULO_RETO, "id": None},
                ],
                "questions": [
                    {"statement": "Quantas galinhas um ovo consegue pôr?",
                     "answer": "Aproximadamente o que uma calculadora pode computar."},
                ],
            }
        },
        "knowledge_area": {
            "estatistica": {"content": "estatística"},
            "algebra": {"content": "álgebra"},
            "calculo": {"content": "cálculo"},
            "cinematica": {"content": "cinemática"},
        },
        "user": {
            "common-user": {
                "name": "Common User",
                "email": "common-user@email.com",
                "password": "pass",
                "username": "common-user",
                "profile_image_base64": base64_encoded_files.DOG
            },
            "admin-user": {
                "name": "Admin User",
                "email": settings.ADMIN_EMAIL,
                "password": "pass",
                "username": "admin-user",
                "profile_image_base64": base64_encoded_files.DOG
            }

        }
    }

    @classmethod
    def get_data(cls, entity_name: str, data_identifier: str) -> dict:
        data = cls.__data[entity_name][data_identifier].copy()

        copied_data = {}
        for key in data:
            if data[key] is list:
                copied_data[key] = [dict_in_list.copy() for dict_in_list in data[key]]
            else:
                copied_data[key] = data[key]

        return copied_data

    @classmethod
    def get_entity_keys(cls, entity_name: str) -> list:
        return cls.__data[entity_name].keys()
