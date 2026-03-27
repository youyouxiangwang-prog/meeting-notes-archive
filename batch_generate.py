"""
Batch generate infographics from conversation_summaries.json
Uses generate_meeting_infographic() with auto-type detection and 28 templates (9:16 mobile)
Supports parallel processing for faster generation
"""

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Import generate_meeting_infographic from the local gemini_image_generator.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemini_image_generator import generate_meeting_infographic

# ── F-Pattern Visual Template ────────────────────────────────────────────────
F_PATTERN_TEMPLATE = """
Create a clean, modern infographic that strictly follows the **F-PATTERN READING LAYOUT**.

=== F-PATTERN STRUCTURE (16:9 Widescreen) ===

The canvas is divided into three horizontal bands that form the letter "F":

┌─────────────────────────────────────────────────────┐  ← F-Bar 1 (top 22%)
│  TITLE + CORE INSIGHT + KEY METRIC (full width)     │
│  Bold headline left-aligned; large accent number    │
│  right; background: accent color; text: white       │
└─────────────────────────────────────────────────────┘

┌──────────────────────────────────┐                     ← F-Bar 2 (next 18%)
│  3 KEY TAKEAWAYS  (left 65%)    │  [right 35% white] │
│  Icon + one-line each, bold     │                     │
└──────────────────────────────────┘

┌────────┐  ┌────────────────────────────────────────┐   ← F-Spine (bottom 60%)
│ LEFT   │  │ DETAIL CARDS (right 75%)               │
│ SPINE  │  │ 2–4 cards with sub-points, data, flow  │
│ (25%)  │  │ arranged in a 2-column grid             │
│        │  │                                        │
│ 4–5    │  │ Bottom strip: action items / next steps │
│ icon   │  └────────────────────────────────────────┘
│ labels │
└────────┘

=== MANDATORY STYLE RULES ===
- Canvas background: PURE WHITE #FFFFFF (no gradients, no off-white)
- F-Bar 1 background: accent_color (see per-slide spec)
- F-Spine background: accent_color at 15% opacity (very light tint)
- All body text on white backgrounds: dark gray #1F2937
- Fonts: title Montserrat ExtraBold ALL CAPS; body Inter/Open Sans Regular
- Icons: flat, monochrome, matching accent color
- NO dense paragraphs — max 8 words per bullet line
- Generous padding: 24px inside every card
- Thin 1px #E5E7EB dividers between cards
- Bottom action strip: light gray #F9FAFB background, left-aligned numbered list

=== CONTENT TO VISUALIZE ===
{content}

=== ACCENT COLOR ===
{accent_color}
"""

ACCENT_COLORS = [
    "#4338CA",  # indigo
    "#065F46",  # emerald
    "#C2410C",  # orange
    "#7C3AED",  # violet
    "#0369A1",  # sky blue
    "#9D174D",  # rose
    "#1D4ED8",  # blue
    "#15803D",  # green
]


def sanitize_filename(title: str, max_length: int = 50) -> str:
    """Convert title to safe filename"""
    # Remove or replace unsafe characters
    safe = title.replace("/", "_").replace("\\", "_").replace(":", "_")
    safe = (
        safe.replace("?", "")
        .replace("*", "")
        .replace('"', "")
        .replace("<", "")
        .replace(">", "")
        .replace("|", "")
    )
    # Truncate if too long
    if len(safe) > max_length:
        safe = safe[:max_length]
    return safe.strip()


def detect_language(text: str) -> str:
    """Detect if text is primarily Chinese or English"""
    chinese_chars = sum(1 for char in text if "\u4e00" <= char <= "\u9fff")
    total_chars = len([c for c in text if c.strip()])

    if total_chars == 0:
        return "en"

    chinese_ratio = chinese_chars / total_chars
    return "zh" if chinese_ratio > 0.3 else "en"


