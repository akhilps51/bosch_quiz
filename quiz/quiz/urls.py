"""quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from bosch.views import *
import nested_admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('_nested_admin', include('nested_admin.urls')),
    path('', Home.as_view(), name = "home"),
    path('login/', Login.as_view(), name = "login"),
    path('logout/', LogoutView.as_view(template_name='home.html'), name = "logout"),
    path('quiz-category-list/', login_required(QuizCategoryView.as_view()), name = "quiz_category_list"),
    path('quiz/<int:c_id>/<int:q_id>/', login_required(QuizView.as_view()), name="quiz"),
    path('result/<int:u_id>/<int:c_id>/', login_required(ResultView.as_view()), name="result")
]
