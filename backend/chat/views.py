from rest_framework.views import APIView
from rest_framework.response import Response
from rag_engine.retriever import retrieve
from rag_engine.generator import generate_answer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes





from .models import ChatMessage
from .serializers import ChatMessageSerializer


class AskQuestionView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        question = request.data.get("question")
        department = request.data.get("department")
        user_role = user.role

        docs, error_or_confidence = retrieve(question, department, user_role)

        if isinstance(error_or_confidence, str) and "denied" in error_or_confidence:
            return Response({"error": error_or_confidence}, status=403)

        if not docs:
            return Response({"answer": "No relevant documents found.", "confidence": "low"})

        # Generate with confidence
        context = "\n\n".join([d["content"] for d in docs])
        confidence = error_or_confidence  # From retriever
        answer = generate_answer(question, context, docs, confidence)

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