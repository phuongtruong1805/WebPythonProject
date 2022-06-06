from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from .form import DangKy,QuenMatKhau
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import FilmData, GuessInfo, FilmInCinema, ShowTimes,BillTemp,ChairInRoom,Chair,TicketDetail,CinemaInfo
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
import re
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date,datetime

############ Trang chủ ############
def home(request):
    """Renders the home page."""
    # Lấy thông tin film đưa lên
    a = FilmData.objects.all()
    try:
        # Kiểm tra xem Billtemp đã khởi tạo chưa nếu rồi thì xóa
        b = GuessInfo.objects.get(UID=User.objects.get(username=request.user.username))
        BillTemp.objects.get(GuessInfo=b).delete()
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'HTML/Home/Home.html',
            {
                'listFilm': a
            }
        )
    except ObjectDoesNotExist: # Chưa thì đi đến trang chủ
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'HTML/Home/Home.html',
            {
                'listFilm':a
            }
        )
############ Khuyến mãi ###########
def LienHe(request):
    return render(request,'HTML/Home/LienHe.html')
############ Đăng nhập ###########
class LoginClass(View):
    def get(self, request):
        return render(request, 'HTML/Home/sign_in.html')

    def post(self, request):
        UserName = request.POST.get('username')
        Password = request.POST.get('password')
        my_user = authenticate(username=UserName, password=Password)#Kiểm tra xem tài khoản mật khẩu đúng hay không
        if my_user is None:
            messages.error(request, 'Tài khoản hoặc mật khẩu không đúng.') #Thông báo lỗi
            return render(request, 'HTML/Home/sign_in.html')
        login(request, my_user)#Đăng nhập được hộ trợ sãn

        return redirect('http://127.0.0.1:8000/')


########### Đăng ký ##############
class CreateAccount(View):
    def get(self,request):
        return render(request, 'HTML/Home/sign_up.html')
    def post(self,request):
        UserName=request.POST.get('UserName')
        Email=request.POST.get('email')
        PassWord=request.POST.get('PassWord')
        Name=request.POST.get('hoten')
        DoB=request.POST.get('namsinh')
        Phone=request.POST.get('sdt')
        Sex=request.POST['sex']
        Repass=request.POST.get('Repass')
        if not re.search(r'^\w+$', UserName):#Tài khoản không nên có ký tự đặc biệt vì một số trường hợp sẽ sinh ra lỗi
            messages.error(request, 'Tài khoản có tồn tại ký tự đặc biệt.')
            return render(request, 'HTML/Home/sign_up.html')
        try:
            User.objects.get(username=UserName)#kiểm tra xem tài khoản đã tồn tại chưa
            messages.error(request,'Tài khoản đã tồn tại.')#có thì xuất ra lỗi
        except ObjectDoesNotExist:# chưa thì tạo tài khoản mới
            UserNameTemp=UserName#Gán temp đề đề phòng có lỗi phát sinh
            if PassWord==Repass:# nếu mà nhập lại passwork đúng thì tạo
                User.objects.create_user(username=UserNameTemp, email=Email,
                                        password=PassWord)# đây là tạo thông tin để đưa vào User

                GuessInfo.objects.create(Name=Name, DateOfBirth=DoB,
                                        PhoneNumber=Phone, Mail=Email,
                                        UID=User.objects.get(username=UserName),Sex=Sex)# còn đây là tạo thông tin bên Guess
                return HttpResponseRedirect('/')# trở lại trang chủ
            else:
                messages.error(request,'nhập lại mật khẩu không chính xác.')
        return render(request,'HTML/Home/sign_up.html')


######### Đăng xuất #############
def logout_view(request):
    logout(request)         # Hàm logout được hỗ trợ sãn
    return redirect("Home") # Đi đến trang có name url là Home là trang chủ


########## Quên tài khoản ##########
def fogot(request):
    b = QuenMatKhau()
    return render(request, 'app/FormForgotPassword.html', {'f': b})


