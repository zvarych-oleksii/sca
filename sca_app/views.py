from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, MissionSerializer, TargetSerializer
import requests

class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

    def create(self, request, *args, **kwargs):
        breed = request.data.get('breed')
        response = requests.get('https://api.thecatapi.com/v1/breeds')
        breeds = [b['name'] for b in response.json()]
        if breed not in breeds:
            return Response({'error': 'Invalid breed'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.assigned_cat:
            return Response({'error': 'Cannot delete an assigned mission'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['patch'])
    def complete_target(self, request, pk=None):
        target_id = request.data.get('target_id')
        try:
            target = Target.objects.get(id=target_id, mission_id=pk)
            if target.is_complete:
                return Response({'error': 'Target already completed'}, status=status.HTTP_400_BAD_REQUEST)
            target.is_complete = True
            target.save()

            # Check if all targets are complete
            mission = target.mission
            if all(t.is_complete for t in mission.targets.all()):
                mission.is_complete = True
                mission.save()

            return Response({'status': 'Target marked as complete'})
        except Target.DoesNotExist:
            return Response({'error': 'Target not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'], url_path='update_notes')
    def update_notes(self, request, pk=None):
        target_id = request.data.get('target_id')
        notes = request.data.get('notes')

        if not target_id or not notes:
            return Response({'error': 'Target ID and Notes are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target = Target.objects.get(id=target_id, mission_id=pk)

            if target.is_complete:
                return Response({'error': 'Cannot update notes for a completed target'},
                                status=status.HTTP_400_BAD_REQUEST)

            if target.mission.is_complete:
                return Response({'error': 'Cannot update notes for a completed mission'},
                                status=status.HTTP_400_BAD_REQUEST)

            target.notes = notes
            target.save()

            return Response({'status': 'Notes updated successfully', 'target': TargetSerializer(target).data})

        except Target.DoesNotExist:
            return Response({'error': 'Target not found'}, status=status.HTTP_404_NOT_FOUND)