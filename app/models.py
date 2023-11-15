from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class QuestionManager(models.Manager):
    def top_tag_questions(self, tag_id):
        question = Question.objects.filter(tags=tag_id.id)
        return question.annotate(answer_count=Count('answer')).order_by('-date_writen')
    def new_question(self):
        return self.annotate(answer_count=Count('answer')).order_by('-date_writen')
    def hot_question(self):
        hot = self.annotate(like_count=Count('like'), answer_count=Count('answer')).order_by('-like_count')
        return hot

class AnswerManager(models.Manager):
    def answer_question(self, question_id):
        answers = self.filter(question__id=question_id).annotate(like_count=Count('like')).order_by('-like_count')
        for ans in answers:
            ans.correct = True
            break
        return answers

class Question(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    date_writen = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name='questions')
    user = models.ForeignKey('Profile', max_length=256, on_delete=models.PROTECT)
    like = models.ManyToManyField('Profile', through="LikeQuestion", related_name="question_likes", related_query_name="question_like")

    objects = QuestionManager()
    def __str__(self):
        return f"{self.title} {self.date_writen}"

class LikeQuestion(models.Model):
    positive = models.BooleanField(null=True)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

class Answer(models.Model):
    content = models.TextField()
    correct = models.BooleanField(default=False)
    question = models.ForeignKey('Question', on_delete=models.PROTECT, null=True, related_query_name="answer")  # точно
    user = models.ForeignKey('Profile', on_delete=models.PROTECT)
    like = models.ManyToManyField('Profile', through="LikeAnswer", related_name="answer_likes",
                                  related_query_name="answer_like")

    objects = AnswerManager()
    def __str__(self):
        return f"{self.content}"

class LikeAnswer(models.Model):
    positive = models.BooleanField(null=True)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=256)
    login = models.CharField(max_length=256)
    avatar = models.ImageField(null=True, blank=True)   # upload_to="avatarka/"
    is_delete = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.nickname}"

class Tag(models.Model):
    tag = models.CharField(max_length=256)
    def __str__(self):
        return f"{self.tag}"