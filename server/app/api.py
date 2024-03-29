from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pytube import YouTube
from pytube import Playlist
from pathlib import Path
import moviepy.editor as mp
import os
import eyed3
import requests
import glob
import urllib.request

app = FastAPI()

origins = [
    "http://localhost:5173",
    "localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to Music Tagger."}


# Youtube to Tagged MP3 Request
@app.get("/youtubetotaggedmp3")
async def download_youtube_video_tagged_mp3(url: str, file_name=None, song_title=None, artist=None, album=None, album_artist=None, track_num=None, cover_url=None):
    try:

        # Downloades mp4 of Youtube Video to 
        # musictagger folder using pytube API
        yt_video = YouTube(url)
        mp4_audio_stream = yt_video.streams.get_highest_resolution()
        mp4_title = mp4_audio_stream.title
        mp4_audio_stream.download()

        # renames video file
        file = glob.glob(f"{os.getcwd()}/**/*.mp4", recursive = True)
        os.rename(file[0], f"{os.getcwd()}/video.mp4")

        # Converts mp4 video to a new mp3 file saved to 
        # musictagger folder using moviepy API
        #mp4_audio = mp.VideoFileClip(f"{mp4_title}.mp4")
        mp4_audio = mp.VideoFileClip("video.mp4")
        if file_name != None:
            song_file = file_name
        else:
            if song_title != None:
                song_file = song_title.lower().replace(' ', '')
            else:
                song_file = mp4_title.lower().replace(' ', '')
        mp4_audio.audio.write_audiofile(f"{song_file}.mp3")

        # Deletes mp4 video from folder
        os.remove("video.mp4")

        # Adds artist, album, album artist, song title, & track number 
        # metadata to mp3 file using eyed3 API
        mp3_file = eyed3.load(f"{song_file}.mp3")
        mp3_file.tag.artist = artist
        mp3_file.tag.album = album
        mp3_file.tag.album_artist = album_artist
        mp3_file.tag.title = song_title
        mp3_file.tag.track_num = track_num
        mp3_file.tag.save()

        # Tags image to mp3 metadata from URL
        if cover_url != None:
            cover = requests.get(cover_url)
            mp3_file.tag.images.set(3, cover.content , "image/jpeg" ,u"Cover")
            mp3_file.tag.save()
        else:
            cover_url = yt_video.thumbnail_url
            cover = requests.get(cover_url)
            mp3_file.tag.images.set(3, cover.content , "image/jpeg" ,u"Cover")
            mp3_file.tag.save()

        # Moves file to downloads folder
        downloads_path = str(Path.home() / "Downloads")        
        os.rename(f"{os.getcwd()}/{song_file}.mp3", f"{downloads_path}/{song_file}.mp3")

        # Success message
        return {"message": f"{song_file}.mp3 downloaded successfully to downloads folder!"}
    
    except KeyError:
        raise HTTPException(status_code=400, detail="Error: Video is not available or cannot be downloaded")
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: Invalid URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error downloading video: " + str(e))
    

# Youtube Playlist to Tagged MP3 Request
@app.get("/downloadyoutubeplaylistmp3")
async def download_youtube_playlist_tagged_mp3(url: str, folder_name=None, artist=None, album=None, album_artist=None, cover_url=None):
    try:

        # Make Playlist object
        yt_playlist = Playlist(url)

        # Make playlist folder
        playlist_title = folder_name if folder_name != None else yt_playlist.title
        path = os.path.join(f"{os.getcwd()}", f"{playlist_title}")
        os.mkdir(path)

        # Download each video and move to folder
        track_num = 0
        for yt_video in yt_playlist.videos:

            # download video
            mp4_audio_stream = yt_video.streams.get_highest_resolution()
            mp4_title = mp4_audio_stream.title
            mp4_audio_stream.download()

            # renames video file
            file = glob.glob(f"{os.getcwd()}/**/*.mp4", recursive = True)
            os.rename(file[0], f"{os.getcwd()}/video.mp4")

            # convert mp4 to mp3
            mp4_audio = mp.VideoFileClip("video.mp4")
            song_file = mp4_title.lower().replace(' ', '')
            mp4_audio.audio.write_audiofile(f"{song_file}.mp3")

            # Deletes mp4 video from folder
            os.remove("video.mp4")

            # Adds artist, album, album artist, song title, & track number 
            # metadata to mp3 file using eyed3 API
            mp3_file = eyed3.load(f"{song_file}.mp3")
            mp3_file.tag.artist = artist
            mp3_file.tag.album = album if album != None else playlist_title
            mp3_file.tag.album_artist = album_artist
            mp3_file.tag.title = mp4_title
            mp3_file.tag.track_num = track_num + 1
            mp3_file.tag.save()

            # Tags image to mp3 metadata from URL
            if cover_url != None:
                cover = requests.get(cover_url)
                mp3_file.tag.images.set(3, cover.content , "image/jpeg" ,u"Cover")
                mp3_file.tag.save()
            else:
                cover_url = yt_video.thumbnail_url
                cover = requests.get(cover_url)
                mp3_file.tag.images.set(3, cover.content , "image/jpeg" ,u"Cover")
                mp3_file.tag.save()

            # move song to folder
            os.rename(f"{os.getcwd()}/{song_file}.mp3", f"{os.getcwd()}/{playlist_title}/{song_file}.mp3")

        # Moves folder to downloads
        downloads_path = str(Path.home() / "Downloads")        
        os.rename(f"{os.getcwd()}/{playlist_title}", f"{downloads_path}/{playlist_title}")

        # Success message
        return {"message": f"{playlist_title} folder downloaded successfully to downloads folder!"}
    
    except KeyError:
        raise HTTPException(status_code=400, detail="Error: Video is not available or cannot be downloaded")
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: Invalid URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error downloading video: " + str(e))
    

