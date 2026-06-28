import json
import os
import glob
import re

PAULA_TIKTOK_DIR = os.path.expanduser("~/paula/tiktok")
SOURCES_DIR = os.path.join(PAULA_TIKTOK_DIR, "wiki/sources")

def consolidate():
    # Iterate over all directories in ~/paula/tiktok that are numeric IDs
    for dir_path in glob.glob(os.path.join(PAULA_TIKTOK_DIR, "[0-9]*")):
        if not os.path.isdir(dir_path):
            continue
            
        tiktok_id = os.path.basename(dir_path)
        md_file = os.path.join(SOURCES_DIR, f"{tiktok_id}.md")
        json_file = os.path.join(dir_path, "visual_analysis.json")
        
        if not os.path.exists(md_file) or not os.path.exists(json_file):
            continue
            
        print(f"Processing {tiktok_id}...")
        
        # Load JSON data
        with open(json_file, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
            
        # Construct Markdown content
        analysis_md = "\n## Visual Analysis\n"
        for key, value in analysis.items():
            formatted_key = key.replace('_', ' ').title()
            analysis_md += f"- **{formatted_key}:** {value}\n"
            
        # Update MD file
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace or append Visual Analysis section
        if "## Visual Analysis" in content:
            # Replace existing section (handles potential multi-line content)
            content = re.sub(r"## Visual Analysis.*", analysis_md, content, flags=re.DOTALL)
        else:
            # Append new section
            content += analysis_md
            
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    consolidate()
    print("Consolidation complete.")
