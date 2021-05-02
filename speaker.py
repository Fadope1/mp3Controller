# system for speaking text or files
class speaker:

    def __init__(self, rate=100):
        import pyttsx3
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', "german")
        self.engine.setProperty('rate', rate)

    @staticmethod
    def parse_txt(input): # parses for german language
        # Needed for mathmatical operators like +, - etc.
        # e-speak can't speak those

        to_parse_chars = {"=": "ist gleich.", "*": "mal.", "/": "geteilt durch.", "+": "plus.", "-": "minus.", "1.": "Erstens.", "3.": "drittens."}

        # future proof :)
        for operator, text in to_parse_chars.items(): # replace operators with words
            if operator in input:
                input.replace(operator, text)

        txt_lst = list(input)

        for i, char in enumerate(txt_lst): # replace numbers with words: 1. -> 1tens -> erstens
            try:
                if char == ".":
                    number = int(txt_lst[i-1])
                    replace = f"{number}."
                    result = f"{number}tens"
                    input_replace(replace, result)
                # TODO: What about number with 2 digits (>=10.)
            except ValueError:
                pass

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
