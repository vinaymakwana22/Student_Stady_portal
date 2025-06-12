from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from .forms import (
    NotesForm, HomeworkForm, DashboardForm, TodoForm,
    ConversionForm, ConversionLengthForm, ConversionMassForm,
    UserRegistrationForm
)
from .models import Notes, Homework, Todo
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from wikipedia.exceptions import DisambiguationError


# Home page
def home(request):
    features = [
        {'title': 'Notes', 'description': 'Create and store notes permanently.', 'url': 'notes', 'image': 'images/notes.jpg'},
        {'title': 'Homework', 'description': 'Add homework with deadlines.', 'url': 'homework', 'image': 'images/homework.jpg'},
        {'title': 'YouTube', 'description': 'Search and play YouTube videos.', 'url': 'youtube', 'image': 'images/youtube.jpg'},
        {'title': 'To Do', 'description': 'Manage your daily tasks.', 'url': 'todo', 'image': 'images/todo.jpg'},
        {'title': 'Books', 'description': 'Browse categorized book lists.', 'url': 'books', 'image': 'images/books.jpg'},
        {'title': 'Dictionary', 'description': 'Search meanings instantly.', 'url': 'dictionary', 'image': 'images/dictionary.jpg'},
        {'title': 'Wikipedia', 'description': 'Search fast academic content.', 'url': 'wiki', 'image': 'images/wiki.jpg'},
        {'title': 'Conversion', 'description': 'Convert units and values.', 'url': 'conversion', 'image': 'images/conversion.jpg'},
        {'title': 'AI Assistant', 'description': 'Chat with your smart AI assistant.', 'url': 'ai_chat', 'image': 'images/ai.jpg'},
    ]
    return render(request, 'dashboard/home.html', {'features': features})


@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            note = Notes(user=request.user, title=title, description=description)
            note.save()
            messages.success(request, f"Note added by {request.user.username} successfully!")
    else:
        form = NotesForm()

    notes_list = Notes.objects.filter(user=request.user)
    context = {'notes': notes_list, 'form': form}
    return render(request, 'dashboard/notes.html', context)


@login_required
def delete_note(request, pk=None):
    try:
        note = Notes.objects.get(id=pk)
        note.delete()
        messages.success(request, "Note deleted successfully!")
    except Notes.DoesNotExist:
        messages.error(request, "Note not found.")
    return redirect("notes")


class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = 'dashboard/notes_detail.html'
    context_object_name = 'note'


@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            finished = request.POST.get('is_finished') == 'on'
            homeworks = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homeworks.save()
            messages.success(request, f'Homework added by {request.user.username} successfully!')

    form = HomeworkForm()
    homeworks = Homework.objects.filter(user=request.user)
    homework_done = not homeworks.exists()

    context = {
        'homeworks': homeworks,
        'homeworks_done': homework_done,
        'form': form,
    }
    return render(request, 'dashboard/homework.html', context)


@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    homework.is_finished = not homework.is_finished
    homework.save()
    return redirect('homework')


@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    messages.success(request, "Homework deleted successfully!")
    return redirect("homework")


@login_required
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=15)
        result_list = []

        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
                'description': '',
            }

            if i.get('descriptionSnippet'):
                result_dict['description'] = ''.join([j['text'] for j in i['descriptionSnippet']])

            result_list.append(result_dict)

        context = {'form': form, 'results': result_list}
        return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardForm()
    return render(request, "dashboard/youtube.html", {'form': form})


@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            finished = request.POST.get("is_finished") == "on"
            todos = Todo(user=request.user, title=request.POST['title'], is_finished=finished)
            todos.save()
            messages.success(request, f'Todo Added From {request.user.username} successfully!')
            return redirect('todo')
    else:
        form = TodoForm()

    todo = Todo.objects.filter(user=request.user)
    todos_done = len(todo) == 0
    context = {
        'form': form,
        'todos': todo,
        "todos_done": todos_done
    }
    return render(request, "dashboard/todo.html", context)


@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    todo.is_finished = not todo.is_finished
    todo.save()
    return redirect('todo')


@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


