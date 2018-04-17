from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from .forms import VenueSearchForm
from .models import Venue, Show


def venue_list(request):

    form = VenueSearchForm()
    search_name = request.GET.get('search_name')

    if search_name:
        venues = Venue.objects.filter(name__icontains=search_name).order_by('name')  # search for this venue, display results

    else:
        venues = Venue.objects.all().order_by('name')

    paginator = Paginator(venues, 25)
    page = request.GET.get('page')

    try:
        venueset = paginator.page(page)

    except PageNotAnInteger:
        venueset = paginator.page(1)

    except EmptyPage:
        venueset = paginator.page(paginator.num_pages)

    page = 'lmn/venues/venue_list.html'
    data = {'venues': venues, 'form': form, 'search_term': search_name, 'venueset': venueset}

    return render(request, page, data)


def artists_at_venue(request, venue_pk):
    """ Get all of the artists who have played a show at the venue with pk provided """

    shows = Show.objects.filter(venue=venue_pk).order_by('show_date').reverse()  # most recent first
    venue = Venue.objects.get(pk=venue_pk)

    paginator = Paginator(shows, 25)
    page = request.GET.get('page')

    try:
        showset = paginator.page(page)

    except PageNotAnInteger:
        showset = paginator.page(1)

    except EmptyPage:
        showset = paginator.page(paginator.num_pages)

    page = 'lmn/artists/artist_list_for_venue.html'
    data = {'venue': venue, 'shows': shows, 'showset': showset}

    return render(request, page, data)


def venue_detail(request, venue_pk):

    venue = get_object_or_404(Venue, pk=venue_pk)

    page = 'lmn/venues/venue_detail.html'
    data = {'venue': venue}

    return render(request, page, data)
