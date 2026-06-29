from django.apps import AppConfig


class NotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notes"

    def ready(self):
        from django.contrib.auth.signals import user_logged_in, user_logged_out
        from django.contrib import messages

        def on_login(sender, request, user, **kwargs):
            messages.success(
                request, f"Zalogowano jako {user.get_full_name() or user.username}."
            )

        def on_logout(sender, request, user, **kwargs):
            if user:
                messages.info(request, "Wylogowano.")

        user_logged_in.connect(on_login, dispatch_uid="notes_login_toast")
        user_logged_out.connect(on_logout, dispatch_uid="notes_logout_toast")
