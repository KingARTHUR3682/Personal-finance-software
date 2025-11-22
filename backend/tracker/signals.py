from django.db.models.signals import post_save
from fjango.dispatch import receiver
from django.contrib.auth.models import User
from .models import Category

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