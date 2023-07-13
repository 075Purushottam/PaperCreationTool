from django.urls import path
from ToolCore import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerPage,name='register'),
    path('tool/',views.toolPage,name='tool'),
    path('bookChapter/',views.bookChapter,name='book-chapter'),
    path('bookChapter/view_pdf/',views.viewPDF, name='view_pdf'),
    path('paper/',views.paper, name='paper'),
    path('paperSolution/',views.paperSolution, name='paper-solution'),
    path('profile/',views.profile, name='profile'),

]

