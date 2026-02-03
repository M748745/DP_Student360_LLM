"""
Fully Dynamic Entity Discovery System
======================================

This system uses PURE LLM DISCOVERY with ZERO guidance or examples.
The LLM analyzes the dataset and discovers entities based solely on data patterns.

NO predefined entity types.
NO examples.
NO templates.

PURE DATA-DRIVEN DISCOVERY.

Author: AI Assistant
Date: 2026-01-18
"""

import pandas as pd
import json
from typing import Dict, List, Any, Optional
from ollama import chat

# ============================================================================
# PHASE 1: AUTONOMOUS ENTITY DISCOVERY (NO GUIDANCE)
# ============================================================================

def discover_entities_autonomously(df: pd.DataFrame, ollama_model: str = "qwen2.5:7b") -> List[Dict[str, Any]]:
    """
    Phase 1: PURE autonomous entity discovery - NO examples, NO guidance.

    The LLM must discover entities by analyzing data patterns alone.

    Args:
        df: The student dataset
        ollama_model: The Ollama model to use

    Returns:
        List of discovered entities
    """

    # Get raw dataset statistics
    dataset_analysis = analyze_dataset_patterns(df)

    prompt = f"""You are analyzing a higher education dataset. Your task is to discover ENTITIES that exist in this data.

**WHAT IS AN ENTITY:**
An entity is a THING that:
1. Has a LIFECYCLE - it progresses through stages over time
2. Has STATUS CHANGES - it can be in different states
3. EVOLVES - its characteristics change

**DO NOT use any predetermined categories. DISCOVER entities from the data patterns below.**

**Dataset Analysis:**
{dataset_analysis}

**Your Task:**
Analyze the data patterns and discover 6-8 entities that have lifecycles. Base your discovery PURELY on what the data reveals.

**Discovery Process:**
1. Look for patterns in the data (correlations, distributions, trends)
2. Identify THINGS that change over time or have different states
3. Find groupings that reveal a progression or lifecycle
4. Discover relationships that suggest an entity's journey

**Rules:**
- DO NOT use predetermined entity types
- DISCOVER entities from data patterns
- Each entity must have a clear lifecycle (beginning → middle → end)
- Each entity must be trackable through different statuses
- Base entity names on what the DATA shows, not on assumptions

**Output Format (JSON only, no explanations):**
[
  {{
    "entity_id": "<unique_identifier>",
    "entity_name": "<descriptive name based on data patterns>",
    "entity_type": "<type you discovered>",
    "description": "<what this entity represents based on data>",
    "data_filter": {{"field": "value"}},
    "discovery_rationale": "<why this is an entity - what patterns in the data revealed it>",
    "student_count": <number>,
    "priority": <1-10>,
    "lifecycle_indicators": ["<status 1>", "<status 2>", ...]
  }}
]

**IMPORTANT:**
- Return ONLY valid JSON array, no markdown
- Base everything on DATA PATTERNS, not assumptions
- Discover 6-8 entities
- Each entity must be justified by data patterns
- Be creative - discover what's actually in the data"""

    try:
        response = chat(
            model=ollama_model,
            messages=[{
                'role': 'user',
                'content': prompt
            }],
            options={
                'temperature': 0.7,  # Higher temperature for creative discovery
                'num_predict': 2500
            }
        )

        entities_json = response['message']['content'].strip()

        # Clean JSON if wrapped in markdown
        if '```json' in entities_json:
            entities_json = entities_json.split('```json')[1].split('```')[0].strip()
        elif '```' in entities_json:
            entities_json = entities_json.split('```')[1].split('```')[0].strip()

        entities = json.loads(entities_json)

        print(f"✅ DISCOVERED {len(entities)} entities autonomously from data patterns")
        return entities

    except Exception as e:
        print(f"❌ Error in autonomous entity discovery: {str(e)}")
        return []


# ============================================================================
# PHASE 2: AUTONOMOUS STAGE DISCOVERY
# ============================================================================

