from django.db import models

class Classroom(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey('accounts.UserProfile', on_delete=models.CASCADE, related_name='teacher_classrooms')
    students = models.IntegerField()
    subject = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=50)
    student = models.ManyToManyField('accounts.UserProfile', related_name='student_classrooms', blank=True)
    
    
    
    def __str__(self):
        return self.name