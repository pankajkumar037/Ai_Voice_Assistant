## Agent for music

from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from prompts11.music_prompts import music_few_shot_examples
from langchain_google_genai import ChatGoogleGenerativeAI



music_player = None  # Global music player

# Initialize LLM for Music Query Processing
#google_api_key="AIzaSyAwMqy6yqO0czghcmiljDOw-cgrTELItEM"



# Few-shot examples for music queries



def refine_music_query(user_input,api_key):
    """
    Use LLM to extract or infer the music query from user input with enhanced accuracy.
    """
    few_shot_text = "\n".join([f"Input: {ex['input']} Query: {ex['query']}" for ex in music_few_shot_examples()])
    prompt = f"""
        You are a music query extraction assistant. Your task is to strictly extract the specific song name and language (if mentioned) 
        from the user's input. Follow these rules:

        1. Output only the song name or genre and the language (if specified).
        2. Do not include any additional interpretation, explanation, or context.
        3. If the input is unclear or ambiguous, return only the most relevant key terms directly related to the song or genre or print the user input directly if it is not clear.

        Here are examples:

        {few_shot_text}

        Input: {user_input}
        Query:
    """
    messages = [
        SystemMessage(content="You are a music query refinement assistant, specializing in accurate song identification."),
        HumanMessage(content=prompt)
    ]
    llm_music = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5, max_tokens=100, api_key=api_key) 
    response = llm_music.invoke(messages)
    refined_query = response.content.strip()
    print(f"[DEBUG] Refined Query: {refined_query}")
    return refined_query




import yt_dlp
import vlc
import os

# Correct VLC path
vlc_path = r"C:\Program Files\VideoLAN\VLC"  # Adjust according to your system

# Global music player
music_player = None

def fetch_and_play_music(query):
    """
    Searches for music on YouTube and streams it directly using VLC.
    """
    try:
        # Configure yt-dlp to extract the streaming URL
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(f"ytsearch:{query}", download=False)
            if not results or 'entries' not in results or not results['entries']:
                return "No results found for your query. Please try a different song."

            # Extract the first result
            result = results['entries'][0]
            video_title = result['title']
            video_url = result['url']

            # Stop any currently playing music
            stop_music()

            # Initialize VLC
            global music_player
            instance = vlc.Instance(f'--plugin-path={vlc_path}')
            media = instance.media_new(video_url)

            # Add headers for VLC to handle YouTube URLs
            media.add_option(
                ":http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            media.add_option(":http-referrer=https://www.youtube.com/")

            # Create media player
            music_player = instance.media_player_new()
            music_player.set_media(media)
            music_player.audio_set_volume(100)  # Set volume to 100%
            music_player.play()

            return f"Playing: {video_title}. Say 'Exit' or 'Quit' to stop the music."
    except Exception as e:
        return f"An error occurred while playing the song: {e}"


def stop_music():
    """
    Stops the currently playing music, if any.
    """
    global music_player
    if music_player:
        music_player.stop()
        music_player = None


def handle_play_music(user_input):
    """
    Handles user requests for music playback.
    """
    # Handle stop-related commands
    if user_input.lower().strip() in ["stop", "exit", "quit"]:
        stop_music()
        return "Music stopped."

    # Refine the query for playing music
    refined_query = user_input.strip()
    if not refined_query:
        return "I couldn't understand the song you want to play. Could you try rephrasing?"

    # Stop any currently playing music before starting a new one
    stop_music()

    # Fetch and play the song
    return fetch_and_play_music(refined_query)
