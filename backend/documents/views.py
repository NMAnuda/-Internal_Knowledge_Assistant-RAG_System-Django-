from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DocumentUploadSerializer
from rag_engine.pipeline import ingest_document

class DocumentUploadView(APIView):
    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)

        if serializer.is_valid():
            document = serializer.save()

            
            ingest_document(document.file.path)

            return Response(
                {"message": "Document uploaded and indexed"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=400)
