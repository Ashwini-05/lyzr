import os
import stat
import hashlib
import logging
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from llama_index.schema import Document

from lyzr.utils.markdown_reader import LyzrMarkdownReader

logger = logging.getLogger(__name__)


class LyzrGithubReader(LyzrMarkdownReader):
    def __init__(self, *args, read_as_single_doc: bool = False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.read_as_single_doc = read_as_single_doc

    def load_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        content: Optional[str] = None,
    ) -> List[Document]:
        if extra_info is None:
            extra_info = {}

        relative_file_path = str(file)
        extra_info["original_file_path"] = relative_file_path
        extra_info["md5_hash"] = get_md5(file)

        if self.read_as_single_doc:
            with open(file, encoding="utf-8") as f:
                content = f.read()
            if self._remove_hyperlinks:
                content = self.remove_hyperlinks(content)
            if self._remove_images:
                content = self.remove_images(content)
            doc_id = relative_file_path

            return [Document(id_=doc_id, text=content, metadata=extra_info)]
        else:
            return super().load_data(file, extra_info, content)


def clone_or_pull_repository(git_url: str, local_path: Path) -> None:
    try:
        from git import InvalidGitRepositoryError, Repo
    except ImportError:
        logger.error(
            'GitPython is not installed. Please "pip install gitpython==3.1.37" to use this feature.'
        )
        raise

    if local_path.exists():
        try:
            repo = Repo(str(local_path))
            repo.remotes.origin.pull()
        except InvalidGitRepositoryError:
            Repo.clone_from(git_url, str(local_path))
    else:
        Repo.clone_from(git_url, str(local_path))


def get_md5(file_path: Path) -> str:
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def on_rm_error(func: Callable, path: str, exc_info: Tuple):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)
