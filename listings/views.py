from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import Listing, Favorite, ChatRoom, ChatMessage, Report
from .forms import ListingForm, ReportForm, ChatMessageForm
from django.contrib.auth.models import User
from django.db.models import Q

def listing_list(request):
    listings = Listing.objects.all().order_by('-created_at') #생성기준 내림차순 정렬
    
    category = request.GET.get('category')
    status = request.GET.get('status')
    query = request.GET.get('query') #제목 검색

    if category:
        listings = listings.filter(category=category)
    if status:
        listings = listings.filter(status=status)
    if query:
        listings = listings.filter(title__icontains=query)
    return render(request, 'listings/listing_list.html', {
        'listings': listings,
        'selected_category': category,
        'selected_status': status,
        'search_query': query,
    })

@login_required
def listing_create(request):  # 물품 등록
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return redirect('listings:listing_detail', pk=listing.pk)
    else:
        form = ListingForm()  

    return render(request, 'listings/listing_form.html', {'form': form})

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    is_favorited = False #찜 여부 확인
    has_reported = False #신고 여부 확인
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, listing=listing).exists()
        has_reported = Report.objects.filter(reporter=request.user, reported_listing=listing).exists()
    return render(request, 'listings/listing_detail.html', {
        'listing': listing,
        'is_favorited': is_favorited,
        'has_reported': has_reported, # context로 넘겨줌
    })

@login_required #물품 수정
def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listings:listing_detail', pk=pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/listing_form.html', {'form': form})

@login_required
def listing_delete(request, pk): #물품 삭제
    listing = get_object_or_404(Listing, pk=pk, seller=request.user) #본인의 글만 표시
    if request.method == 'POST':
        listing.delete()
        return redirect('listings:listing_list')
    return render(request, 'listings/listing_confirm_delete.html', {'listing': listing})

@login_required #찜하기 토글
def toggle_favorite(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        favorite.delete()
    return redirect('listings:listing_detail', pk=pk)

@login_required
def favorite_list(request): #찜 목록
    favorites = Favorite.objects.filter(user=request.user).select_related('listing')
    return render(request, 'listings/favorite_list.html', {'favorites': favorites})

@login_required
def my_store(request, pk):#내 상점
    seller_user = get_object_or_404(User, pk=pk)
    listings = Listing.objects.filter(seller=seller_user)
    return render(request, 'listings/my_store.html',{
                      'seller_user':seller_user,
                      'listings': listings
                  })

@login_required
def report_user(request, user_pk): #유저신고 
    reported_user = get_object_or_404(User, pk=user_pk)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reported_user = request.user
            report.save()
            messages.success(request, "유저신고가 접수되었습니다.")
            return redirect('listings:listing_list')
    else:
        form = ReportForm()
    return render(request, 'listings/report_form.html', {'form': form})

@login_required
def report_listing(request, listing_pk): #물품신고
    listing = get_object_or_404(Listing, pk=listing_pk)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reported_listing = listing
            report.save()
            messages.success(request, "신고가 접수되었습니다.")
            return redirect('listings:listing_list')
    else:
        form = ReportForm()
    return render(request, 'listings/report_form.html', {'form': form})

@login_required
def chat_list(request):#채팅목록
    rooms = ChatRoom.objects.filter(
        Q(seller=request.user) | Q(buyer=request.user)
    ).select_related('listing', 'buyer', 'seller')
    return render(request, 'listings/chat_list.html', {'rooms': rooms})

@login_required
def chat_room(request, room_id):#채팅창
    room = get_object_or_404(ChatRoom, pk=room_id)
    show_numbers = room.is_closed #거래완료시 학번공개
    #참여자만 접근
    if request.user not in [room.buyer, room.seller]:
        return redirect('listings:chat_list')

    messages_list = ChatMessage.objects.filter(room=room).order_by('created_at')

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.room = room
            message.save()

            # 판매 상태 변경
            status = request.POST.get('status')
            if status and request.user == room.seller:
                room.listing.status = status
                room.listing.save()
                if status =='D':
                    room.is_closed = True
                    room.save()
                    
            return redirect('listings:chat_room', room_id=room_id)
    else:
        form = ChatMessageForm()

    return render(request, 'listings/chat_room.html', {
        'room': room,
        'listing': room.listing,
        'messages_list': messages_list,
        'form': form,
        'STATUS_CHOICES': Listing.STATUS_CHOICES,
        'show_numbers': show_numbers,
        'seller': room.seller,
        'buyer': room.buyer,
    })

@login_required
def start_chat(request, listing_pk):#채팅 시작하기
    listing = get_object_or_404(Listing, pk=listing_pk)
    if listing.seller == request.user:
        return redirect('listings:listing_detail', pk=listing_pk)
    
    room, created = ChatRoom.objects.get_or_create(
        listing=listing, buyer=request.user,
        defaults={'seller': listing.seller}
    )
    return redirect('listings:chat_room', room_id=room.pk)

@login_required
def my_page(request):
    return redirect('listing_list')

