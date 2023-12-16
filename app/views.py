from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
import math
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .forms import *
from .models  import *
from django.db.models import Count

def pop_tags():
    tag = Tag.objects.annotate(q_count=Count('questions')).order_by('-q_count')
    return tag[:6]

def paginate(request, objects, page_namber, per_page=10):
    try:
        page = request.GET.get('page', page_namber)
        paginator = Paginator(objects, per_page)
        return paginator.page(page)
    except Exception as err:
        print(f"Unexpected {err}")
    return []

def index(request, page_number=1):
    QUESTIONS = Question.objects.new_question()
    return render(request, 'index.html', {'objects': paginate(request, QUESTIONS, page_number), 'pop_tags': pop_tags()})

def hot(request, page_number=1):
    hot_question = Question.objects.hot_question()
    return render(request, 'index.html', {'objects': paginate(request, hot_question, page_number), 'pop_tags': pop_tags()})

def question(request, question_id, page_number=1):
    item = Question.objects.new_question().get(id=question_id)
    answers = Answer.objects.answer_question(question_id)
    if request.method == "GET":
        answer_form = AnswerForm(request.user, question_id)
    if request.method == "POST":
        if not request.user.is_authenticated:               #проверка на аутентификацию
            return redirect("/login")
        answer_form = AnswerForm(request.user, question_id, request.POST)
        if answer_form.is_valid():
            _answer = answer_form.save()
            if _answer is not None:
                my_answer = Answer.objects.filter(question__id=question_id).count()
                page_number_answer = math.ceil(my_answer / 10)
                request.method = "GET"
                return redirect(f"%s?page={page_number_answer}" % reverse("question", args=[question_id]))
            else:
                answer_form.add_error(field=None, error="Wrong text question")
    return render(request, 'question.html', context={'question': item, 'pop_tags': pop_tags(), 'objects': paginate(request, answers, page_number), 'form': answer_form})

def popular_tags(request, tag = '', page_number=1):
    tag = Tag.objects.get(tag=tag)
    question = Question.objects.top_tag_questions(tag)
    return render(request, 'index.html', {'objects': paginate(request, question, page_number), 'pop_tags': pop_tags()})

# Заходить на форму нового вопроса могут только авторизованные пользователи
@login_required(login_url='login/', redirect_field_name='continue')
def ask(request):
    if request.method == "GET":
        question_form = QuestionForm(request.user)
    if request.method == "POST":
        question_form = QuestionForm(request.user, request.POST)
        if question_form.is_valid():
            _question = question_form.save()
            if _question is not None:
                request.method = "GET"
                return redirect(reverse("question", args=[_question.id]))
            else:
                question_form.add_error(field=None, error="Wrong text question")
    return render(request, 'ask.html', context={'form': question_form, 'pop_tags': pop_tags()})

@csrf_protect
def log_in(request):
    if request.method == "GET":
        login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, "Wrong password or user does not exist")
    return render(request, 'login.html', context={'form': login_form, 'pop_tags': pop_tags()})

def signup(request):
    if request.method == "GET":
        user_form = RegisterForm()
    if request.method == "POST":
        user_form = RegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="A user with this name already exists")
    return render(request, 'register.html', context={'form': user_form, 'pop_tags': pop_tags()})

@login_required(login_url='login/', redirect_field_name='continue')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile, 'pop_tags': pop_tags()})

@csrf_protect
@login_required(login_url='login/', redirect_field_name='continue')
def edit_profile(request):
    if request.method == "GET":
        form = ProfileForm(initial=model_to_dict(request.user))
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    return render(request, 'edit_profile.html', context={'form': form, 'pop_tags': pop_tags()})

@csrf_protect
@login_required(login_url='login/', redirect_field_name='continue')
def like_question(request):
    id = request.POST.get('object_id')
    question = get_object_or_404(Question, pk=id)
    print(request.POST.get('like'))
    if request.POST.get('like') == "True":
        LikeQuestion.objects.toggle_like(user=request.user.profile, question=question)
    elif request.POST.get('like') == "False":
        LikeQuestion.objects.toggle_dislike(user=request.user.profile, question=question)
    count = question.rating
    return JsonResponse({"counter": count})

@csrf_protect
@login_required(login_url='login/', redirect_field_name='continue')
def like_answer(request):
    id = request.POST.get('object_id')
    answer = get_object_or_404(Answer, pk=id)
    if request.POST.get('like') == "True":
        LikeAnswer.objects.toggle_like(user=request.user.profile, answer=answer)
    elif request.POST.get('like') == "False":
        LikeAnswer.objects.toggle_dislike(user=request.user.profile, answer=answer)
    count = answer.rating
    return JsonResponse({"counter": count})

@csrf_protect
@login_required(login_url='login/', redirect_field_name='continue')
def answer_correct(request):
    id = request.POST.get('object_id')
    print(id)
    answer = get_object_or_404(Answer, pk=id)
    if answer.correct == True:
        answer.correct = False
    else:
        answer.correct = True
    answer.save()
    return JsonResponse({"status": "OK"})

def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))

def error_404_view(request, exception):
    return render(request, 'error/404.html')