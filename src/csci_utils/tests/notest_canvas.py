import os
from unittest import TestCase, mock
from dotenv import load_dotenv

from ..canvas.canvas import *

MOCK_ENV = {
    "CANVAS_TOKEN": "token",
    "CANVAS_COURSE_ID": "11",
    "CANVAS_ASSIGNMENT_ID": "22",
    "CANVAS_QUIZ_ID": "33",
    "CANVAS_URL": "url",
}

load_dotenv()

@mock.patch.dict(os.environ, MOCK_ENV)
class CanvasApiTests(TestCase):
    @mock.patch("..canvas.canvas ")
    @mock.patch.dict(os.environ, MOCK_ENV)
    def test_canvas_single_call(self, mock_canvas):
        """
        verify a single API call to canvas
        """
        canvas_client = login()

        print(canvas_client.__dict__)
        # calling properties
        canvas_client.client
        canvas_client.quiz
        canvas_client.assignment

        # validating that we only called the canvas client once
        mock_canvas.assert_called_once_with(
            MOCK_ENV.get("CANVAS_URL"), MOCK_ENV.get("CANVAS_TOKEN")
        )
        canvas_client.course.get_quiz.assert_called_once_with(
            int(MOCK_ENV.get("CANVAS_QUIZ_ID"))
        )
        canvas_client.course.get_assignment.assert_called_once_with(
            int(MOCK_ENV.get("CANVAS_ASSIGNMENT_ID"))
        )
    #
    # @mock.patch("pset_1.canvas.Canvas")
    # @mock.patch("pset_1.canvas.QuizSubmission")
    # def test_canvas_quiz_submission_calls(self, mock_canvas, mock_submission):
    #     """
    #     validate context manager method submission call
    #     """
    #     canvas_client = CanvasApi()
    #     with canvas_client.create_quiz_submission() as q:
    #         submission = q
    #         mock_submission.assert_called_once()
    #     submission.complete.assert_called_once()
    #
    # @mock.patch("pset_1.canvas.Canvas")
    # @mock.patch("pset_1.canvas.QuizSubmission")
    # def test_canvas_quiz_submission_calls_when_submission_fails(
    #     self, mock_canvas, mock_submission
    # ):
    #     """
    #     validate context manager method submission call when submission fails. should still close the file.
    #     """
    #     canvas_client = CanvasApi()
    #     with self.assertRaises(Exception) as e:
    #         with canvas_client.create_quiz_submission() as q:
    #             submission = q
    #             raise e
    #     submission.complete.assert_called_once()
    #
    # @mock.patch("pset_1.canvas.Canvas")
    # @mock.patch("pset_1.canvas.QuizSubmission")
    # def test_canvas_quiz_submission_calls(self, mock_canvas, mock_submission):
    #     """
    #     validate calls to QuizSubmission object with expected arguments
    #     """
    #     canvas_client = CanvasApi()
    #     canvas_client.get_submission_questions(mock_submission)
    #     mock_submission.get_submission_questions.assert_called_once()
    #
    #     answers = [{1: "answer"}]
    #     canvas_client.submit_quiz(mock_submission, answers)
    #
    #     mock_submission.answer_submission_questions.assert_called_once_with(
    #         quiz_questions=answers
    #     )
    #
    # @mock.patch("pset_1.canvas.Canvas")
    # def test_canvas_assignment_submission_calls(self, mock_canvas):
    #     """
    #     validate the calls when submitting an assignment
    #     """
    #     canvas_client = CanvasApi()
    #     submission_type = {"type": 1, 2: 3}
    #     submission_comment = {"comment": 3, 4: 5}
    #     canvas_client.submit_assignment(submission_type, submission_comment)
    #
    #     canvas_client.assignment.submit.assert_called_once_with(
    #         submission_type, comment=submission_comment
    #     )