######### Lấy thông tin phim #########
def FilmInfor(request,filmdata_id):
    q=FilmData.objects.get(pk=filmdata_id)
    return render(request,'HTML/Film/Film.html',{'fi':q})


######## Hiện thị thông tin tài khoản #######
def CustomerInfo(request):
    q=GuessInfo.objects.get(UID=User.objects.get(username=request.user.username))
    return (render(request,'HTML/CustomerInfor/AccountInfor.html',{'q':q}))

def History(request):
    q = GuessInfo.objects.get(UID=User.objects.get(username=request.user.username))
    hs=TicketDetail.objects.all().filter(GuessInfo=GuessInfo.objects.get(UID=User.objects.get(username=request.user.username)))
    return render(request, 'HTML/CustomerInfor/History.html', {'q': q,'hs':hs})

######### Đổi mật khẩu ################
class ChangePass(View):
    def get(self,request):
        q = GuessInfo.objects.get(UID=User.objects.get(username=request.user.username))
        return render(request,'HTML/CustomerInfor/ChangePass.html',{'q':q})
    def post(self,request):
        a=User.objects.get(username=request.user.username)
        password = request.POST.get('Pass1')
        password1 = request.POST.get('Pass2')
        oldpass = request.POST.get('OldPass')
        if password == password1 and a.check_password(
                str(oldpass)):
            a.set_password(str(password))
            a.save()
            return HttpResponseRedirect('/')


######  Đổi thông tin tài khoản ###########
class ChangeGuessInfo(View):
    def get(self,request):
        q = GuessInfo.objects.get(UID=User.objects.get(username=request.user.username))
        return render(request,'HTML/CustomerInfor/ChangeInfor.html',{'q':q})
    def post(self,request):
        a=request.user.username
        u = User.objects.get(username=a);
        g = GuessInfo.objects.get(UID=User.objects.get(username=a))
        name = request.POST.get('Name')
        birth = request.POST.get('DayOfBirth')
        phone = request.POST.get('PhoneNumber')
        mail = request.POST.get('Email')
        Sex=request.POST['Sex']
        Photo=request.POST.get('Photo')
        if Photo !=None and Photo!='':
            g.Name = name
            g.DateOfBirth = birth
            g.PhoneNumber = phone
            g.Mail=mail
            g.Sex=Sex
            g.Photo=Photo
            g.save()
        else:
            g.Name = name
            g.DateOfBirth = birth
            g.PhoneNumber = phone
            g.Mail = mail
            g.Sex = Sex
            #g.Photo = Photo
            g.save()
        q = GuessInfo.objects.get(UID=User.objects.get(username=request.user.username))
        return (render(request, 'HTML/CustomerInfor/AccountInfor.html', {'q': q}))


