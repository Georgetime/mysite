from django.forms import modelformset_factory
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from django.views import generic
from django.utils import timezone
from .models import Student, Teacher, Assignment, Schedule, Score, Subject, UserProfile, Total
from .forms import LoginForm, RegistrationForm, ProfileForm, PwdChangeForm, make_score_form, AssignmentForm
from functools import wraps

# Create your views here.

def login(request):
    print(request.method)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # user = Student.objects.filter(student_name__exact=username, student_password__exact=password)
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # request.session['is_login'] = '1'
                auth.login(request, user)
                request.session['user_id'] = user.id
                return HttpResponseRedirect(reverse('scores:index'))
                # return HttpResponseRedirect('/scores/')
            else:
                return render(request, 'scores/login.html',
                              {'form': form, 'message': 'Wrong Username or password, Try again!'})
    else:
        print(123)
        form = LoginForm()
    return render(request, "scores/login.html", {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user_type = form.cleaned_data['user_type']
            password = form.cleaned_data['password2']
            user = User.objects.create_user(username=username, password=password, email=email)
            user_profile = UserProfile(user=user, user_type=user_type)
            user_profile.save()
            if user_type == '0':
                student = Student(student=user)
                student.save()
            elif user_type == '1':
                teacher = Teacher(teacher=user)
                teacher.save()
            else:
                print('NUll')
            return HttpResponseRedirect('/scores/login/')
    else:
        form = RegistrationForm()
    return render(request, "scores/registration.html", {'form': form})

@login_required
def profile(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'scores/profile.html', {'user': user})

@login_required
def profile_update(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()
            return HttpResponseRedirect(reverse('scores:profile', args=[user.id]))
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name,
                        'org': user_profile.org, 'telephone': user_profile.telephone, }
        form = ProfileForm(default_data)
    return render(request, 'scores/profile_update.html', {'form': form, 'user': user})

@login_required
def pwd_change(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = PwdChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['old_password']
            username = user.username
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect("/scores/login/")

            else:
                return render(request, 'scores/pwd_change.html',
                              {'form': form, 'user': user, 'message': 'Old password is wrong. Try again'})
    else:
        form = PwdChangeForm()
    return render(request, 'scores/pwd_change.html', {'form': form, 'user': user})

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/scores/login/")

# def logout(request):
#     request.session['is_login'] = ''
#     request.session['user_id'] = ''
#     return HttpResponseRedirect('/scores/login/')

# 说明："wraps"这个装饰器的作用，就是在每个视图函数被调用时，都验证下有没法有登录，
# 如果有过登录，则可以执行新的视图函数，
# 否则没有登录则自动跳转到登录页面。
# def checklogin(func):
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#         if request.session.get('is_login') == '1':
#             return func(request, *args, **kwargs)
#         else:
#             return HttpResponseRedirect("/scores/login/")
#     return wrapper

def index(request):
    latest_Assignment_list = Assignment.objects.filter(create_date__lte=timezone.now()).order_by('-create_date')[:5]
    context = {'latest_Assignment_list': latest_Assignment_list, }
    # output = ', '.join([q.question_text for q in latest_question_list])
    user_id = request.session.get('user_id')
    if user_id:
        user = get_object_or_404(User, pk=user_id)
        context['user'] = user
    else:
        context['user'] = 'Guest'
    return render(request, 'scores/index.html', context)

@login_required
def score_detail(request, schedule_term):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    student = get_object_or_404(Student, student=user)
    subject_list = Subject.objects.all()
    term_schedule_list = Schedule.objects.filter(class_name=student.class_name, term=schedule_term)
    score_list = Score.objects.filter(student=student, assignment__schedule__term__in=term_schedule_list)
    for schedule in term_schedule_list:
        total = 0
        schedule_score_list = Score.objects.filter(student=student, assignment__schedule=schedule)
        for schedule_score in schedule_score_list:
            total += schedule_score.grade + schedule_score.extra_grade
        Total.objects.get_or_create(student=student, schedule=schedule)
        student_total = Total.objects.get(student=student, schedule=schedule)
        student_total.total = total
        student_total.save()
    total = Total.objects.filter(student=student)
    context = {
        'student': student,
        'subject_list': subject_list,
        'score_list': score_list,
        'total_list': total,
    }
    return render(request, 'scores/score_detail.html', context)

@login_required
def score(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    student = get_object_or_404(Student, student=user)
    context = {
        'student': student,
    }
    return render(request, 'scores/score.html', context)

@login_required
def score_manage(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    latest_Assignment_list = Assignment.objects.filter(
        schedule__representative__student=user,
        create_date__lte=timezone.now()
    ).order_by('-create_date')[:5]
    context = {'latest_Assignment_list': latest_Assignment_list, }
    return render(request, 'scores/score_manage.html', context)

@login_required
def score_manage_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    context = {'assignment': assignment}
    return render(request, 'scores/score_manage_detail.html', context)

def check_grade(student,assignment):
    flag = True
    student_score_list = Score.objects.filter(
        student=student,
        assignment__schedule=assignment.schedule,
        assignment__finish_date__lte=assignment.finish_date
    ).order_by('assignment__finish_date')
    if student_score_list.__len__() > 1:
        for student_score in student_score_list:
            if student_score.level >= 10:
                flag = False
                break
    return flag

def get_grade_list(student,assignment,level):
    coefficient_list = {
        10: 0.1,
        8: 0.05,
        6: -0.3,
        4: -0.4,
        2: -0.6,
        1: -0.8,
        0: 0,
    }
    grade = int(level)
    extra_grade = 0
    keep_count = 0
    student_score_list = Score.objects.filter(
        student=student,
        assignment__schedule=assignment.schedule,
        assignment__finish_date__lte=assignment.finish_date
    ).order_by('assignment__finish_date')
    if level == 10 and check_grade(student, assignment):
        extra_grade = 30
    for student_score in student_score_list:
        if student_score.assignment != assignment:
            if student_score.level == level:
                keep_count += 1
            elif student_score.level - level > 4:
                grade = -int(level)/2
                break
            else:
                break
    print(keep_count)
    grade = grade * keep_count * coefficient_list[int(level)] + grade
    grade_list = {'grade': grade, 'extra_grade': extra_grade}
    return grade_list

@login_required
def score_manage_input(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    assignment_score_list = Score.objects.filter(assignment=assignment)
    class_student = assignment.schedule.class_name.student_set.all()
    ScoreForm = make_score_form(assignment_id)
    ScoreFormSet = modelformset_factory(
        Score,
        form=ScoreForm,
        extra=class_student.count(),
        max_num=class_student.count()
    )
    if request.method == 'POST':
        formset = ScoreFormSet(request.POST, request.FILES, queryset=assignment_score_list)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.assignment = assignment
                student = instance.student
                student_score = instance.level
                grade_list = get_grade_list(student, assignment, student_score)
                instance.extra_grade = grade_list['extra_grade']
                instance.grade = grade_list['grade']
                instance.save()
            formset.save_m2m()
            return render(
                request,
                'scores/score_manage_detail.html',
                {'assignment': assignment, 'succeed_msg': "Save Succeed!"}
            )
    else:
        formset = ScoreFormSet(
            queryset=assignment_score_list,
        )
    context = {'assignment': assignment, 'formset': formset}
    return render(request, 'scores/score_manage_input.html', context)

@login_required
def assignment_update(request, assignment_id):

    return render(request, 'scores/assignment_update.html')

@login_required
def assignment_manage(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    student = get_object_or_404(Student, student=user)
    schedule = get_object_or_404(Schedule, representative=student)
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            new_assignment = form.save()
            class_student = new_assignment.schedule.class_name.student_set.all()
            for student in class_student:
                s = Score.objects.create(student=student, assignment=new_assignment)
                s.save()
            return HttpResponseRedirect(reverse('scores:score_manage_detail', args=[new_assignment.id]))
    else:
        form = AssignmentForm(initial={
            'schedule': schedule.id
            })
    latest_Assignment_list = Assignment.objects.filter(
        schedule__representative__student=user,
        create_date__lte=timezone.now()
    ).order_by('-finish_date')[:5]
    context = {'form': form, 'latest_Assignment_list': latest_Assignment_list, }
    return render(request, 'scores/assignment_manage.html', context)

@login_required
def detail(request, assignment_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    context = {'assignment': assignment}
    return render(request, 'scores/detail.html', context)

@login_required
def vote(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    try:
        selected_choice = assignment.score_set.get(pk=request.POST['choice'])
    except(KeyError, Score.DoesNotExist):
        return render(request, 'scores/detail.html', {
            'assignment': assignment,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('scores:detail', args=(assignment.id,)))
        # This code does have a small problem called a race condition.