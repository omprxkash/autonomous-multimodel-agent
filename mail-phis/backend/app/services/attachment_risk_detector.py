"""
Attachment Risk Detector
Analyzes attachment metadata for risky file types without executing any files.
"""
import os
from typing import List, Dict, Any

from app.core.security import EXECUTABLE_EXTENSIONS, MACRO_EXTENSIONS, ARCHIVE_EXTENSIONS


class AttachmentRiskResult:
    def __init__(self):
        self.attachment_count: int = 0
        self.has_executable: bool = False
        self.has_script: bool = False
        self.has_macro_document: bool = False
        self.has_archive: bool = False
        self.double_extension_detected: bool = False
        self.archive_with_executable: bool = False
        self.mime_mismatch_detected: bool = False
        self.rtlo_attack: bool = False
        self.risky_attachments: List[Dict[str, Any]] = []
        self.risk_score: float = 0.0


def analyze_attachments(attachments: List[Dict[str, Any]]) -> AttachmentRiskResult:
    """Analyze attachment metadata for risk indicators."""
    result = AttachmentRiskResult()
    result.attachment_count = len(attachments)

    if not attachments:
        return result

    for attachment in attachments:
        raw_filename = attachment.get("filename", "")
        filename = raw_filename.lower()
        content_type = attachment.get("content_type", "").lower()
        size = attachment.get("size", 0)

        risks = []

        # RTLO (Right-to-Left Override) attack — U+202E reverses filename display
        if "‮" in raw_filename or "‭" in raw_filename:
            result.rtlo_attack = True
            risks.append("rtlo_attack")

        _, ext = os.path.splitext(filename)

        if ext in EXECUTABLE_EXTENSIONS:
            result.has_executable = True
            risks.append("executable")

        if ext in [".js", ".vbs", ".ps1", ".bat", ".cmd", ".wsf"]:
            result.has_script = True
            risks.append("script")

        if ext in MACRO_EXTENSIONS:
            result.has_macro_document = True
            risks.append("macro_document")

        if ext in ARCHIVE_EXTENSIONS:
            result.has_archive = True
            risks.append("archive")

        # Double extension: e.g. document.pdf.exe
        name_without_ext = filename.rsplit(".", 1)[0] if "." in filename else filename
        if "." in name_without_ext and ext in EXECUTABLE_EXTENSIONS:
            result.double_extension_detected = True
            risks.append("double_extension")

        if _detect_mime_mismatch(ext, content_type):
            result.mime_mismatch_detected = True
            risks.append("mime_mismatch")

        if risks:
            result.risky_attachments.append({
                "filename": raw_filename,
                "content_type": content_type,
                "size": size,
                "sha256": attachment.get("sha256", ""),
                "risks": risks,
                "is_executable": result.has_executable,
                "has_macros": result.has_macro_document,
                "double_extension": result.double_extension_detected,
            })

    risk_factors = [
        result.has_executable * 0.35,
        result.has_script * 0.25,
        result.has_macro_document * 0.2,
        result.double_extension_detected * 0.3,
        result.mime_mismatch_detected * 0.15,
        result.has_archive * 0.1,
        result.rtlo_attack * 0.4,
    ]
    result.risk_score = min(sum(risk_factors), 1.0)

    return result


def _detect_mime_mismatch(extension: str, content_type: str) -> bool:
    expected = {
        ".pdf": ["application/pdf"],
        ".doc": ["application/msword"],
        ".docx": ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
        ".xls": ["application/vnd.ms-excel"],
        ".xlsx": ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
        ".zip": ["application/zip", "application/x-zip-compressed"],
        ".exe": ["application/x-msdownload", "application/x-executable"],
        ".jpg": ["image/jpeg"],
        ".png": ["image/png"],
    }
    if extension in expected:
        return content_type not in expected[extension]
    return False
