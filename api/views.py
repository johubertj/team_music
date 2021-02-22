from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.serializers import Serializer
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class CreateRoomViewView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        # strat: creates a session for the user once they go onto the website
        # purpose: to remember the person's existing data
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

            # converts to json object and checks if 2 fields for createroomserializer 
            # is valid
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                guest_can_pause = serializer.data.guest_can_pause
                votes_to_skip = serializer.data.votes_to_skip
                host = self.request.session.session_key

                # checks if the room alrdy exists, we update specific settings
                queryset = Room.objects.filter(host=host)
                if queryset.exists():
                    room = queryset[0]
                    room.guest_can_pause = guest_can_pause
                    room.votes_to_skip = votes_to_skip
                    #in order to save and send the field
                    room.save(update_fields=['guest_can_pause','votes_to_skip'])

            