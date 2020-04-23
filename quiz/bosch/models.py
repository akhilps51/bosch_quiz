from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# Create your models here.



class Category(models.Model):
	category = models.CharField(max_length=50, unique=True)
	question_count = models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created']


class Question(models.Model):
	category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
	question = models.CharField(max_length=1000)
	order = models.IntegerField(default=0)
	draft = models.BooleanField(blank=True, default=False)

	def __str__(self):
		return self.question


class Answer(models.Model):
	question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
	answer = models.CharField(max_length=100)
	is_correct = models.BooleanField(default=False)

	def __str__(self):
		return self.answer


class QuizResult(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	correct_answer = models.IntegerField(default=0)
	completed = models.BooleanField(blank=True, default=False)

	def __str__(self):
		return self.user.username


class QuizProgress(models.Model):
	attender = models.ForeignKey(QuizResult, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
	correct_answer = models.CharField(max_length=100)

	def __str__(self):
		return self.question.question


# @receiver(post_save, sender=Category)
# def set_default_quiz(sender, instance, created, **kwargs):
# 	category = Category.objects.filter(id=instance.id)
# 	category.update(questions_count=)