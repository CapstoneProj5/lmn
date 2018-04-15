from django.db import models
from django.contrib.auth.models import User
import datetime

# Every model gets a primary key field by default.
# Users, venues, shows, artists, notes

# User is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.
User._meta.get_field('email')._unique = True

# Require email, first name and last name
User._meta.get_field('email')._blank = False
User._meta.get_field('last_name')._blank = False
User._meta.get_field('first_name')._blank = False

''' A User profile '''
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# ***Both Julie and I worked on this code.
    about_me = models.TextField(max_length=1000, blank=True)
    user_photo_file_name = models.CharField(null=True, max_length=255)
    user_photo_type = models.CharField(null=True, max_length=255)
    user_photo = models.BinaryField(null=True, blank=True)
# ***

    def __str__(self):
        return "About me: " + self.about_me


''' A music artist '''
class Artist(models.Model):
    pkey = models.IntegerField(blank=False)
    sk_id = models.IntegerField(blank=False)
    name = models.CharField(max_length=200, blank=False)
    picture = models.ImageField(upload_to='pictures/', blank=True)

    def __str__(self):
        return "Artist: " + self.name


''' A venue, that hosts shows. '''
class Venue(models.Model):
    pkey = models.IntegerField(blank=False)
    sk_id = models.IntegerField(blank=False)
    name = models.CharField(max_length=200, blank=False, unique=True)
    city = models.CharField(max_length=200, blank=False)
    state = models.CharField(max_length=2, blank=False)  # What about international?
    picture = models.ImageField(upload_to='pictures/', blank=True)

    def __str__(self):
        return 'Venue name: {} in {}, {}'.format(self.name, self.city, self.state)


''' A show - one artist playing at one venue at a particular date. '''
class Show(models.Model):
    pkey = models.IntegerField(blank=True)
    sk_id = models.IntegerField(blank=False)
    show_date = models.DateTimeField(blank=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='pictures/', blank=True)

    def __str__(self):
        return 'Show with artist {} at {} on {}'.format(self.artist, self.venue, self.show_date)


''' One user's opinion of one show. '''
class Note(models.Model):
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    picture = models.ImageField(upload_to='pictures/', null=True, blank=True)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(blank=False)

    def publish(self):
        posted_date = datetime.datetime.today()
        self.save()

    def __str__(self):
        return 'Note for user ID {} for show ID {} with title {} text {} posted on {}'\
            .format(self.user, self.show, self.title, self.text, self.posted_date)
