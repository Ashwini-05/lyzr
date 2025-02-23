import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, cast

from llama_index.readers.base import BaseReader
from llama_index.schema import Document


class LyzrMarkdownReader(BaseReader):
    def __init__(
        self,
        *args: Any,
        remove_hyperlinks: bool = True,
        remove_images: bool = True,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._remove_hyperlinks = remove_hyperlinks
        self._remove_images = remove_images

    def markdown_to_tups(self, markdown_text: str) -> List[Tuple[Optional[str], str]]:
        markdown_tups: List[Tuple[Optional[str], str]] = []
        lines = markdown_text.split("\n")

        current_header = None
        current_text = ""

        for line in lines:
            header_match = re.match(r"^#+\s", line)
            if header_match:
                if current_header is not None:
                    if current_text == "" or None:
                        continue
                    markdown_tups.append((current_header, current_text))

                current_header = line
                current_text = ""
            else:
                current_text += line + "\n"
        markdown_tups.append((current_header, current_text))

        if current_header is not None:
            markdown_tups = [
                (re.sub(r"#", "", cast(str, key)).strip(), re.sub(r"<.*?>", "", value))
                for key, value in markdown_tups
            ]
        else:
            markdown_tups = [
                (key, re.sub("<.*?>", "", value)) for key, value in markdown_tups
            ]

        return markdown_tups

    def remove_images(self, content: str) -> str:
        pattern = r"!{1}\[\[(.*)\]\]"
        content = re.sub(pattern, "", content)
        return content

    def remove_hyperlinks(self, content: str) -> str:
        pattern = r"\[(.*?)\]\((.*?)\)"
        content = re.sub(pattern, r"\1", content)
        return content

    def parse_tups(
        self, filepath: Path, content: Optional[str] = None, errors: str = "ignore"
    ) -> List[Tuple[Optional[str], str]]:
        if content is None:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
        if self._remove_hyperlinks:
            content = self.remove_hyperlinks(content)
        if self._remove_images:
            content = self.remove_images(content)
        markdown_tups = self.markdown_to_tups(content)
        return markdown_tups

    def load_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        content: Optional[str] = None,
    ) -> List[Document]:
        tups = self.parse_tups(file, content=content)
        results = []

        for header, value in tups:
            doc_id = (
                f"{str(file)}_{header.replace(' ', '_')}"
                if header
                else str(uuid.uuid4())
            )

            results.append(
                Document(
                    id_=doc_id,
                    text=f"\n\n{header}\n{value}" if header else value,
                    metadata=extra_info or {},
                )
            )

        return results
