from django.shortcuts import render

# Create your views here.
from sistema_sga.messages.models import Message
from sistema_sga.core.models import Profile

def inbox(request):
    conversations = Message.get_conversations(user=request.user)
    active_conversation = None
    messages = None
    if conversations:
        conversation = conversations[0]
        active_conversation = conversation['user'].username
        messages = Message.objects.filter(user=request.user, conversation=conversation['user'])
        messages.update(is_read=True)
        for conversation in conversations:
            if conversation['user'].username == active_conversation:
                conversation['unread'] = 0              
    return render(request, 'messages/inbox.html', {
        'messages': messages, 
        'conversations': conversations,
        'active': active_conversation
        })

def messages(request, username):
    conversations =Message.get_conversations(user=request.user)
    active_conversation = username
    messages = Message.objects.filter(user=request.user, conversation__username=username)
    messages.update(is_read=True)
    for conversation in conversations:
        if conversation['user'].username == username:
            conversation['unread'] = 0
    return render(request, 'messages/inbox.html', {
        'messages': messages,
        'conversations': conversations,
        'active': active_conversation
        })

def new(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        try:
            to_user = Profile.objects.get(username=to_user_username)
        except Exception, e:
            try:
                to_user_username = to_user_username[to_user_username.rfind('(')+1:len(to_user_username)-1]
                to_user = Profile.objects.get(username=to_user_username)
            except Exception, e:
                return redirect('/messages/new/')
        message = request.POST.get('message')
        if len(message.strip()) == 0:
            return redirect('/messages/new/')
        if from_user != to_user:
            Message.send_message(from_user, to_user, message)
        return redirect(u'/messages/{0}/'.format(to_user_username))
    else:
        conversations = Message.get_conversations(user=request.user)
        return render(request, 'messages/inbox.html', {
            'conversations': conversations
            })

def send(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        to_user = Profile.objects.get(username=to_user_username)
        message = request.POST.get('message')
        if len(message.strip()) == 0:
            return HttpResponse()
        if from_user != to_user:
            msg = Message.send_message(from_user, to_user, message)
            return render(request, 'messages/includes/partial_message.html', {'message': msg})
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def users(request):
    users = Profile.objects.filter(is_active=True)
    dump = []
    template = u'{0} ({1})'
    for user in users:
        if user.profile.get_screen_name() != user.username:
            dump.append(template.format(user.profile.get_screen_name(), user.username))
        else:
            dump.append(user.username)
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')