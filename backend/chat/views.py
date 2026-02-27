from rest_framework.views import APIView
from rest_framework.response import Response
from rag_engine.retriever import retrieve
from rag_engine.generator import generate_answer, check_ollama_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes





from .models import ChatMessage
from .serializers import ChatMessageSerializer


class AskQuestionView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("debug 1")
        try:
            user = request.user
            question = request.data.get("question")
            department = request.data.get("department")
            user_role = user.role
            print("user",user,"user_role",user_role)
            print("aa",question)
            docs, error_or_confidence = retrieve(question, department, user_role)
            print("docs",docs)
            if isinstance(error_or_confidence, str) and "denied" in error_or_confidence:
                return Response({"error": error_or_confidence}, status=403)

            if not docs:
                return Response({"answer": "No relevant documents found.", "confidence": "low"})

            # Generate with confidence
            context = "\n\n".join([d["content"] for d in docs])
            confidence = error_or_confidence  # From retriever
            
            try:
                answer = generate_answer(question, context, docs, confidence)
            except Exception as e:
                return Response({
                    "error": str(e),
                    "message": "Failed to generate answer. Check Ollama service.",
                    "hint": "Run 'GET /api/chat/health/' to diagnose the issue"
                }, status=503)
            print("Response",Response)
            # Save to history (include confidence)
            chat_msg = ChatMessage.objects.create(
                user=user,
                question=question,
                answer=answer,
                department=department,
                sources=[{"doc_name": d["doc_name"], "score": d["score"]} for d in docs],
                confidence=confidence  # Add to model if you update it
            )

            return Response({
                "answer": answer,
                "confidence": confidence,
                "sources": [{"id": i+1, "doc": d["doc_name"], "score": d["score"]} for i, d in enumerate(docs)],
                "message_id": chat_msg.id
            })
        except Exception as e:
            return Response({
                "error": str(e),
                "message": "An unexpected error occurred"
            }, status=500)
    
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ChatHistoryView(request):
    user = request.user
    page = request.query_params.get('page', 1)  # Basic pagination
    limit = request.query_params.get('limit', 10)
    messages = ChatMessage.objects.filter(user=user).order_by('-timestamp')[:int(limit) * int(page)]

    serializer = ChatMessageSerializer(messages, many=True)
    return Response({
        "history": serializer.data,
        "count": messages.count()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def OllamaHealthCheck(request):
    """Diagnostic endpoint to check if Ollama is running and configured correctly"""
    is_ok, message = check_ollama_connection()
    
    return Response({
        "status": "healthy" if is_ok else "unhealthy",
        "ollama_running": is_ok,
        "message": message,
        "endpoint": "http://localhost:11434/api/generate"
    }, status=200 if is_ok else 503)