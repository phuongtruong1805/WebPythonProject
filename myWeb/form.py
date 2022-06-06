import datetime
from django import forms
from django.views import View
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import GuessInfo
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect


class DangKy(forms.Form):
    Name = forms.CharField(max_length=100, label="Họ và tên")
    Sex = forms.BooleanField(required=False, label="Nữ")
    DayOfBirth = forms.DateField(label="Ngày sinh")
    PhoneNumber = forms.CharField(max_length=10, label="Số điện thoại")
    Email = forms.EmailField(label="Email")
    UserName = forms.CharField(max_length=50, label="Tài khoản")
    PassWord = forms.CharField(max_length=50, widget=forms.PasswordInput(), label="Mật khẩu")
    RePassWord = forms.CharField(max_length=50, widget=forms.PasswordInput(), label="Nhập lại mật khẩu")
    # Còn lỗi
    """
    # Kiểm tra xem 2 mật khẩu có giống nhau ko
    def clean_RePassWord(self) :
        if 'PassWord' in self.cleaned_data:
            passWord = self.cleaned_data['PassWord']
            rePassWord = self.cleaned_data['RePassWord']
            if passWord == rePassWord and passWord:
                return rePassWord
        raise forms.ValidationError("Mật khẩu không hợp lệ")
    # Kiểm tra xem tên tài khoản đã tạo chưa hay có chứa ký tự đặc biệt ko
    def clean_UserName(self):
        username = self.cleaned_data['UserName']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tài khoản có ký tự đặc biệt")
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")
"""

    def save(self):
        User.objects.create_user(username=self.cleaned_data['UserName'], email=self.cleaned_data['Email'],
                                 password=self.cleaned_data['PassWord'])

        GuessInfo.objects.create(Name=self.cleaned_data['Name'], DateOfBirth=self.cleaned_data['DayOfBirth'],
                                 PhoneNumber=self.cleaned_data['PhoneNumber'], Mail=self.cleaned_data['Email'],
                                 UID=User.objects.get(username=self.cleaned_data['UserName']))
    # Save đã chạy


class QuenMatKhau(forms.Form):
    Email = forms.EmailField()
    PassWord = forms.CharField(max_length=50)
    RePassWord = forms.CharField(max_length=50)
