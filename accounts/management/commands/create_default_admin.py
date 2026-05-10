import os

from django.core.management.base import BaseCommand

from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Create or update the deployment admin account from environment variables.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    'Skipping admin creation. Set DJANGO_SUPERUSER_USERNAME '
                    'and DJANGO_SUPERUSER_PASSWORD to enable it.'
                )
            )
            return

        user, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'role': 'ADMIN',
                'is_approved': True,
                'is_staff': True,
                'is_superuser': True,
            },
        )

        user.email = email or user.email
        user.role = 'ADMIN'
        user.is_approved = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'{action} admin account: {username}'))
