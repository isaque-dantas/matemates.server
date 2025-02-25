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
                    {"content": "Ângulo com valor de 90°. Semirretas que formam um ângulo de 90º são chamadas de perpendiculares.", "knowledge_area__content": "geometria"},
                    {"content": "Parte da definição de um retângulo, polígono que tem seus quatro ângulos internos classificados como retos", "knowledge_area__content": "geometria"},
                ],
                "images": [
                    {"caption": "Ângulo reto na imagem", "base64_image": base64_encoded_files.ANGULO_RETO, "id": None},
                    {"caption": "A mesma imagem, com outra legenda", "base64_image": base64_encoded_files.ANGULO_RETO,
                     "id": None},
                ],
                "questions": [
                    {
                        "statement": "Quantos ângulos retos tem um quadrado?",
                        "answer": "Todos os ângulos internos de um quadrado são retos. Ou seja, há quatro deles."
                    },
                ],
            },
            "calculadora": {
                "content": "cal.cu.la.do.ra",
                "main_term_gender": "F",
                "main_term_grammatical_category": "substantivo",
                "definitions": [
                    {
                        "content": "Dispositivo eletrônico usado para efetuar cálculos matemáticos.",
                        "knowledge_area__content": "álgebra"
                    },
                    {
                        "content": "Máquina que efetua operações de aritmética.",
                        "knowledge_area__content": "álgebra"
                    },
                ],
                "images": [
                    {"caption": "Ilustração de uma calculadora", "base64_image": base64_encoded_files.CALCULADORA, "id": None}
                ],
                "questions": []
            },
            "abaco": {
                "content": "á.ba.co",
                "main_term_gender": "M",
                "main_term_grammatical_category": "substantivo",
                "definitions": [
                    {
                        "content": "Instrumento que possui uma base e hastes perpendiculares que indicam as ordens numéricas (unidade, dezena, centena, etc) e bolinhas ou discos nessas hastes representando uma unidade dessa ordem específica",
                        "knowledge_area__content": "álgebra"
                    },
                ],
                "images": [
                    {"caption": "Ábaco simples, com hastes horizontais.", "base64_image": base64_encoded_files.ABACO, "id": None}
                ],
                "questions": []
            },
            "funcao": {
                "content": "fun.ção",
                "main_term_gender": "F",
                "main_term_grammatical_category": "substantivo",
                "definitions": [
                    {
                        "content": "Corresponde ao conjunto de pares de valores de duas variáveis, em que há uma independente e outra, originária dessa, que é chamada de dependente.",
                        "knowledge_area__content": "álgebra"
                    },
                    {
                        "content": "Relação de correspondência entre os valores de dois conjuntos, X (chamado de domínio) e Y (imagem ou contradomínio), em que seja possível associar cada elemento de X a apenas um elemento de Y. Formalmente, essa é uma função f: X -> Y, ou f(x) = y.",
                        "knowledge_area__content": "álgebra"
                    },
                ],
                "images": [
                    {"caption": "Exemplo de uma função", "base64_image": base64_encoded_files.FUNCAO, "id": None}
                ],
                "questions": [
                    {"statement": "A relação entre os dias do ano e se é feriado ou não é um exemplo de função?", "answer": "Sim, já que cada dia tem apenas um valor associado: \"verdadeiro\" ou \"falso\"."}
                ]
            },
            "tetraedro": {
                "content": "te.tra.e.dro",
                "main_term_gender": "M",
                "main_term_grammatical_category": "substantivo",
                "definitions": [
                    {
                        "content": "Poliedro com 4 faces poligonais. O tetraedro regular é composto por quatro faces no formato de triângulos equiláteros.",
                        "knowledge_area__content": "geometria"
                    },
                    {
                        "content": "Sólido cuja superfície é formada por quatro faces triangulares.",
                        "knowledge_area__content": "geometria"
                    },
                ],
                "images": [
                    {"caption": "Ilustração de um tetraedro regular", "base64_image": base64_encoded_files.TETRAEDRO, "id": None}
                ],
                "questions": []
            },
            "dados": {
                "content": "da.dos",
                "main_term_gender": "M",
                "main_term_grammatical_category": "substantivo",
                "definitions": [
                    {
                        "content": "Registros de observações ou fatos do mundo real, mas desprovidos de seu contexto original. Por exemplo, “camisa”, “2007” e “Bonifácio” são dados.",
                        "knowledge_area__content": "estatística"
                    },
                    {
                        "content": "Objetos na forma de sólidos geométricos usados para sortear números, letras ou símbolos. Há aqueles com quatro, cinco, seis e até 20 faces, todos com aplicações diversas, que vão desde jogos de tabuleiro até o estudo de probabilidade e estatística.",
                        "knowledge_area__content": "geometria"
                    },
                ],
                "images": [
                    {"caption": "Dado de vinte faces, comumente usado em RPGs (role-playing game – jogo de interpretação de papéis, em tradução livre).", "base64_image": base64_encoded_files.DADO, "id": None}
                ],
                "questions": []
            },
            "diagrama-venn": {
                "content": "*di.a.gra.ma* de Venn",
                "main_term_gender": "M",
                "main_term_grammatical_category": "substantivo",
                "definitions": [
                    {
                        "content": "O diagrama de Venn é uma forma de representar graficamente conjuntos e suas operações por meio de circunferências, onde cada uma delas representa um conjunto. Com ele, é possível solucionar vários problemas apenas com cálculos simples.",
                        "knowledge_area__content": "álgebra"
                    },
                ],
                "images": [
                    {"caption": "Típica ilustração de um diagrama de Venn, com três conjuntos que se intersectam mutuamente.", "base64_image": base64_encoded_files.VENN, "id": None}
                ],
                "questions": []
            },
            "eneagono": {
                "content": "e.ne.á.go.no",
                "main_term_gender": "M",
                "main_term_grammatical_category": "substantivo",
                "definitions": [
                    {
                        "content": "Polígono com 9 lados, regular ou não, cuja soma interna dos ângulos resulta em 1260 graus.",
                        "knowledge_area__content": "geometria"
                    },
                    {
                        "content": "Polígono de nove lados e nove ângulos.",
                        "knowledge_area__content": "geometria"
                    },
                ],
                "images": [
                    {"caption": "Eneágono regular.", "base64_image": base64_encoded_files.ENEAGONO, "id": None}
                ],
                "questions": []
            }
        },
        "knowledge_area": {
            "geometria": {"content": "geometria"},
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
