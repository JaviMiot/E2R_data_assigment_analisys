#!/usr/bin/env python3
import argparse
import logging
import re
from pathlib import Path
import pandas as pd
import numpy as np

# Configure logging
ROOT_DIR = Path(__file__).resolve().parent.parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(ROOT_DIR / "logs/part2_cleaning.log", mode="w", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

def normalize_time(x):
    """Normalize time strings to a standard format."""
    if not isinstance(x, str):
        return None
    x = x.lower()
    
    # Normalize time units
    x = re.sub(r"(minutes|mins|min|m)", " m", x)
    x = re.sub(r"(hours|hour|hr|h)", " h", x)
    x = re.sub(r"(around|approximately)", "", x)
    x = re.sub(r"\s{2,}", " ", x)
    
    # Clean specific patterns
    x = re.sub(r'.*~=\s*(\d+)\s*m$', r"\1 m", x)
    x = re.sub('1 h 10 m', "70 m", x)
    x = re.sub('approxi mately 2 h', "120 m", x)
    x = x.strip()
    
    return x

def convert_time_to_minutes(x):
    """Convert normalized time string to minutes as float."""
    if not isinstance(x, str):
        return None
    
    match = re.match(r"(\d+\.?\d*)", x)
    if not match:
        return None
    
    time_value = np.float64(match[0])
    
    if "h" in x:
        return time_value * 60
    return time_value

def normalize_tool_name(x):
    """Normalize tool names to standard forms."""
    if not isinstance(x, str):
        return x
    
    # Handle multiline submissions (e.g., Website URL + Tool name)
    if '\n' in x:
        x = x.split('\n')[-1].strip()
        
    # Remove prefix "Analysis performed with " if present
    x = re.sub(r"^Analysis performed with\s*", "", x)
    
    # Copilot variations
    x = re.sub(r"(CoPilot|Copilot)", "Copilot", x)
    
    # Gemini variations
    x = re.sub(r".*Gemini$", "Gemini", x)
    x = re.sub("Google Gemini 3.0 Pro", "Gemini", x)
    x = re.sub(r"Gemini \(Version: 3 Flash\)", "Gemini", x)
    x = re.sub("https://gemini.google.com/", "Gemini", x)
    x = re.sub("Gemini 3 Pro Preview", "Gemini", x)
    x = re.sub("Gemini 3 Pro - Thinking", "Gemini", x)
    x = re.sub("Tool 2: Gemini 3", "Gemini", x)
    x = re.sub("Gemini Pro 3", "Gemini", x)
    x = re.sub("Gemini 3 Pro", "Gemini", x)
    x = re.sub("Gemini V3", "Gemini", x)
    x = re.sub("GEMINI", "Gemini", x)
    
    # ChatGPT variations
    x = re.sub(r".*ChatGPT 5.2$", "ChatGPT", x)
    x = re.sub(r"^ChatGPT based on GPT-5.2$", "ChatGPT", x)
    x = re.sub(r"^Chat GPT$", "ChatGPT", x)
    x = re.sub(r"^ChatGPT 5.2$", "ChatGPT", x)
    x = re.sub(r"^Chat-GPT$", "ChatGPT", x)
    x = re.sub(r"^Tool 1: ChatGPT 5.2$", "ChatGPT", x)
    x = re.sub(r"^GPT$", "ChatGPT", x)
    
    # Claude variations
    x = re.sub(r"^Claude Sonnet 4.5 - Extended Thinking$", "Claude", x)
    x = re.sub(r"^Claude AI$", "Claude", x)
    x = re.sub(r"^Claude \+ Manual analysis$", "Claude", x)
    x = re.sub(r"^Claude \+ Manual Analysis$", "Claude", x)
    
    return x

def normalize_e2r_element(x):
    """Normalize E2R element names."""
    if not isinstance(x, str):
        return x
    
    x = re.sub(r'^Special characters like , \\&, \\<, \\§ or \\#\\$', r'Special characters like \\, &, <, § or #', x)
    x = re.sub(r'^"etc." and suspension points$', '"etc." and suspension points', x)
    x = re.sub(r'^Passive language / voice$', 'Passive language/voice', x)
    x = re.sub(r'^Words from other languages$', 'Words from other languages (unless they are very well known)', x)
    x = re.sub(r'^Use of synonyms instead of same word$', 'Use of synonyms instead of the same word across the text', x)
    x = re.sub(r'^Adverbs ending in "-ly"$', "Adverbs ending in '-ly'", x)
    
    # Handle smart quotes and missed backslashes in certain submissions
    x = x.replace('“etc.” and suspension points', '"etc." and suspension points')
    x = x.replace("'etc.' and suspension points", '"etc." and suspension points')
    x = x.replace("etc.' and suspension points", '"etc." and suspension points')
    x = x.replace('Adverbs ending in “-ly”', "Adverbs ending in '-ly'")
    x = x.replace('Special characters like , &, <, § or #', r'Special characters like \, &, <, § or #')
    
    return x

def extract_e2r_category(x):
    """Extract E2R category from guideline string."""
    if not isinstance(x, str):
        return 'Unknown'
    
    if 'Spelling' in x:
        return 'Spelling'
    elif 'Grammar' in x:
        return 'Grammar'
    elif 'Vocabulary' in x:
        return 'Vocabulary'
    elif 'Composition' in x:
        return 'Composition'
    else:
        return 'Other'

def normalize_website(x):
    """Normalize website URLs."""
    if not isinstance(x, str):
        return x
    
    # Fix weird encoding artefacts
    x = x.replace("_xfffe_", "-")
    
    # Extract the first valid URL if multiple are joined or prefixed
    urls = re.findall(r'(https?://[^\s/$.?#].[^\s]*)', x)
    if urls:
        return urls[0].strip()
        
    return x.strip()

def normalize_value(x):
    """Normalize the evaluation outcome values."""
    if not isinstance(x, str):
        return x
    
    x = x.strip()
    x_lower = x.lower()
    
    # Standardize to identical representations
    if x_lower in ['pass', 'identified by the tool']:
        return 'Identified by the tool'
    elif x_lower in ['not identified', 'fail', 'not identified by the tool']:
        return 'Not identified by the tool'
    elif 'partially' in x_lower:
        return 'Partially identified by the tool'
    elif 'evaluator' in x_lower or 'manual' in x_lower:
        return 'Identified by the evaluator (in a manual way)'
    elif x_lower in ['to be verified', 'unknown']:
        return 'Unknown'
        
    return x

def clean_data(input_path: Path, output_path: Path) -> None:
    logger.info(f"Loading data from {input_path}")
    try:
        df = pd.read_csv(input_path, encoding='utf-8-sig')
    except Exception as e:
        logger.error(f"Failed to read {input_path}: {e}")
        return

    logger.info(f"Initial dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")

    # Filter out RevisionFACILE tools
    tools_to_exclude = ['RevisionFACILE', 'RevisiónFACILE', 'ChatGPT & Gemini']
    df_clean = df[~df['Tool used'].isin(tools_to_exclude)]
    df_clean = df_clean[~df_clean['Tool used'].str.contains('revisionfacile.oeg.fi.upm.es', na=False)].copy()

    logger.info(f"Rows after filtering tools: {len(df_clean)} (removed {len(df) - len(df_clean)} rows)")

    # Apply normalization functions
    logger.info("Normalizing time, tools, and elements...")
    
    # Process time to float minutes, then update column
    temp_time = df_clean['Time Spent'].apply(normalize_time)
    df_clean['Time Spent'] = temp_time.apply(convert_time_to_minutes).astype(float).fillna(0.0)

    df_clean.loc[:, 'Tool used'] = df_clean['Tool used'].apply(normalize_tool_name)
    df_clean.loc[:, 'Elements to be identified'] = df_clean['Elements to be identified'].apply(normalize_e2r_element)
    df_clean.loc[:, 'Web'] = df_clean['Web'].apply(normalize_website)
    df_clean.loc[:, 'Value'] = df_clean['Value'].apply(normalize_value)

    # Drop rows with null Value
    initial_clean_len = len(df_clean)
    df_clean = df_clean.dropna(subset=['Value']).copy()
    logger.info(f"Rows after dropping null Values: {len(df_clean)} (removed {initial_clean_len - len(df_clean)} rows)")

    # Create derived columns
    df_clean.loc[:, 'E2R_Category'] = df_clean['E2R Guidelines'].apply(extract_e2r_category)

    logger.info(f"Final cleaned dataset shape: {df_clean.shape[0]} rows × {df_clean.shape[1]} columns")

    # Save to CSV
    try:
        df_clean.to_csv(output_path, index=False, encoding='utf-8-sig')
        logger.info(f"Cleaned dataset saved successfully to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save {output_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Clean and standardize Part 2 data")
    parser.add_argument(
        "--input", 
        type=Path, 
        default=ROOT_DIR / "data/part2_consolidated.csv",
        help="Path to input consolidated CSV file"
    )
    parser.add_argument(
        "--output", 
        type=Path, 
        default=ROOT_DIR / "data/part2_cleaned.csv",
        help="Path to output cleaned CSV file"
    )
    
    args = parser.parse_args()
    clean_data(args.input, args.output)

if __name__ == "__main__":
    main()