@login_required
def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('PageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('PageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks', {}).get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
        context = {'form': form, 'results': result_list}
        return render(request, "dashboard/books.html", context)
    else:
        form = DashboardForm()
    return render(request, "dashboard/books.html", {'form': form})


@login_required
def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST.get('text', '').strip()
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text

        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            answer = r.json()

            phonetics = answer[0]['phonetics'][0].get('text', '')
            audio = answer[0]['phonetics'][0].get('audio', '')
            definition = answer[0]['meanings'][0]['definitions'][0].get('definition', '')
            example = answer[0]['meanings'][0]['definitions'][0].get('example', '')

            synonyms = []
            for meaning in answer[0]['meanings']:
                for definition_item in meaning['definitions']:
                    synonyms += definition_item.get('synonyms', [])
            synonyms = list(set(synonyms))

            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms,
            }
        except requests.exceptions.RequestException as e:
            context = {'form': form, 'input': text, 'error': f"Could not retrieve data: {str(e)}"}
        except (IndexError, KeyError):
            context = {'form': form, 'input': text, 'error': "No data found for this word."}

        return render(request, "dashboard/dictionary.html", context)
    else:
        form = DashboardForm()
        return render(request, "dashboard/dictionary.html", {'form': form})


@login_required
def wiki(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        form = DashboardForm(request.POST)
        results = wikipedia.search(text)

        if results:
            first_result = results[0]
            try:
                page = wikipedia.page(first_result)
                context = {
                    'form': form,
                    'title': page.title,
                    'link': page.url,
                    'details': page.summary,
                    'note': f"Showing results for '{first_result}'."
                }
            except DisambiguationError as e:
                try:
                    page = wikipedia.page(e.options[0])
                    context = {
                        'form': form,
                        'title': page.title,
                        'link': page.url,
                        'details': page.summary,
                        'note': f"Term is ambiguous, showing results for '{e.options[0]}'."
                    }
                except Exception:
                    context = {'form': form, 'error': "Sorry, could not find a detailed page to show."}
            except Exception:
                context = {'form': form, 'error': "Sorry, could not fetch the Wikipedia page."}
        else:
            context = {'form': form, 'error': f"No Wikipedia results found for '{text}'."}

        return render(request, "dashboard/wiki.html", context)
    else:
        form = DashboardForm()
        return render(request, "dashboard/wiki.html", {'form': form})


@login_required
def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)

        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {'form': form, 'm_form': measurement_form, 'input': True}
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input) * 3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input) / 3} yard'
                context['answer'] = answer

        elif request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {'form': form, 'm_form': measurement_form, 'input': True}
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input) * 0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input) * 2.20462} pound'
                context['answer'] = answer

    else:
        form = ConversionForm()
        context = {'form': form, 'input': False}

    return render(request, "dashboard/conversion.html", context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account Created for {username}!!")
            return redirect("login")
    else:
        form = UserRegistrationForm()

    return render(request, "dashboard/register.html", {'form': form})


@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)

    homework_done = len(homeworks) == 0
    todos_done = len(todos) == 0

    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        'todos_done': todos_done
    }
    return render(request, "dashboard/profile.html", context)


def logout_view(request):
    logout(request)
    return render(request, 'dashboard/logout.html')


@login_required
def ai_chat_view(request):
    form = DashboardForm()
    chat_history = []
    return render(request, 'dashboard/ai-chat.html', {
        'form': form,
        'chat_history': chat_history
    })


"""
DOCUMENTATION:

This Django application provides a robust backend framework for user management, database handling, and routing.

It enhances functionality by integrating with multiple external APIs, including:
- YouTube API for video search.
- Google Books API for retrieving book information.
- Dictionary API for word meanings.
- Wikipedia API for quick knowledge lookup.

Key Components:

1. Forms:
   - Used to collect and validate user input such as notes, homework entries, and search queries.

2. Models:
   - Define the structure of data stored in the database, including Notes, Homework, and Todo items linked to users.

3. Views:
   - Handle application logic by processing incoming requests, interacting with models, and returning appropriate responses.

4. Templates:
   - Render dynamic HTML pages to present data in the user interface.

5. Third-Party Libraries:
   - External packages like `youtubesearchpython` for YouTube video searches,
     `requests` for API calls (Google Books, Dictionary), and
     `wikipedia` for Wikipedia searches.
   - These libraries add powerful features without requiring complex implementation from scratch.
"""