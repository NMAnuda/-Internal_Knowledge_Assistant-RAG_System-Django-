from rest_framework.views import APIView
from rest_framework.response import Response
from rag_engine.retriever import retrieve
from rag_engine.generator import generate_answer

class AskQuestionView(APIView):
    def post(self, request):
        question = request.data.get("question")
        context = retrieve(question)
        answer = generate_answer(question, context)

        return Response({
            "answer": answer,
            "sources": context
        })
