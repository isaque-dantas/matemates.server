from django.db.models.aggregates import Count, Max

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
        # return EntryAccessHistory.objects.filter(user_id=user_id).order_by("-access_moment")[:10].all()

        return (
            Entry.objects
            .filter(access_history__user_id=user_id)
            .annotate(access_moment=Max('access_history__access_moment'))
            .order_by('-access_moment')
        )

        # return (
        #     EntryAccessHistory.objects
        #     .filter(user_id=user_id)
        #     .annotate(last_moment_accessed=Max('access_history__access_moment'))
        #     .order_by('-last_moment_accessed')
        # )

    # SELECT e.id FROM api_entryaccesshistory as eah JOIN entry as e ON eah.entry_id = e.id ORDER BY eah.access_moment DESC GROUP BY e.id
    @classmethod
    def get_most_accessed(cls, should_get_only_validated: bool):
        if should_get_only_validated:
            return (
                Entry.objects
                .filter(is_validated=True)
                .annotate(accessed_times=Count("access_history"))
                .order_by('-accessed_times').all()
                [:cls.MOST_ACCESSED_MAX_LENGTH]
            )

        return (
            Entry.objects
            .annotate(accessed_times=Count("access_history"))
            .order_by('-accessed_times').all()
            [:cls.MOST_ACCESSED_MAX_LENGTH]
        )
