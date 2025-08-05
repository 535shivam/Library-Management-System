from django.db import models
from datetime import timedelta

# Create your models here.

class CategoryModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BookModel(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    category = models.ForeignKey(CategoryModel , on_delete=models.SET_NULL , null=True)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    

class MemberModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name
    

class IssueModel(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    member = models.ForeignKey(MemberModel, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField(null=True,blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} to {self.member.name}"
    
    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.issue_date + timedelta(days=14)  
        super().save(*args, **kwargs)