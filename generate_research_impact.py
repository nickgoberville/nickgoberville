#!/usr/bin/env python3
"""
Generate a unified Research Impact SVG combining bibliometrics and research areas
with consistent, modern styling. Fetches live data from Google Scholar.
"""

import os
from collections import Counter

try:
    from scholarly import scholarly
    SCHOLARLY_AVAILABLE = True
except ImportError:
    SCHOLARLY_AVAILABLE = False
    print("Warning: scholarly not installed, using fallback data")

# Google Scholar ID
SCHOLAR_ID = os.environ.get('SCHOLAR_ID', 'BGCbkEUAAAAJ')

# Research area keywords
RESEARCH_KEYWORDS = {
    "Autonomous Vehicles": ["autonomous", "automated vehicle", "automated driving", "self-driving", "adas", "av "],
    "Perception & Sensing": ["lidar", "camera", "sensor", "perception", "sensing", "detection"],
    "Weather & Environment": ["weather", "snow", "rain", "inclement", "precipitation", "conditions"],
    "Control Systems": ["control", "controller", "synthesis", "law"],
    "Computer Vision": ["vision", "image", "u-net", "deep learning", "estimation"],
    "Electric & Energy": ["electric", "energy", "fuel", "eco-", "efficiency"],
    "Connected Vehicles": ["connected", "v2x", "infrastructure", "intersection"],
    "Simulation & Testing": ["simulation", "simulator", "dynamometer", "testing", "evaluation"],
}

# Fallback data if scholarly fails
FALLBACK_METRICS = {
    "Citations": 197,
    "h-index": 8,
    "i10-index": 4,
    "Publications": 23,
}

FALLBACK_PUBLICATIONS = [
    "Analysis of LiDAR and camera data in real-world weather conditions for autonomous vehicle operations",
    "Development of an energy efficient and cost effective autonomous vehicle research platform",
    "Tire track identification: A method for drivable region detection in conditions of snow-occluded lane lines",
    "No cost autonomous vehicle advancements in CARLA through ROS",
    "Tire track identification: Application of u-net deep learning model for drivable region detection in snow occluded conditions",
    "Using reinforcement learning and simulation to develop autonomous vehicle control strategies",
    "Evaluation of autonomous vehicle sensing and compute load on a chassis dynamometer",
    "Techno-economic analysis of fixed-route autonomous and electric shuttles",
    "Snow coverage estimation using camera data for automated driving applications",
    "Vehicle performance analysis of a wheelchair accessible autonomous electric shuttle",
    "Road snow coverage estimation using camera and weather infrastructure sensor inputs",
    "Observer for faulty perception correction in autonomous vehicles",
    "Automation in Inclement Weather",
    "Control Law Synthesis for Lockheed Martin's Innovative Control Effectors Aircraft Concept",
    "Modular Dynamometer Testing Framework to Evaluate Energy Impacts of Longitudinal Automated Driving Systems",
    "Portable Track-Based Connected Intersection Testing System for Connected and Automated Vehicles",
    "Raw Lidar and Camera Data Synchronized with Precipitation and Present Weather Data",
    "Automated Vehicle Perception Sensor Evaluation in Real-World Weather Conditions",
    "Cost-Effective Enablement of Automated Driving Systems on Snow-Covered Roads",
]


def fetch_scholar_data(scholar_id):
    """Fetch live data from Google Scholar."""
    if not SCHOLARLY_AVAILABLE:
        return FALLBACK_METRICS, FALLBACK_PUBLICATIONS
    
    try:
        print(f"Fetching Google Scholar data for {scholar_id}...")
        author = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(author, sections=['basics', 'publications'])
        
        # Extract metrics
        metrics = {
            "Citations": author.get('citedby', 0),
            "h-index": author.get('hindex', 0),
            "i10-index": author.get('i10index', 0),
            "Publications": len(author.get('publications', [])),
        }
        
        # Extract publication titles
        publications = []
        for pub in author.get('publications', []):
            title = pub.get('bib', {}).get('title', '')
            if title:
                publications.append(title)
        
        print(f"Fetched: {metrics}")
        return metrics, publications
        
    except Exception as e:
        print(f"Error fetching Scholar data: {e}")
        print("Using fallback data")
        return FALLBACK_METRICS, FALLBACK_PUBLICATIONS


