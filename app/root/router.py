from django.db.utils import DatabaseError


class DBRouter:
    read_only_dbs = ['oms', 'pms', 'ums', 'bms']

    def db_for_write(self, model, **hints):
        if model.__module__ in self.read_only_dbs:
            raise DatabaseError(f'{model.__name__} in {model.__module__} is not writable')
        return None

    @staticmethod
    def db_for_read(model, **hints):
        if model.__module__ == 'management.models.oms':
            return 'oms'
        if model.__module__ == 'management.models.ums':
            return 'ums'
        if model.__module__ == 'management.models.pms':
            return 'pms'
        if model.__module__ == 'management.models.bms':
            return 'bms'
        return None

    @staticmethod
    def allow_migrate(db, app_label, model_name=None, **hints):
        if db == 'default':
            return True
        return None
