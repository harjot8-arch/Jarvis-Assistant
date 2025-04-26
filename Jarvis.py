import pyttsx3
import speech_recognition as sr
import requests
import webbrowser
from datetime import datetime

# Initialize the speech engine
engine = pyttsx3.init()

# Function to make Jarvis speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user's command
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print("You said: " + command)  # Debug: show what was said
            return command.lower()  # Always return the command in lowercase for consistent comparison
        except Exception as e:
            print("Sorry, I didn't catch that.")  # Debug: output error message
            return None

# Function to wait for the name "Jarvis"
def wait_for_name():
    print("Listening for 'Jarvis'...")
    while True:
        command = listen()
        if command and "jarvis" in command:
            speak("Yes, how can I assist you?")
            return  # Start listening for other commands

# Function to get the current time
def get_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    return current_time

# Function to get the weather
def get_weather():
    api_key = "your_actual_weather_api_key"  # Replace with your actual API key
    city = "London"  # You can change the city or ask the user for it
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    # Send request to the API
    response = requests.get(url)
    
    # Print the status code and the response content for debugging
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)
    
    # Parse the response data
    weather_data = response.json()
    
    # Check if the response code is 200 (successful)
    if response.status_code == 200:
        main = weather_data["main"]
        weather = weather_data["weather"][0]["description"]
        temp = main["temp"]
        return f"The weather in {city} is {weather} with a temperature of {temp}°C."
    else:
        return f"Error fetching weather: {weather_data.get('message', 'Unknown error occurred.')}"
        
# Function to open websites
def open_website(website):
    webbrowser.open(website)

# Main interaction loop
def main():
    speak("Hello! I am Jarvis. Say my name to begin.")
    wait_for_name()  # Wait for "Jarvis"
    
    # After hearing "Jarvis", start listening for other commands
    while True:
        command = listen()

        if command is None:
            continue
        
        print(f"Debug: Command received - {command}")  # Debug print to show the command
        
        # Check if the user says "stop" to exit
        if "stop" in command:
            speak("Stopping. Goodbye!")  # Speak when "stop" is detected
            break  # Exit the loop and stop further listening
        
        # Commands after activation
        if "time" in command:
            speak(f"The current time is {get_time()}")
        
        elif "weather" in command:
            speak(get_weather())
        
        elif "open" in command:
            if "google" in command:
                speak("Opening Google")
                open_website("https://www.google.com")
            elif "youtube" in command:
                speak("Opening YouTube")
                open_website("https://www.youtube.com")
            elif "github" in command:
                speak("Opening GitHub")
                open_website("https://www.github.com")
        
        elif "exit" in command or "bye" in command:
            speak("Goodbye! Have a nice day.")
            break

if __name__ == "__main__":
    main()
