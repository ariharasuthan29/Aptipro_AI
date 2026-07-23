from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from exam.models import Category, Question
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds initial aptitude categories, 40+ MCQs, and default superuser.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding Online Exam System database..."))

        # Create Admin User
        admin_user, created = User.objects.get_or_create(username='admin')
        if created:
            admin_user.set_password('admin123')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created superuser 'admin' with password 'admin123'."))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' already exists."))

        # Categories list
        categories_data = [
            ("Quantitative Aptitude", "bi-calculator", "Mathematical, numerical, and problem-solving aptitude questions."),
            ("Logical Reasoning", "bi-diagram-3", "Deductive logic, series completion, and pattern recognition."),
            ("Verbal Ability", "bi-chat-text", "English grammar, vocabulary, comprehension, and sentence structuring."),
            ("Data Interpretation", "bi-bar-chart-line", "Charts, tables, graphs analysis and numerical interpretation."),
            ("Analytical Reasoning", "bi-cpu", "Complex puzzle solving, data relationships, and critical evaluation."),
            ("Programming Fundamentals", "bi-code-slash", "C/C++, Java, Python fundamentals, data structures, and output prediction."),
            ("Coding and Decoding", "bi-hash", "Coding, decoding, and ciphering aptitude questions."),
            ("Number System", "bi-sort-numeric-down", "Numbers, divisibility, prime numbers, and numerical series."),
            ("Percentage, Profit and Loss", "bi-percent", "Percentage, profit, loss, discount, and finance aptitude."),
            ("Time and Work", "bi-calendar-range", "Time, work, rate, and group efficiency problem solving."),
            ("Time, Speed and Distance", "bi-speedometer", "Train, speed, distance, and relative motion questions."),
            ("Clocks and Calendars", "bi-clock", "Clock angles, calendar dates, and leap year calculations."),
            ("Puzzles", "bi-puzzle", "Logical puzzles, seating arrangements, and riddle questions."),
            ("Placement Mock Tests", "bi-file-earmark-check", "Comprehensive placement mock tests and company-specific preparation.")
        ]

        cat_objs = {}
        for name, icon, desc in categories_data:
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name), 'icon': icon, 'description': desc}
            )
            cat_objs[name] = cat

        questions_seed = [
            # Quantitative Aptitude
            {
                "category": cat_objs["Quantitative Aptitude"],
                "difficulty": Question.EASY,
                "question": "What is the average of the first 5 prime numbers?",
                "option_a": "5.2", "option_b": "5.6", "option_c": "6.0", "option_d": "6.2",
                "correct": "B",
                "explanation": "First 5 prime numbers are 2, 3, 5, 7, 11. Sum = 28. Average = 28 / 5 = 5.6."
            },
            {
                "category": cat_objs["Quantitative Aptitude"],
                "difficulty": Question.EASY,
                "question": "If 20% of a number is 120, then what is 120% of that number?",
                "option_a": "480", "option_b": "600", "option_c": "720", "option_d": "840",
                "correct": "C",
                "explanation": "Let the number be x. 0.20 * x = 120 => x = 600. 120% of 600 = 1.20 * 600 = 720."
            },
            {
                "category": cat_objs["Quantitative Aptitude"],
                "difficulty": Question.EASY,
                "question": "A train running at the speed of 60 km/hr crosses a pole in 9 seconds. What is the length of the train?",
                "option_a": "120 metres", "option_b": "150 metres", "option_c": "180 metres", "option_d": "324 metres",
                "correct": "B",
                "explanation": "Speed = 60 * (5/18) m/s = 50/3 m/s. Length = Speed * Time = (50/3) * 9 = 150 metres."
            },
            {
                "category": cat_objs["Quantitative Aptitude"],
                "difficulty": Question.MEDIUM,
                "question": "A and B can do a piece of work in 12 days, B and C in 15 days, C and A in 20 days. In how many days can A alone do it?",
                "option_a": "30 days", "option_b": "40 days", "option_c": "24 days", "option_d": "15 days",
                "correct": "A",
                "explanation": "2(A+B+C)'s 1 day work = (1/12 + 1/15 + 1/20) = 12/60 = 1/5. (A+B+C)'s 1 day work = 1/10. A's 1 day work = (1/10 - 1/15) = 1/30. Thus 30 days."
            },
            {
                "category": cat_objs["Quantitative Aptitude"],
                "difficulty": Question.MEDIUM,
                "question": "Find the compound interest on Rs. 10,000 at 10% per annum for 2 years compounded annually.",
                "option_a": "Rs. 2,000", "option_b": "Rs. 2,100", "option_c": "Rs. 2,200", "option_d": "Rs. 12,100",
                "correct": "B",
                "explanation": "Amount = 10000 * (1.10)^2 = 12100. CI = 12100 - 10000 = 2100."
            },
            {
                "category": cat_objs["Quantitative Aptitude"],
                "difficulty": Question.HARD,
                "question": "In how many different ways can the letters of the word 'LEADING' be arranged such that the vowels always come together?",
                "option_a": "360", "option_b": "480", "option_c": "720", "option_d": "5040",
                "correct": "C",
                "explanation": "Vowels (E, A, I) group as 1 unit + 4 consonants = 5 units. Arrange 5 units in 5! = 120 ways. Vowels arrange in 3! = 6 ways. Total = 120 * 6 = 720 ways."
            },

            # Logical Reasoning
            {
                "category": cat_objs["Logical Reasoning"],
                "difficulty": Question.EASY,
                "question": "Look at this series: 2, 1, (1/2), (1/4), ... What number should come next?",
                "option_a": "(1/3)", "option_b": "(1/8)", "option_c": "(2/8)", "option_d": "(1/16)",
                "correct": "B",
                "explanation": "This is a simple division series. Each number is half of the previous number."
            },
            {
                "category": cat_objs["Logical Reasoning"],
                "difficulty": Question.EASY,
                "question": "SCA, TVB, UWC, VXD, ______?",
                "option_a": "WYE", "option_b": "VYE", "option_c": "YZE", "option_d": "WZD",
                "correct": "A",
                "explanation": "1st letter +1 (S->T->U->V->W), 2nd letter +1 (C->V... wait C,V,W,X,Y), 3rd letter +1 (A->B->C->D->E)."
            },
            {
                "category": cat_objs["Logical Reasoning"],
                "difficulty": Question.MEDIUM,
                "question": "Pointing to a photograph of a boy Suresh said, 'He is the son of the only son of my mother.' How is Suresh related to that boy?",
                "option_a": "Brother", "option_b": "Uncle", "option_c": "Cousin", "option_d": "Father",
                "correct": "D",
                "explanation": "Only son of Suresh's mother is Suresh himself. So the boy is Suresh's son."
            },
            {
                "category": cat_objs["Logical Reasoning"],
                "difficulty": Question.MEDIUM,
                "question": "If SOUTH-EAST becomes NORTH, NORTH-EAST becomes WEST and so on. What will WEST become?",
                "option_a": "SOUTH-EAST", "option_b": "NORTH-EAST", "option_c": "SOUTH-WEST", "option_d": "NORTH-WEST",
                "correct": "A",
                "explanation": "Direction rotates by 135 degrees anti-clockwise. West rotated 135 degrees anti-clockwise becomes South-East."
            },
            {
                "category": cat_objs["Logical Reasoning"],
                "difficulty": Question.HARD,
                "question": "Five girls are sitting on a bench to be photographed. Seema is to the left of Rani and to the right of Bindu. Mary is to the right of Rani. Reeta is between Rani and Mary. Who is sitting third from the left?",
                "option_a": "Bindu", "option_b": "Seema", "option_c": "Rani", "option_d": "Reeta",
                "correct": "C",
                "explanation": "Order from left to right: Bindu, Seema, Rani, Reeta, Mary. Third from left is Rani."
            },

            # Verbal Ability
            {
                "category": cat_objs["Verbal Ability"],
                "difficulty": Question.EASY,
                "question": "Choose the synonym for the word: 'CANDID'",
                "option_a": "Secretive", "option_b": "Frank", "option_c": "Dishonest", "option_d": "Shy",
                "correct": "B",
                "explanation": "'Candid' means truthful, straightforward, or frank."
            },
            {
                "category": cat_objs["Verbal Ability"],
                "difficulty": Question.EASY,
                "question": "Choose the correct antonym for: 'ENORMOUS'",
                "option_a": "Tiny", "option_b": "Huge", "option_c": "Vast", "option_d": "Grand",
                "correct": "A",
                "explanation": "Enormous means extremely large. Its opposite is tiny."
            },
            {
                "category": cat_objs["Verbal Ability"],
                "difficulty": Question.MEDIUM,
                "question": "Fill in the blank: The manager was impressed _______ his dedication and work ethic.",
                "option_a": "by", "option_b": "with", "option_c": "on", "option_d": "at",
                "correct": "B",
                "explanation": "The idiom 'impressed with' is standard when expressing admiration for qualities or work."
            },
            {
                "category": cat_objs["Verbal Ability"],
                "difficulty": Question.MEDIUM,
                "question": "Identify the error in sentence: 'Neither the teacher nor the students (A) / was present (B) / in the annual seminar (C) / yesterday (D).'",
                "option_a": "Part A", "option_b": "Part B", "option_c": "Part C", "option_d": "Part D",
                "correct": "B",
                "explanation": "With 'neither...nor', the verb agrees with the closer subject ('students'). Hence it should be 'were present'."
            },

            # Analytical Reasoning
            {
                "category": cat_objs["Analytical Reasoning"],
                "difficulty": Question.EASY,
                "question": "Statements: All bags are handles. All handles are clips. Conclusion I: All bags are clips. Conclusion II: All clips are handles.",
                "option_a": "Only I follows", "option_b": "Only II follows", "option_c": "Either I or II follows", "option_d": "Neither follows",
                "correct": "A",
                "explanation": "Bags -> Handles -> Clips. All bags are inside Clips (I follows). But not all clips are inside Handles (II does not follow)."
            },
            {
                "category": cat_objs["Analytical Reasoning"],
                "difficulty": Question.MEDIUM,
                "question": "A is the father of B. C is the sister of A. D is the mother of C. How is B related to D?",
                "option_a": "Grandson / Granddaughter", "option_b": "Daughter", "option_c": "Grandfather", "option_d": "Father",
                "correct": "A",
                "explanation": "A and C are children of D. B is the child of A. Therefore, B is the grandchild of D."
            },
            {
                "category": cat_objs["Analytical Reasoning"],
                "difficulty": Question.HARD,
                "question": "Six people P, Q, R, S, T, U are standing in a circle. P is between S and T. Q is between U and R. S is to the immediate left of R. Who is to the immediate right of P?",
                "option_a": "S", "option_b": "T", "option_c": "U", "option_d": "R",
                "correct": "B",
                "explanation": "Arrangement in clockwise order: S, P, T, U, Q, R. S is left of P, T is right of P."
            },

            # Data Interpretation
            {
                "category": cat_objs["Data Interpretation"],
                "difficulty": Question.EASY,
                "question": "If Company X produced 500 units in 2021 and 650 units in 2022, what is the percentage increase in production?",
                "option_a": "20%", "option_b": "25%", "option_c": "30%", "option_d": "35%",
                "correct": "C",
                "explanation": "Increase = 150. Percentage increase = (150 / 500) * 100 = 30%."
            },
            {
                "category": cat_objs["Data Interpretation"],
                "difficulty": Question.MEDIUM,
                "question": "A pie chart shows expenditure: Food 40%, Rent 25%, Education 15%, Savings 20%. If total income is $4,000, how much is saved?",
                "option_a": "$600", "option_b": "$800", "option_c": "$1,000", "option_d": "$1,600",
                "correct": "B",
                "explanation": "Savings = 20% of $4,000 = 0.20 * 4000 = $800."
            },

            # Programming Fundamentals
            {
                "category": cat_objs["Programming Fundamentals"],
                "difficulty": Question.EASY,
                "question": "What is the output of `print(type([]) is list)` in Python?",
                "option_a": "True", "option_b": "False", "option_c": "Error", "option_d": "<class 'list'>",
                "correct": "A",
                "explanation": "`[]` creates an empty list. Its type is `list`, so `type([]) is list` evaluates to `True`."
            },
            {
                "category": cat_objs["Programming Fundamentals"],
                "difficulty": Question.MEDIUM,
                "question": "Which data structure operates on a Last In First Out (LIFO) basis?",
                "option_a": "Queue", "option_b": "Stack", "option_c": "Tree", "option_d": "Array",
                "correct": "B",
                "explanation": "Stack uses LIFO order (Last-In, First-Out)."
            },
            {
                "category": cat_objs["Programming Fundamentals"],
                "difficulty": Question.HARD,
                "question": "What is the worst-case time complexity of QuickSort?",
                "option_a": "O(N log N)", "option_b": "O(N)", "option_c": "O(N^2)", "option_d": "O(log N)",
                "correct": "C",
                "explanation": "When the pivot choice is poor (e.g. already sorted array with smallest/largest element as pivot), QuickSort degrades to O(N^2)."
            },

            # Placement Mock Tests
            {
                "category": cat_objs["Placement Mock Tests"],
                "difficulty": Question.EASY,
                "question": "In a 100m race, A beats B by 10m and B beats C by 10m. By how many meters does A beat C?",
                "option_a": "18m", "option_b": "19m", "option_c": "20m", "option_d": "21m",
                "correct": "B",
                "explanation": "When A covers 100m, B covers 90m. When B covers 100m, C covers 90m. When B covers 90m, C covers 81m. A beats C by 100 - 81 = 19m."
            },
            {
                "category": cat_objs["Placement Mock Tests"],
                "difficulty": Question.MEDIUM,
                "question": "A man sold two chairs at Rs. 1200 each. On one he gained 20% and on the other he lost 20%. His net gain or loss percentage is:",
                "option_a": "4% gain", "option_b": "4% loss", "option_c": "No profit no loss", "option_d": "2% loss",
                "correct": "B",
                "explanation": "When two items are sold at same price with same gain% and loss% x, there is always a loss = (x/10)^2 % = (20/10)^2 % = 4% loss."
            },
        ]

        # Generate extra pool of questions programmatically to reach 40+ total questions
        extra_q_templates = [
            ("Quantitative Aptitude", "Find the HCF of 36 and 84.", "6", "12", "18", "24", "B", "12 is the highest common factor of 36 and 84."),
            ("Quantitative Aptitude", "A car covers 300 km in 5 hours. What is its average speed in m/s?", "15.6 m/s", "16.67 m/s", "18 m/s", "20 m/s", "B", "Speed = 60 km/h = 60 * (5/18) = 16.67 m/s."),
            ("Quantitative Aptitude", "Simplify: 15^2 - 10^2", "125", "150", "175", "200", "A", "225 - 100 = 125."),
            ("Quantitative Aptitude", "What is 15% of 450?", "67.5", "65", "62.5", "70", "A", "0.15 * 450 = 67.5."),
            ("Quantitative Aptitude", "Ratio of boys to girls is 4:5. If total students are 45, how many girls are there?", "20", "25", "30", "15", "B", "Girls = (5/9) * 45 = 25."),

            ("Logical Reasoning", "If CAT is coded as 3120, how is DOG coded?", "4157", "4158", "4147", "3157", "A", "Alphabet positions: D=4, O=15, G=7 -> 4157."),
            ("Logical Reasoning", "Which number replaces the question mark? 5, 11, 23, 47, ?", "95", "96", "94", "92", "A", "Pattern: (x * 2) + 1. 47 * 2 + 1 = 95."),
            ("Logical Reasoning", "Clock shows 3:00. What is the angle between hour hand and minute hand?", "60 degrees", "90 degrees", "120 degrees", "180 degrees", "B", "3 hours * 30 deg/hour = 90 degrees."),
            ("Logical Reasoning", "Identify the odd one out: Apple, Mango, Carrot, Banana", "Apple", "Mango", "Carrot", "Banana", "C", "Carrot is a root vegetable, others are fruits."),

            ("Verbal Ability", "Select correct spelling:", "Accomodate", "Accommodate", "Acommodate", "Accommodat", "B", "The correct spelling is 'Accommodate' with double c and double m."),
            ("Verbal Ability", "A person who collects stamps is called a:", "Philatelist", "Numismatist", "Anthropologist", "Curator", "A", "A stamp collector is a philatelist."),
            ("Verbal Ability", "Choose sentence with correct punctuation:", "It's a fine day.", "Its a fine day.", "It's a fine day", "Its' a fine day.", "A", "It's is contraction for It is."),

            ("Analytical Reasoning", "Statements: Some actors are singers. All singers are dancers. Conclusion: Some actors are dancers.", "True", "False", "Cannot determine", "Invalid statement", "A", "Actors overlap Singers which are inside Dancers. Thus Some Actors are Dancers."),
            ("Analytical Reasoning", "If A is taller than B, B is taller than C, who is the shortest?", "A", "B", "C", "Cannot say", "C", "Order of height: A > B > C. C is shortest."),

            ("Data Interpretation", "If a graph shows monthly sales: Jan(100), Feb(150), Mar(200). What is total sales?", "400", "450", "500", "350", "B", "100 + 150 + 200 = 450."),
            ("Programming Fundamentals", "Which keyword is used to define a function in Python?", "func", "def", "function", "lambda", "B", "`def` keyword defines functions in Python."),
            ("Programming Fundamentals", "Which of the following is an immutable data type in Python?", "List", "Dictionary", "Tuple", "Set", "C", "Tuples cannot be changed once created (immutable)."),
            ("Placement Mock Tests", "What is the probability of getting a head on tossing an unbiased coin?", "1/4", "1/2", "3/4", "1", "B", "2 outcomes (H, T), 1 favorable outcome -> 1/2.")
        ]

        diff_cycle = [Question.EASY, Question.MEDIUM, Question.HARD]
        for idx, item in enumerate(extra_q_templates):
            cat_name, q_txt, op_a, op_b, op_c, op_d, corr, exp = item
            diff = diff_cycle[idx % len(diff_cycle)]
            questions_seed.append({
                "category": cat_objs[cat_name],
                "difficulty": diff,
                "question": q_txt,
                "option_a": op_a, "option_b": op_b, "option_c": op_c, "option_d": op_d,
                "correct": corr,
                "explanation": exp
            })

        # Save all questions
        count = 0
        for q in questions_seed:
            Question.objects.get_or_create(
                category=q["category"],
                question_text=q["question"],
                defaults={
                    "difficulty": q["difficulty"],
                    "option_a": q["option_a"],
                    "option_b": q["option_b"],
                    "option_c": q["option_c"],
                    "option_d": q["option_d"],
                    "correct_option": q["correct"],
                    "explanation": q["explanation"]
                }
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} aptitude questions into the database!"))
