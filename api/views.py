from django.shortcuts import render
from rest_framework import generics,viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import *
from api.serializers import *

# ViewSet for Creating Data
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class=ClassSerializer
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class=SubjectSerializer
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class=BookSerializer
class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class=ChapterSerializer
class TheoryQuestionViewSet(viewsets.ModelViewSet):
    queryset = TheoryQuestion.objects.all()
    serializer_class=TheoryQuestionSerializer
class FillUpViewSet(viewsets.ModelViewSet):
    queryset = FillUp.objects.all()
    serializer_class=FillUpSerializer
class MCQViewSet(viewsets.ModelViewSet):
    queryset = MCQ.objects.all()
    serializer_class=MCQSerializer
class TrueFalseViewSet(viewsets.ModelViewSet):
    queryset = TrueFalse.objects.all()
    serializer_class=TrueFalseSerializer


#ListAPIView only read
# Classes and Subjects

# classes/
class ClassListAPIView(generics.ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
# subjects/
class SubjectListAPIView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

# classes/{class_id}/
class ClassDetailAPIView(generics.RetrieveAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
# subjects/{subject_id}
class SubjectDetailAPIView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
# chapters/{chapter_id}
class ChapterDetailAPIView(generics.RetrieveAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
# theory_questions/{question_id}
class TheoryQuestionDetailAPIView(generics.RetrieveAPIView):
    queryset = TheoryQuestion.objects.all()
    serializer_class = TheoryQuestionSerializer
class FillUpDetailAPIView(generics.RetrieveAPIView):
    queryset = FillUp.objects.all()
    serializer_class = FillUpSerializer
class MCQDetailAPIView(generics.RetrieveAPIView):
    queryset = MCQ.objects.all()
    serializer_class = MCQSerializer
class TrueFalseDetailAPIView(generics.RetrieveAPIView):
    queryset = TrueFalse.objects.all()
    serializer_class = TrueFalseSerializer
# classes/{class_id}/subjects/
class ClassSubjectsAPIView(generics.ListAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        return Subject.objects.filter(Class_id=class_id)
    
# subjects/<subject_id>/books/
class SubjectBooksAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        subject_id = self.kwargs['subject_id']
        return Book.objects.filter(Subject_id=subject_id)

class BookChaptersAPIView(generics.ListAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Chapter.objects.filter(Book_id=book_id)

class ChapterTheoryQuestionsListView(generics.ListAPIView):
    serializer_class = TheoryQuestionSerializer

    def get_queryset(self):
        chapter_id = self.kwargs['chapter_id']
        return TheoryQuestion.objects.filter(Chapter_id=chapter_id)

class ChapterMCQsListView(generics.ListAPIView):
    serializer_class = MCQSerializer

    def get_queryset(self):
        chapter_id = self.kwargs['chapter_id']
        return MCQ.objects.filter(Chapter_id=chapter_id)
    
class ChapterFillUpsListView(generics.ListAPIView):
    serializer_class = FillUpSerializer

    def get_queryset(self):
        chapter_id = self.kwargs['chapter_id']
        return FillUp.objects.filter(Chapter_id=chapter_id)
    
class ChapterTrueFalsesListView(generics.ListAPIView):
    serializer_class = TrueFalseSerializer

    def get_queryset(self):
        chapter_id = self.kwargs['chapter_id']
        return TrueFalse.objects.filter(Chapter_id=chapter_id)

class TheoryQuestionLengthAPIView(APIView):
    serializer_class = TheoryQuestionSerializer

    def get(self, request, chapter_id):
        length_filter = request.query_params.get('length')
        
        queryset = TheoryQuestion.objects.filter(Chapter_id=chapter_id, length__iexact=length_filter)
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
class TheoryQuestionDifficultyAPIView(APIView):
    serializer_class = TheoryQuestionSerializer

    def get(self, request, chapter_id):
        difficulty_filter = request.query_params.get('difficulty')
        
        queryset = TheoryQuestion.objects.filter(Chapter_id=chapter_id, difficulty__iexact=difficulty_filter)
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class SearchQuestionsAPIView(APIView):
    def get(self, request):
        query = request.GET.get('q')
        theory_questions = TheoryQuestion.objects.all()
        fillup_questions = FillUp.objects.all()
        truefalse_questions = TrueFalse.objects.all()
        mcq_questions = MCQ.objects.all()

        if query:
            theory_questions = theory_questions.filter(question__icontains=query)
            fillup_questions = fillup_questions.filter(question__icontains=query)
            truefalse_questions = truefalse_questions.filter(question__icontains=query)
            mcq_questions = mcq_questions.filter(question__icontains=query)


        serializer = TheoryQuestionSerializer(theory_questions, many=True)
        fillupserializer = FillUpSerializer(fillup_questions, many=True)
        truefalseserializer = TrueFalseSerializer(truefalse_questions, many=True)
        mcqserializer = MCQSerializer(mcq_questions, many=True)
        return Response(serializer.data + fillupserializer.data + truefalseserializer.data + mcqserializer.data)


class filter_question(APIView):
    def get(self, request):
        chapter_id = request.query_params.get('chapter_id')
        question_type = request.query_params.get('question_type')
        length = request.query_params.get('length')
        difficulty = request.query_params.get('difficulty')

        # Filter based on provided criteria
        if question_type == 'theory_questions':
            theory_question_queryset = TheoryQuestion.objects.all()
            if chapter_id:
                theory_question_queryset = theory_question_queryset.filter(Chapter_id=chapter_id)
            if length:
                theory_question_queryset = theory_question_queryset.filter(length=length)
            if difficulty:
                theory_question_queryset = theory_question_queryset.filter(difficulty=difficulty)
            
            questions = TheoryQuestionSerializer(theory_question_queryset, many=True) 

        if question_type == 'fillups':
            fillup_queryset = FillUp.objects.all()
            if chapter_id:
                fillup_queryset = fillup_queryset.filter(Chapter_id=chapter_id)
            questions = FillUpSerializer(fillup_queryset, many=True) 
        
        if question_type == 'mcqs':
            mcq_queryset = MCQ.objects.all()
            if chapter_id:
                mcq_queryset = mcq_queryset.filter(Chapter_id=chapter_id)
            questions = MCQSerializer(mcq_queryset, many=True) 

        if question_type == 'true_falses':
            truefalse_queryset = TrueFalse.objects.all()
            if chapter_id:
                truefalse_queryset = truefalse_queryset.filter(Chapter_id=chapter_id)
            questions = TrueFalseSerializer(truefalse_queryset, many=True) 

       
        return Response(questions.data)