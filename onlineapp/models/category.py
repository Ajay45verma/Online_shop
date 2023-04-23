from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=50,default="")
    def __str__(self):
        return self.name

    @staticmethod
    def get_all_Category():
        return Category.objects.all()