def discover_stages_autonomously(
    entity: Dict[str, Any],
    df: pd.DataFrame,
    ollama_model: str = "qwen2.5:7b"
) -> List[Dict[str, Any]]:
    """
    Phase 2: Discover journey stages autonomously based on entity data patterns.

    NO predetermined stage templates. LLM discovers stages from data.

    Args:
        entity: Discovered entity from Phase 1
        df: The student dataset
        ollama_model: The Ollama model to use

    Returns:
        List of discovered stages
    """

    # Filter dataset for this entity
    from llm_entity_journey_system import filter_dataset_for_entity
    entity_data = filter_dataset_for_entity(df, entity)

    # Analyze entity data patterns
    entity_patterns = analyze_entity_patterns(entity_data)

    prompt = f"""You are analyzing a specific entity discovered in the data. Your task is to discover its LIFECYCLE STAGES.

**Entity Discovered:**
- Name: {entity['entity_name']}
- Type: {entity['entity_type']}
- Description: {entity['description']}
- Discovery Rationale: {entity.get('discovery_rationale', 'N/A')}

**Entity Data Patterns:**
{entity_patterns}

**Your Task:**
Analyze the data patterns and discover 4-6 lifecycle stages for this entity. Base your discovery PURELY on what the data reveals.

**Discovery Process:**
1. Look for natural transitions in the data (performance changes, status shifts, time-based progression)
2. Identify milestones or inflection points
3. Find patterns that suggest different phases
4. Discover the natural progression this entity follows

**Rules:**
- DO NOT use predetermined stage names
- DISCOVER stages from data patterns
- Each stage must be evident in the data
- Stages should follow a logical progression
- Base stage names on what the DATA shows

**Output Format (JSON only):**
[
  {{
    "stage_id": "<unique_id>",
    "stage_name": "<name based on data pattern>",
    "stage_order": <1, 2, 3...>,
    "description": "<what happens in this stage based on data>",
    "discovery_rationale": "<what data patterns revealed this stage>",
    "data_indicators": ["<metric 1>", "<metric 2>", ...]
  }}
]

**IMPORTANT:**
- Return ONLY valid JSON, no markdown
- Discover stages from DATA PATTERNS
- Include 4-6 stages in logical order
- Each stage must be justified by data evidence"""

    try:
        response = chat(
            model=ollama_model,
            messages=[{
                'role': 'user',
                'content': prompt
            }],
            options={
                'temperature': 0.7,
                'num_predict': 1800
            }
        )

        stages_json = response['message']['content'].strip()

        # Clean JSON
        if '```json' in stages_json:
            stages_json = stages_json.split('```json')[1].split('```')[0].strip()
        elif '```' in stages_json:
            stages_json = stages_json.split('```')[1].split('```')[0].strip()

        stages = json.loads(stages_json)

        print(f"  ✅ DISCOVERED {len(stages)} stages for {entity['entity_name']}")
        return stages

    except Exception as e:
        print(f"  ❌ Error discovering stages: {str(e)}")
        return []


# ============================================================================
# PHASE 3: NARRATIVE + VISUALIZATION GENERATION (SAME AS GUIDED)
# ============================================================================

def generate_narrative_for_discovered_stage(
    entity: Dict[str, Any],
    stage: Dict[str, Any],
    df: pd.DataFrame,
    ollama_model: str = "qwen2.5:7b"
) -> Dict[str, Any]:
    """
    Phase 3: Generate narrative for a discovered stage.

    This is the same as the guided version since we're telling the story
    of what we discovered.
    """

    from llm_entity_journey_system import (
        filter_dataset_for_entity,
        calculate_stage_metrics,
        generate_narrative_for_stage
    )

    # Use the same narrative generation since we're just describing what we found
    return generate_narrative_for_stage(entity, stage, df, ollama_model)


# ============================================================================
# COMPLETE AUTONOMOUS DISCOVERY PIPELINE
# ============================================================================

