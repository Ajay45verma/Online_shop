from django.db import models

class Customer(models.Model):
    first_name=models.CharField(max_length=30, default='')
    last_name=models.CharField(max_length=30, default="")
    phone=models.CharField( max_length=15, default="")
    email=models.EmailField()
    password=models.CharField( max_length=50, default="")

    def __str__(self) -> str:
        return self.first_name+self.last_name

    def IsExist(self):
        if Customer.objects.filter(email=self.email):
            return True
        else:
            return False



    @staticmethod
    def get_customerData_by_email(email):
        try:
          return Customer.objects.get(email=email)      
        except:
            return False