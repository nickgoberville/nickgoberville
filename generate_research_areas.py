#!/usr/bin/env python3
"""
Generate a research areas bar chart SVG from Google Scholar publications.
"""

from collections import Counter

# Research area keywords to look for in paper titles
RESEARCH_KEYWORDS = {
    "Autonomous Vehicles": ["autonomous", "automated vehicle", "automated driving", "self-driving", "adas", "av "],
    "Perception & Sensing": ["lidar", "camera", "sensor", "perception", "sensing", "detection"],
    "Weather & Environment": ["weather", "snow", "rain", "inclement", "precipitation", "conditions"],
    "Control Systems": ["control", "controller", "synthesis", "law"],
    "Computer Vision": ["vision", "image", "u-net", "deep learning", "estimation"],
    "Electric & Energy": ["electric", "energy", "fuel", "eco-", "efficiency"],
    "Connected Vehicles": ["connected", "v2x", "infrastructure", "intersection"],
    "Simulation & Testing": ["simulation", "simulator", "dynamometer", "testing", "evaluation"],
    "Robotics": ["robotic", "arm", "3d printing"]
}

# Your actual publications from Google Scholar
PUBLICATIONS = [
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
    "Session 6: Weather, Automated Vehicles, and Society",
    "Automated Vehicle Perception Sensor Evaluation in Real-World Weather Conditions",
    "Cost-Effective Enablement of Automated Driving Systems on Snow-Covered Roads",
    "Autonomous Vehicle Camera Mount Application",
    "3D Printing Robotic Arm on Linear Rails",
    "Transportation Research Interdisciplinary Perspectives"
]

def count_research_areas(publications, keywords_dict):
    """Count mentions of research area keywords in publication titles."""
    area_counts = Counter()
    
    for title in publications:
        title_lower = title.lower()
        for area, keywords in keywords_dict.items():
            for keyword in keywords:
                if keyword in title_lower:
                    area_counts[area] += 1
                    break  # Only count once per area per paper
    
    return area_counts

def generate_bar_chart_svg(area_counts, max_items=7):
    """Generate a minimal horizontal bar chart SVG."""
    # Get top areas
    top_areas = area_counts.most_common(max_items)
    
    if not top_areas:
        return None
    
    # SVG dimensions
    width = 380
    bar_height = 22
    spacing = 6
    left_margin = 135
    right_margin = 40
    top_margin = 38
    chart_width = width - left_margin - right_margin
    
    max_count = max(count for _, count in top_areas)
    height = top_margin + len(top_areas) * (bar_height + spacing) + 20
    
    # Colors matching the tokyonight theme
    bg_color = "#1a1b27"
    border_color = "#3d59a1"
    title_color = "#7aa2f7"
    text_color = "#a9b1d6"
    bar_color = "#7aa2f7"
    bar_bg = "#24283b"
    
    svg_parts = [
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="{bg_color}" rx="8"/>',
        f'  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="none" stroke="{border_color}" stroke-width="1" rx="7"/>',
        f'  <text x="{width/2}" y="24" text-anchor="middle" fill="{title_color}" font-family="Segoe UI, Ubuntu, sans-serif" font-size="13" font-weight="600">Research Areas</text>',
    ]
    
    for i, (area, count) in enumerate(top_areas):
        y = top_margin + i * (bar_height + spacing)
        bar_width = max((count / max_count) * chart_width, 8)  # Minimum bar width
        
        # Background bar
        svg_parts.append(
            f'  <rect x="{left_margin}" y="{y}" width="{chart_width}" height="{bar_height}" fill="{bar_bg}" rx="3"/>'
        )
        
        # Filled bar
        svg_parts.append(
            f'  <rect x="{left_margin}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{bar_color}" rx="3"/>'
        )
        
        # Label
        svg_parts.append(
            f'  <text x="{left_margin - 6}" y="{y + bar_height/2 + 4}" text-anchor="end" fill="{text_color}" font-family="Segoe UI, Ubuntu, sans-serif" font-size="10">{area}</text>'
        )
        
        # Count
        svg_parts.append(
            f'  <text x="{left_margin + chart_width + 6}" y="{y + bar_height/2 + 4}" fill="{text_color}" font-family="Segoe UI, Ubuntu, sans-serif" font-size="10">{count}</text>'
        )
    
    svg_parts.append('</svg>')
    
    return '\n'.join(svg_parts)


if __name__ == "__main__":
    # Count research areas
    area_counts = count_research_areas(PUBLICATIONS, RESEARCH_KEYWORDS)
    
    print("Research area counts:")
    for area, count in area_counts.most_common():
        print(f"  {area}: {count}")
    
    # Generate SVG
    svg_content = generate_bar_chart_svg(area_counts)
    
    if svg_content:
        with open("research-areas.svg", "w") as f:
            f.write(svg_content)
        print("\nGenerated research-areas.svg")
    else:
        print("\nNo research areas found")