def generate_fully_dynamic_journeys(df: pd.DataFrame, ollama_model: str = "qwen2.5:7b") -> List[Dict[str, Any]]:
    """
    Complete autonomous discovery pipeline with ZERO guidance.

    Pipeline:
    1. LLM discovers entities from data patterns (NO examples)
    2. LLM discovers stages for each entity (NO templates)
    3. LLM generates narratives and visualizations

    Args:
        df: Student dataset
        ollama_model: Ollama model to use

    Returns:
        List of complete journeys discovered autonomously
    """

    print("\n" + "="*80)
    print("🔬 FULLY AUTONOMOUS ENTITY DISCOVERY (NO GUIDANCE)")
    print("="*80 + "\n")

    all_journeys = []

    # PHASE 1: Discover entities autonomously
    print("🔍 PHASE 1: Discovering entities from data patterns (NO examples)...")
    entities = discover_entities_autonomously(df, ollama_model)

    if not entities:
        print("❌ No entities discovered. Aborting.")
        return []

    print(f"\n✅ DISCOVERED {len(entities)} entities autonomously:\n")
    for ent in entities:
        print(f"   • {ent['entity_name']} ({ent['entity_type']}) - {ent.get('discovery_rationale', 'N/A')[:80]}...")

    # PHASE 2 & 3: For each discovered entity, discover stages and generate narratives
    for idx, entity in enumerate(entities, 1):
        print(f"\n{'='*80}")
        print(f"🎯 Processing Discovered Entity {idx}/{len(entities)}: {entity['entity_name']}")
        print(f"{'='*80}\n")

        # Discover stages autonomously
        print(f"  🔍 PHASE 2: Discovering lifecycle stages from data patterns...")
        stages = discover_stages_autonomously(entity, df, ollama_model)

        if not stages:
            print(f"  ❌ No stages discovered for {entity['entity_name']}, skipping.")
            continue

        # Generate narratives for discovered stages
        print(f"\n  ✍️  PHASE 3: Generating narratives for {len(stages)} discovered stages...")
        stage_narratives = []

        for stage in stages:
            narrative = generate_narrative_for_discovered_stage(entity, stage, df, ollama_model)
            stage_narratives.append({
                **stage,
                **narrative
            })

        # Compile complete journey
        complete_journey = {
            **entity,
            'stages': stage_narratives,
            'total_stages': len(stage_narratives),
            'discovery_method': 'FULLY_AUTONOMOUS'
        }

        all_journeys.append(complete_journey)

        print(f"\n  ✅ Completed autonomous discovery for {entity['entity_name']}")

    print("\n" + "="*80)
    print(f"✅ AUTONOMOUS DISCOVERY COMPLETE - {len(all_journeys)} journeys discovered")
    print("="*80 + "\n")

    return all_journeys


# ============================================================================
# HELPER FUNCTIONS - DATA PATTERN ANALYSIS
# ============================================================================

def analyze_dataset_patterns(df: pd.DataFrame) -> str:
    """
    Analyze dataset to reveal patterns for entity discovery.

    NO assumptions - just raw data patterns.
    """

    analysis = f"""
DATASET SIZE: {len(df)} records

AVAILABLE FIELDS: {', '.join(df.columns.tolist())}

FIELD ANALYSIS:
"""

    # Analyze each field
    for col in df.columns:
        if df[col].dtype == 'object' or df[col].nunique() < 50:
            # Categorical field
            unique_count = df[col].nunique()
            top_values = df[col].value_counts().head(5)
            analysis += f"\n{col}: {unique_count} unique values\n"
            analysis += f"  Top values: {dict(top_values)}\n"
        else:
            # Numerical field
            analysis += f"\n{col}: Numeric field\n"
            analysis += f"  Range: {df[col].min():.2f} - {df[col].max():.2f}\n"
            analysis += f"  Mean: {df[col].mean():.2f}, Median: {df[col].median():.2f}\n"

    # Correlation patterns
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 1:
        analysis += "\nCORRELATION PATTERNS:\n"
        corr_matrix = df[numeric_cols].corr()

        # Find strong correlations
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.3:
                    analysis += f"  {corr_matrix.columns[i]} <-> {corr_matrix.columns[j]}: {corr_value:.2f}\n"

    return analysis


def analyze_entity_patterns(entity_df: pd.DataFrame) -> str:
    """Analyze patterns within a specific entity's data."""

    if len(entity_df) == 0:
        return "No data available."

    analysis = f"""
ENTITY SIZE: {len(entity_df)} records

FIELD DISTRIBUTIONS:
"""

    for col in entity_df.columns:
        if entity_df[col].dtype == 'object' or entity_df[col].nunique() < 20:
            unique_count = entity_df[col].nunique()
            analysis += f"{col}: {unique_count} unique values\n"
        else:
            analysis += f"{col}: Range {entity_df[col].min():.2f} - {entity_df[col].max():.2f}\n"

    return analysis
