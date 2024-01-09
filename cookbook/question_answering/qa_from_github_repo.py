from pprint import pprint

import openai

from lyzr import QABot

openai.api_key = "sk-" 

rag = QABot.github_repo_qa(
    git_repo_url="https://github.com/ultralytics/ultralytics.git",
    relative_folder_path="docs",
    llm_params={"model": "gpt-3.5-turbo"},
)

_query = "what is ultralytics?"

res = rag.query(_query)

pprint(res.response)
