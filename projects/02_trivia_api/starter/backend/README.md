# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

- Python 3.8

### PIP Dependencies

- All the requirements in the `requirements.txt` file

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

The environment variables are stored in the `.env` file, so you can just run flask directly `flask run`.

## API Endpoints and Response Examples

- **GET** `/categories`, get all the categories.

  ```json
  {
    "categories": [
      {
        "id": 1,
        "type": "Science"
      },
      {
        "id": 2,
        "type": "Art"
      },
      {
        "id": 3,
        "type": "Geography"
      },
      {
        "id": 4,
        "type": "History"
      },
      {
        "id": 5,
        "type": "Entertainment"
      },
      {
        "id": 6,
        "type": "Sports"
      }
    ],
    "success": true
  }
  ```

- **GET** `/categories/<int:category_id>/questions`, get all questions of a single category

  ```json
  {
  "currentCategory": "Science",
  "questions": [
      {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
      },
      {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
      },
      {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
      }],
  "success": true,
  "totalQuestions": 3
  }
  ```

- **GET** `/questions`, get all questions along with categories

  ```json
  {
  "categories": [
  {
    "id": 1,
    "type": "Science"
  }...],
  "current_category": "Science",
  "questions": [
  {
    "answer": "Apollo 13",
    "category": 5,
    "difficulty": 4,
    "id": 2,
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  },
  {
    "answer": "Tom Cruise",
    "category": 5,
    "difficulty": 4,
    "id": 4,
    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  },
  {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  {
    "answer": "Edward Scissorhands",
    "category": 5,
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  ```

- **POST** `/questions`, create a question, takes a json body of (question, answer, category, difficulty) and returns the new record id

  ```json
  {
    "id": 37,
    "success": true
  }
  ```

- **POST** `/questions/search`, search with a keyword in the questions

  ```json
  {
    "currentCategory": "",
    "questions": [
      {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      },
      {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }
    ],
    "success": true,
    "totalQuestions": 2
  }
  ```

- **DELETE** `/questions/<int:question_id>`, delete a question by its id

  ```json
  {
    "success": true
  }
  ```

- **POST** `/quizzes`, takes a list `previous_questions` and a category then returns a random question that is unique in the current game session
  ```json
  {
    "question": {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    "success": true
  }
  ```

## Testing

- Automatically
  - Run `./runtest.sh` or `python test_flaskr.py`
- Manually, run the tests
  ```
  dropdb trivia_test
  createdb trivia_test
  psql trivia_test < trivia.psql
  python test_flaskr.py
  ```
