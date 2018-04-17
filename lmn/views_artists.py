from django.shortcuts import render, redirect, get_object_or_404
from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def venues_for_artist(request, artist_pk):

    '''
    Get all of the venues where this artist has played a show
    :param request:
    :param artist_pk:
    :return:
    '''

    shows = Show.objects.filter(artist=artist_pk).order_by('show_date').reverse()
    artist = Artist.objects.get(pk=artist_pk)

    paginator = Paginator(shows, 25)
    page = request.GET.get('page')

    try:
        showset = paginator.page(page)

    except PageNotAnInteger:
        showset = paginator.page(1)

    except EmptyPage:
        showset = paginator.page(paginator.num_pages)

    render_page = 'lmn/venues/venue_list_for_artist.html'
    data_dict = {'artist': artist, 'shows': shows, 'showset': showset}

    return render(request, render_page, data_dict)


def artist_list(request):

    form = ArtistSearchForm()
    search_name = request.GET.get('search_name')

    if search_name:
        artists = Artist.objects.filter(name__icontains=search_name).order_by('name')

    else:
        artists = Artist.objects.all().order_by('name')

    paginator = Paginator(artists, 25)
    page = request.GET.get('page')

    try:
        artistset = paginator.page(page)

    except PageNotAnInteger:
        artistset = paginator.page(1)

    except EmptyPage:
        artistset = paginator.page(paginator.num_pages)

    render_page = 'lmn/artists/artist_list.html'
    data_dict = {'artists': artists, 'form': form, 'search_term': search_name, 'artistset': artistset}

    return render(request, render_page, data_dict)


def artist_detail(request, artist_pk):

    artist = get_object_or_404(Artist, pk=artist_pk)
    render_page = 'lmn/artists/artist_detail.html'
    data_dict = {'artist': artist}

    return render(request, render_page, data_dict)
