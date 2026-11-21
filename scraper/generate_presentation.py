"""
Generate a professional, executive-ready PowerPoint presentation (12 slides)
for the EV Spare Parts Prioritization project.
Embeds publication charts and sets slide notes for a 7-minute presentation defense.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

NAVY = RGBColor(26, 54, 93)
TEAL = RGBColor(13, 148, 136)
CHARCOAL = RGBColor(45, 55, 72)
LIGHT_BG = RGBColor(247, 250, 252)
WHITE = RGBColor(255, 255, 255)
RED = RGBColor(197, 48, 48)

blank_layout = prs.slide_layouts[6]

def set_slide_background(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_header(slide, title_text, category_text="EV SPARE-PARTS IMPORT PRIORITIZATION"):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.0))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    
    p0 = tf.paragraphs[0]
    p0.text = category_text.upper()
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = TEAL
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = NAVY
    p1.space_before = Pt(4)

# ==============================================================================
# SLIDE 1: TITLE SLIDE
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1, NAVY)

t_box = s1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(3.5))
tf1 = t_box.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "DATA-DRIVEN EV SPARE-PARTS IMPORT PRIORITIZATION"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = WHITE

p_sub = tf1.add_paragraph()
p_sub.text = "Strategic Multi-Factor Decision Framework for the Ethiopian EV Market"
p_sub.font.size = Pt(20)
p_sub.font.color.rgb = TEAL
p_sub.space_before = Pt(12)

p_auth = tf1.add_paragraph()
p_auth.text = "iCog Labs Internship Technical Assessment\nDate: November 2026  |  Market: Addis Ababa & Regional Corridors"
p_auth.font.size = Pt(13)
p_auth.font.color.rgb = RGBColor(226, 232, 240)
p_auth.space_before = Pt(24)

s1.notes_slide.notes_text_frame.text = (
    "Good morning, evaluators. Today I am presenting a data-driven decision framework designed to solve a critical commercial dilemma in Ethiopia: "
    "identifying exactly which replacement parts an automotive importer should prioritize under constrained working capital and foreign exchange rationing. "
    "Rather than relying on unverified assumptions, our system integrates live marketplace evidence, third-party catalogues, and verified supplier inventories into an explainable, robust scoring framework."
)

# ==============================================================================
# SLIDE 2: ETHIOPIAN POLICY CONTEXT & FOREX BOTTLENECK
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2, LIGHT_BG)
add_header(s2, "The Ethiopian EV Dilemma: Policy Shift & Forex Rationing")

c2_1 = s2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
tf2_1 = c2_1.text_frame
tf2_1.word_wrap = True

p = tf2_1.paragraphs[0]
p.text = "Policy & Market Catalysts"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NAVY

bullets2_1 = [
    ("Federal ICE Prohibition (2024): ", "Ethiopia's complete ban on non-electric private passenger vehicle imports spurred an immediate influx of Chinese and global EVs into Addis Ababa."),
    ("Rapid Fleet Expansion: ", "Massive surge in urban micro-EVs (e.g. BYD Seagull) and compact crossovers (BYD Yuan Up) operating without mature aftermarket parts support."),
    ("Severe Parts Lag: ", "While vehicle imports surged, replacement parts supply chains remain severely fragmented, creating critical vehicle downtime risks for fleet and private owners.")
]

for title, desc in bullets2_1:
    bp = tf2_1.add_paragraph()
    bp.space_before = Pt(10)
    r1 = bp.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(12)
    r1.font.color.rgb = NAVY
    r2 = bp.add_run()
    r2.text = desc
    r2.font.size = Pt(12)
    r2.font.color.rgb = CHARCOAL

c2_2 = s2.shapes.add_textbox(Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8))
tf2_2 = c2_2.text_frame
tf2_2.word_wrap = True

p = tf2_2.paragraphs[0]
p.text = "Importer Commercial Constraints"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NAVY

bullets2_2 = [
    ("Forex & LC Rationing: ", "Severe foreign exchange constraints require importers to justify every allocated dollar with rapid-turning, high-demand inventory."),
    ("Dead Inventory Risk: ", "Stocking unverified, slow-moving parts ties up limited capital for months and risks fatal fitment incompatibilities."),
    ("Harsh Road Conditions: ", "Addis Ababa's congested corridors create frequent exterior contact scrapes (mirrors, bumpers), while cobblestone and peri-urban roads accelerate suspension wear."),
    ("The Decision Mandate: ", "Importers need a mathematically defensible prioritization system before deploying scarce capital.")
]

for title, desc in bullets2_2:
    bp = tf2_2.add_paragraph()
    bp.space_before = Pt(10)
    r1 = bp.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(12)
    r1.font.color.rgb = TEAL
    r2 = bp.add_run()
    r2.text = desc
    r2.font.size = Pt(12)
    r2.font.color.rgb = CHARCOAL

s2.notes_slide.notes_text_frame.text = (
    "The problem space is unique to Ethiopia. With the government's ban on ICE imports, electric vehicles now dominate new car arrivals. "
    "But spare parts supply has severely lagged behind. An importer faces two risks: stocking parts that sit on shelves for months, or stocking parts with unverified fitment. "
    "Because foreign exchange is rationed, inventory decisions must be mathematically defensible and grounded in verified data."
)

# ==============================================================================
# SLIDE 3: VEHICLE SELECTION MATRIX
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3, LIGHT_BG)
add_header(s3, "Vehicle Selection: 3 Representative Fleet Archetypes")

table_shape = s3.shapes.add_table(6, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
t3 = table_shape.table

t3.columns[0].width = Inches(2.2)
t3.columns[1].width = Inches(1.8)
t3.columns[2].width = Inches(2.0)
t3.columns[3].width = Inches(4.2)
t3.columns[4].width = Inches(1.5)

headers3 = ["Vehicle Model", "Segment", "Market Evidence", "Rationale & Strategic Role", "Status"]
for i, h in enumerate(headers3):
    cell = t3.cell(0, i)
    cell.text = h
    cell.fill.solid()
    cell.fill.fore_color.rgb = NAVY
    for p in cell.text_frame.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE

rows3 = [
    ("BYD Seagull", "Subcompact Hatch", "37 listings in project sample\n(Adey Market S001)", "Leading urban commuter EV; high traffic contact exposure; 35 Landin catalogue listings (S003) — 23 priced, stock not stated, compatibility supplier-claimed.", "SELECTED"),
    ("BYD Yuan Up", "Compact SUV / CUV", "36 listings in project sample\n(Adey Market S001)", "Mass-market family crossover; documented supplier catalogue gap; critical test case for scarcity analysis.", "SELECTED"),
    ("Toyota bZ4X", "Midsize Electric SUV", "28 listings in project sample\n(Adey Market S001)", "Brand-equity benchmark; established corporate fleet presence; evaluated via third-party parts catalogue (S005).", "SELECTED"),
    ("Volkswagen ID.4", "Compact SUV", "12 listings (Adey)", "Grey-market import; dispersed EU/China variants introduce severe VIN fragmentation.", "EXCLUDED"),
    ("Tesla Model 3/Y", "Premium Sedan/SUV", "5 listings (Adey)", "Niche luxury tier; closed proprietary service ecosystem; low mass-market replacement volume.", "EXCLUDED")
]

for row_idx, r in enumerate(rows3, start=1):
    for col_idx, text in enumerate(r):
        cell = t3.cell(row_idx, col_idx)
        cell.text = text
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(11)
            if col_idx == 4:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
                p.font.color.rgb = RGBColor(16, 185, 129) if text == "SELECTED" else RED
            elif col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = NAVY

s3.notes_slide.notes_text_frame.text = (
    "We evaluated five candidate vehicles against marketplace listings on Adey Market and a catalogue/model-level distributor review (Gezat Electric; no per-part search recorded). "
    "Seagull, Yuan Up, and bZ4X represent distinct market tiers: entry commuter, family crossover, and brand-equity premium."
)

# ==============================================================================
# SLIDE 4: EVIDENCE ARCHITECTURE & SOURCE LOG
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4, LIGHT_BG)
add_header(s4, "Evidence Architecture: 59 Observations Classified by Type (S001–S008)")

box4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
tf4 = box4.text_frame
tf4.word_wrap = True

p = tf4.paragraphs[0]
p.text = "Strict Evidence Attribution & Four Explicit Observation Types"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NAVY

sources_desc = [
    ("45 Supplier Catalogue Listings (S003 & S005): ", "Verified part listings with supplier-listed OE references and prices (35 Landin Seagull items, 10 Toyota bZ4X items). Note: S005 is a third-party aggregator catalogue, not official Toyota EPC."),
    ("8 Documented Catalogue Gaps (S003): ", "Confirmed negative search findings in Landin Parts (e.g. Seagull filter/wiper, and complete lack of Yuan Up listings). Treated as empirical supply constraints."),
    ("4 Unverified Trade Quotations (S008): ", "Overseas export directory quotes for Yuan Up. Part numbers are trade listing codes, not confirmed OEM EPC numbers. Scored conservatively (P=1, E=1)."),
    ("2 Safety Context Records (S006): ", "NHTSA defect records (Campaign 22V444 hub bolt recall; brake shudder). Documented strictly as platform stress context; decoupled from part demand/fitment."),
    ("S001, S002, S004, S007: ", "Adey Market local volume, Gezat catalogue/model-level review (no per-part search recorded), CQSW EQEA- prefix cross-check, and aftermarket catalogue cross-references.")
]

for title, desc in sources_desc:
    bp = tf4.add_paragraph()
    bp.space_before = Pt(8)
    run1 = bp.add_run()
    run1.text = "• " + title
    run1.font.bold = True
    run1.font.size = Pt(12)
    run1.font.color.rgb = TEAL
    run2 = bp.add_run()
    run2.text = desc
    run2.font.size = Pt(12)
    run2.font.color.rgb = CHARCOAL

s4.notes_slide.notes_text_frame.text = (
    "Our dataset contains 59 observations across four distinct categories. We enforce research honesty: "
    "only 45 rows are verified supplier catalogue listings. The 8 catalogue gaps, 4 unverified trade quotations, "
    "and 2 NHTSA safety context records are clearly distinguished."
)

# ==============================================================================
# SLIDE 5: DATA CLEANING & REPRODUCIBILITY
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5, LIGHT_BG)
add_header(s5, "Data Cleaning: Taxonomy Standardization & Missing Value Integrity")

c5_1 = s5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
tf5_1 = c5_1.text_frame
tf5_1.word_wrap = True

p = tf5_1.paragraphs[0]
p.text = "Cleaning Pipeline Transformations"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NAVY

transforms = [
    ("Taxonomy Harmonization: ", "Standardized irregular scraping labels (e.g. 'Bumpers' → 'Bumper', 'Fenders/body panels' → 'Fender / body panel')."),
    ("Currency Normalization: ", "Converted RMB and ETB prices to USD using fixed benchmark rates (0.14 USD/RMB, 0.008 USD/ETB). Retained original currency and amount for auditability."),
    ("Missing Value Preservation: ", "Preserved unpriced rows with price_missing = True. Never zero-filled or guessed catalogue prices."),
    ("NHTSA Isolation: ", "Excluded safety_context records from part cross-check counts so US recall records do not falsely inflate compatibility confidence.")
]

for title, desc in transforms:
    bp = tf5_1.add_paragraph()
    bp.space_before = Pt(8)
    r1 = bp.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(12)
    r1.font.color.rgb = NAVY
    r2 = bp.add_run()
    r2.text = desc
    r2.font.size = Pt(12)
    r2.font.color.rgb = CHARCOAL

c5_2 = s5.shapes.add_textbox(Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8))
tf5_2 = c5_2.text_frame
tf5_2.word_wrap = True

p = tf5_2.paragraphs[0]
p.text = "Pipeline Validation Summary"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NAVY

bullets5_2 = [
    ("Raw Observations: ", "59 rows, 19 columns in data/raw/raw_observations.csv."),
    ("Cleaned Observations: ", "59 rows, 23 columns in data/cleaned/cleaned_observations.csv."),
    ("Reproducibility Check: ", "Cleaned CSV loads flawlessly with pandas (0 tokenizing errors; fully quoted fields)."),
    ("Source ID Integrity: ", "All observations map 1:1 with data/source_log.csv (S003: 43, S005: 10, S008: 4, S006: 2).")
]

for title, desc in bullets5_2:
    bp = tf5_2.add_paragraph()
    bp.space_before = Pt(8)
    r1 = bp.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(12)
    r1.font.color.rgb = TEAL
    r2 = bp.add_run()
    r2.text = desc
    r2.font.size = Pt(12)
    r2.font.color.rgb = CHARCOAL

s5.notes_slide.notes_text_frame.text = (
    "Our data cleaning pipeline enforces total reproducibility. Commas inside descriptions are properly quoted, "
    "missing prices are preserved as True rather than zero-filled, and NHTSA records are excluded from part cross-checks."
)

# ==============================================================================
# SLIDE 6: MULTI-FACTOR SCORING METHODOLOGY
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6, LIGHT_BG)
add_header(s6, "Scoring Methodology: Grounded in Collected Evidence")

c6 = s6.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.0))
tf6 = c6.text_frame
tf6.word_wrap = True

p_f = tf6.paragraphs[0]
p_f.text = "Priority Score = 0.30·D + 0.25·S + 0.20·C + 0.15·P + 0.10·E"
p_f.font.size = Pt(20)
p_f.font.bold = True
p_f.font.color.rgb = NAVY
p_f.alignment = PP_ALIGN.CENTER

table6_shape = s6.shapes.add_table(6, 4, Inches(0.8), Inches(2.4), Inches(11.7), Inches(4.3))
t6 = table6_shape.table

t6.columns[0].width = Inches(2.4)
t6.columns[1].width = Inches(1.0)
t6.columns[2].width = Inches(4.4)
t6.columns[3].width = Inches(3.9)

h6 = ["Factor", "Weight", "Operational Definition (Empirical Basis)", "Scoring Range (1–5)"]
for i, h in enumerate(h6):
    cell = t6.cell(0, i)
    cell.text = h
    cell.fill.solid()
    cell.fill.fore_color.rgb = NAVY
    for p in cell.text_frame.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE

factors_data = [
    ("Demand Evidence Proxy (D)", "30%", "Vehicle volume on Adey Market + functional wear classification. (Indicative assessment; no workshop replacement rate measured).", "1 = Rare model / cosmetic\n5 = Top volume / primary wear"),
    ("Local Distributor Catalogue Gap (S)", "25%", "Degree of absence from the investigated catalogues (Landin S003 confirmed gaps; Gezat S002 reviewed at catalogue/model level only — no per-part search recorded, so local per-part availability is unverified).", "1 = Readily listed in an investigated catalogue\n5 = No listing in any investigated catalogue"),
    ("Vehicle Compatibility (C)", "20%", "Verification level: supplier-listed OE reference in named catalogue with model compatibility statement.", "1 = Catalogue gap\n5 = Confirmed OE in named catalogue"),
    ("Catalogue Sourcing Practicality (P)", "15%", "Active catalogue listing status and unit price visibility applied to primary evaluated application (<$50 -> 5, $50-$250 -> 4, >$250/Inquiry -> 3, gap -> 1).", "1 = Unverified quote / gap\n5 = Verified price < $50 USD"),
    ("Evidence Confidence (E)", "10%", "Number and independence of corroborating sources (Landin, CQSW benchmark, third-party catalogue).", "1 = Unverified quote / gap\n5 = Named catalogue + cross-check")
]

for row_idx, r in enumerate(factors_data, start=1):
    for col_idx, text in enumerate(r):
        cell = t6.cell(row_idx, col_idx)
        cell.text = text
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(10)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = NAVY
            elif col_idx == 1:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
                p.font.color.rgb = TEAL

s6.notes_slide.notes_text_frame.text = (
    "Our scoring rubric is strictly grounded in collected evidence. Demand is an indicative proxy based on Adey Market vehicle listings. "
    "Scarcity measures absence from the investigated catalogues (Landin S003 confirmed gaps; the Gezat S002 review was catalogue/model-level only with no per-part search recorded). "
    "Catalogue Sourcing Practicality evaluates verified catalogue pricing of the primary evaluated application without speculative shipping claims."
)

# ==============================================================================
# SLIDE 7: MATRIX HEATMAP & INSIGHTS
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7, LIGHT_BG)
add_header(s7, "Prioritization Heatmap: 30 Vehicle-Part Combinations")

if os.path.exists('reports/figures/scoring_matrix_heatmap.png'):
    s7.shapes.add_picture('reports/figures/scoring_matrix_heatmap.png', Inches(0.8), Inches(1.6), width=Inches(7.2))

c7 = s7.shapes.add_textbox(Inches(8.2), Inches(1.6), Inches(4.3), Inches(5.2))
tf7 = c7.text_frame
tf7.word_wrap = True

p = tf7.paragraphs[0]
p.text = "Key Analytical Findings"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NAVY

heat_insights = [
    ("Seagull Dominance: ", "Averages 3.96 across all categories. Complete supplier pricing and high local fleet presence elevate Seagull scores."),
    ("Toyota Realistic Ranking: ", "Averages 3.61. Third-party catalogue sourcing appropriately yields C=4 and E=3, placing bZ4X shock absorber at Rank 8 (Score 3.90)."),
    ("Yuan Up Sourcing Constraint: ", "High demand (5/5) but penalized by upstream catalogue absence on Landin and unverified trade quotes (P=1, E=1)."),
    ("Consumable & Contact Focus: ", "Side mirrors, brake pads, shock absorbers, bumpers, and headlights capture the top 5 positions.")
]

for title, desc in heat_insights:
    bp = tf7.add_paragraph()
    bp.space_before = Pt(10)
    r1 = bp.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = NAVY
    r2 = bp.add_run()
    r2.text = desc
    r2.font.size = Pt(11)
    r2.font.color.rgb = CHARCOAL

s7.notes_slide.notes_text_frame.text = (
    "Looking at our full 3x10 heatmap, BYD Seagull captures the highest priority scores because supplier catalogue pricing "
    "and supplier-listed OE references confirm immediate sourcing feasibility. Toyota bZ4X ranks realistically at 3.90 due to third-party catalogue labelling."
)

# ==============================================================================
# SLIDE 8: TOP 5 RECOMMENDATIONS (DEFENSIBLE & DISTINCT)
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8, LIGHT_BG)
add_header(s8, "Top 5 Recommendations: Prioritized Categories with Concrete OE Applications")

table8_shape = s8.shapes.add_table(6, 6, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
t8 = table8_shape.table

t8.columns[0].width = Inches(0.9)
t8.columns[1].width = Inches(1.8)
t8.columns[2].width = Inches(2.6)
t8.columns[3].width = Inches(1.2)
t8.columns[4].width = Inches(2.2)
t8.columns[5].width = Inches(3.0)

h8 = ["Rank", "Vehicle", "Part Category & Defined Application", "Score", "Catalogue Price", "Supplier-Listed OE Reference & Source"]
for i, h in enumerate(h8):
    cell = t8.cell(0, i)
    cell.text = h
    cell.fill.solid()
    cell.fill.fore_color.rgb = NAVY
    for p in cell.text_frame.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE

top5_data = [
    ("#1", "BYD Seagull", "Side mirror\n(LH mirror; companion RH)", "4.60", "429 RMB ($60.06 USD)\n(RH: 264 RMB / $36.96)", "EQEA-8202100 (LH) / EQEA-8202109\nLandin Parts (S003) catalogue listing (stock not stated)"),
    ("#2", "BYD Seagull", "Brake pads\n(Front pad set; companion Rear)", "4.45", "64 RMB ($8.96 USD)\n(Rear: 64 RMB / $8.96)", "EQEA-3501500CH (Front) / 3502140SS\nLandin Parts (S003) / CQSW"),
    ("#3", "BYD Seagull", "Shock absorber\n(Front strut LH; companion RH)", "4.45", "138 RMB ($19.32 USD)\n(RH: 138 RMB / $19.32)", "EQEA-2905100A (LH) / 2905200A\nLandin Parts (S003)"),
    ("#4", "BYD Seagull", "Bumper\n(Front bumper cover upper fascia)", "4.45", "198 RMB ($27.72 USD)", "EQEA-2083111 (OE flagged for supplier confirmation)\nLandin Parts (S003)"),
    ("#5", "BYD Seagull", "Headlight assembly\n(LH headlight; companion RH)", "4.30", "418 RMB ($58.52 USD)\n(RH: 418 RMB / $58.52)", "EQEA-4121010B (LH) / 4121020B\nLandin Parts (S003)")
]

for row_idx, r in enumerate(top5_data, start=1):
    for col_idx, text in enumerate(r):
        cell = t8.cell(row_idx, col_idx)
        cell.text = text
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(10)
            if col_idx == 0:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
                p.font.color.rgb = TEAL
            elif col_idx == 3:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
                p.font.color.rgb = NAVY
            elif col_idx == 1:
                p.font.bold = True

s8.notes_slide.notes_text_frame.text = (
    "Our top 5 recommendations represent prioritized part categories for the BYD Seagull, supported by specific supplier-listed OE applications and transparent catalogue prices. "
    "All five top recommendations are BYD Seagull parts, directly reflecting that Seagull is the only vehicle with 35 Landin catalogue listings (23 priced, 12 price on request; compatibility supplier-claimed, stock not stated). Toyota bZ4X shock absorber is at Rank 8 (3.90) due to honest third-party source labelling."
)

# ==============================================================================
# SLIDE 9: SENSITIVITY ANALYSIS & STABILITY VERIFICATION
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9, LIGHT_BG)
add_header(s9, "Sensitivity Analysis: Stability Across 4 Tested Scenarios")

if os.path.exists('reports/figures/sensitivity_comparison.png'):
    s9.shapes.add_picture('reports/figures/sensitivity_comparison.png', Inches(0.8), Inches(1.6), width=Inches(7.2))

c9 = s9.shapes.add_textbox(Inches(8.2), Inches(1.6), Inches(4.3), Inches(5.2))
tf9 = c9.text_frame
tf9.word_wrap = True

p = tf9.paragraphs[0]
p.text = "Mathematical Robustness"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NAVY

sc_notes = [
    ("4 Contrasting Scenarios Tested: ", "Baseline, Scarcity-First (30% S), Equal-Weights (20% each), and Evidence-Focused (20% E)."),
    ("100.0% Set Overlap: ", "The same five vehicle-category combinations remained in the top five across the four tested weighting scenarios (|Top5_base ∩ Top5_sc| / 5 = 1.0)."),
    ("Score Ranges: ", "Seagull mirror ranges from 4.55 to 4.65 across scenarios; brake pads, shock absorbers, and bumpers range from 4.45 to 4.60."),
    ("Defensible Interpretation: ", "The result demonstrates stability under these selected scenarios, not universal robustness or proven market demand.")
]

for title, desc in sc_notes:
    bp = tf9.add_paragraph()
    bp.space_before = Pt(10)
    r1 = bp.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = NAVY
    r2 = bp.add_run()
    r2.text = desc
    r2.font.size = Pt(11)
    r2.font.color.rgb = CHARCOAL

s9.notes_slide.notes_text_frame.text = (
    "Our sensitivity analysis verifies 100.0% set stability across four competing scenarios in notebook 04. "
    "The same five vehicle-category combinations remained in the top five across the four tested weighting scenarios. "
    "The result demonstrates stability under these selected scenarios, not universal robustness or proven market demand."
)

# ==============================================================================
# SLIDE 10: STRATEGIC IMPORT ROADMAP & LOGISTICS
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10, LIGHT_BG)
add_header(s10, "Strategic Import Roadmap: Two-Tier Logistics Allocation")

c10_1 = s10.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
tf10_1 = c10_1.text_frame
tf10_1.word_wrap = True

p = tf10_1.paragraphs[0]
p.text = "Phase 1: Air Cargo Fast-Turn (High-Exposure Wear)"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NAVY

p1_bullets = [
    ("Target Categories: ", "BYD Seagull Side Mirrors & Brake Pad Sets."),
    ("Logistics Mode: ", "Air cargo consolidation (Shenzhen/Guangzhou → Bole International, Addis Ababa)."),
    ("Commercial Rationale: ", "Compact volumetric size; rapid turnaround to address urgent vehicle downtime for high-exposure collision and wear parts."),
    ("Capital Exposure: ", "Low unit capital outlay ($8.96 pads, $36.96-$60.06 mirrors), mitigating initial foreign exchange exposure.")
]

for title, desc in p1_bullets:
    bp = tf10_1.add_paragraph()
    bp.space_before = Pt(8)
    r1 = bp.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(12)
    r1.font.color.rgb = TEAL
    r2 = bp.add_run()
    r2.text = desc
    r2.font.size = Pt(12)
    r2.font.color.rgb = CHARCOAL

c10_2 = s10.shapes.add_textbox(Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8))
tf10_2 = c10_2.text_frame
tf10_2.word_wrap = True

p = tf10_2.paragraphs[0]
p.text = "Phase 2: Ocean Freight Heavy-Stock (Consolidated)"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NAVY

p2_bullets = [
    ("Target Categories: ", "BYD Seagull Suspension Struts, Headlight Assemblies, & Bumper Covers."),
    ("Logistics Mode: ", "LCL/FCL ocean container (China → Port of Djibouti → Modjo Dry Port, Ethiopia)."),
    ("Commercial Rationale: ", "Heavy suspension dampers and bulky bumper covers require ocean freight consolidation to manage dimensional shipping costs effectively."),
    ("Order Timing: ", "Scheduled as planned inventory replenishment following initial market validation.")
]

for title, desc in p2_bullets:
    bp = tf10_2.add_paragraph()
    bp.space_before = Pt(8)
    r1 = bp.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(12)
    r1.font.color.rgb = NAVY
    r2 = bp.add_run()
    r2.text = desc
    r2.font.size = Pt(12)
    r2.font.color.rgb = CHARCOAL

s10.notes_slide.notes_text_frame.text = (
    "We translate our analytical ranking into a practical commercial roadmap. Phase 1 uses air cargo for compact, high-turnover wear items to minimize customer vehicle downtime. "
    "Phase 2 leverages ocean freight via Djibouti and Modjo Dry Port for heavier suspension dampers and bulky body panels to optimize freight efficiency."
)

# ==============================================================================
# SLIDE 11: LIMITATIONS & DATA BOUNDARIES
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11, LIGHT_BG)
add_header(s11, "Methodological Limitations & Honest Data Boundaries")

c11 = s11.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
tf11 = c11.text_frame
tf11.word_wrap = True

p = tf11.paragraphs[0]
p.text = "What Our Public Evidence Can and Cannot Claim"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NAVY

limits = [
    ("Demand Is An Indicative Assessment Proxy: ", "Grounded in Adey Market listing density and mechanical wear classification. Workshop replacement frequency was not surveyed."),
    ("No Brick-and-Mortar Survey: ", "Physical stock availability across Addis Ababa spare-parts shops was not surveyed; scarcity scores reflect investigated online catalogue gaps."),
    ("Marketplace Listings != Total Vehicle Fleet: ", "Adey Market's listings reflect advertised seller stock, not cumulative licensed EV registrations."),
    ("NHTSA Datasets Are Geographic Boundaries: ", "NHTSA recall campaigns reflect US-market investigations. Used strictly as platform engineering stress context, not direct local failure frequency."),
    ("Yuan Up Upstream Catalog Gap: ", "Landin Parts had zero listings for Yuan Up. We documented this gap rather than inventing part numbers."),
    ("Currency Exchange Volatility: ", "Prices benchmarked at 0.14 USD/RMB; parallel-market foreign exchange dynamics in Ethiopia will impact landed costs.")
]

for title, desc in limits:
    bp = tf11.add_paragraph()
    bp.space_before = Pt(8)
    r1 = bp.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(12)
    r1.font.color.rgb = RED
    r2 = bp.add_run()
    r2.text = desc
    r2.font.size = Pt(12)
    r2.font.color.rgb = CHARCOAL

s11.notes_slide.notes_text_frame.text = (
    "A defensible analysis must state its boundaries. We did not conduct physical shop visits in Addis Ababa. "
    "Adey Market listings represent active listings, not total registrations. Demand is an indicative proxy, and NHTSA recalls are US data used strictly for chassis stress context."
)

# ==============================================================================
# SLIDE 12: CONCLUSION & DEFENSE CHEATSHEET
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12, NAVY)

c12 = s12.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.7), Inches(5.8))
tf12 = c12.text_frame
tf12.word_wrap = True

p = tf12.paragraphs[0]
p.text = "KEY TAKEAWAYS & DEFENSE CHEATSHEET"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = WHITE

qas = [
    ("Q: Why did Seagull rank higher than Yuan Up if Yuan Up has more marketplace listings?",
     "A: Yuan Up has high demand presence on Adey Market, but investigated supplier catalogues (Landin S003) had zero public listings for Yuan Up. Seagull has 35 Landin catalogue listings (23 priced, 12 price on request; stock not stated), giving it far higher Catalogue Sourcing Practicality (P) and Evidence Confidence (E)."),
    ("Q: Why did Toyota bZ4X shock absorber drop to Rank 8?",
     "A: Because toyota-spare-parts.com is a third-party aggregator catalogue, not official Toyota EPC. Labeling it honestly lowered Compatibility from 5 to 4 and Confidence from 5 to 3, yielding an honest score of 3.90."),
    ("Q: How sensitive is the ranking to your weight selections?",
     "A: The same five vehicle-category combinations remained in the top five across the four tested weighting scenarios. The result demonstrates stability under these selected scenarios, not universal robustness or proven market demand.")
]

for q, a in qas:
    bp = tf12.add_paragraph()
    bp.space_before = Pt(14)
    rq = bp.add_run()
    rq.text = q + "\n"
    rq.font.bold = True
    rq.font.size = Pt(13)
    rq.font.color.rgb = TEAL
    ra = bp.add_run()
    ra.text = a
    ra.font.size = Pt(12)
    ra.font.color.rgb = RGBColor(241, 245, 249)

s12.notes_slide.notes_text_frame.text = (
    "In conclusion, this project delivers a defensible, reproducible, and robust recommendation system. "
    "By honoring data boundaries and grounding every score in verifiable evidence, we provide an importer with a clear, low-risk path. Thank you."
)

output_path = 'reports/EV_Spare_Parts_Prioritization_Presentation.pptx'
prs.save(output_path)
print(f"Successfully generated PowerPoint presentation at {output_path}")
