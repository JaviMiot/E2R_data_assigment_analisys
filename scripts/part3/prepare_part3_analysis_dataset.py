#!/usr/bin/env python3
"""Build an analysis-ready dataset from the raw Part III consolidated CSV."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import unicodedata
from pathlib import Path
from typing import Iterable, Optional
from langdetect import detect

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parent.parent.parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(ROOT_DIR / "logs/part3/part3_analysis_preparation.log", mode="w", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_INPUT_PATH = ROOT_DIR / "data/part3/part3_consolidated.csv"
DEFAULT_OUTPUT_PATH = ROOT_DIR / "data/part3/part3_analysis_ready.csv"
DEFAULT_TOOLS_LONG_PATH = ROOT_DIR / "data/part3/part3_tools_long.csv"
DEFAULT_REPORT_PATH = ROOT_DIR / "logs/part3/part3_analysis_preparation_report.txt"

RAW_TO_CANONICAL_COLUMNS = {
    "Group": "group_id",
    "Document Name": "document_name_raw",
    "Language": "language_raw",
    "Tool used for the adaptation": "tool_raw",
    "Original Text": "original_text_raw",
    "Proposal for E2R Text": "proposal_text_raw",
    "Comments": "comments_raw",
}

NULL_LIKE_VALUES = {"", "none", "nan", "null", "n/a", "na"}
LANGUAGE_CODE_MAP = {
    "en": "en",
    "english": "en",
    "es": "es",
    "spanish": "es",
}
LANGUAGE_LABEL_MAP = {
    "en": "English",
    "es": "Spanish",
    "unknown": "Unknown",
}

TOOL_PATTERNS = (
    (re.compile(r"\bchat\s*gpt(?:\d+(?:\.\d+)?)?|\bgpt[-\s]?\d+(?:\.\d+)?\b", re.IGNORECASE), "ChatGPT"),
    (re.compile(r"\bgemini(?:\d+(?:\.\d+)?)?\b", re.IGNORECASE), "Gemini"),
    (re.compile(r"\bclaude(?:\d+(?:\.\d+)?)?|\bcloude(?:\d+(?:\.\d+)?)?\b", re.IGNORECASE), "Claude"),
    (
        re.compile(r"\bfacile\b|facile-test\.linkeddata\.es", re.IGNORECASE),
        "FACILE",
    ),
    (
        re.compile(r"\bread\s*easy(?:\.ai)?\b|\breadeasy\.ai\b", re.IGNORECASE),
        "ReadEasy.ai",
    ),
    (
        re.compile(r"\bread\s*essay\s*ai\b", re.IGNORECASE),
        "ReadEasy.ai",
    ),
    (re.compile(r"\bperplexity\b", re.IGNORECASE), "Perplexity"),
)
TOOL_FAMILY_MAP = {
    "ChatGPT": "llm",
    "Gemini": "llm",
    "Claude": "llm",
    "Perplexity": "llm",
    "FACILE": "accessibility_tool",
    "ReadEasy.ai": "accessibility_tool",
}


def _to_nullable_string(value: object) -> pd._libs.missing.NAType | str:
    """Return a pandas nullable string preserving the original value."""
    if pd.isna(value):
        return pd.NA
    return str(value)


def normalize_text(value: object) -> pd._libs.missing.NAType | str:
    """Normalize a text field: lowercase, remove bullets/numbering, preserve structure."""
    if pd.isna(value):
        return pd.NA

    text = unicodedata.normalize("NFKC", str(value))
    text = text.replace("\u00a0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    lines = []
    for raw_line in text.split("\n"):
        # Remove noise: bullets (*, -, •), numeric lists (1., 1.1.), and letter lists (a), (1))
        # This regex looks for these patterns at the start of the line
        clean_line = re.sub(
            r"^[ \t]*([-*•◦]|(\d+(\.\d+)*[.)])|\([a-z0-9]+\)|[a-z][.)])[ \t]*", 
            "", 
            raw_line, 
            flags=re.IGNORECASE
        )
        
        # Remove extraction artifacts like long sequences of underscores or dots
        clean_line = re.sub(r"_{2,}| \.{3,}", " ", clean_line)
        
        # Remove page markers (e.g., Page 1 of 5)
        clean_line = re.sub(r"(?i)page\s+\d+\s+of\s+\d+", " ", clean_line)
        
        # Final whitespace cleanup
        clean_line = re.sub(r"[ \t]+", " ", clean_line).strip()
        
        if clean_line:
            lines.append(clean_line.lower())

    normalized = "\n".join(lines).strip()
    if normalized.lower() in NULL_LIKE_VALUES or not normalized:
        return pd.NA
    return normalized


def normalize_comments_json(value: object) -> pd._libs.missing.NAType | str:
    """Normalize text within a JSON comments structure."""
    if pd.isna(value) or not str(value).strip():
        return pd.NA
    
    try:
        # Check if it's actually JSON
        raw_str = str(value).strip()
        if not (raw_str.startswith("[") and raw_str.endswith("]")):
            return normalize_text(value)
            
        data = json.loads(raw_str)
        if not isinstance(data, list):
            return normalize_text(value)
        
        normalized_data = []
        for item in data:
            norm_item = {
                "orig": normalize_text(item.get("orig", "")),
                "prop": normalize_text(item.get("prop", "")),
                "comment": normalize_text(item.get("comment", ""))
            }
            # Keep as dict but clean up NAs to empty strings for JSON compatibility
            clean_item = {
                k: (v if not pd.isna(v) else "") 
                for k, v in norm_item.items()
            }
            if any(clean_item.values()):
                normalized_data.append(clean_item)
        
        if not normalized_data:
            return pd.NA
        return json.dumps(normalized_data, ensure_ascii=False)
    except Exception:
        # Fallback to generic normalization if JSON parsing fails
        return normalize_text(value)


def normalize_document_name(value: object) -> pd._libs.missing.NAType | str:
    """Normalize a document name while preserving its original casing."""
    text = normalize_text(value)
    if pd.isna(text):
        return pd.NA
    return re.sub(r"\s+", " ", str(text)).strip()


def fingerprint_text(value: object) -> pd._libs.missing.NAType | str:
    """Build a punctuation-insensitive fingerprint for fuzzy duplicate checks."""
    text = normalize_text(value)
    if pd.isna(text):
        return pd.NA

    fingerprint = re.sub(r"[^\w]+", "", str(text).casefold(), flags=re.UNICODE)
    if not fingerprint:
        return pd.NA
    return fingerprint


def normalize_language(value: object) -> tuple[str, str]:
    """Return canonical language code and label."""
    if pd.isna(value):
        return "unknown", "Unknown"

    normalized = normalize_text(value)
    if pd.isna(normalized):
        return "unknown", "Unknown"

    code = LANGUAGE_CODE_MAP.get(str(normalized).casefold(), "unknown")
    return code, LANGUAGE_LABEL_MAP[code]


def extract_tools(value: object) -> list[str]:
    """Extract ordered canonical tools from a raw tool description."""
    if pd.isna(value):
        return []

    raw_text = str(value)
    matches = []
    for pattern, canonical_name in TOOL_PATTERNS:
        match = pattern.search(raw_text)
        if match:
            if canonical_name == "Perplexity":
                matches.append((match.start(), "ChatGPT"))
                matches.append((match.start(), "Gemini"))
            else:
                matches.append((match.start(), canonical_name))

    ordered_names = []
    seen = set()
    for _, canonical_name in sorted(matches, key=lambda item: item[0]):
        if canonical_name not in seen:
            seen.add(canonical_name)
            ordered_names.append(canonical_name)

    return ordered_names


def derive_tool_family(tool_names: Iterable[str]) -> str:
    """Return the family for one or more canonical tools."""
    families = {
        TOOL_FAMILY_MAP.get(tool_name, "unknown")
        for tool_name in tool_names
        if tool_name
    }
    families.discard("unknown")

    if not families:
        return "llm"
    if len(families) > 1:
        return "hybrid"
    return next(iter(families))


def build_row_id(row: pd.Series) -> str:
    """Generate a stable row identifier from the raw analytical key."""
    raw_parts = [
        row["group_id"],
        row["document_name_raw"],
        row["language_raw"],
        row["tool_raw"],
        row["original_text_raw"],
        row["proposal_text_raw"],
        row["comments_raw"],
    ]
    raw_key = "||".join("" if pd.isna(part) else str(part) for part in raw_parts)
    digest = hashlib.sha1(raw_key.encode("utf-8")).hexdigest()[:16]
    return f"part3-{digest}"


def word_count(value: object) -> int:
    """Count words in a normalized text field."""
    if pd.isna(value):
        return 0
    return len(re.findall(r"\b\w+\b", str(value), flags=re.UNICODE))


def char_count(value: object) -> int:
    """Count characters in a normalized text field."""
    if pd.isna(value):
        return 0
    return len(str(value))


def join_quality_flags(row: pd.Series) -> Optional[str]:
    """Create a pipe-separated quality flag summary."""
    flags = []
    if row["language_code"] == "unknown":
        flags.append("language_unknown")
    if not row["has_original_text"]:
        flags.append("missing_original_text")
    if not row["has_proposal_text"]:
        flags.append("missing_proposal_text")
    if row["tool_count"] == 0:
        flags.append("tool_unknown")
    if row["tool_count"] > 1:
        flags.append("multi_tool")
    if row["is_duplicate_exact"]:
        flags.append("duplicate_exact")
    if row["is_duplicate_semantic_candidate"]:
        flags.append("duplicate_semantic_candidate")

    if not flags:
        return pd.NA
    return "|".join(flags)


def build_analysis_ready_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Transform the raw consolidated CSV into an analysis-ready dataframe."""
    missing_columns = set(RAW_TO_CANONICAL_COLUMNS) - set(raw_df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    df = raw_df.rename(columns=RAW_TO_CANONICAL_COLUMNS).copy()
    df = df[list(RAW_TO_CANONICAL_COLUMNS.values())]

    string_columns = [
        "document_name_raw",
        "language_raw",
        "tool_raw",
        "original_text_raw",
        "proposal_text_raw",
        "comments_raw",
    ]
    for column in string_columns:
        df[column] = df[column].map(_to_nullable_string).astype("string")

    df["group_id"] = pd.to_numeric(df["group_id"], errors="coerce").astype("Int64")
    df["row_id"] = df.apply(build_row_id, axis=1)

    df["document_name_clean"] = df["document_name_raw"].map(normalize_document_name).astype("string")
    df["original_text_clean"] = df["original_text_raw"].map(normalize_text).astype("string")
    df["proposal_text_clean"] = df["proposal_text_raw"].map(normalize_text).astype("string")
    df["comments_clean"] = df["comments_raw"].map(normalize_comments_json).astype("string")

    language_pairs = df["language_raw"].map(normalize_language)
    df["language_code"] = language_pairs.map(lambda item: item[0]).astype("string")
    df["language_label"] = language_pairs.map(lambda item: item[1]).astype("string")

    tool_lists = df["tool_raw"].map(extract_tools)
    df["tools_normalized"] = tool_lists.map(
        lambda items: " | ".join(items) if items else pd.NA
    ).astype("string")
    df["tool_primary"] = tool_lists.map(lambda items: items[0] if len(items) >= 1 else pd.NA).astype("string")
    df["tool_secondary"] = tool_lists.map(lambda items: items[1] if len(items) >= 2 else pd.NA).astype("string")
    df["tool_count"] = tool_lists.map(len).astype("Int64")
    df["tool_family"] = tool_lists.map(derive_tool_family).astype("string")

    df["original_text_fingerprint"] = df["original_text_clean"].map(fingerprint_text).astype("string")
    df["proposal_text_fingerprint"] = df["proposal_text_clean"].map(fingerprint_text).astype("string")

    df["has_original_text"] = df["original_text_clean"].notna()
    df["has_proposal_text"] = df["proposal_text_clean"].notna()
    df["has_comments"] = df["comments_clean"].notna()
    df["is_analysis_pair"] = df["has_original_text"] & df["has_proposal_text"]

    exact_key = [
        "group_id",
        "document_name_clean",
        "language_code",
        "tools_normalized",
        "original_text_clean",
        "proposal_text_clean",
    ]
    semantic_key = [
        "group_id",
        "document_name_clean",
        "language_code",
        "original_text_fingerprint",
        "proposal_text_fingerprint",
    ]
    df["is_duplicate_exact"] = df.duplicated(subset=exact_key, keep=False)
    df["duplicate_exact_group_size"] = df.groupby(exact_key, dropna=False)["row_id"].transform("size").astype("Int64")
    df["is_duplicate_semantic_candidate"] = df.duplicated(subset=semantic_key, keep=False) & ~df["is_duplicate_exact"]
    df["duplicate_semantic_group_size"] = df.groupby(semantic_key, dropna=False)["row_id"].transform("size").astype("Int64")

    df["original_char_len"] = df["original_text_clean"].map(char_count).astype("Int64")
    df["proposal_char_len"] = df["proposal_text_clean"].map(char_count).astype("Int64")
    df["comments_char_len"] = df["comments_clean"].map(char_count).astype("Int64")
    df["original_word_count"] = df["original_text_clean"].map(word_count).astype("Int64")
    df["proposal_word_count"] = df["proposal_text_clean"].map(word_count).astype("Int64")

    ratio = df["proposal_word_count"].div(df["original_word_count"].replace({0: pd.NA}))
    df["length_ratio_proposal_vs_original"] = ratio.astype("Float64")
    df["quality_flags"] = df.apply(join_quality_flags, axis=1).astype("string")

    ordered_columns = [
        "row_id",
        "group_id",
        "document_name_raw",
        "document_name_clean",
        "language_raw",
        "language_code",
        "language_label",
        "tool_raw",
        "tools_normalized",
        "tool_primary",
        "tool_secondary",
        "tool_count",
        "tool_family",
        "original_text_raw",
        "original_text_clean",
        "proposal_text_raw",
        "proposal_text_clean",
        "comments_raw",
        "comments_clean",
        "has_original_text",
        "has_proposal_text",
        "has_comments",
        "is_analysis_pair",
        "is_duplicate_exact",
        "duplicate_exact_group_size",
        "is_duplicate_semantic_candidate",
        "duplicate_semantic_group_size",
        "original_text_fingerprint",
        "proposal_text_fingerprint",
        "original_char_len",
        "proposal_char_len",
        "comments_char_len",
        "original_word_count",
        "proposal_word_count",
        "length_ratio_proposal_vs_original",
        "quality_flags",
    ]
    return df[ordered_columns]


def build_tools_long_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Create a long-form tool dataset from the normalized wide dataframe."""
    records = []
    for row in df.itertuples(index=False):
        tool_names = []
        if pd.notna(row.tools_normalized):
            tool_names = str(row.tools_normalized).split(" | ")

        if not tool_names:
            records.append(
                {
                    "row_id": row.row_id,
                    "group_id": row.group_id,
                    "document_name_clean": row.document_name_clean,
                    "tool_position": pd.NA,
                    "tool_name": pd.NA,
                    "tool_member_family": pd.NA,
                    "tool_raw": row.tool_raw,
                }
            )
            continue

        for position, tool_name in enumerate(tool_names, start=1):
            records.append(
                {
                    "row_id": row.row_id,
                    "group_id": row.group_id,
                    "document_name_clean": row.document_name_clean,
                    "tool_position": position,
                    "tool_name": tool_name,
                    "tool_member_family": TOOL_FAMILY_MAP.get(tool_name, "unknown"),
                    "tool_raw": row.tool_raw,
                }
            )

    tools_long_df = pd.DataFrame.from_records(records)
    if tools_long_df.empty:
        return tools_long_df

    tools_long_df["tool_position"] = pd.to_numeric(
        tools_long_df["tool_position"], errors="coerce"
    ).astype("Int64")
    for column in ["tool_name", "tool_member_family", "tool_raw", "document_name_clean"]:
        tools_long_df[column] = tools_long_df[column].astype("string")
    return tools_long_df


def write_report(df: pd.DataFrame, report_path: Path) -> None:
    """Write a plain-text report with the main normalization outcomes."""
    report_lines = [
        "PART III ANALYSIS DATASET PREPARATION REPORT",
        "=" * 80,
        "",
        f"Rows: {len(df)}",
        f"Columns: {len(df.columns)}",
        "",
        "Missingness / flags",
        "-" * 80,
        f"Rows with original text: {int(df['has_original_text'].sum())}",
        f"Rows with proposal text: {int(df['has_proposal_text'].sum())}",
        f"Rows with comments: {int(df['has_comments'].sum())}",
        f"Rows ready for pair analysis: {int(df['is_analysis_pair'].sum())}",
        f"Exact duplicate rows: {int(df['is_duplicate_exact'].sum())}",
        f"Semantic duplicate candidates: {int(df['is_duplicate_semantic_candidate'].sum())}",
        "",
        "Canonical languages",
        "-" * 80,
        df["language_label"].value_counts(dropna=False).to_string(),
        "",
        "Canonical tools",
        "-" * 80,
        df["tools_normalized"].fillna("<NA>").value_counts(dropna=False).head(20).to_string(),
        "",
        "Quality flags",
        "-" * 80,
        df["quality_flags"].fillna("<NA>").value_counts(dropna=False).head(20).to_string(),
        "",
    ]
    report_path.write_text("\n".join(report_lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Prepare an analysis-ready Part III dataset."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Path to the raw consolidated Part III CSV.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Path to the analysis-ready output CSV.",
    )
    parser.add_argument(
        "--tools-output",
        type=Path,
        default=DEFAULT_TOOLS_LONG_PATH,
        help="Path to the long-form tools output CSV.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT_PATH,
        help="Path to the preparation report.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the analysis-ready dataset preparation pipeline."""
    args = parse_args()
    logger.info("Loading raw Part III CSV: %s", args.input)
    raw_df = pd.read_csv(args.input, encoding="utf-8-sig")

    raw_df["Language"] = raw_df.apply(lambda x: detect(x["Proposal for E2R Text"]), axis=1)

    analysis_df = build_analysis_ready_dataframe(raw_df)
    tools_long_df = build_tools_long_dataframe(analysis_df)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    analysis_df.to_csv(args.output, index=False, encoding="utf-8-sig")
    tools_long_df.to_csv(args.tools_output, index=False, encoding="utf-8-sig")
    write_report(analysis_df, args.report)

    logger.info("Analysis-ready CSV written to: %s", args.output)
    logger.info("Tool-long CSV written to: %s", args.tools_output)
    logger.info("Preparation report written to: %s", args.report)
    logger.info("Rows preserved: %s", len(analysis_df))
    logger.info("Rows ready for pair analysis: %s", int(analysis_df["is_analysis_pair"].sum()))


if __name__ == "__main__":
    main()
