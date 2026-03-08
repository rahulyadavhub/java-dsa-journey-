import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import sys
import datetime
import wikipedia
import pyjokes
import platform
import shlex

WAKE_WORD = "k2jac"

class K2JacAssistant:

    def __init__(self):

        # Text-to-speech setup
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 155)

        # Speech recognition setup
        self.recognizer = sr.Recognizer()
        self.mic = None

        # Detect microphones
        try:
            mic_names = sr.Microphone.list_microphone_names()
            print("[k2jac] Available microphones:", mic_names)

            mic_index = None
            for i, name in enumerate(mic_names):
                if "smart sound" in name.lower() or "microphone" in name.lower():
                    mic_index = i
                    break

            if mic_index is not None:
                self.mic = sr.Microphone(device_index=mic_index)
                print(f"[k2jac] Using microphone: {mic_names[mic_index]}")
            else:
                self.mic = sr.Microphone()
                print("[k2jac] Using default microphone")

        except Exception as e:
            print(f"[k2jac] Microphone not found ({e})")
            self.mic = None

        wikipedia.set_lang("en")

    # Speak
    def speak(self, text):
        print(f"k2jac: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    # Listen
    def listen(self, timeout=10, phrase_time_limit=10):

        if not self.mic:
            return None

        try:
            with self.mic as source:

                print("Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

                print("Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

                print("Recognizing...")
                text = self.recognizer.recognize_google(audio)

                print("You said:", text)
                return text.lower()

        except sr.WaitTimeoutError:
            print("[k2jac] Timeout")
            return None

        except sr.UnknownValueError:
            print("[k2jac] Could not understand")
            return None

        except sr.RequestError as e:
            print("[k2jac] API error:", e)
            return None

    def input_text(self):
        return input("You: ").strip().lower()

    # Tell time
    def tell_time(self):
        now = datetime.datetime.now()
        self.speak(now.strftime("Time is %I:%M %p"))

    # Open website
    def open_website(self, site):

        if not site.startswith("http"):
            if "." not in site:
                site += ".com"
            site = "https://" + site

        webbrowser.open(site)
        self.speak(f"Opening {site}")

    # Google search
    def search_web(self, query):

        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

        self.speak(f"Searching {query}")

    # Wikipedia
    def wiki_summary(self, topic):

        try:
            summary = wikipedia.summary(topic, sentences=2)
            self.speak(summary)

        except:
            self.speak("No Wikipedia result found")

    # Joke
    def tell_joke(self):

        joke = pyjokes.get_joke()
        self.speak(joke)

    # Open app
    def open_app(self, command):

        try:
            if platform.system() == "Windows":
                subprocess.Popen(shlex.split(command), shell=True)
            else:
                subprocess.Popen(shlex.split(command))

            self.speak(f"Opening {command}")

        except Exception as e:
            self.speak(f"Cannot open {command}")

    # Handle command
    def handle(self, command):

        if not command:
            return

        if WAKE_WORD in command:
            command = command.replace(WAKE_WORD, "").strip()

        if "time" in command:

            self.tell_time()

        elif "open website" in command:

            site = command.split("open website")[-1].strip()
            self.open_website(site)

        elif command.startswith("open ") and "." in command:

            site = command.split("open ")[-1].strip()
            self.open_website(site)

        elif "search" in command:

            query = command.split("search")[-1].strip()
            self.search_web(query)

        elif "wikipedia" in command:

            topic = command.split("wikipedia")[-1].strip()
            self.wiki_summary(topic)

        elif "joke" in command:

            self.tell_joke()

        elif "exit" in command or "quit" in command:

            self.speak("Goodbye")
            sys.exit()

        else:

            self.speak("I did not understand")

    # Run assistant
    def run(self):

        if self.mic:
            self.speak("Hello I am k2jac. Say k2jac before your command.")
        else:
            self.speak("Microphone not available. Please type commands.")

        while True:

            if self.mic:

                text = self.listen()

                if not text:
                    text = self.input_text()

            else:
                text = self.input_text()

            self.handle(text)


if __name__ == "__main__":

    assistant = K2JacAssistant()
    assistant.run()