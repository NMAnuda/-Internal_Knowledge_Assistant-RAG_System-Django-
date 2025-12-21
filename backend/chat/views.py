from rest_framework.views import APIView
from rest_framework.response import Response
from rag_engine.retriever import retrieve
from rag_engine.generator import generate_answer

class AskQuestionView(APIView):
    def post(self, request):
        question = request.data.get("question")
        department = request.data.get("department")
        user_role = request.data.get("user_role")

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