from django.shortcuts import render
from django.core.paginator import Paginator
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
    return render(request, 'question.html', {'question': item, 'pop_tags': pop_tags(), 'objects': paginate(request, answers, page_number)})

def popular_tags(request, tag = '', page_number=1):
    tag_id = Tag.objects.get(tag=tag)
    question = Question.objects.top_tag_questions(tag_id)
    return render(request, 'index.html', {'objects': paginate(request, question, page_number), 'pop_tags': pop_tags()})

def ask(request):
    return render(request, 'ask.html', {'pop_tags': pop_tags()})

def login(request):
    return render(request, 'login.html', {'pop_tags': pop_tags()})

def signup(request):
    return render(request, 'register.html', {'pop_tags': pop_tags()})

def profile(request):
    return render(request, 'profile.html', {'pop_tags': pop_tags()})

def error_404_view(request, exception):
    print("-----------------")
    return render(request, 'error/404.html')