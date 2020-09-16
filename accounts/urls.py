from django.urls import path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import TemplateView
from . import views

urlpatterns = [

path('', views.profilePage, name = 'profilePage'),
path('register/', views.registerPage, name = 'registerPage'),
path('login/', views.loginPage, name = "loginPage"),
path('logout/', views.logoutUser, name = 'logoutUser'),

path('activate/', TemplateView.as_view(template_name='accounts/activatepage.html'), name='activatePage'),
path('activate/<uidb64>/<token>/', views.activateUser, name = 'activateUser'),

path('edit/', views.editProfile, name = 'editProfile'),
path('editpassword/', views.editPassword, name = 'editPassword'),

path('resetpassword/', PasswordResetView.as_view(template_name = 'accounts/passwordreset.html'), name = 'password_reset'),
path('resetpassword/sent/', PasswordResetDoneView.as_view(template_name = 'accounts/passwordresetdone.html'), name = 'password_reset_done'),
path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name = 'accounts/passwordresetconfirm.html'), name = 'password_reset_confirm'),
path('resetpassword/complete/', PasswordResetCompleteView.as_view(template_name = 'accounts/passwordresetcomplete.html'), name = 'password_reset_complete')

]