####### Chức năng lọc vé ###################
class filtertickets(LoginRequiredMixin, View):
    login_url='/login/'

    def get(self,request,filmdata_id):
        try:
            # Kiểm tra xem có hay không
            BillTemp.objects.get(GuessInfo=GuessInfo.objects.get(UID=User.objects.get(username=request.user.username)))
            #nếu có thì xóa đi
            BillTemp.objects.get(GuessInfo=GuessInfo.objects.get(UID=User.objects.get(username=request.user.username))).delete()
            # tạo lại
            BillTemp.objects.create(GuessInfo=GuessInfo.objects.get(UID=User.objects.get(username=request.user.username)))
        except ObjectDoesNotExist:
            # khi mở ra tạo 1 record mới  trong bill temp (không hiểu thì nói sau)
            # còn nếu không có thì tạo mới
            BillTemp.objects.create(GuessInfo=GuessInfo.objects.get(UID=User.objects.get(username=request.user.username)))
        b = FilmInCinema.objects.all().filter(FilmData=filmdata_id)  # Lấy phim chiếu ở đâu
        # lọc ra những xuất chiếu đó chiếu ngày nào (mặc định sẽ là today)
        today = date.today()
        a = ShowTimes.objects.all().filter(Film_id=filmdata_id, DateOfShow=today,Room__CinemaInfo=1)  # lấy xuất chiếu
        c = FilmData.objects.get(id=filmdata_id)
        Ghe = ChairInRoom.objects.all().filter(Daytemp=date.today(), Room=1)
        content = {'a': a, 'b': b, 'c': c,'chair':Ghe}# có 1 lỗi nhỏ là khi chạy lần đầu nó không lấy được giá trị lên thẻ input
        return render(request, 'HTML/Film/Booking.html', content)

    Show = 1
    Ngay = date.today()
    Rap = 1
    def post(self,request,filmdata_id):
        global Show, Ngay, Rap
        b = FilmInCinema.objects.all().filter(FilmData=filmdata_id)  # Lấy phim chiếu ở đâu
        # lọc ra những xuất chiếu đó chiếu ngày nào (mặc định sẽ là today)
        #ngay=date.today()
        day = request.POST.get('Date')
        cinema = request.POST.get('Cinema')
        if(day != None and day!=''):
            Ngay=day
        if(cinema != None and cinema != ''):
            Rap = cinema

        if day==None or day=='':
            if cinema == None:
                a = ShowTimes.objects.all().filter(Film_id=filmdata_id, DateOfShow=Ngay,Room__CinemaInfo=Rap)  # lấy xuất chiếu
            else :
                a = ShowTimes.objects.all().filter(Film_id=filmdata_id, DateOfShow=Ngay,Room__CinemaInfo=Rap)
        else :
            if cinema == None:
                a = ShowTimes.objects.all().filter(Film_id=filmdata_id, DateOfShow=Ngay,Room__CinemaInfo=Rap)  # lấy xuất chiếu
            else:
                a = ShowTimes.objects.all().filter(Film_id=filmdata_id, DateOfShow=Ngay,Room__CinemaInfo=Rap)  # lấy xuất chiếu


        showtime=request.POST.get('Showtime')
        if (showtime != None and showtime != ''):
            Show=showtime
        if showtime == None or showtime == '':
            temp=ShowTimes.objects.get(id=1)
            Ghe = ChairInRoom.objects.all().filter(Daytemp=date.today(), Room=temp.Room,showtime=1)
        else:
            temp = ShowTimes.objects.get(id=Show)
            if not (ChairInRoom.objects.all().filter(Daytemp=temp.DateOfShow, Room=temp.Room,showtime=showtime)):
                for item in (Chair.objects.all()):
                    ChairInRoom.objects.create(Daytemp=temp.DateOfShow,Room=temp.Room,showtime=showtime,Chair=item)
            Ghe = ChairInRoom.objects.all().filter(Daytemp=temp.DateOfShow, Room=temp.Room,showtime=showtime)
        c = FilmData.objects.get(id=filmdata_id)
        sb = request.POST.get('submit1')
        ghechon=request.POST.get('test')
        if ghechon!=''and ghechon!=None:
            ghetemp = ghechon.split(" ")
            for item in ghetemp:
                if item!='':
                    TicketDetail.objects.create(ShowTimes=ShowTimes.objects.get(id=Show),CinemaInfo=CinemaInfo.objects.get(id=Rap),Chair=item,GuessInfo=GuessInfo.objects.get(UID=User.objects.get(username=request.user.username)))
                    temp = ShowTimes.objects.get(id=Show)
                    stat=ChairInRoom.objects.get(Daytemp=temp.DateOfShow, Room=temp.Room,showtime=Show,Chair=Chair.objects.get(Name=item))
                    stat.Status=1
                    stat.save()
            return HttpResponseRedirect('/')  # trở lại trang chủ

        content = {'a': a, 'b': b, 'c': c,'day':Ngay,'chair':Ghe}
        return render(request, 'HTML/Film/Booking.html', content)




