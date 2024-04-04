from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from task1.models import *
from task1.serializers import *
from django.views.generic import TemplateView
from django.db import IntegrityError
from marks.models import *
from marks.serializers import *
# Create your views here.
class StudentDashboardView(TemplateView):
    template_name = 'task1/student_dashboard.html' 


# STUDENT DETAILS RELATED API/FUNCTIONS STARTS
class StudentDetailsView(TemplateView):
    template_name = 'task1/Student_details.html' 
class StudentAPI(APIView):
    def post(self,request):
        serializer = StudentSerializers(data = request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({'status':201,'msg':'Data Created Successfully!!!'},status=201)
            else:
                print(str(serializer.errors))
                return Response({'status':500,'error':str(serializer.errors)},status=500)
        except IntegrityError:
            return Response({'status':500,'error':'Roll number must be unique'},status=500)
    def put(self,request):
        id = request.data.get('id')
        try:
            student = Student.objects.get(id=id)
            serializer = StudentSerializers(student,data = request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':200,'msg':'Data Updated!!'},status=200)
            else:
                print(str(serializer.errors))
                return Response({'status':500,'error':str(serializer.errors)},status=500)
        except Student.DoesNotExist as e:
            return Response({'status':404,'error':f"{e}"},status=404)
    def get(self,request,student_id=None):
        id = student_id
        if id:
            try:
                student = Student.objects.get(id=id)
                serializer = GetAllStudentSerializers(student)
                return Response({'status':200,'data':serializer.data},status=200)
            except Student.DoesNotExist as e:
                return Response({'status':400,'error':str(e)},status=400)
        else:
            #get all data
            student = Student.objects.all()
            serializer = GetAllStudentSerializers(student,many=True)
            return Response({'status':200,'data':serializer.data},status=200)
    def delete(self,request):
        id = request.data.get('id')
        try:
            student = Student.objects.get(id=id)
            student.delete()
            return Response({'status':200,'msg':'Data Deleted'},status=200)
        except Student.DoesNotExist as e:
            return Response({'status':500,'error':e},status=500)
  # STUDENT DETAILS RELATED API/FUNCTIONS ENDS       
  
# STUDENT CATEGORY RELATED FUNCTIONS STARTS
class StudentCategoryPage(TemplateView):
    template_name = 'task1/student_category.html'
class StudentCategoryAPI(APIView):
    def post(self,request):
        serializer = StudentCategorySerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':201,'msg':'Student Category Created'},status=201)
        else:
            print(str(serializer.errors))
            return Response({'status':500,'error':str(serializer.errors)},status=500)
    def get(self,request,category_id=None):
        id = category_id
        if id:
            try:
                student_category = StudentCategory.objects.get(id=id)
                serializer = StudentCategorySerializers(student_category)
                return Response({'status':200,'data':serializer.data},status=200)
            except StudentCategory.DoesNotExist as e:
                print(str(e))
                return Response({'status':400,'error':str(e)},status=400)
        else:
            student_category = StudentCategory.objects.all()
            serializer = StudentCategorySerializers(student_category,many=True)
            return Response({'status':200,'data':serializer.data},status=200)
    def put(self,request):
        id = request.data.get('category_id')
        if id:
            try:
                student_category = StudentCategory.objects.get(id=id)
                serializer = StudentCategorySerializers(student_category,data=request.data,partial=False)
                if serializer.is_valid():
                    print(serializer)
                    serializer.save()
                    return Response({'status':200,'msg':'Student category updated'},status=200)
                else:
                    print(str(serializer.errors))
                    return Response({'status':500,'error':str(serializer.errors)},status=500)
            except StudentCategory.DoesNotExist as e:
                return Response({'status':500,'error':str(e)},status=500)
        else:
            return Response({'status':500,'error':'Category id missing'},status=500)
    def delete(self,request):
        id=request.data.get('id')
        if id:
            student_category = StudentCategory.objects.get(id=id)
            try:
                student_category.delete()
                return Response({'status':200,'msg':'Data Deleted'},status=200)
            except StudentCategory.DoesNotExist as e:
                return Response({'status':400,'error':str(e)},status=400)
        else:
            return Response({'status':500,'error':'Record ID to Delete is not Found'},status=500)
# STUDENT CATEGORY RELATED FUNCTIONS ENDS  

# GET MARKS OF THE SELECTED STUDENT STARTS
class MarksCRUD_student_API(APIView):
    def get(self, request,student_id=None):
        # id = request.data.get('marks_id')
        id=student_id
        if id:
            #get one record of marks from DB
            try:
                marks = Marks.objects.get(student=id)
                serializer = MarksSerializers(marks)
                return Response({'status':200,'data':serializer.data},status=200)
            except Marks.DoesNotExist as e:
                return Response({'status':500,'error':str(e)},status=500)
        else:
            marks = Marks.objects.all()
            serializer = Get_All_MarksSerializers(marks, many=True)  # Query for instances of Marks
            if marks:  # You might want to check if there are any instances retrieved
                return Response({'status': 200, 'data': str(serializer.data)}, status=200)
            else:
                return Response({'status': 500, 'error': 'Marks Not Found'}, status=500)
# GET MARKS OF THE SELECTED STUDENT ENDS