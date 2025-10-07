#!/usr/bin/env python3
"""
Data Models for CHI-Grants System
Defines structured data formats and validation schemas for grant information.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from datetime import datetime
from enum import Enum
import json
from pathlib import Path


class GrantType(Enum):
    """Types of grants."""
    RESEARCH = "Research"
    EDUCATION = "Education"
    INFRASTRUCTURE = "Infrastructure"
    TRAINING = "Training"
    EQUIPMENT = "Equipment"
    OTHER = "Other"


class GrantStatus(Enum):
    """Grant status options."""
    PENDING = "Pending"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    DECLINED = "Declined"
    WITHDRAWN = "Withdrawn"


class ConfidenceLevel(Enum):
    """Confidence levels for AI-extracted data."""
    HIGH = "high"        # 90-100% confidence
    MEDIUM = "medium"    # 70-89% confidence
    LOW = "low"          # 50-69% confidence
    UNCERTAIN = "uncertain"  # <50% confidence


@dataclass
class ExtractedField:
    """Represents a field extracted by AI with confidence scoring."""
    value: Union[str, float, int, List[str]]
    confidence: ConfidenceLevel
    source_text: Optional[str] = None  # Original text that led to extraction
    alternatives: List[str] = field(default_factory=list)  # Alternative interpretations


@dataclass
class BudgetSummary:
    """Budget breakdown for a grant."""
    personnel: Optional[ExtractedField] = None
    equipment: Optional[ExtractedField] = None
    travel: Optional[ExtractedField] = None
    supplies: Optional[ExtractedField] = None
    indirect_costs: Optional[ExtractedField] = None
    other: Optional[ExtractedField] = None
    total: Optional[ExtractedField] = None


@dataclass
class Timeline:
    """Grant timeline information."""
    application_date: Optional[ExtractedField] = None
    award_date: Optional[ExtractedField] = None
    project_start_date: Optional[ExtractedField] = None
    project_end_date: Optional[ExtractedField] = None
    duration_months: Optional[ExtractedField] = None


@dataclass
class TeamMember:
    """Team member information."""
    name: ExtractedField
    role: ExtractedField  # PI, Co-PI, Co-Investigator, etc.
    institution: Optional[ExtractedField] = None
    email: Optional[ExtractedField] = None


@dataclass
class ProjectInfo:
    """Project-specific information."""
    title: Optional[ExtractedField] = None
    abstract: Optional[ExtractedField] = None
    objectives: List[ExtractedField] = field(default_factory=list)
    keywords: List[ExtractedField] = field(default_factory=list)
    technical_approach: Optional[ExtractedField] = None


@dataclass
class ExtractionMetadata:
    """Metadata about the extraction process."""
    source_document: str
    extraction_timestamp: datetime
    ai_model_used: str
    processing_time_seconds: float
    total_pages: Optional[int] = None
    file_size_bytes: Optional[int] = None
    extraction_version: str = "1.0"


@dataclass
class ValidationFlags:
    """Flags for data validation issues."""
    missing_required_fields: List[str] = field(default_factory=list)
    inconsistent_dates: List[str] = field(default_factory=list)
    budget_calculation_errors: List[str] = field(default_factory=list)
    suspicious_values: List[str] = field(default_factory=list)
    needs_human_review: bool = False


@dataclass
class GrantData:
    """Complete grant information structure."""
    
    # Basic Information
    grant_id: Optional[ExtractedField] = None
    grant_name: Optional[ExtractedField] = None
    funding_agency: Optional[ExtractedField] = None
    award_amount: Optional[ExtractedField] = None
    grant_type: Optional[ExtractedField] = None
    
    # Timeline
    timeline: Timeline = field(default_factory=Timeline)
    
    # Team Information
    principal_investigator: Optional[TeamMember] = None
    co_investigators: List[TeamMember] = field(default_factory=list)
    other_personnel: List[TeamMember] = field(default_factory=list)
    
    # Project Information
    project: ProjectInfo = field(default_factory=ProjectInfo)
    
    # Budget
    budget: BudgetSummary = field(default_factory=BudgetSummary)
    
    # Status and Progress
    current_status: Optional[ExtractedField] = None
    progress_notes: Optional[ExtractedField] = None
    
    # Documents and Links
    proposal_document: Optional[str] = None
    award_letter: Optional[str] = None
    related_documents: List[str] = field(default_factory=list)
    
    # Metadata
    extraction_metadata: Optional[ExtractionMetadata] = None
    validation_flags: ValidationFlags = field(default_factory=ValidationFlags)
    
    # Custom fields for additional data
    custom_fields: Dict[str, ExtractedField] = field(default_factory=dict)


class GrantDataEncoder(json.JSONEncoder):
    """Custom JSON encoder for GrantData objects."""
    
    def default(self, obj):
        if isinstance(obj, (GrantData, Timeline, BudgetSummary, TeamMember, 
                          ProjectInfo, ExtractionMetadata, ValidationFlags, 
                          ExtractedField)):
            return obj.__dict__
        elif isinstance(obj, (GrantType, GrantStatus, ConfidenceLevel)):
            return obj.value
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class GrantDataValidator:
    """Validates grant data and provides feedback."""
    
    REQUIRED_FIELDS = [
        'grant_id', 'grant_name', 'funding_agency', 
        'award_amount', 'principal_investigator'
    ]
    
    @classmethod
    def validate(cls, grant_data: GrantData) -> ValidationFlags:
        """Validate grant data and return validation flags."""
        flags = ValidationFlags()
        
        # Check required fields
        for field_name in cls.REQUIRED_FIELDS:
            field_value = getattr(grant_data, field_name, None)
            if not field_value or not field_value.value:
                flags.missing_required_fields.append(field_name)
        
        # Check date consistency
        timeline = grant_data.timeline
        if (timeline.project_start_date and timeline.project_end_date and
            timeline.project_start_date.value and timeline.project_end_date.value):
            try:
                start_date = datetime.fromisoformat(timeline.project_start_date.value)
                end_date = datetime.fromisoformat(timeline.project_end_date.value)
                if start_date >= end_date:
                    flags.inconsistent_dates.append("Project start date is after end date")
            except ValueError:
                flags.inconsistent_dates.append("Invalid date format")
        
        # Check budget calculations
        budget = grant_data.budget
        if budget.total and budget.total.value:
            try:
                total = float(budget.total.value)
                calculated_total = 0
                
                for field_name in ['personnel', 'equipment', 'travel', 'supplies', 
                                 'indirect_costs', 'other']:
                    field_value = getattr(budget, field_name, None)
                    if field_value and field_value.value:
                        try:
                            calculated_total += float(field_value.value)
                        except (ValueError, TypeError):
                            pass
                
                # Allow for small rounding differences
                if abs(total - calculated_total) > 1000:  # $1000 tolerance
                    flags.budget_calculation_errors.append(
                        f"Budget total ({total}) doesn't match sum of components ({calculated_total})"
                    )
            except (ValueError, TypeError):
                flags.budget_calculation_errors.append("Invalid budget total format")
        
        # Check for suspicious values
        if grant_data.award_amount and grant_data.award_amount.value:
            try:
                amount = float(grant_data.award_amount.value)
                if amount <= 0:
                    flags.suspicious_values.append("Award amount is zero or negative")
                elif amount > 50000000:  # $50M threshold
                    flags.suspicious_values.append("Award amount seems unusually high")
            except (ValueError, TypeError):
                flags.suspicious_values.append("Award amount is not a valid number")
        
        # Check confidence levels
        low_confidence_fields = []
        for field_name, field_value in grant_data.__dict__.items():
            if isinstance(field_value, ExtractedField):
                if field_value.confidence in [ConfidenceLevel.LOW, ConfidenceLevel.UNCERTAIN]:
                    low_confidence_fields.append(field_name)
        
        if low_confidence_fields:
            flags.suspicious_values.append(
                f"Low confidence extraction for: {', '.join(low_confidence_fields)}"
            )
        
        # Determine if human review is needed
        flags.needs_human_review = bool(
            flags.missing_required_fields or 
            flags.inconsistent_dates or 
            flags.budget_calculation_errors or 
            len(flags.suspicious_values) > 2
        )
        
        return flags


def save_grant_data(grant_data: GrantData, filepath: str):
    """Save grant data to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(grant_data, f, cls=GrantDataEncoder, indent=2)


