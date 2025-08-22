from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Crear usuario administrador de prueba'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@moteleclipse.com'
        password = 'admin123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'El usuario {username} ya existe')
            )
            return
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Admin',
            last_name='Eclipse',
            role='admin'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Usuario {username} creado exitosamente')
        )
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write(f'Email: {email}')
