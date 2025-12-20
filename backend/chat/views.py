from rest_framework.views import APIView
from rest_framework.response import Response
from rag_engine.retriever import retrieve

class AskQuestionView(APIView):
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({'error': 'Question required'}, status=400)
        print("question",question)
        docs = retrieve(question)
        # simple RAG response: join retrieved docs
        answer = "\n".join(docs)
        return Response({'answer': answer})