def count_research_areas(publications, keywords_dict):
    """Count mentions of research area keywords in publication titles."""
    area_counts = Counter()
    for title in publications:
        title_lower = title.lower()
        for area, keywords in keywords_dict.items():
            for keyword in keywords:
                if keyword in title_lower:
                    area_counts[area] += 1
                    break
    return area_counts


def generate_unified_svg(metrics, area_counts, top_n=5):
    """Generate a unified, modern research impact card."""
    
    top_areas = area_counts.most_common(top_n)
    
    # Dimensions
    width = 700
    metrics_height = 80
    areas_height = 30 + len(top_areas) * 28
    total_height = metrics_height + areas_height + 50
    
    # Colors - clean minimal palette
    bg = "#0d1117"
    card_bg = "#161b22"
    border = "#30363d"
    text_primary = "#e6edf3"
    text_secondary = "#8b949e"
    accent = "#58a6ff"
    bar_bg = "#21262d"
    
    max_count = max(count for _, count in top_areas) if top_areas else 1
    
    svg = f'''<svg width="{width}" height="{total_height}" viewBox="0 0 {width} {total_height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="barGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{accent};stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#1f6feb;stop-opacity:1"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="{width}" height="{total_height}" fill="{bg}" rx="12"/>
  <rect x="1" y="1" width="{width-2}" height="{total_height-2}" fill="none" stroke="{border}" stroke-width="1" rx="11"/>
  
  <!-- Metrics Row -->
  <g transform="translate(0, 20)">'''
    
    # Metrics cards
    metric_items = list(metrics.items())
    card_width = 150
    card_spacing = (width - len(metric_items) * card_width) / (len(metric_items) + 1)
    
    for i, (label, value) in enumerate(metric_items):
        x = card_spacing + i * (card_width + card_spacing)
        svg += f'''
    <g transform="translate({x}, 0)">
      <rect width="{card_width}" height="60" fill="{card_bg}" rx="8"/>
      <text x="{card_width/2}" y="28" text-anchor="middle" fill="{text_primary}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="22" font-weight="600">{value}</text>
      <text x="{card_width/2}" y="48" text-anchor="middle" fill="{text_secondary}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="12">{label}</text>
    </g>'''
    
    svg += '''
  </g>
  
  <!-- Research Areas -->
  <g transform="translate(30, ''' + str(metrics_height + 30) + ''')">
    <text x="0" y="0" fill="''' + text_secondary + '''" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="11" font-weight="500" text-transform="uppercase" letter-spacing="1">RESEARCH FOCUS</text>'''
    
    bar_max_width = width - 200
    
    for i, (area, count) in enumerate(top_areas):
        y = 20 + i * 28
        bar_width = max((count / max_count) * bar_max_width, 20)
        area_escaped = area.replace('&', '&amp;')
        
        svg += f'''
    <g transform="translate(0, {y})">
      <rect x="130" y="0" width="{bar_max_width}" height="20" fill="{bar_bg}" rx="4"/>
      <rect x="130" y="0" width="{bar_width}" height="20" fill="url(#barGrad)" rx="4"/>
      <text x="125" y="14" text-anchor="end" fill="{text_secondary}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="12">{area_escaped}</text>
      <text x="{130 + bar_max_width + 10}" y="14" fill="{text_secondary}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="11">{count}</text>
    </g>'''
    
    svg += '''
  </g>
</svg>'''
    
    return svg


if __name__ == "__main__":
    # Fetch live data from Google Scholar
    metrics, publications = fetch_scholar_data(SCHOLAR_ID)
    
    # Count research areas from publication titles
    area_counts = count_research_areas(publications, RESEARCH_KEYWORDS)
    
    print(f"Metrics: {metrics}")
    print(f"Top areas: {area_counts.most_common(5)}")
    
    # Generate SVG
    svg = generate_unified_svg(metrics, area_counts)
    
    with open("research-impact.svg", "w") as f:
        f.write(svg)
    
    print("Generated research-impact.svg")
