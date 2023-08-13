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
    path('edit_page/view_pdf/',views.viewPDF, name='view_pdf'),
    path('paper/',views.paper, name='paper'),
    path('paperSolution/<int:paper_id>',views.paperSolution, name='paper-solution'),
    path('profile/',views.profile, name='profile'),
    path('user_register/',views.UserRegister, name='user-register'),
    path('user_login/',views.User_Login, name='user-login'),
    path('save_paper/<int:paper_id>/', views.save_paper, name='save_paper'),
    path('verify/<str:token>/',views.verify),


path('edit_page/<int:paper_id>',views.editPaper, name='edit-paper'),
path('view_page/<int:paper_id>',views.viewPaper, name='view-paper'),
    
]

