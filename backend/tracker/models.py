from django.db import models
from django.contrib.auth.models import User

# Category model
class Category(models.Model):
    TRANSACTION_TYPES = [
        ('expense', 'Expense'),
        ('income', 'Income')
    ]
    name = models.CharField(max_length=100)
    # Icon name
    icon = models.CharField(max_length=50, default='mdi-help-circle')

    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='expense')

    # If parent = null, this category = main category
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

class Expense(models.Model):
    TRANSACTION_TYPES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='expense')

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.CharField(max_length=255, blank=True, null=True)
    
    date = models.DateField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type}: {self.amount}"