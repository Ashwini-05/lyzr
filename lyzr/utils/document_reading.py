import shutil
import logging
from pathlib import Path
from typing import Callable, List, Sequence, Optional, Tuple

from llama_index.readers.file.base import SimpleDirectoryReader
from llama_index.schema import Document

from lyzr.utils.docx_reader import LyzrDocxReader
from lyzr.utils.pdf_reader import LyzrPDFReader
from lyzr.utils.txt_reader import LyzrTxtReader
from lyzr.utils.webpage_reader import LyzrWebPageReader
from lyzr.utils.website_reader import LyzrWebsiteReader
from lyzr.utils.youtube_reader import LyzrYoutubeReader
from lyzr.utils.github_reader import LyzrGithubReader, clone_or_pull_repository, on_rm_error

logger = logging.getLogger(__name__)


def read_pdf_as_documents(
    input_dir: Optional[str] = None,
    input_files: Optional[List] = None,
    exclude_hidden: bool = True,
    filename_as_id: bool = True,
    recursive: bool = True,
    required_exts: Optional[List[str]] = None,
    **kwargs,
) -> Sequence[Document]:
    file_extractor = {".pdf": LyzrPDFReader()}

    reader = SimpleDirectoryReader(
        input_dir=input_dir,
        exclude_hidden=exclude_hidden,
        file_extractor=file_extractor,
        input_files=input_files,
        filename_as_id=filename_as_id,
        recursive=recursive,
        required_exts=required_exts,
        **kwargs,
    )

    documents = reader.load_data()

    logger.info(f"Found {len(documents)} 'documents'.")
    return documents


def read_docx_as_documents(
    input_dir: Optional[str] = None,
    input_files: Optional[List] = None,
    exclude_hidden: bool = True,
    filename_as_id: bool = True,
    recursive: bool = True,
    required_exts: Optional[List[str]] = None,
    **kwargs,
) -> Sequence[Document]:
    file_extractor = {".docx": LyzrDocxReader()}

    reader = SimpleDirectoryReader(
        input_dir=input_dir,
        exclude_hidden=exclude_hidden,
        file_extractor=file_extractor,
        input_files=input_files,
        filename_as_id=filename_as_id,
        recursive=recursive,
        required_exts=required_exts,
        **kwargs,
    )

    documents = reader.load_data()

    logger.info(f"Found {len(documents)} 'documents'.")
    return documents


def read_txt_as_documents(
    input_dir: Optional[str] = None,
    input_files: Optional[List] = None,
    exclude_hidden: bool = True,
    filename_as_id: bool = True,
    recursive: bool = True,
    required_exts: Optional[List[str]] = None,
    **kwargs,
) -> Sequence[Document]:
    file_extractor = {".txt": LyzrTxtReader()}

    reader = SimpleDirectoryReader(
        input_dir=input_dir,
        exclude_hidden=exclude_hidden,
        file_extractor=file_extractor,
        input_files=input_files,
        filename_as_id=filename_as_id,
        recursive=recursive,
        required_exts=required_exts,
        **kwargs,
    )

    documents = reader.load_data()

    logger.info(f"Found {len(documents)} 'documents'.")
    return documents


def read_website_as_documents(url: str) -> List[Document]:
    reader = LyzrWebsiteReader()
    documents = reader.load_data(url)
    return documents


def read_webpage_as_documents(url: str) -> List[Document]:
    reader = LyzrWebPageReader()
    documents = reader.load_data(url)
    return documents


def read_youtube_as_documents(
    urls: List[str] = None,
) -> List[Document]:
    reader = LyzrYoutubeReader()
    documents = reader.load_data(urls)
    return documents


def read_github_repo_as_documents(
    git_repo_url: str,
    relative_folder_path: Optional[str] = None,
    required_exts: Optional[List[str]] = None,
) -> Sequence[Document]:
    temp_dir = Path("lyzr/temp/")
    temp_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Temporary directory created at {temp_dir}")

    try:
        clone_or_pull_repository(git_repo_url, temp_dir)

        docs_path = (
            temp_dir
            if relative_folder_path is None
            else (temp_dir / Path(relative_folder_path))
        )

        file_extractor = {".md": LyzrGithubReader(read_as_single_doc=True)}

        reader = SimpleDirectoryReader(
            file_extractor=file_extractor,
            input_dir=str(docs_path),
            required_exts=required_exts,
        )
        documents = reader.load_data()
        

        logger.info(f"Deleting temporary directory {temp_dir}..")
    finally:
        shutil.rmtree(temp_dir, onerror=on_rm_error)

    return documents
