from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Faculty, Department, UserProfile, Election, Candidate, Vote
from .serializers import (
    UserSerializer, UserProfileSerializer, ElectionSerializer, 
    CandidateSerializer, VoteSerializer, FacultySerializer, DepartmentSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def candidates(self, request, pk=None):
        election = self.get_object()
        candidates = Candidate.objects.filter(election=election, is_approved=True)
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')
        student_id = request.data.get('student_id')
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            student_id=student_id
        )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class VerifyUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user_profile = request.user.userprofile
        user_profile.is_verified = True
        user_profile.save()
        return Response({'message': 'User verified successfully'})

class VoteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        election_id = request.data.get('election_id')
        candidate_id = request.data.get('candidate_id')
        
        try:
            election = Election.objects.get(id=election_id)
            candidate = Candidate.objects.get(id=candidate_id, election=election)
            
            # Check if user already voted
            if Vote.objects.filter(election=election, voter=request.user).exists():
                return Response({'error': 'You have already voted in this election'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create vote
            vote = Vote.objects.create(
                election=election,
                voter=request.user,
                candidate=candidate
            )
            
            # Update candidate vote count
            candidate.votes_received += 1
            candidate.save()
            
            return Response({'message': 'Vote recorded successfully'}, status=status.HTTP_201_CREATED)
            
        except Election.DoesNotExist:
            return Response({'error': 'Election not found'}, status=status.HTTP_404_NOT_FOUND)
        except Candidate.DoesNotExist:
            return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)

class ElectionResultsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, election_id):
        try:
            election = Election.objects.get(id=election_id)
            candidates = Candidate.objects.filter(election=election).annotate(
                vote_count=Count('vote')
            ).order_by('-vote_count')
            
            results = []
            for candidate in candidates:
                results.append({
                    'candidate_name': candidate.user.get_full_name() or candidate.user.username,
                    'position': candidate.position,
                    'votes': candidate.vote_count
                })
            
            return Response({
                'election': ElectionSerializer(election).data,
                'results': results
            })
        except Election.DoesNotExist:
            return Response({'error': 'Election not found'}, status=status.HTTP_404_NOT_FOUND)
