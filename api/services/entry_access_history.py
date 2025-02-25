from django.db.models.aggregates import Count

from api.models import Entry
from api.models.entry_access_history import EntryAccessHistory
from api import log


class EntryAccessHistoryService:
    MOST_ACCESSED_MAX_LENGTH = 10

    @staticmethod
    def register(entry_id: int, user_id: int) -> EntryAccessHistory:
        eah = EntryAccessHistory(entry_id=entry_id, user_id=user_id)
        eah.save()

        return eah

    @staticmethod
    def get_from_user(user_id: int) -> list[EntryAccessHistory]:
        return EntryAccessHistory.objects.filter(user_id=user_id)[:10].all()

    @classmethod
    def get_most_accessed(cls):

        return (
            Entry.objects
            .annotate(accessed_times=Count("access_history"))
            .order_by('-accessed_times').all()
            [:cls.MOST_ACCESSED_MAX_LENGTH]
        )