# Youtube to MP4 Request
@app.get("/downloadyoutubevideomp4")
async def download_youtube_video_mp4(url: str, file_name=None):
    try:

        # Downloades mp4 of Youtube Video to 
        # musictagger folder using pytube API
        yt_video = YouTube(url)
        mp4_audio_stream = yt_video.streams.get_highest_resolution()
        mp4_title = mp4_audio_stream.title
        mp4_audio_stream.download()

        # renames video file
        file = glob.glob(f"{os.getcwd()}/**/*.mp4", recursive = True)
        os.rename(file[0], f"{os.getcwd()}/video.mp4")

        if file_name == None:
            file_name = mp4_title

        # Moves file to downloads folder
        downloads_path = str(Path.home() / "Downloads")        
        os.rename(f"{os.getcwd()}/video.mp4", f"{downloads_path}/{file_name}.mp4")

        # Success message
        return {"message": f"{file_name}.mp4 downloaded successfully to downloads folder!"}
    
    except KeyError:
        raise HTTPException(status_code=400, detail="Error: Video is not available or cannot be downloaded")
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: Invalid URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error downloading video: " + str(e))
    
# Youtube Playlist to MP4 Request
@app.get("/downloadyoutubeplaylistmp4")
async def download_youtube_playlist_mp4(url: str, folder_name=None):
    try:

        # Make Playlist object
        yt_playlist = Playlist(url)

        # Make playlist folder
        playlist_title = folder_name if folder_name != None else yt_playlist.title
        path = os.path.join(f"{os.getcwd()}", f"{playlist_title}")
        os.mkdir(path)

        # Download each video and move to folder
        for yt_video in yt_playlist.videos:
            # download video
            mp4_audio_stream = yt_video.streams.get_highest_resolution()
            mp4_title = mp4_audio_stream.title
            mp4_audio_stream.download()
            # renames video file
            file = glob.glob(f"{os.getcwd()}/**/*.mp4", recursive = True)
            os.rename(file[0], f"{os.getcwd()}/video.mp4")
            # move video to folder
            os.rename(f"{os.getcwd()}/video.mp4", f"{os.getcwd()}/{playlist_title}/{mp4_title}.mp4")

        # Moves folder to downloads
        downloads_path = str(Path.home() / "Downloads")        
        os.rename(f"{os.getcwd()}/{playlist_title}", f"{downloads_path}/{playlist_title}")

        # Success message
        return {"message": f"{playlist_title} folder downloaded successfully to downloads folder!"}
    
    except KeyError:
        raise HTTPException(status_code=400, detail="Error: Video is not available or cannot be downloaded")
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: Invalid URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error downloading video: " + str(e))
    
# Youtube Thumbnail Request
@app.get("/downloadyoutubethumbnail")
async def download_youtube_thumbnail(url: str, file_name=None):
    try:

        # Downloades mp4 of Youtube Video to 
        # musictagger folder using pytube API
        yt_video = Playlist(url)
        thumbnail_url = yt_video.thumbnail_url

        # Download thumbnail to current directory
        if file_name == None:
            mp4_stream = yt_video.streams.get_highest_resolution()
            file_name = mp4_stream.title
        urllib.request.urlretrieve(thumbnail_url, f"{file_name}.jpg")

        # Moves file to downloads folder
        downloads_path = str(Path.home() / "Downloads")        
        os.rename(f"{os.getcwd()}/{file_name}.jpg", f"{downloads_path}/{file_name}.jpg")

        # Success message
        return {"message": f"{file_name}.jpg downloaded successfully to downloads folder!"}
    
    except KeyError:
        raise HTTPException(status_code=400, detail="Error: Video is not available or cannot be downloaded")
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: Invalid URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error downloading video: " + str(e))

# Untagged MP3 to Tagged MP3 Request
@app.get("/mp3tagger")
async def tag_song_from_downloads(file_name: str, song_title=None, artist=None, album=None, album_artist=None, track_num=None, cover_url=None):
    try:

        downloads_path = str(Path.home() / "Downloads")
        os.rename(f"{downloads_path}/{file_name}.mp3", f"{os.getcwd()}/{file_name}.mp3")

        # Adds artist, album, album artist, song title, & track number 
        # metadata to mp3 file using eyed3 API
        mp3_file = eyed3.load(f"{file_name}.mp3")
        mp3_file.tag.artist = artist
        mp3_file.tag.album = album
        mp3_file.tag.album_artist = album_artist
        mp3_file.tag.title = song_title
        mp3_file.tag.track_num = track_num
        mp3_file.tag.save()

        # Tags image to mp3 metadata from URL
        if cover_url != None:
            cover = requests.get(cover_url)
            mp3_file.tag.images.set(3, cover.content , "image/jpeg" ,u"Cover")
            mp3_file.tag.save()

        # Moves file to downloads folder
        downloads_path = str(Path.home() / "Downloads")        
        os.rename(f"{os.getcwd()}/{file_name}.mp3", f"{downloads_path}/{file_name}.mp3")

        # message
        return {"message": f"{song_title} downloaded successfully!"}
    except KeyError:
        raise HTTPException(status_code=400, detail="Error: Video is not available or cannot be downloaded")
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: Invalid URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error downloading video: " + str(e))
    