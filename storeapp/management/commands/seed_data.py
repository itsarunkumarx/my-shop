from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from storeapp.models import Category, Product, Customer, Order, OrderItem, Review
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds the database with initial categories, products, users, and orders'

    def handle(self, *args, **kwargs):
        # 1. Create Superuser / Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Store',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))
        else:
            self.stdout.write("Admin user already exists.")

        # 2. Create Regular Demo Customer
        demo_user, created = User.objects.get_or_create(
            username='johndoe',
            defaults={
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
            }
        )
        if created:
            demo_user.set_password('password123')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS("Created demo user: johndoe / password123"))

        customer, _ = Customer.objects.get_or_create(
            user=demo_user,
            defaults={
                'phone': '+91 9876543210',
                'address': '123 Tech Park, MG Road',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560001',
            }
        )

        # 3. Create Categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Laptops, gadgets, accessories, and premium tech devices.'},
            {'name': 'Smartphones', 'description': 'Next-gen flagship and budget mobile smartphones.'},
            {'name': 'Fashion', 'description': 'Trendy apparel, t-shirts, casual wear, and stylish accessories.'},
            {'name': 'Furniture', 'description': 'Comfortable home and office furniture, ergonomic chairs, and tables.'},
            {'name': 'Books', 'description': 'Bestselling fiction, non-fiction, technology, and learning books.'},
        ]

        cats = {}
        for cdata in categories_data:
            cat, _ = Category.objects.get_or_create(
                name=cdata['name'],
                defaults={'description': cdata['description']}
            )
            cats[cdata['name']] = cat
        self.stdout.write(self.style.SUCCESS("Categories created/verified."))

        # 4. Create Products
        products_data = [
            {
                'category': cats['Electronics'],
                'name': 'MacBook Pro M3 (16GB, 512GB SSD)',
                'description': 'The 14-inch MacBook Pro blasts forward with M3, an incredibly advanced chip that brings serious speed and capability.',
                'specifications': 'Apple M3 Chip, 16GB Unified RAM, 512GB SSD, Liquid Retina XDR 14-inch Display, Space Grey',
                'price': Decimal('149999.00'),
                'stock': 15,
                'image': 'products/laptop.jpg',
                'is_available': True
            },
            {
                'category': cats['Smartphones'],
                'name': 'Samsung Galaxy S24 Ultra 5G',
                'description': 'Experience the new era of Galaxy AI with stunning camera capabilities and titan durability.',
                'specifications': 'Snapdragon 8 Gen 3, 12GB RAM, 256GB Storage, 200MP Quad Camera, S-Pen Included',
                'price': Decimal('119999.00'),
                'stock': 20,
                'image': 'products/mobile.jpg',
                'is_available': True
            },
            {
                'category': cats['Fashion'],
                'name': 'Premium Cotton Crewneck T-Shirt',
                'description': '100% premium combed organic cotton t-shirt for supreme comfort and all-day breathable wear.',
                'specifications': '100% Organic Cotton, Pre-shrunk, Regular Fit, Machine Washable, Navy Blue',
                'price': Decimal('799.00'),
                'stock': 50,
                'image': 'products/tshirt.jpg',
                'is_available': True
            },
            {
                'category': cats['Furniture'],
                'name': 'Ergonomic Executive Office Chair',
                'description': 'High back ergonomic mesh desk chair with adjustable lumbar support, 3D armrests, and recline function.',
                'specifications': 'Breathable Mesh Back, High Density Foam Seat, Heavy-duty Nylon Base, 360-degree Swivel',
                'price': Decimal('8499.00'),
                'stock': 12,
                'image': 'products/furniture.jpg',
                'is_available': True
            },
            {
                'category': cats['Books'],
                'name': 'Clean Code & Architecture Master Collection',
                'description': 'A Handbook of Agile Software Craftsmanship and modern software engineering best practices.',
                'specifications': 'Hardcover, 464 Pages, English, Pearson Education Publishing',
                'price': Decimal('1299.00'),
                'stock': 30,
                'image': 'products/books.jpg',
                'is_available': True
            },
        ]

        created_products = []
        for pdata in products_data:
            prod, _ = Product.objects.get_or_create(
                name=pdata['name'],
                defaults=pdata
            )
            created_products.append(prod)
        self.stdout.write(self.style.SUCCESS("Products created/verified."))

        # 5. Create Sample Reviews
        Review.objects.get_or_create(
            product=created_products[0],
            user=demo_user,
            defaults={
                'rating': 5,
                'comment': 'Exceptional performance and incredible battery life. Best laptop I have ever owned!'
            }
        )
        Review.objects.get_or_create(
            product=created_products[1],
            user=demo_user,
            defaults={
                'rating': 5,
                'comment': 'Stunning camera clarity and smooth AI features. Highly recommended.'
            }
        )
        Review.objects.get_or_create(
            product=created_products[2],
            user=demo_user,
            defaults={
                'rating': 4,
                'comment': 'Great fabric quality and fit. Colors stayed intact after multiple washes.'
            }
        )

        # 6. Create a Sample Order
        order, ord_created = Order.objects.get_or_create(
            customer=customer,
            status='Delivered',
            defaults={'total_amount': Decimal('2098.00')}
        )
        if ord_created:
            OrderItem.objects.create(
                order=order,
                product=created_products[2],
                quantity=1,
                price=Decimal('799.00')
            )
            OrderItem.objects.create(
                order=order,
                product=created_products[4],
                quantity=1,
                price=Decimal('1299.00')
            )
            order.total_amount = Decimal('2098.00')
            order.save()
            self.stdout.write(self.style.SUCCESS("Sample order created."))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
