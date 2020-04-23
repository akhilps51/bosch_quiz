from django.contrib import admin
from bosch.models import Category, Question, Answer, QuizResult, QuizProgress
import nested_admin


class AnswerInline(nested_admin.NestedTabularInline):
	model = Answer
	extra = 4
	max_num = 4


class QuestionInline(nested_admin.NestedTabularInline):
	model = Question
	inlines = [AnswerInline,]
	extra = 2


class QuizCategory(nested_admin.NestedModelAdmin):
	model = Question
	inlines = [QuestionInline,]
	list_display = ('category', 'question_count', 'created')


class QuizTakerResponse(admin.TabularInline):
	model = QuizProgress


class QuizTakerAdmin(admin.ModelAdmin):
	inlines = [QuizTakerResponse,]


admin.site.register(Category, QuizCategory)
admin.site.register(QuizResult, QuizTakerAdmin)
admin.site.register(QuizProgress)