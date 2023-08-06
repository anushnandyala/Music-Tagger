from fastapi import FastAPI, HTTPException
from pytube import YouTube
import moviepy.editor as mp
import os
import eyed3

app = FastAPI()

@app.get("/download")
async def download_video(url: str, song_title=None, artist=None, album=None, album_artist=None, track_num=None):
    try:
        # Creates pytube API YouTube object
        yt_video = YouTube(url)

        # Creates pytube API Stream object with audio only
        mp4_audio_stream = yt_video.streams.get_highest_resolution()
        
        mp4_title = mp4_audio_stream.title

        mp4_audio_stream.download()

        mp4_audio = mp.VideoFileClip(f"{mp4_title}.mp4")

        mp4_audio.audio.write_audiofile(f"{mp4_title}.mp3")

        os.remove(f"{mp4_title}.mp4")

        mp3_file = eyed3.load(f"{mp4_title}.mp3")
        mp3_file.tag.artist = artist
        mp3_file.tag.album = album
        mp3_file.tag.album_artist = album_artist
        mp3_file.tag.title = song_title
        mp3_file.tag.track_num = track_num

        mp3_file.tag.save()


        return {"message": f"{mp4_title} downloaded successfully!"}
    except KeyError:
        raise HTTPException(status_code=400, detail="Error: Video is not available or cannot be downloaded")
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: Invalid URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error downloading video: " + str(e))