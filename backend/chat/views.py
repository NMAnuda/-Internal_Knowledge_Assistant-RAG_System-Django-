from rest_framework.views import APIView
from rest_framework.response import Response
from rag_engine.retriever import retrieve
from rag_engine.generator import generate_answer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

class AskQuestionView(APIView):
    permission_classes = [IsAuthenticated]  # 🔥 NEW: Requires login
    
    def post(self, request):
        # Get user role from token
        user_role = request.user.role
        question = request.data.get("question")
        department = request.data.get("department")

        docs, error = retrieve(question, department, user_role)

        if error:
            return Response({"error": error}, status=403)

        if not docs:
            return Response({"answer": "No relevant documents found."})

        context = "\n\n".join([d["content"] for d in docs])

        answer = generate_answer(question, context)

        return Response({
            "answer": answer,
            "department": department,
            "role": user_role
        })