from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.views.generic import DetailView
from bosch.models import Category, Question, Answer, QuizResult, QuizProgress
from django.contrib.auth.models import User
from django.urls import reverse




# Create your views here.

class Home(TemplateView):
	template_name = 'home.html'


class Login(LoginView):
	template_name = 'login.html'
	success_url = 'quiz_category_list'


class QuizCategoryView(ListView):
	model = Category
	template_name = 'category_list.html'


class QuizView(DetailView):
	model = Question
	template_name = 'quiz_app.html'


	def get(self, request, *args, **kwargs):
		c_id = kwargs['c_id']
		q_id = kwargs['q_id']
		context = {}
		context['page'] = "quizz"
		context['status'] = False
		if q_id == 0:
			user = User.objects.filter(id=request.user.id).first()
			category = Category.objects.filter(id=c_id).first()
			quizResult = QuizResult.objects.filter(user=user, category=category).first()
			if quizResult:
				progress = QuizProgress.objects.all().filter(attender__user_id=request.user.id)
				result = QuizResult.objects.get(user_id=request.user.id, category_id=c_id)
				context['status'] = True
				context['result'] = result
				context['progress'] = progress
			else:
				questions = Question.objects.filter(category_id=c_id, draft=0).order_by('order')
				q_ids = [question.id for question in questions]
				context['is_question'] = False
				if len(q_ids):
					context['is_question'] = True
				request.session['q_ids'] = q_ids
				context['start_quizz'] = True
		else:
			context['is_question'] = True
			context['question'] =  Question.objects.filter(id=q_id).first()
		if not context['status']:
			context['category_id'] = c_id
			context['question_id'] = request.session['q_ids'][0]
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		user_ans = request.POST.get('answer', False)
		c_id = kwargs['c_id']
		q_id = kwargs['q_id']
		q_ids = request.session['q_ids']
		ans = Answer.objects.filter(question_id=q_id, is_correct=1).first()
		ans_id = ans.id if ans else None
		user = User.objects.filter(id=request.user.id).first()
		category = Category.objects.filter(id=c_id).first()
		question = Question.objects.filter(id=q_id).first()
		correct_answer = Answer.objects.get(question_id_id=q_id, is_correct=True)
		try:
			quizResult = QuizResult.objects.get(user=user, category=category)
		except:
			quizResult = QuizResult.objects.create(user=user, category=category)
		if user_ans:
			if int(user_ans) == int(ans_id):
				quizResult.correct_answer += 1
				quizResult.save()
			answer = Answer.objects.filter(id=user_ans).first()
			quizProgress = QuizProgress.objects.create(attender=quizResult, question=question, answer=answer, correct_answer=correct_answer.answer)
		else:
			quizProgress = QuizProgress.objects.create(attender=quizResult, question=question, correct_answer=correct_answer.answer)
		q_ids.pop(0)
		request.session['q_ids'] = q_ids
		try:
			next_q_id = request.session['q_ids'][0]
			return redirect(reverse('quiz', args=(c_id, next_q_id)))
		except:
			quizResult.completed = True
			quizResult.save()
			return redirect(reverse('result', args=(request.user.id, c_id)))


class ResultView(DetailView):
	model = QuizResult
	template_name = 'quiz_app.html'

	def get(self, request, *args, **kwargs):
		c_id = kwargs['c_id']
		u_id = kwargs['u_id']
		context = {}
		context['page'] = "result"
		result = QuizResult.objects.get(user_id=request.user.id, category_id=c_id)
		progress = QuizProgress.objects.all().filter(attender__user_id=request.user.id)
		context['result'] = result
		context['progress'] = progress
		return self.render_to_response(context)