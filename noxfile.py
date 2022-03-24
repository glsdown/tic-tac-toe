import nox

nox.options.sessions = ["lint"]

PYTHON_SOURCES = ["."]


@nox.session
def lint(session):
    """
    Lint all python code
    """
    session.install("black", "flake8", "isort")
    session.run("black", "--check", *PYTHON_SOURCES)
    session.run("flake8", *PYTHON_SOURCES)
    session.run("isort", "--check", *PYTHON_SOURCES)


@nox.session(name="format")
def format_(session):
    """
    Format and sort all imports in python code
    """
    session.install("black", "isort")
    session.run("black", *PYTHON_SOURCES)
    session.run("isort", *PYTHON_SOURCES)
