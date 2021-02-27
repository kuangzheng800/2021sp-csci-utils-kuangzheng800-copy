"""Utils for accessing and submitting to Canvas"""


from pprint import pprint
import json
import os
from typing import List, Dict

from canvasapi import Canvas
from canvasapi.quiz import QuizSubmissionQuestion, QuizSubmission
from git import Repo
from dotenv import load_dotenv


def login(masquerade = {}):
    '''use envrionmental variables to log on to canvas, return a Canvas object and prespecified masquerade'''
    load_dotenv()
    as_user_id = int(os.environ["CANVAS_AS_USER_ID"])  # Optional - for test student
    if as_user_id:
        masquerade['as_user_id'] = as_user_id
    canvas = Canvas(str(os.environ["CANVAS_URL"]), str(os.environ["CANVAS_TOKEN"]))
    return canvas

def courseNameToID(canvas, name, masquerade = {}, UUID = True):
    '''
    Look for registered class, return class ID by class name. Case insensitive
    Can return id or uuid specified by type
    '''
    name = name.lower().replace(' ','')
    for i in canvas.get_courses(**masquerade):
        if name in i.name.lower().replace(' ',''):
            print('Found course: %s'%(i.name))
            if UUID:
                return i.uuid
            else:
                return i.id
    print('No course found')
    return None


def getQuizByTitle(course, quiz_title, masquerade = {}):
    '''Look for quiz in a course by title, return course ID. Case insensitive'''
    quiz_title = quiz_title.lower().replace(' ', '')
    for quiz in course.get_quizzes(**masquerade):
        if quiz_title in quiz.title.lower().replace(' ',''):
            print('Found quiz: %s, quiz ID is %s'%(quiz.title, quiz.id))
            return quiz
    print('No quiz found')
    return None

def getAssignmentByTitle(course, assginment_title, masquerade = {}):
    '''Look for quiz in a course by title, return course ID. Case insensitive'''
    assginment_title = assginment_title.lower().replace(' ', '')
    found = {}
    for assignment in course.get_assignments(**masquerade):
        if assginment_title in assignment.name.lower().replace(' ',''):
            print('Found quiz: %s, quiz ID is %s'%(assignment.name, assignment.id))
            found[assignment.name] = assignment
    if found == {}:
        print('No quiz found')
    return found

def get_submission_comments(repo, qsubmission: QuizSubmission) -> Dict:
    """Get some info about this submission"""
    return dict(
        hexsha=repo.head.commit.hexsha[:8],
        submitted_from=repo.remotes.origin.url,
        dt=repo.head.commit.committed_datetime.isoformat(),
        branch=os.environ.get("TRAVIS_BRANCH", None),  # repo.active_branch.name,
        is_dirty=repo.is_dirty(),
        quiz_submission_id=qsubmission.id,
        quiz_attempt=qsubmission.attempt,
        travis_url=os.environ.get("TRAVIS_BUILD_WEB_URL", None),
    )

def submitQuiz(course, quizID, answers, masquerade = {}, printQuestions = False):
    '''submit quiz by quiz ID'''
    quiz = course.get_quiz(quizID,**masquerade)

    try:
        qsubmission = quiz.create_submission(**masquerade)
        questions = qsubmission.get_submission_questions(**masquerade)
        if printQuestions:
            for q in questions:
                print("{} - {}".format(q.question_name, q.question_text.split("\n", 1)[0]))

                # MC and some q's have 'answers' not 'answer'
                pprint(
                    {
                        k: getattr(q, k, None)
                        for k in ["question_type", "id", "answer", "answers"]
                    }
                )
                print()
        responses = qsubmission.answer_submission_questions(
            quiz_questions=answers, **masquerade
        )

    except Exception as e:
        print('Quiz submission error, no submission made! \n' + str(e))
        return

    finally:
        if qsubmission is not None:
            qsubmission.complete(**masquerade)
        pass


def submitAssignment(assignment, masquerade = {}, ALLOW_DIRTY = False):
    repo = Repo(".")

    if repo.is_dirty() and not ALLOW_DIRTY:
        raise RuntimeError(
            "Must submit from a clean working directory - commit your code and rerun"
        )

    url = "https://github.com/csci-e-29/{}/commit/{}".format(
        os.path.basename(repo.working_dir), repo.head.commit.hexsha
    )
    submission = assignment.submit(
        dict(
            submission_type="online_url",
            url=url,
        ),
        **masquerade,
    )
    print(submission)

# if __name__ == '__main__':
#     canvas = login()
#     course_ID = courseNameToID(canvas,'advanced python', UUID = False)
#     print(course_ID)
#     course = canvas.get_course(course_ID, type = 'ID')
#     quiz = getQuizByTitle(course, 'Pset 1')
#     print(quiz.id)
