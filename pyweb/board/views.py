from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from board.forms import QuestionForm, AnswerForm
from board.models import Question

def index(request):

    return render(request, 'board/index.html')

def question_list(request):
    question_list = Question.objects.all()
    context = {'question_list':question_list}
    return render(request, 'board/question_list.html', context)

def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'board/detail.html', context)

#질문등록
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST) #getparameter 입력된 데이터가 있는 폼
        if form.is_valid(): #폼이 유효하다면 (유효성검사)를통과했다면
            question = form.save(commit=False) #가짜 저장
            question.create_date = timezone.now() #등록일생성
            form.save() #실제저장
            return redirect('board:question_list') #질문목록 페이지 이동

    else: #get방식
        form = QuestionForm() #v폼 객체 생성(빈 폼 생성)
        context = {'form': form}
        return render(request, 'board/question_form.html',context) #get 방식
    
#답변등록
def answer_create(request, question_id):
    # 질문이 1개 있어야 답변을 등록할 수 있음
    question = Question.objects.get(id=question_id)
    if request.method == 'Post':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False) #content만 저장
            answer.create_date = timezone.now() #답변 등록일
            answer.question = question
            form.save()
            return redirect('board:detail',question_id=question.id)
                                            #모델주소 = 객체 (객체값을 모델주소로)
    else:
        form = AnswerForm()   #빈 폼 생성
    context = {'question': question, 'form':form}
    return render(request,'board/detail.html',context)


