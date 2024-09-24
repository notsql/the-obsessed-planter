from threading import Event
import json

import pygame

from firebase_admin import initialize_app, firestore
from vonage import Client

TOP = 5
playlist = []

vcSecrets = json.load(open("./vonageAccountKey.json"))

pygame.mixer.init()

app = initialize_app()
db = firestore.client(app)

vc = Client(
  application_id=vcSecrets["VONAGE_APPLICATION_ID"],
  private_key=vcSecrets["VONAGE_APPLICATION_PRIVATE_KEY"],
)

def play_sound(file_path):
  sound = pygame.mixer.Sound(file_path)

  playing = sound.play()

  sound.set_volume(1)

  while playing.get_busy():
    pygame.time.delay(100)

def add_fixed_playlist(file_path):
  playlist.insert(0, file_path)

  if len(playlist) > TOP:
    playlist.pop()



callback_done = Event()



def on_snap(col_snap, changes, read_time):
  for change in changes:
    if change.type.name == "ADDED":
      file_path = f"./output/{change.document.id}"
      
      try:
        res = vc.voice.get_recording(change.document.to_dict()["recording_url"])

        f = open(file_path, "wb+")
        f.write()
        f.close()

        add_fixed_playlist(file_path)
      except:
        print("File does not exist or has expired")

col_query = db.collection("Callers").on_snapshot(on_snap)

while True:
  for audio in playlist:
    play_sound(audio)
