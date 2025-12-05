from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, update_session_auth_hash
from .forms import UserRegistrationForm, ProfileUpdateForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
<<<<<<< HEAD
from django.db import transaction, IntegrityError
=======
>>>>>>> 795a641462518ad92f8ebdab0c6de2d8c070364a

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('accounts:login')  
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect("listings:listing_list")

def my_page(request):
    user = request.user
<<<<<<< HEAD
=======
    
>>>>>>> 795a641462518ad92f8ebdab0c6de2d8c070364a
    # 유저에게 프로필이 없다면 자동 생성
    if not hasattr(user, 'profile'):
        from .models import Profile
        Profile.objects.create(user=user)
<<<<<<< HEAD
    profile = user.profile
    # GET 요청 기본 폼 생성
    profile_form = ProfileUpdateForm(instance=profile)
    password_form = PasswordChangeForm(user=user)
=======

    profile = user.profile

    # GET 요청 기본 폼 생성
    profile_form = ProfileUpdateForm(instance=profile)
    password_form = PasswordChangeForm(user=user)

>>>>>>> 795a641462518ad92f8ebdab0c6de2d8c070364a
    # POST 요청이면 폼 데이터 업데이트
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        password_form = PasswordChangeForm(user=user, data=request.POST)
<<<<<<< HEAD
        # 프로필 정보 유효
        if profile_form.is_valid():
            profile_form.save()
=======

        # 프로필 정보 유효
        if profile_form.is_valid():
            profile_form.save()

>>>>>>> 795a641462518ad92f8ebdab0c6de2d8c070364a
        # 비밀번호 변경 로직 (항상 password_form.is_valid()로 체크)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
        else:
            # 입력은 했는데 비밀번호 검증 실패
            if request.POST.get('old_password'):
                messages.error(request, '비밀번호 변경 실패. 다시 확인해주세요.')
<<<<<<< HEAD
=======

>>>>>>> 795a641462518ad92f8ebdab0c6de2d8c070364a
    return render(request, 'accounts/my_page.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })