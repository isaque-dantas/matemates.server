from api.models.entry_access_history import EntryAccessHistory


class EntryAccessHistoryService:

    @staticmethod
    def register(entry_id: int, user_id: int) -> EntryAccessHistory:
        eah = EntryAccessHistory(entry_id=entry_id, user_id=user_id)
        eah.save()

        return eah

    @staticmethod
    def get_from_user(user_id: int) -> list[EntryAccessHistory]:
        return EntryAccessHistory.objects.filter(user_id=user_id).all()
