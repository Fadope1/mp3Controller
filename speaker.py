# system for speaking text or files
class speaker:

    def __init__(self, rate=100):
        import pyttsx3
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', "german")
        self.engine.setProperty('rate', rate)

    @staticmethod
    def parse_txt(input):
        # Needed for mathmatical operators like +, - etc.
        # e-speak can't speak those

        to_parse_chars = {"=": "geteilt durch.", "*": "mal.", "/": "geteilt.", "+": "plus.", "-": "minus."}

        # future proof :)
        for operator, text in to_parse_chars.items():
            if operator in input:
                input.replace(operator, text)

        # Not future proof:
        # input.replace("+", "plus.")
        # input.replace("-", "minus.") ...

        return input

    def speak_file(self, file):
        with open(file) as f:
            content = f.read()

            cleaned_content = self.parse_txt(content)

            self.speak(cleaned_content)

    def speak(self, txt):
        self.engine.say(txt)
        self.engine.runAndWait()
