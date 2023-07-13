from rest_framework import serializers
from api.models import Class,Subject,Chapter,TheoryQuestion,FillUp,TrueFalse,MCQ,Book


class TheoryQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=TheoryQuestion
        fields='__all__'

class FillUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=FillUp
        fields='__all__'

class MCQSerializer(serializers.ModelSerializer):
    class Meta:
        model=MCQ
        fields='__all__'
        
class TrueFalseSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrueFalse
        fields='__all__'


class ChapterSerializer(serializers.ModelSerializer):
    TheoryQuestions = TheoryQuestionSerializer(many=True,read_only=True)
    FillUps = FillUpSerializer(many=True,read_only=True)
    MCQs = MCQSerializer(many=True,read_only=True)
    TrueFalses = TrueFalseSerializer(many=True,read_only=True)
    class Meta:
        model=Chapter
        fields='__all__'


class BookSerializer(serializers.ModelSerializer):
    Chapters = ChapterSerializer(many=True,read_only=True)
    class Meta:
        model=Book
        fields='__all__'

class SubjectSerializer(serializers.ModelSerializer):
    Chapters = ChapterSerializer(many=True,read_only=True)
    Book = BookSerializer(many=True,read_only=True)
    TheoryQuestions = TheoryQuestionSerializer(many=True,read_only=True)
    FillUps = FillUpSerializer(many=True,read_only=True)
    MCQs = MCQSerializer(many=True,read_only=True)
    TrueFalses = TrueFalseSerializer(many=True,read_only=True)
    class Meta:
        model=Subject
        fields='__all__'

class ClassSerializer(serializers.ModelSerializer):
    Subjects = SubjectSerializer(many=True, read_only=True)
    class Meta:
        model=Class
        fields='__all__'

