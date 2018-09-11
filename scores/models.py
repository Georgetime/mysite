from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Class(models.Model):
    class_name = models.CharField(max_length=160)

    def __str__(self):
        return self.class_name

class UserProfile(models.Model):
    type_choices = (
        (1, '教师'),
        (0, '学生'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    org = models.CharField('Organization', max_length=128, blank=True)
    telephone = models.CharField('Telephone', max_length=50, blank=True)
    mod_date = models.DateTimeField('Last modified', auto_now=True)
    user_type = models.IntegerField('User Type', choices=type_choices, default=0)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.user.__str__()

class AccessControl(models.Model):
    '''
    自定义权限控制
    '''

    class Meta:
        permissions = (
            ('access_dashboard', u'控制面板'),
            ('access_score_manage', u'成绩管理'),
            ('access_schedule_manage', u'课程管理'),
            ('access_assignment_manage', u'作业管理'),
        )

class Teacher(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    teacher_name = models.CharField(max_length=160, blank=True)
    teacher_telephone = models.CharField(max_length=11, blank=True)

    def __str__(self):
        return self.teacher.__str__()

class Subject(models.Model):
    subject_name = models.CharField(max_length=160)

    def __str__(self):
        return self.subject_name

class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    student_name = models.CharField(max_length=160, blank=True)
    student_sex = models.IntegerField(default=0, blank=True)
    student_birthday = models.DateField(blank=True, null=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.student.__str__()


class Schedule(models.Model):
    term_choice =(
        (1, '第一学年上学期'),
        (2, '第一学年下学期'),
        (3, '第二学年上学期'),
        (4, '第二学年下学期'),
        (5, '第三学年上学期'),
        (6, '第三学年下学期'),
    )

    schedule_name = models.CharField(default=1, max_length=160)
    term = models.IntegerField(choices=term_choice, blank=True, null=True)
    year = models.DateField(blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    representative = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.schedule_name

class Assignment(models.Model):
    assignment_title = models.CharField(max_length=160, unique=True)
    assignment_detail = models.CharField(max_length=1200, blank=True)
    create_date = models.DateField(auto_now_add=True)
    finish_date = models.DateField(blank=True, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.assignment_title

class Score(models.Model):
    SCORE_LEVEL = (
        (0, 'Null'),
        (10, 'A+'),
        (8, 'A'),
        (6, 'B+'),
        (4, 'B'),
        (2, 'C+'),
        (1, 'C'),
    )
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE,)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    level = models.IntegerField(choices=SCORE_LEVEL, default=0)
    grade = models.IntegerField(default=0, blank=True, null=True)
    extra_grade = models.IntegerField(default=0, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'assignment')

    def __str__(self):
        return self.assignment.assignment_title

class Total(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)

    class Meta:
        unique_together = ('student', 'schedule')

    def __str__(self):
        return self.student.student

    # class Meta:
    #     ordering = ['assignment']