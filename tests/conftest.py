import pytest


@pytest.fixture
def sample_text():

    return """
    Retrieval Augmented Generation (RAG) combines
    information retrieval with language generation.

    It retrieves relevant documents from a knowledge
    base and provides them to a language model as context.
    """


@pytest.fixture
def sample_question():

    return "What is Retrieval Augmented Generation?"