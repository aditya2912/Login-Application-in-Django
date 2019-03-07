from django.contrib import admin
from django.urls import path
from projectapp.views import hello, login, registerPage, registerUser, loginPage, userLogin, enterUserDetails, enterUserDetailsPage, viewUserDetails , updateUserDetails, submitUpdatedUserDetails, logOut, rubricsForm, submitRubrics, viewRubricsForUser, adminLogOut, deleteUser, deleteFormForUser


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'hello/', hello),
    path(r'your-name/', login),
    path(r'register/', registerPage),
    path(r'userRegistered/', registerUser),
    path(r'login/', loginPage),
    path(r'userLogin/', userLogin),
    path(r'enterUserDetails/', enterUserDetails),
    path(r'enterUserDetailsPage/', enterUserDetailsPage),
    path(r'viewUserDetails/', viewUserDetails),
    path(r'updateUserDetails/', updateUserDetails),
    path(r'submitUpdatedUserDetails/', submitUpdatedUserDetails),
    path(r'logOut/', logOut),
    path(r'rubricsForm/', rubricsForm),
    path(r'rubricSubmit/', submitRubrics),
    path(r'viewRubricsForUser/', viewRubricsForUser),
    path(r'adminLogOut/', adminLogOut),
    path(r'deleteUser/', deleteUser),
    path(r'deleteForm/', deleteFormForUser)
]
