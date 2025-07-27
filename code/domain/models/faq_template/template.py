def faqs_template(quiz_category):
    template = f"""
        Below is the {quiz_category} FAQ:
        Generate the quiz with 5 questions, in the below format. Try to randomize the questions
       
    
        Quiz:

        Q1: <Question 1 text>
        a. <Option 1 for Question 1>
        b. <Option 2 for Question 1>
        c. <Option 3 for Question 1>
        d. <Option 4 for Question 1>

        Correct Answer: <Correct option letter for Question 1>.

        Q2: <Question 2 text>
        a. <Option 1 for Question 2>
        b. <Option 2 for Question 2>
        c. <Option 3 for Question 2>
        d. <Option 4 for Question 2>

        Correct Answer: <Correct option letter for Question 2>.

        ... (Repeat the same format for all questions)
    
        Strickly follow the format above.
        """
    return template
