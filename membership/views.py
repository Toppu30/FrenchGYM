from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from .models import *
from .forms import *
from django.http import JsonResponse


# Create your views here.
def index(req):
    return render(req, 'index.html')

def check(req):
    obj = Users.objects.all()
    member_check = Member_checkin.objects.all()
    return render(req, 'check_in.html', {'Users':obj, 'Member_check': member_check})

def check_member(req):
    obj = Register.objects.all()
    return render(req, 'check_member.html', { 'Register': obj })

def check_in(req, reg_id):
    member = Register.objects.get(reg_id=reg_id)
    # สร้างวัตถุใหม่จากโมเดลใหม่และบันทึกข้อมูล
    new_entry = Member_checkin(name=member.name, tel=member.tel, des=member.des, reg_current_time=datetime.now().time().strftime('%H:%M:%S'), date=timezone.now().date())
    new_entry.save()

    return redirect(check)  # ไปยังหน้าที่ต้องการหลังจากบันทึกข้อมูลเสร็จสิ้น

def home(req):
    obj = Register.objects.all()
    return render(req, 'home.html', { 'Register': obj })

def create_member(req, form):
    if req.method == 'POST':
        # สร้าง member ใหม่
        form = Member(req.POST)
        if form.is_valid():
            form.save()

def your_view(request):
    today_date = datetime.date.today()
    filtered_data = Register.objects.filter(date_field=today_date)
    return render(request, 'your_template.html', {'filtered_data': filtered_data, 'today_date': today_date})

def user(req):
    form = UserForm()
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('check_in.html')
        
        name = req.POST.get('name')
        des = req.POST.get('des')
        dropdown_value = req.POST.get('dropdown')

        current_time = datetime.now().time().strftime('%H:%M:%S')
        today = timezone.now().date()

        Users.objects.create(
                name=name, 
                des=des,
                pay=dropdown_value,
                current_time=current_time,
                date=today
            )
        return redirect(check)

    return render(req, 'user_form.html', {"form":form})



def calculate_date(req):
    form = Member()
    create_member(req, form)
    if req.method == 'POST':
         # สร้าง member ใหม่
        form = Member(req.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
        start_date_str = req.POST.get('start_date')
        dropdown_value = req.POST.get('dropdown')
        reg_id = req.POST.get('reg_id')  
        name = req.POST.get('name')  
        tel = req.POST.get('tel')  
        des = req.POST.get('des')
        
        if start_date_str:
            # แปลงข้อมูลวันที่จากสตริงเป็นวัตถุ datetime
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

            # คำนวณเวลาที่กรอกแบบฟอร์ม
            current_time = datetime.now().time().strftime('%H:%M:%S')

            amount = int(req.POST.get('amount'))

            # คำนวณวันที่หมดอายุ 
            end_date = start_date + timedelta(days=30 * amount)

            today = timezone.now().date()

            remaining = (end_date - today).days if today <= end_date else 0
            
            dropdown_value = req.POST.get('dropdown')

            # บันทึกข้อมูลลงในฐานข้อมูล
            Register.objects.create(
                start_date=start_date,
                current_time=current_time,
                pay=dropdown_value,
                end_date=end_date,
                remain_day=remaining,
                reg_id=reg_id, 
                name=name, 
                tel=tel,
                des=des  
            )

            # ส่งข้อมูลไปยังเท็มเพลต HTML เพื่อแสดงผล
            #return render(req, 'home.html', {'form':form, 'start_date': start_date, 'end_date': end_date, 'remaining' : remaining, 'dropdown_value': dropdown_value, 'cur_time': current_time })
            return redirect(home)
    return render(req, 'form.html')

def search(request):
    query = request.GET.get('q')  # รับค่าคำค้นหาจากแบบฟอร์ม

    if query:  # ตรวจสอบว่ามีคำค้นหาหรือไม่
        # ค้นหาข้อมูลจากชื่อ (i.name) ที่มีคำค้นหาใน query
        results = Register.objects.filter(name__icontains=query)
    else:
        results = None

    return render(request, 'search_results.html', {'results': results, 'query': query})

def search_results(request):
    query = request.GET.get('q')
    results = Register.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})

