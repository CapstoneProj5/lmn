from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import NewNoteForm
from .models import Note, Show


@login_required
def new_note(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST':

        form = NewNoteForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            note = form.save(commit=False)

            if note.title and note.text:  # If note has both title and text

                note.user = request.user
                note.show = show
                note.picture = note.picture
                note.posted_date = timezone.now()
                note.save()

                return redirect('lmn:note_detail', note_pk=note.pk)

    else:
        form = NewNoteForm()

    page = 'lmn/notes/new_note.html'
    data = {'form': form, 'show': show}

    return render(request, page, data)


def latest_notes(request):

    notes = Note.objects.all().order_by('posted_date').reverse()

    paginator = Paginator(notes, 25)
    page = request.GET.get('page')

    try:
        noteset = paginator.page(page)

    except PageNotAnInteger:
        noteset = paginator.page(1)

    except EmptyPage:
        noteset = paginator.page(paginator.num_pages)

    page = 'lmn/notes/note_list.html'
    data = {'notes': notes, "noteset": noteset}

    return render(request, page, data)


def notes_for_show(request, show_pk):

    notes = Note.objects.filter(show=show_pk).order_by('posted_date').reverse()  # Notes for show, most recent first
    show = Show.objects.get(pk=show_pk)  # Contains artist, venue

    page = 'lmn/notes/note_list.html'
    data = {'show': show, 'notes': notes}

    return render(request, page, data)


@login_required
def edit_notes(request, pk):

    notes = get_object_or_404(Note, pk=pk)

    if request.method == "Post":
        form = NewNoteForm(request.POST or None, request.FILES, instance=notes)
        if form.is_valid():
            notes = form.save(commit=False)
            notes.save()
            return redirect('lmn:notes')

    else:
        form = NewNoteForm( instance=notes)

    page = r'lmn/notes/note_edit.html'
    data = {'form': form}

    return render(request, page, data)


@login_required
def delete_notes(request, note_pk):

    notes = get_object_or_404(Note, pk=note_pk)
    notes.delete()

    return redirect('lmn:latest_notes')


def note_detail(request, note_pk):

    note = get_object_or_404(Note, pk=note_pk)
    page = 'lmn/notes/note_detail.html'
    data = {'note': note}

    return render(request, page, data)


@login_required
def note_edit(request, note_pk):

    note = get_object_or_404(Note, pk=note_pk)
    show = get_object_or_404(Show, pk=note.show.pk)

    if request.method == "POST":
        form = NewNoteForm(request.POST or None, request.FILES, instance=note)
        if form.is_valid():
            note.save()
            return redirect('lmn:note_detail', pk=note.pk)

    else:
        form = NewNoteForm(instance=note)

    page = 'lmn/notes/note_edit.html'
    data = {'form': form,'note': note,'show': show}

    return render(request, page, data)


@login_required
def note_delete(request, note_pk):

    note = get_object_or_404(Note, pk=note_pk)
    note.delete()

    return redirect('lmn:user_profile')
