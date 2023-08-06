from fastapi import FastAPI, HTTPException
from pytube import YouTube
import moviepy.editor as mp
import os
import eyed3
import requests

app = FastAPI()


# Youtube to Tagged MP3 Request
@app.get("/youtubetotaggedmp3")
async def download_youtube_video(url: str, song_title=None, artist=None, album=None, album_artist=None, track_num=None, cover_url=None):
    try:

        # Downloades mp4 of Youtube Video to 
        # musictagger folder using pytube API
        yt_video = YouTube(url)
        mp4_audio_stream = yt_video.streams.get_highest_resolution()
        mp4_title = mp4_audio_stream.title
        mp4_audio_stream.download()

        # Converts mp4 video to a new mp3 file saved to 
        # musictagger folder using moviepy API
        mp4_audio = mp.VideoFileClip(f"{mp4_title}.mp4")
        song_file = song_title.lower().replace(' ', '')
        mp4_audio.audio.write_audiofile(f"{song_file}.mp3")

        # Deletes mp4 video from folder
        os.remove(f"{mp4_title}.mp4")

        # Adds artist, album, album artist, song title, & track number 
        # metadata to mp3 file using eyed3 API
        mp3_file = eyed3.load(f"{song_file}.mp3")
        mp3_file.tag.artist = artist
        mp3_file.tag.album = album
        mp3_file.tag.album_artist = album_artist
        mp3_file.tag.title = song_title
        mp3_file.tag.track_num = track_num
        mp3_file.tag.save()

        #Tags image to mp3 metadata from URL
        cover = requests.get(cover_url)
        mp3_file.tag.images.set(3, cover.content , "image/jpeg" ,u"Cover")
        mp3_file.tag.save()


        return {"message": f"{song_title} downloaded successfully!"}
    except KeyError:
        raise HTTPException(status_code=400, detail="Error: Video is not available or cannot be downloaded")
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: Invalid URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error downloading video: " + str(e))
    


# Untagged MP3 to Tagged MP3 Request
# work in progress
@app.get("/mp3totaggedmp3")
async def download_tagged_song(url: str, song_title=None, artist=None, album=None, album_artist=None, track_num=None, cover_url=None):
    try:

        # Downloades mp4 of Youtube Video to 
        # musictagger folder using pytube API
        yt_video = YouTube(url)
        mp4_audio_stream = yt_video.streams.get_highest_resolution()
        mp4_title = mp4_audio_stream.title
        mp4_audio_stream.download()

        # Converts mp4 video to a new mp3 file saved to 
        # musictagger folder using moviepy API
        mp4_audio = mp.VideoFileClip(f"{mp4_title}.mp4")
        song_file = song_title.lower().replace(' ', '')
        mp4_audio.audio.write_audiofile(f"{song_file}.mp3")

        # Deletes mp4 video from folder
        os.remove(f"{mp4_title}.mp4")

        # Adds artist, album, album artist, song title, & track number 
        # metadata to mp3 file using eyed3 API
        mp3_file = eyed3.load(f"{song_file}.mp3")
        mp3_file.tag.artist = artist
        mp3_file.tag.album = album
        mp3_file.tag.album_artist = album_artist
        mp3_file.tag.title = song_title
        mp3_file.tag.track_num = track_num
        mp3_file.tag.save()

        #Tags image from URL
        cover = requests.get(cover_url)
        mp3_file.tag.images.set(3, cover.content , "image/jpeg" ,u"Cover")
        mp3_file.tag.save()


        return {"message": f"{song_title} downloaded successfully!"}
    except KeyError:
        raise HTTPException(status_code=400, detail="Error: Video is not available or cannot be downloaded")
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: Invalid URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error downloading video: " + str(e))