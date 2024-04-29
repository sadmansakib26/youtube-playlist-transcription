from pytube import YouTube, Playlist
import whisper
import os

out_dir = "Transcripts" #output .txt file save location

if not os.path.exists(out_dir):
    os.makedirs(out_dir) #craete if it doesn't exist

def transcribe_playlist(playlist_url: str, 
                        multiple_file_output: bool,
                         delete_files: bool, 
                         model_name: str):
    
    """
    Transcribes a YouTube playlist using the OpenAI Whisper ASR model.

    This function downloads each video in the playlist, extracts the audio, and transcribes it using the specified Whisper model.
    The transcriptions are saved to text files in the 'Transcripts' directory. If `multiple_file_output` is True, each video's transcription is saved to a separate file. Otherwise, all transcriptions are appended to a single file.
    If `delete_files` is True, the downloaded audio files are deleted after transcription.

    Args:
        playlist_url (str): The URL of the YouTube playlist to transcribe.
        multiple_file_output (bool): Whether to save each video's transcription to a separate file.
        delete_files (bool): Whether to delete the downloaded audio files after transcription.
        model_name (str): The name of the Whisper ASR model to use for transcription.

    Returns:
        str: A message indicating the result of the transcription process. If an error occurs, the message describes the error.
    """

    try:
        model = whisper.load_model(model_name) #load the model
    except Exception as e:
        return f"An error occurred while loading the model: {e}"
    
    try:
        playlist = Playlist(playlist_url)
    except Exception as e:
        return f"An error occurred while accessing the playlist: {e}"
    
    for video_url in playlist.video_urls:
        try:
            video = YouTube(video_url) #url of the video
            title = video.title #title of the video
            print(f"Downloading Video: {title}...")
            audio = video.streams.filter(only_audio=True)[-1].download() #download audio
            print('Download Complete, Transcribing...')
            result = model.transcribe(audio)['text'] #transcribe using whisper
            print('Transcription Complete')
            if delete_files:
                os.remove(audio) #delete the audio file
                print(f'Removed Video From Storage: {title}')
            if multiple_file_output:
                with open(os.path.join(out_dir, f"{title}.txt"), "w") as f:
                    f.write(result)
                    print(f'Output saved at {os.path.join(out_dir, f"{title}.txt")}')
            else:
                out_file = "Transcript.txt"
                with open(os.path.join(out_dir, out_file), "a") as f:
                        f.write(f"{title}\n\n{result}\n\n")
                        f.write("--"*50)
                        f.write("\n\n")
                        print(f'Output saved at {os.path.join(out_dir, out_file)}')
          
            print('--'*50)
        except Exception as e:
            return f"An error occurred while processing the video {title}: {e}"
    print('All Transcription Complete')

playlist_url = input("Enter the URL of the playlist: ")
multiple_file_output = input("Do you want to save the transcript in multiple files? (y/n): ").lower() == "y"
delete_files = input("Do you want to delete the audio files after the transcript is generated? (y/n): ").lower() == "y"
model_name = input("Select the model (tiny.en, small.en, medium.en, large.en etc.): ")

if __name__=="__main__":
  transcribe_playlist(playlist_url, 
                      multiple_file_output=multiple_file_output,
                        delete_files=delete_files, 
                        model_name=model_name)