def load_grant_data(filepath: str) -> GrantData:
    """Load grant data from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    # Convert back to GrantData object (simplified reconstruction)
    # In a full implementation, you'd want more sophisticated deserialization
    grant_data = GrantData()
    
    # Basic reconstruction - this would need to be more comprehensive
    for key, value in data.items():
        if hasattr(grant_data, key):
            setattr(grant_data, key, value)
    
    return grant_data


def create_sample_grant_data() -> GrantData:
    """Create a sample grant data object for testing."""
    return GrantData(
        grant_id=ExtractedField("NSF-2024-001", ConfidenceLevel.HIGH),
        grant_name=ExtractedField("AI Research Initiative", ConfidenceLevel.HIGH),
        funding_agency=ExtractedField("National Science Foundation", ConfidenceLevel.HIGH),
        award_amount=ExtractedField(500000, ConfidenceLevel.MEDIUM),
        grant_type=ExtractedField(GrantType.RESEARCH.value, ConfidenceLevel.HIGH),
        principal_investigator=TeamMember(
            name=ExtractedField("Dr. Jane Smith", ConfidenceLevel.HIGH),
            role=ExtractedField("Principal Investigator", ConfidenceLevel.HIGH)
        ),
        timeline=Timeline(
            project_start_date=ExtractedField("2024-01-01", ConfidenceLevel.MEDIUM),
            project_end_date=ExtractedField("2026-12-31", ConfidenceLevel.MEDIUM)
        ),
        extraction_metadata=ExtractionMetadata(
            source_document="sample_grant.pdf",
            extraction_timestamp=datetime.now(),
            ai_model_used="gpt-4",
            processing_time_seconds=15.5
        )
    )


if __name__ == "__main__":
    # Create and validate sample data
    sample_data = create_sample_grant_data()
    validator = GrantDataValidator()
    flags = validator.validate(sample_data)
    
    print("Sample Grant Data Created")
    print(f"Validation flags: {flags}")
    
    # Save sample data
    save_grant_data(sample_data, "sample_grant_data.json")
    print("Sample data saved to sample_grant_data.json")