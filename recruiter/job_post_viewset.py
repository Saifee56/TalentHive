from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from recruiter.models import JobPost,RecruiterProfile
from recruiter.serializers import JobPostSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction

class JobPostViewset(viewsets.ModelViewSet):

    permission_classes=[AllowAny]
    serializer_class=JobPostSerializer

    @action(detail=True,methods=['post'],url_path='create-job-post')
    def create_job_post(self,request):
        recruiter_id=request.data.get('recruiter')

        if not recruiter_id:
            return Response({
                "message":"Every job should be associated with a recruiter id"
            },status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                serializer=JobPostSerializer(data=request.data)
                if not serializer.is_valid():
                    return Response({
                        "success":False,
                        "message":"Job post publish failed",
                        "errrors":serializer.errors
                    },status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response({
                    "success":True,
                    "message":"Job post published successfully",
                    "data":serializer.data
                },status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "success":False,
                "errors":f"An error occurred{str(e)}"
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True,methods=['patch'],url_path='update-job-post')
    def update_job_post(self,request,pk=None):
        job_post=get_object_or_404(JobPost,pk=pk)

        try:
            with transaction.atomic(): 
                   serializer=JobPostSerializer(job_post,data=request.data,partial=True)
                   if not serializer.is_valid():
                        return Response(
                            {
                                "success":False,
                                "message":"Job Post update failed",
                                "data":serializer.errors
                            },status=status.HTTP_400_BAD_REQUEST
                        )
                   serializer.save()
                   return Response({
                         "success":True,
                         "message":"Job Post updated successfully",
                         "data":serializer.data
                    },status=status.HTTP_201_CREATED)
        except Exception as e:
             return Response({
                  "success":False,
                  "message":f"An error occured {str(e)}"
             })

    @action(detail=True, methods=['delete'], url_path='delete-job-post')
    def delete_job_post(self, request, pk=None):
        job_post = get_object_or_404(JobPost, pk=pk)
        
        try:
            with transaction.atomic():
                job_post.delete()
                return Response({
                    "success": True,
                    "message": "Job deleted successfully"
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True,methods=['get'],url_path='fetch-all')
    def fetch_all(self,request,pk=None):
        recruiter_id=request.query_params.get('recruiter',pk=pk)

        if not recruiter_id:
            return Response({
                "message":"Recruiter Profile ID is required"
            },status=status.HTTP_400_BAD_REQUEST)
        
        job_posts=JobPost.objects.filter(recruiter=recruiter_id).order_by('-created_at')

        serializer=JobPostSerializer(job_posts,many=True)

        return Response({
            "success":True,
            "recruiter_id":recruiter_id.user.name,
            "total_jobs":job_posts.count(),
            "data":serializer.data
        },status=status.HTTP_200_OK)
