import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3 # boto3 is a package which programatically communicatw with aws services.
from datetime import datetime

def lambda_handler(event, context):
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')

    client_credentials_manager=SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    playlist_link = 'https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF'
    playlist_URI = playlist_link.split('/')[-1]
    
    data = sp.playlist_tracks(playlist_URI)
    print(data)
    # Till here we have extract data from api.
    
    # Now we have to store data in s3 and we required boto3 for that
    # dump entire json data into s3 bucket
    
    filename = "spotify_raw_" + str(datetime.now()) + ".json" # actual name of file which is stored in raw data>processed folder
    
    client = boto3.client('s3')
    client.put_object(
        Bucket='spotify-etl-project1-vaishnav',
        Key='raw_data/to_processed/' + filename, # key is where we want to store the data (folder path)
        Body=json.dumps(data) # json.dump convert entire data into json strings and put it into s3
        )
        
        
# Note: We add permision to IAM role to communicate two aws servies such as lambda and s3 bucket authorization.