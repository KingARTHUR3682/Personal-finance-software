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
    # Check if a receipt exists
    if instance.receipt:
        # If this is an update, check if the receipt is actually new to avoid re-compressing
        if instance.pk:
            try:
                old_instance = Expense.objects.get(pk=instance.pk)
                if old_instance.receipt == instance.receipt:
                    return  # The image hasn't changed, do nothing
            except Expense.DoesNotExist:
                pass  # It's a new expense

        # Open the image using Pillow
        img = Image.open(instance.receipt)

        # Convert images (like PNGs with transparency) to RGB so they can be saved as JPEG
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # Resize logic: limit width to 1080px (maintaining aspect ratio)
        max_width = 800
        if img.width > max_width:
            output_size = (max_width, int(img.height * (max_width / img.width)))
            img.thumbnail(output_size)

        # Compress the image
        im_io = BytesIO()
        # Quality=70 is a good balance between size and visibility for receipts
        img.save(im_io, format='JPEG', quality=60, optimize=True)
        
        # Change the extension to .jpg since we converted it
        new_filename = os.path.splitext(instance.receipt.name)[0] + '.jpg'

        # Save the new compressed file back to the instance
        instance.receipt.save(new_filename, ContentFile(im_io.getvalue()), save=False)