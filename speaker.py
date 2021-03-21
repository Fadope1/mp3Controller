# system for speaking text or files
class speaker:
    # TODO: Add possibility to play mp3 file

    def __init(self, rate=100):
        import pyttsx3
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', "german")
        self.engine.setProperty('rate', rate)

    def speak_file(self, file):
        with open(file) as file:
            content = file.read()

            self.speak(content)

    def speak(self, txt):
        self.engine.say(txt)
        self.engine.runAndWait()
