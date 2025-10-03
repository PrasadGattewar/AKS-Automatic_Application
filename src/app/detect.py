"""File type detection utilities.

Primary detection uses file extension mapping.
Secondary (optional) detection uses magic bytes heuristics for a few common types.
"""
from __future__ import annotations
from pathlib import Path
from typing import Tuple
import filetype

# Map common extensions to human-friendly document type names
EXTENSION_MAP = {
    # Text / code
    '.txt': 'Text Document',
    '.md': 'Markdown Document',
    '.rtf': 'Rich Text Format Document',
    '.csv': 'CSV (Comma-Separated Values)',
    '.log': 'Log File',

    # Office / productivity
    '.doc': 'Legacy Word Document (.doc)',
    '.docx': 'Word Document (.docx)',
    '.dotx': 'Word Template (.dotx)',
    '.ppt': 'Legacy PowerPoint Presentation (.ppt)',
    '.pptx': 'PowerPoint Presentation (.pptx)',
    '.ppsx': 'PowerPoint Slideshow (.ppsx)',
    '.xls': 'Legacy Excel Workbook (.xls)',
    '.xlsx': 'Excel Workbook (.xlsx)',
    '.xlsm': 'Excel Macro-Enabled Workbook (.xlsm)',
    '.ods': 'OpenDocument Spreadsheet (.ods)',
    '.odt': 'OpenDocument Text (.odt)',
    '.odp': 'OpenDocument Presentation (.odp)',
    '.pdf': 'PDF Document',

    # Archives
    '.zip': 'ZIP Archive',
    '.rar': 'RAR Archive',
    '.7z': '7-Zip Archive',
    '.tar': 'TAR Archive',
    '.gz': 'GZip Compressed File',

    # Images
    '.png': 'PNG Image',
    '.jpg': 'JPEG Image',
    '.jpeg': 'JPEG Image',
    '.gif': 'GIF Image',
    '.bmp': 'Bitmap Image',
    '.tiff': 'TIFF Image',
    '.webp': 'WebP Image',
    '.svg': 'SVG Vector Image',

    # Others
    '.json': 'JSON File',
    '.xml': 'XML File',
    '.yml': 'YAML File',
    '.yaml': 'YAML File',
    '.ini': 'INI Configuration File',
    '.cfg': 'Configuration File',
    '.exe': 'Windows Executable',
}


def detect_type(filename: str, file_bytes: bytes) -> Tuple[str, str]:
    """Return a tuple (display_type, method).

    display_type: human readable detected type
    method: description of how it was determined
    """
    path = Path(filename)
    ext = path.suffix.lower()

    # 1. Extension map
    if ext in EXTENSION_MAP:
        return EXTENSION_MAP[ext], f"extension match ({ext})"

    # 2. Try magic bytes via filetype library
    try:
        kind = filetype.guess(file_bytes)
        if kind:
            # Provide general category and mime
            return f"{kind.mime} (detected by signature)", f"magic bytes ({kind.extension})"
    except Exception:
        pass

    # 3. Simple heuristics for plain text if decodable
    try:
        file_bytes.decode('utf-8')
        return "Plain Text (UTF-8)", "heuristic text decode"
    except Exception:
        pass

    return "Unknown File Type", "no match"
