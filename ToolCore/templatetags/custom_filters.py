from django import template

register = template.Library()

@register.filter
def get_marks_by_id(marks, question_id):
    mark = next((item['marks'] for item in marks if item['id'] == question_id), None)
    return mark
