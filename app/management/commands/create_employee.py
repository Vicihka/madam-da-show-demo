"""
Management command to create employee users quickly
Usage: python manage.py create_employee
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
import getpass


class Command(BaseCommand):
    help = 'Create a new employee user with access to the employee dashboard'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username for the employee',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the employee',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email for the employee',
        )
        parser.add_argument(
            '--staff',
            action='store_true',
            help='Make user a staff member (can access Django admin)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('  Create Employee User'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')

        # Get or create Employee group
        employee_group, created = Group.objects.get_or_create(name='Employee')
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created "Employee" group'))
        
        # Get username
        username = options.get('username')
        if not username:
            username = input('Username: ').strip()
            while not username:
                self.stdout.write(self.style.ERROR('Username cannot be empty'))
                username = input('Username: ').strip()
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'✗ User "{username}" already exists!'))
            return
        
        # Get password
        password = options.get('password')
        if not password:
            while True:
                password = getpass.getpass('Password: ')
                if not password:
                    self.stdout.write(self.style.ERROR('Password cannot be empty'))
                    continue
                password_confirm = getpass.getpass('Password (again): ')
                if password == password_confirm:
                    break
                self.stdout.write(self.style.ERROR('Passwords do not match. Try again.'))
        
        # Get email
        email = options.get('email')
        if not email:
            email = input('Email (optional): ').strip()
        
        # Get staff status
        is_staff = options.get('staff', False)
        if not is_staff and not options.get('username'):
            staff_input = input('Make this user a staff member? (can access Django admin) [y/N]: ').strip().lower()
            is_staff = staff_input in ['y', 'yes']
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=is_staff,
                is_active=True
            )
            
            # Add to Employee group
            user.groups.add(employee_group)
            
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('✓ Employee user created successfully!'))
            self.stdout.write('')
            self.stdout.write(f'  Username:    {username}')
            self.stdout.write(f'  Email:       {email or "(not set)"}')
            self.stdout.write(f'  Staff:       {"Yes" if is_staff else "No"}')
            self.stdout.write(f'  Group:       Employee')
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS(f'✓ User can now login at: /employee/login/'))
            self.stdout.write('')
            
            if is_staff:
                self.stdout.write(self.style.WARNING('⚠ This user can also access Django admin at: /admin/'))
                self.stdout.write('')
            
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating user: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Unexpected error: {e}'))

