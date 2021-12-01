from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    # this function is what will do the whole work of signals
    # in the administration instead of you doing it mannually
    def ready(self):
        import users.signals