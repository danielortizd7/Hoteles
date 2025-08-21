from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rooms.models import RoomType, Room
from inventory.models import Category, Product

User = get_user_model()

class Command(BaseCommand):
    help = 'Carga datos iniciales para el sistema hotelero'

    def handle(self, *args, **options):
        self.stdout.write('Cargando datos iniciales...')
        
        # Crear usuario administrador
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@motel.com',
                password='admin123',
                first_name='Alvaro',
                last_name='Velasquez',
                role='admin'
            )
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(f'✓ Usuario administrador creado: admin/admin123')
        
        # Crear usuario recepcionista
        if not User.objects.filter(username='martha').exists():
            User.objects.create_user(
                username='martha',
                email='martha@motel.com',
                password='martha123',
                first_name='Martha',
                last_name='Suarez',
                role='receptionist'
            )
            self.stdout.write(f'✓ Usuario recepcionista creado: martha/martha123')
        
        # Crear tipos de habitaciones
        room_types_data = [
            {
                'name': 'standard',
                'description': 'Habitación estándar con servicios básicos',
                'base_price_5h': 40000,
                'icon': '🏠'
            },
            {
                'name': 'love_machine',
                'description': 'Habitación con máquina del amor y servicios especiales',
                'base_price_5h': 45000,
                'icon': '💕'
            },
            {
                'name': 'suite',
                'description': 'Suite de lujo con jacuzzi y servicios premium',
                'base_price_5h': 60000,
                'icon': '👑'
            }
        ]
        
        for room_type_data in room_types_data:
            room_type, created = RoomType.objects.get_or_create(
                name=room_type_data['name'],
                defaults=room_type_data
            )
            if created:
                self.stdout.write(f'✓ Tipo de habitación creado: {room_type.get_name_display()}')
        
        # Crear habitaciones
        room_types = {rt.name: rt for rt in RoomType.objects.all()}
        rooms_data = [
            # Habitaciones estándar
            {'number': '1', 'room_type': room_types['standard'], 'floor': 1},
            {'number': '2', 'room_type': room_types['standard'], 'floor': 1},
            {'number': '3', 'room_type': room_types['standard'], 'floor': 1},
            {'number': '4', 'room_type': room_types['standard'], 'floor': 1},
            {'number': '7', 'room_type': room_types['standard'], 'floor': 1},
            {'number': '8', 'room_type': room_types['standard'], 'floor': 1},
            {'number': '9', 'room_type': room_types['standard'], 'floor': 1},
            
            # Habitaciones con máquina del amor
            {'number': '5', 'room_type': room_types['love_machine'], 'floor': 1},
            {'number': '6', 'room_type': room_types['love_machine'], 'floor': 1},
            
            # Suites
            {'number': '10', 'room_type': room_types['suite'], 'floor': 2},
            {'number': '11', 'room_type': room_types['suite'], 'floor': 2},
        ]
        
        for room_data in rooms_data:
            room, created = Room.objects.get_or_create(
                number=room_data['number'],
                defaults=room_data
            )
            if created:
                self.stdout.write(f'✓ Habitación creada: {room.number} - {room.room_type}')
        
        # Crear categorías de productos
        categories_data = [
            {'name': 'Bebidas', 'description': 'Bebidas alcohólicas y no alcohólicas', 'icon': '🍺'},
            {'name': 'Comida', 'description': 'Alimentos y snacks', 'icon': '🍽️'},
            {'name': 'Cuidado Personal', 'description': 'Productos de higiene y cuidado', 'icon': '🧴'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'✓ Categoría creada: {category.name}')
        
        # Crear productos
        categories = {cat.name: cat for cat in Category.objects.all()}
        products_data = [
            # Bebidas
            {'name': 'cerveza corona', 'category': categories['Bebidas'], 'price': 4500, 'current_stock': 8, 'minimum_stock': 5},
            
            # Comida
            {'name': 'DE TODITO', 'category': categories['Comida'], 'price': 3500, 'current_stock': 13, 'minimum_stock': 5},
            
            # Cuidado Personal
            {'name': 'preservativos', 'category': categories['Cuidado Personal'], 'price': 3000, 'current_stock': 92, 'minimum_stock': 5},
        ]
        
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults=prod_data
            )
            if created:
                self.stdout.write(f'✓ Producto creado: {product.name}')
        
        self.stdout.write(
            self.style.SUCCESS('✅ Datos iniciales cargados exitosamente!')
        )
