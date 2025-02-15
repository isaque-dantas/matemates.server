from api.models import Entry, KnowledgeArea, User
from api.tests.utils import entry_utils, user_utils, knowledge_area_utils

def reset_all_entities():
    Entry.objects.all().delete()
    KnowledgeArea.objects.all().delete()
    User.objects.all().delete()

    entry_utils.EntryUtils().create_all()
    knowledge_area_utils.KnowledgeAreaUtils().create_all()
    user_utils.UserUtils().create_all()