from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class ExaminationCenter(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Assignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    center = models.ForeignKey(ExaminationCenter, on_delete=models.CASCADE)
    date_assigned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.name} -> {self.center.name}"