def process_single_item(idx, total, item, output_dir, model_name, resolution):
    """Process a single summary item using auto-detected template"""
    title = item.get("title", f"Untitled_{idx}")
    summary = item.get("summary", "")

    result = {
        "index": idx,
        "title": title,
        "success": False,
        "file_size": 0,
        "error": None,
    }

    if not summary or summary.strip() == "":
        result["error"] = "Empty summary"
        return result

    # Output filename
    safe_title = sanitize_filename(title)
    output_filename = f"{idx:02d}_{safe_title}.png"
    output_path = os.path.join(output_dir, output_filename)

    print(f"\n[{idx}/{total}] 🚀 Starting: {title}")

    try:
        generate_meeting_infographic(
            meeting_summary=f"Title: {title}\n\n{summary}",
            output_path=output_path,
            model_name=model_name,
            aspect_ratio="9:16",
            resolution=resolution,
        )

        # Check if file was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(
                f"[{idx}/{total}] ✅ Completed: {output_filename} ({file_size:.1f} MB)"
            )
            result["success"] = True
            result["file_size"] = file_size
        else:
            result["error"] = "File not created"
            print(f"[{idx}/{total}] ❌ Failed: File not created")

    except Exception as e:
        result["error"] = str(e)
        print(f"[{idx}/{total}] ❌ Error: {str(e)}")

    return result


def batch_generate_infographics(
    json_path: str = "conversation_summaries.json",
    output_dir: str = None,
    model_name: str = "gemini-3.1-flash-image-preview",
    resolution: str = "2K",
    max_items: int = None,
    max_workers: int = 4,
):
    """
    Batch generate F-pattern infographics from JSON file with parallel processing

    Args:
        json_path: Path to JSON file with summaries
        output_dir: Output directory (default: f_pattern_images_TIMESTAMP next to this script)
        model_name: Gemini model to use
        resolution: Image resolution
        max_items: Maximum number of items to process (None = all)
        max_workers: Number of parallel workers (default: 4)
    """

    # Default timestamped output directory next to this script
    if output_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(script_dir, f"batch_infographics_{timestamp}")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Load JSON data
    print(f"\n{'='*80}")
    print(f"📂 Loading summaries from: {json_path}")
    print(f"🎨 Auto-detecting meeting type from 28 templates (9:16 mobile)")
    print(f"{'='*80}\n")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    if max_items:
        total = min(total, max_items)
        data = data[:max_items]

    print(f"Found {total} summaries to process")
    print(f"Using {max_workers} parallel workers\n")

    # Statistics
    stats = {
        "total": total,
        "success": 0,
        "failed": 0,
        "total_size": 0.0,
    }

    failed_items = []

    # Process items in parallel
    print(f"{'='*80}")
    print(f"🚀 Starting parallel generation...")
    print(f"{'='*80}\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_item = {
            executor.submit(
                process_single_item,
                idx,
                total,
                item,
                output_dir,
                model_name,
                resolution,
            ): (idx, item)
            for idx, item in enumerate(data, 1)
        }

        # Collect results as they complete
        for future in as_completed(future_to_item):
            result = future.result()

            if result["success"]:
                stats["success"] += 1
                stats["total_size"] += result["file_size"]
            else:
                stats["failed"] += 1
                failed_items.append(
                    {
                        "index": result["index"],
                        "title": result["title"],
                        "reason": result["error"],
                    }
                )

    # Print summary
    print(f"\n\n{'='*80}")
    print(f"🎉 Batch Generation Complete!")
    print(f"{'='*80}")
    print(f"\n📊 Statistics:")
    print(f"   Total processed: {stats['total']}")
    print(f"   ✅ Successful: {stats['success']}")
    print(f"   ❌ Failed: {stats['failed']}")
    print(f"   💾 Total size: {stats['total_size']:.1f} MB")

    if failed_items:
        print(f"\n⚠️  Failed items:")
        for item in failed_items:
            print(f"   [{item['index']}] {item['title']}")
            print(f"       Reason: {item['reason']}")

    print(f"\n📁 Output directory: {os.path.abspath(output_dir)}")
    print(f"{'='*80}\n")

    return stats


if __name__ == "__main__":
    import sys

    # Parse command line arguments
    max_items = None
    max_workers = 4  # Default parallel workers

    if len(sys.argv) > 1:
        try:
            max_items = int(sys.argv[1])
            print(f"Processing first {max_items} items only")
        except ValueError:
            print(f"Invalid number: {sys.argv[1]}, processing all items")

    if len(sys.argv) > 2:
        try:
            max_workers = int(sys.argv[2])
            print(f"Using {max_workers} parallel workers")
        except ValueError:
            print(f"Invalid worker count: {sys.argv[2]}, using default 4 workers")

    # Resolve paths relative to this script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "conversation_summaries.json")

    # Run batch generation
    stats = batch_generate_infographics(
        json_path=json_path,
        model_name="gemini-3.1-flash-image-preview",
        resolution="2K",
        max_items=max_items,
        max_workers=max_workers,
    )

    print("\n🎨 Batch generation finished!")
