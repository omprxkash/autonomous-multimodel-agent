"""
Attachment metadata extraction and per-attachment risk summary.
Complements attachment_risk_detector.py — this module handles structured
metadata extraction, while the detector handles binary-level analysis.
"""
import hashlib
import os
from dataclasses import dataclass, field
from typing import Optional

# Extension categories
EXECUTABLE_EXTS = {".exe", ".msi", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".jar", ".com", ".scr", ".hta"}
SCRIPT_EXTS = {".sh", ".bash", ".py", ".rb", ".pl", ".php"}
MACRO_EXTS = {".docm", ".xlsm", ".pptm", ".dotm", ".xltm", ".potm"}
ARCHIVE_EXTS = {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"}


@dataclass
class AttachmentMetadata:
    filename: str
    content_type: str
    size_bytes: int
    sha256: str

    extension: str = ""
    has_executable: bool = False
    has_script: bool = False
    has_macro: bool = False
    is_archive: bool = False
    double_extension: bool = False
    risk_flags: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.extension = os.path.splitext(self.filename)[1].lower()
        self.has_executable = self.extension in EXECUTABLE_EXTS
        self.has_script = self.extension in SCRIPT_EXTS
        self.has_macro = self.extension in MACRO_EXTS
        self.is_archive = self.extension in ARCHIVE_EXTS

        # Double extension: e.g. "invoice.pdf.exe"
        stem = os.path.splitext(self.filename)[0]
        if os.path.splitext(stem)[1]:
            self.double_extension = True

        # Build risk flags
        if self.has_executable:
            self.risk_flags.append("executable_attachment")
        if self.has_script:
            self.risk_flags.append("script_attachment")
        if self.has_macro:
            self.risk_flags.append("macro_document")
        if self.is_archive:
            self.risk_flags.append("archive_attachment")
        if self.double_extension:
            self.risk_flags.append("double_extension")


def parse_attachment(raw: dict) -> AttachmentMetadata:
    """
    Build an AttachmentMetadata from a raw attachment dict produced by email_parser.
    Expected keys: filename, content_type, content (bytes).
    """
    content: bytes = raw.get("content", b"")
    sha256 = hashlib.sha256(content).hexdigest() if content else ""
    return AttachmentMetadata(
        filename=raw.get("filename", "unknown"),
        content_type=raw.get("content_type", "application/octet-stream"),
        size_bytes=len(content),
        sha256=sha256,
    )


def get_attachment_risk_summary(attachments: list[dict]) -> dict:
    """
    Aggregate risk flags across all attachments.
    Returns a summary dict compatible with the feature_builder.
    """
    metas = [parse_attachment(a) for a in attachments]

    return {
        "has_executable": any(m.has_executable for m in metas),
        "has_script": any(m.has_script for m in metas),
        "has_macro": any(m.has_macro for m in metas),
        "is_archive": any(m.is_archive for m in metas),
        "double_extension": any(m.double_extension for m in metas),
        "attachment_count": len(metas),
        "total_size_bytes": sum(m.size_bytes for m in metas),
        "attachments": [
            {
                "filename": m.filename,
                "sha256": m.sha256,
                "extension": m.extension,
                "risk_flags": m.risk_flags,
            }
            for m in metas
        ],
    }
