from django.contrib.messages.storage.base import BaseStorage

class NullStorage(BaseStorage):
    """Just discards all messages"""

    def _get(self, *args, **kwargs):
        """
        Returns a (None, True) tuple to feign empty message store
        """
        return (None, True)

    def _store(self, *args, **kwargs):
        """
        Returns an empty list to feign successful operation
        """
        return []