def search_results_member(request):
    query = request.GET.get('q')
    results = Register.objects.filter(name__icontains=query)
    return render(request, 'search_results_member.html', {'results': results, 'query': query})


def edit(request, id):
    # ดึงข้อมูลที่ต้องการแก้ไขจากฐานข้อมูล
    obj = Register.objects.get(pk=id)

    if request.method == 'POST':
        # สร้างฟอร์มโดยใช้ข้อมูลที่ถูกแก้ไข
        form = Member(request.POST, instance=obj)
        if form.is_valid():
            # บันทึกข้อมูลที่ถูกแก้ไขลงในฐานข้อมูล
            form.save()
            # หลังจากบันทึก นำผู้ใช้กลับไปยังหน้าที่แสดงรายการข้อมูล
            return redirect('home')  # แก้ไขตาม url pattern ของคุณ
        
        name = request.POST.get('name')  
        tel = request.POST.get('tel')  
        des = request.POST.get('des')
        
        start_date_str = request.POST.get('start_date')
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            current_time = datetime.now().time().strftime('%H:%M:%S')
            amount = int(request.POST.get('amount'))
            end_date = start_date + timedelta(days=30 * amount)
            today = timezone.now().date()
            remaining = (end_date - today).days if today <= end_date else 0
            
            # อัปเดตข้อมูลในฐานข้อมูล
            Register.objects.filter(pk=id).update(
                start_date=start_date,
                current_time=current_time,
                pay=request.POST.get('dropdown'),
                end_date=end_date,
                remain_day=remaining,
                name=name, 
                tel=tel,
                des=des
            )
            return redirect(home)

    else:
        # สร้างฟอร์มโดยใช้ข้อมูลปัจจุบัน
        form = Member(instance=obj)

    context = {
        'b' : form.instance,
        'form': form,
    }
    return render(request, 'edit.html', {'b': Register,'form': form})



def delete(req, id):
    obj = Register.objects.get(pk=id)
    obj.delete()
    return redirect(home)

def delete_user(req, id):
    obj = Users.objects.get(pk=id)
    obj.delete()
    return redirect(check)

def delete_member_check(req, id):
    obj = Member_checkin.objects.get(pk=id)
    obj.delete()
    return redirect(check)

def remain(req, id):
    obj = Register.objects.get(pk=id)

    if req.method == 'POST':
        # สร้างฟอร์มโดยใช้ข้อมูลที่ถูกแก้ไข
        form = Member(req.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(home)

        day = int(req.POST.get('day'))
        remain = day + obj.remain_day
        end_date = timedelta(days=day) + obj.end_date

        Register.objects.filter(pk=id).update(
            remain_day=remain,
            end_date=end_date
        )

        return redirect(home)
    else:
        # สร้างฟอร์มโดยใช้ข้อมูลปัจจุบัน
        form = Member(instance=obj)

    context = {
        'b' : form.instance,
        'form': form,
    }
    return render(req, 'remain.html', {'b': Register, 'form':form})

""" 
def check_attendance(req):
    if req.method == 'POST':
        # รับข้อมูลจากฟอร์ม
        member_id = req.POST['member_id']
        # ตรวจสอบว่าสมาชิกมีอยู่ในระบบหรือไม่
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            # ถ้าไม่พบสมาชิกในระบบ
            return render(req, 'attendance_error.html', {'message': 'Member not found'})

        # สร้างข้อมูลการเข้าร่วม
        Attendance.objects.create(member=member)

        # ส่งกลับไปยังหน้าเช็คชื่อ
        return redirect('attendance_success')
    return render(req, 'attendance_form.html') """