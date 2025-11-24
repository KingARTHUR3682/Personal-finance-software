from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Category

from django.db.models.signals import pre_save
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import os
from .models import Expense

# This is a function that should automatic runs every time when a user in saved.
@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        # --- Expense Categories ---

        # Food
        food = Category.objects.create(name='Food', icon='🍔', type='expense', user=instance)
        Category.objects.create(name='Breakfast', icon='🍞', type='expense', parent=food, user=instance)
        Category.objects.create(name='Lunch', icon='🍗', type='expense', parent=food, user=instance)
        Category.objects.create(name='Dinner', icon='🍜', type='expense', parent=food, user=instance)
        Category.objects.create(name='Dessert', icon='🍦', type='expense', parent=food, user=instance)

        # Transport
        transport = Category.objects.create(name='Transport', icon='🚗', type='expense', user=instance)
        Category.objects.create(name='Grab/Taxi', icon='🚕', type='expense', parent=transport, user=instance)
        Category.objects.create(name='Fuel', icon='⛽', type='expense', parent=transport, user=instance)
        Category.objects.create(name='Public Transport', icon='🚆', type='expense', parent=transport, user=instance)

        # Shopping
        shopping = Category.objects.create(name='Shopping', icon='🛍️', type='expense', user=instance)
        Category.objects.create(name='Groceries', icon='🥦', type='expense', parent=shopping, user=instance)
        Category.objects.create(name='Clothes', icon='👕', type='expense', parent=shopping, user=instance)

        # Entertainment
        entertainment = Category.objects.create(name='Entertainment', icon='🎉', type='expense', user=instance)
        Category.objects.create(name='Movies', icon='🎬', type='expense', parent=entertainment, user=instance)
        Category.objects.create(name='Games', icon='🎮', type='expense', parent=entertainment, user=instance)

        # --- Income Categories ---
        income = Category.objects.create(name='Income', icon='💰', type='income', user=instance)
        Category.objects.create(name='Salary', icon='💵', type='income', parent=income, user=instance)
        Category.objects.create(name='Bonus', icon='🎁', type='income', parent=income, user=instance)


@receiver(pre_save, sender=Expense)
def compress_receipt_image(sender, instance, **kwargs):
    if not instance.receipt:
        return

    # If updating, check if image actually changed to avoid re-compressing
    if instance.pk:
        try:
            old_instance = Expense.objects.get(pk=instance.pk)
            if old_instance.receipt == instance.receipt:
                return
        except Expense.DoesNotExist:
            pass

    try:
        # Open the file from Cloud Storage before reading
        if not instance.receipt.closed:
             instance.receipt.open()
        
        # Read image with Pillow
        image_field = instance.receipt
        with Image.open(image_field) as img:
            
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Resize
            max_width = 800
            if img.width > max_width:
                output_size = (max_width, int(img.height * (max_width / img.width)))
                img.thumbnail(output_size)

            # Compress
            im_io = BytesIO()
            img.save(im_io, format='JPEG', quality=60, optimize=True)
            
            new_filename = os.path.splitext(instance.receipt.name)[0] + '.jpg'

            # Save back to field (save=False prevents infinite loop)
            instance.receipt.save(new_filename, ContentFile(im_io.getvalue()), save=False)

    except Exception as error:
        print(f"Error compressing image: {error}")