from django.contrib import admin
from django.urls import path,include
from api.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'classView',ClassViewSet)
router.register(r'subjectView',SubjectViewSet)
router.register(r'bookView',BookViewSet)
router.register(r'chapterView',ChapterViewSet)
router.register(r'theoryquestionView',TheoryQuestionViewSet)
router.register(r'mcqView',MCQViewSet)
router.register(r'fillupView',FillUpViewSet)
router.register(r'truefalseView',TrueFalseViewSet)

urlpatterns = [
    path('',include(router.urls)),
    
    path('search-questions/', SearchQuestionsAPIView.as_view(), name='question_api'),

    path('classes/', ClassListAPIView.as_view(), name='class_list'),
    path('subjects/', SubjectListAPIView.as_view(), name='subject_list'),
     path('classes/<pk>/',ClassDetailAPIView.as_view(),name='class-detail'),
    path('subjects/<pk>/',SubjectDetailAPIView.as_view(),name='subject-detail'),
    path('chapters/<pk>/',ChapterDetailAPIView.as_view(),name='chapter-detail'),
    path('theory_questions/<pk>/',TheoryQuestionDetailAPIView.as_view(),name='chapter-detail'),
    path('fillups/<pk>/',FillUpDetailAPIView.as_view(),name='chapter-detail'),
    path('mcqs/<pk>/',MCQDetailAPIView.as_view(),name='chapter-detail'),
    path('true_falses/<pk>/',TrueFalseDetailAPIView.as_view(),name='chapter-detail'),
    path('classes/<int:class_id>/subjects/', ClassSubjectsAPIView.as_view(), name='subject_list'),

    path('subjects/<int:subject_id>/books/',SubjectBooksAPIView.as_view(),name='book-list'),
    path('books/<int:book_id>/chapters/',BookChaptersAPIView.as_view(),name='book-list'),


    path('chapters/<int:chapter_id>/theory_questions/',ChapterTheoryQuestionsListView.as_view(),name='theory_questions_corresponding_chapter'),
    path('chapters/<int:chapter_id>/fillups/',ChapterFillUpsListView.as_view(),name='theory_questions_corresponding_chapter'),
    path('chapters/<int:chapter_id>/true_falses/',ChapterTrueFalsesListView.as_view(),name='theory_questions_corresponding_chapter'),
    path('chapters/<int:chapter_id>/mcqs/',ChapterMCQsListView.as_view(),name='theory_questions_corresponding_chapter'),
    path('chapters/<int:chapter_id>/theory_questions_length/', TheoryQuestionLengthAPIView.as_view(), name='theory-question-_corresponding_to_length'),
    path('chapters/<int:chapter_id>/theory_questions_difficulty/', TheoryQuestionDifficultyAPIView.as_view(), name='theory-question-_corresponding_to_difficulty'),

    path('chapterFilterQuestions/', filter_question.as_view(), name='your_endpoint'),


]