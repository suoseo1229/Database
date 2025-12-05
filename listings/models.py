
from django.db import models
from django.contrib.auth.models import User

#물품 상태 선택

#카테고리 선택
CATEGORY_CHOICES = [
    ('의류', '의류'),
    ('디지털/가전', '디지털/가전'),
    ('가구/인테리어', '가구/인테리어'),
    ('도서', '도서'),
    ('기타', '기타'),
]

class Listing(models.Model):
    STATUS_CHOICES = [
    ('S', '판매중'),
    ('R', '예약중'),
    ('D', '거래완료'),
    ]
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='기타')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='S')
    location = models.CharField(max_length=100, blank=True)
    image1 = models.ImageField(upload_to='listings/', blank=True, null=True)
    image2 = models.ImageField(upload_to='listings/', blank=True, null=True)
    image3 = models.ImageField(upload_to='listings/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')


class ChatRoom(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms_as_buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms_as_seller')
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False) #거래 완료 여부

    class Meta:
        unique_together = ('listing', 'buyer')


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

#신고 대상 종류
REPORT_TYPE_CHOICES = [
    ('사용자', '사용자'),
    ('물품', '물품'),
]


class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # 신고 대상
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='reports_received')
    reported_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name='reports_received')

    def __str__(self):
        return f'{self.report_type} 신고 by {self.reporter.username}'