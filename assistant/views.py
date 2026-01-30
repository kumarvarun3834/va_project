from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .va_core import process_command
from .models import ChatSession, ChatMessage
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request):
    return render(request, "assistant/index.html")

@csrf_exempt
def assistant_view(request, session_id=None):
    if request.method == "POST":
        data = json.loads(request.body)
        command = data.get("command", "")

        if not command.strip():
            return JsonResponse({"error": "Empty command"}, status=400)

        response = process_command(command)

        # If session exists, continue; else create new
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id)
            except ChatSession.DoesNotExist:
                return JsonResponse({"error": "Session not found"}, status=404)
        else:
            session = ChatSession.objects.create(title=command[:30] or "New Chat")

        # Save user + assistant messages
        ChatMessage.objects.create(session=session, role="user", content=command)
        ChatMessage.objects.create(session=session, role="assistant", content=response)

        return JsonResponse({"response": response, "session_id": session.id})

    return JsonResponse({"error": "POST request required"}, status=400)



def get_sessions(request):
    sessions = ChatSession.objects.all().order_by("-created_at")
    data = [{"id": s.id, "title": s.title or f"Session {s.id}"} for s in sessions]
    return JsonResponse({"sessions": data})


def get_history(request, session_id):
    try:
        session = ChatSession.objects.get(id=session_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Session not found"}, status=404)

    messages = session.messages.order_by("timestamp")
    history = [{"role": m.role, "content": m.content} for m in messages]
    return JsonResponse({"history": history})


@csrf_exempt
def delete_session(request, session_id):
    if request.method == "DELETE":
        try:
            session = ChatSession.objects.get(id=session_id)
            session.delete()
            return JsonResponse({"success": True, "message": "Session deleted successfully"})
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Session not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "DELETE request required"}, status=400)


@csrf_exempt
def update_session(request, session_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            new_title = data.get("title", "").strip()
            
            if not new_title:
                return JsonResponse({"error": "Title cannot be empty"}, status=400)
            
            session = ChatSession.objects.get(id=session_id)
            session.title = new_title
            session.save()
            
            return JsonResponse({"success": True, "message": "Session title updated successfully"})
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Session not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "PUT request required"}, status=400)
