import re

class QuizParser:
    @staticmethod
    def parse(text):
        questions = text.replace("\\n", "\n")
        question_blocks = re.split(r'\nQ\d+: ', questions)
        quiz = []
        for block in question_blocks[1:]:
            question_match = re.match(r'(.*?)(?=\na\.)', block, re.DOTALL)
            question = question_match.group(1).strip() if question_match else None

            options = re.findall(r'\n([a-d])\. (.*?)(?=\n[a-d]\.|[\n\r]+Correct Answer:|$)', block, re.DOTALL)
            option_texts = [opt[1].strip() for opt in options]

            correct_letter_match = re.search(r'Correct Answer:\s*([a-dA-D])\.', block)
            correct_letter = correct_letter_match.group(1).lower() if correct_letter_match else None

            correct_answer_index = None
            if correct_letter:
                for idx, (letter, _) in enumerate(options):
                    if letter.lower() == correct_letter:
                        correct_answer_index = idx
                        break

            if question and option_texts:
                quiz.append({
                    'question': question,
                    'options': option_texts,
                    'correct_answer_index': correct_answer_index
                })
        return quiz
