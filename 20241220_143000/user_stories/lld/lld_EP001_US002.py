# Low Level Design Document

## Objective
Design and implement a GxP and Non-GxP Event Classification system that automatically evaluates quality events for regulatory compliance requirements, ensuring appropriate classification based on FDA guidelines and product impact assessment.

## 1. Backend Python API Details

### 1.1 API Model

#### Routers
```python
# FastAPI Router Structure
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional

gxp_classification_router = APIRouter(
    prefix="/api/v1/gxp-classification",
    tags=["GxP Classification"]
)

@gxp_classification_router.post("/classify", response_model=ClassificationResponse)
@gxp_classification_router.post("/batch-classify", response_model=BatchClassificationResponse)
@gxp_classification_router.get("/classification/{event_id}", response_model=ClassificationResult)
@gxp_classification_router.put("/override/{event_id}", response_model=OverrideResponse)
```

#### Services
```python
# Service Layer Architecture
class GxPClassificationService:
    def __init__(self, classifier: GxPClassifier, validator: ClassificationValidator)
    async def classify_event(self, event_data: QualityEvent) -> ClassificationResult
    async def batch_classify_events(self, events: List[QualityEvent]) -> BatchClassificationResult
    async def override_classification(self, event_id: str, override_data: ClassificationOverride) -> OverrideResult

class GxPClassifier:
    def analyze_product_impact(self, event: QualityEvent) -> ProductImpactAnalysis
    def evaluate_regulatory_scope(self, event: QualityEvent) -> RegulatoryScope
    def calculate_confidence_score(self, analysis: ClassificationAnalysis) -> float
    def generate_decision_rationale(self, analysis: ClassificationAnalysis) -> str

class ClassificationValidator:
    def validate_input_completeness(self, event: QualityEvent) -> ValidationResult
    def validate_classification_confidence(self, result: ClassificationResult) -> bool
    def validate_regulatory_alignment(self, result: ClassificationResult) -> ComplianceCheck

class AuditTrailService:
    async def log_classification_decision(self, event_id: str, result: ClassificationResult) -> None
    async def log_override_action(self, event_id: str, override: ClassificationOverride) -> None
    async def generate_audit_report(self, date_range: DateRange) -> AuditReport
```

#### Schemas
```python
# Pydantic Models
from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime

class GxPClassification(str, Enum):
    GXP = "GxP"
    NON_GXP = "Non-GxP"

class ProductImpactLevel(str, Enum):
    DIRECT = "direct"
    INDIRECT = "indirect"
    NONE = "none"

class RegulatoryScope(str, Enum):
    FDA_21CFR = "FDA_21CFR"
    EMA_GMP = "EMA_GMP"
    ICH_Q7 = "ICH_Q7"
    NONE = "none"

class ClassificationInput(BaseModel):
    event_id: str
    event_type: str
    affected_systems: List[str]
    product_involvement: bool
    manufacturing_impact: bool
    quality_system_impact: bool
    patient_safety_risk: bool
    lifecycle_stage: str
    regulatory_context: Optional[Dict[str, Any]] = None

class ProductImpactAnalysis(BaseModel):
    impact_level: ProductImpactLevel
    affected_products: List[str]
    manufacturing_processes: List[str]
    quality_attributes: List[str]
    patient_safety_implications: bool

class ClassificationAnalysis(BaseModel):
    product_impact: ProductImpactAnalysis
    regulatory_scope: RegulatoryScope
    compliance_requirements: List[str]
    decision_factors: Dict[str, Any]

class ClassificationResult(BaseModel):
    event_id: str
    classification: GxPClassification
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    decision_rationale: str
    compliance_flags: List[str]
    required_documentation: List[str]
    analysis_details: ClassificationAnalysis
    classified_at: datetime
    classified_by: str

class ClassificationOverride(BaseModel):
    original_classification: GxPClassification
    new_classification: GxPClassification
    override_reason: str
    override_justification: str
    overridden_by: str
    requires_approval: bool = True

    @validator('override_reason')
    def validate_override_reason(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Override reason must be at least 10 characters')
        return v
```

#### Utilities
```python
# Utility Functions
class GxPRulesEngine:
    @staticmethod
    def evaluate_fda_21cfr_applicability(event: QualityEvent) -> bool
    @staticmethod
    def assess_product_lifecycle_impact(event: QualityEvent, lifecycle_stage: str) -> bool
    @staticmethod
    def calculate_patient_safety_risk(event: QualityEvent) -> float

class ComplianceUtils:
    @staticmethod
    def get_required_documentation(classification: GxPClassification) -> List[str]
    @staticmethod
    def determine_approval_workflow(event: QualityEvent, classification: GxPClassification) -> str
    @staticmethod
    def validate_regulatory_alignment(classification: ClassificationResult) -> bool

class ConfidenceCalculator:
    @staticmethod
    def calculate_weighted_confidence(factors: Dict[str, float], weights: Dict[str, float]) -> float
    @staticmethod
    def adjust_confidence_for_ambiguity(base_confidence: float, ambiguity_factors: List[str]) -> float
```

#### Exception Handling
```python
# Custom Exceptions
class GxPClassificationException(Exception):
    pass

class InsufficientDataException(GxPClassificationException):
    def __init__(self, missing_fields: List[str])

class ClassificationAmbiguityException(GxPClassificationException):
    def __init__(self, ambiguous_factors: List[str])

class RegulatoryComplianceException(GxPClassificationException):
    def __init__(self, compliance_issues: List[str])

class OverrideAuthorizationException(GxPClassificationException):
    def __init__(self, user_role: str, required_role: str)
```

### 1.2 API Details

#### REST Method: POST
**URL:** `/api/v1/gxp-classification/classify`

**Request JSON:**
```json
{
  "event_id": "QE001234",
  "event_type": "quality_deviation",
  "affected_systems": ["manufacturing_line_1", "quality_control"],
  "product_involvement": true,
  "manufacturing_impact": true,
  "quality_system_impact": true,
  "patient_safety_risk": false,
  "lifecycle_stage": "commercial_production",
  "regulatory_context": {
    "facility_type": "drug_manufacturing",
    "product_class": "prescription_drug",
    "regulatory_body": "FDA",
    "gmp_applicable": true
  }
}
```

**Response JSON:**
```json
{
  "event_id": "QE001234",
  "classification": "GxP",
  "confidence_score": 0.92,
  "decision_rationale": "Event classified as GxP due to direct product involvement in commercial manufacturing with quality system impact. Manufacturing process deviation affects drug product quality attributes.",
  "compliance_flags": [
    "FDA_21CFR_PART_211",
    "ENHANCED_DOCUMENTATION_REQUIRED",
    "REGULATORY_NOTIFICATION_REQUIRED"
  ],
  "required_documentation": [
    "deviation_investigation_report",
    "capa_plan",
    "regulatory_assessment",
    "batch_disposition_report"
  ],
  "analysis_details": {
    "product_impact": {
      "impact_level": "direct",
      "affected_products": ["DRUG_ABC_100MG"],
      "manufacturing_processes": ["tablet_compression", "coating"],
      "quality_attributes": ["dissolution", "content_uniformity"],
      "patient_safety_implications": false
    },
    "regulatory_scope": "FDA_21CFR",
    "compliance_requirements": [
      "21_CFR_211.192_production_record_review",
      "21_CFR_211.198_laboratory_records"
    ],
    "decision_factors": {
      "product_involvement_weight": 0.35,
      "manufacturing_impact_weight": 0.30,
      "quality_system_weight": 0.25,
      "regulatory_context_weight": 0.10
    }
  },
  "classified_at": "2024-12-20T14:30:00Z",
  "classified_by": "gxp_classification_engine_v2.1"
}
```

#### REST Method: POST
**URL:** `/api/v1/gxp-classification/batch-classify`

**Request JSON:**
```json
{
  "events": [
    {
      "event_id": "QE001234",
      "event_type": "quality_deviation",
      "product_involvement": true,
      "manufacturing_impact": true
    },
    {
      "event_id": "QE001235",
      "event_type": "system_failure",
      "product_involvement": false,
      "manufacturing_impact": false
    }
  ]
}
```

**Response JSON:**
```json
{
  "batch_id": "BATCH-20241220-001",
  "total_events": 2,
  "processed_events": 2,
  "failed_events": 0,
  "results": [
    {
      "event_id": "QE001234",
      "classification": "GxP",
      "confidence_score": 0.92
    },
    {
      "event_id": "QE001235",
      "classification": "Non-GxP",
      "confidence_score": 0.88
    }
  ],
  "processing_summary": {
    "gxp_events": 1,
    "non_gxp_events": 1,
    "average_confidence": 0.90,
    "processing_time_ms": 1250
  }
}
```

#### REST Method: PUT
**URL:** `/api/v1/gxp-classification/override/{event_id}`

**Request JSON:**
```json
{
  "original_classification": "Non-GxP",
  "new_classification": "GxP",
  "override_reason": "Additional regulatory review identified indirect product impact",
  "override_justification": "Upon further analysis, the IT system failure affected manufacturing execution system which has indirect impact on batch record integrity",
  "overridden_by": "quality_manager_001",
  "requires_approval": true
}
```

### 1.3 Functional Design

#### Class Diagram
```mermaid
classDiagram
    class GxPClassificationController {
        +classify_event(classification_input)
        +batch_classify_events(batch_input)
        +override_classification(event_id, override_data)
        +get_classification_history(event_id)
    }
    
    class GxPClassificationService {
        -classifier: GxPClassifier
        -validator: ClassificationValidator
        -audit_service: AuditTrailService
        +classify_event(event_data)
        +batch_classify_events(events)
        +override_classification(event_id, override_data)
    }
    
    class GxPClassifier {
        -rules_engine: GxPRulesEngine
        -confidence_calculator: ConfidenceCalculator
        +analyze_product_impact(event)
        +evaluate_regulatory_scope(event)
        +generate_classification_result(analysis)
    }
    
    class GxPRulesEngine {
        +evaluate_fda_21cfr_applicability(event)
        +assess_manufacturing_impact(event)
        +evaluate_quality_system_involvement(event)
        +assess_patient_safety_risk(event)
    }
    
    class ClassificationValidator {
        +validate_input_completeness(event)
        +validate_classification_confidence(result)
        +validate_regulatory_alignment(result)
    }
    
    class AuditTrailService {
        +log_classification_decision(event_id, result)
        +log_override_action(event_id, override)
        +generate_audit_report(date_range)
    }
    
    class ClassificationRepository {
        +save_classification_result(result)
        +find_by_event_id(event_id)
        +find_overrides_by_event_id(event_id)
        +get_classification_history(event_id)
    }
    
    GxPClassificationController --> GxPClassificationService
    GxPClassificationService --> GxPClassifier
    GxPClassificationService --> ClassificationValidator
    GxPClassificationService --> AuditTrailService
    GxPClassifier --> GxPRulesEngine
    GxPClassificationService --> ClassificationRepository
```

#### Sequence Diagram
```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    participant Classifier
    participant RulesEngine
    participant Validator
    participant AuditService
    participant Repository
    
    Client->>Controller: POST /classify
    Controller->>Service: classify_event(event_data)
    Service->>Validator: validate_input_completeness(event)
    
    alt Input Valid
        Validator-->>Service: ValidationResult(valid=True)
        Service->>Classifier: analyze_and_classify(event)
        Classifier->>RulesEngine: evaluate_fda_21cfr_applicability(event)
        RulesEngine-->>Classifier: applicability_result
        Classifier->>RulesEngine: assess_product_impact(event)
        RulesEngine-->>Classifier: impact_analysis
        Classifier->>Classifier: calculate_confidence_score(factors)
        Classifier->>Classifier: generate_decision_rationale(analysis)
        Classifier-->>Service: ClassificationResult
        
        Service->>Validator: validate_classification_confidence(result)
        alt Confidence Acceptable
            Validator-->>Service: validation_passed
            Service->>Repository: save_classification_result(result)
            Service->>AuditService: log_classification_decision(event_id, result)
            Service-->>Controller: ClassificationResult
            Controller-->>Client: 200 OK with classification
        else Low Confidence
            Validator-->>Service: confidence_too_low
            Service-->>Controller: ClassificationAmbiguityException
            Controller-->>Client: 422 Unprocessable Entity
        end
    else Input Invalid
        Validator-->>Service: ValidationResult(errors)
        Service-->>Controller: InsufficientDataException
        Controller-->>Client: 400 Bad Request
    end
```

#### Components
```mermaid
graph TB
    A[API Gateway] --> B[GxP Classification Controller]
    B --> C[GxP Classification Service]
    C --> D[GxP Classifier]
    C --> E[Classification Validator]
    C --> F[Audit Trail Service]
    D --> G[GxP Rules Engine]
    D --> H[Confidence Calculator]
    E --> I[Compliance Utils]
    F --> J[Audit Repository]
    C --> K[Classification Repository]
    G --> L[FDA Regulations DB]
    G --> M[Product Lifecycle DB]
    H --> N[ML Confidence Models]
```

### 1.4 Service Layer Business Logic

#### Classification Workflow
```python
# GxP Classification Workflow
class GxPClassificationWorkflow:
    async def execute_classification(self, event: QualityEvent) -> ClassificationResult:
        # Step 1: Input validation and preprocessing
        validation_result = await self.validate_input(event)
        if not validation_result.is_valid:
            raise InsufficientDataException(validation_result.missing_fields)
        
        # Step 2: Product impact analysis
        product_impact = await self.analyze_product_impact(event)
        
        # Step 3: Regulatory scope evaluation
        regulatory_scope = await self.evaluate_regulatory_scope(event)
        
        # Step 4: Decision factor analysis
        decision_factors = await self.analyze_decision_factors(event, product_impact, regulatory_scope)
        
        # Step 5: Classification determination
        classification = await self.determine_classification(decision_factors)
        
        # Step 6: Confidence calculation
        confidence_score = await self.calculate_confidence(decision_factors)
        
        # Step 7: Rationale generation
        rationale = await self.generate_rationale(classification, decision_factors)
        
        # Step 8: Compliance flag setting
        compliance_flags = await self.set_compliance_flags(classification, event)
        
        return ClassificationResult(
            event_id=event.event_id,
            classification=classification,
            confidence_score=confidence_score,
            decision_rationale=rationale,
            compliance_flags=compliance_flags,
            analysis_details=decision_factors
        )
```

#### Decision Rules Engine
```python
# GxP Decision Rules Implementation
class GxPDecisionRules:
    def __init__(self):
        self.rules = self._load_classification_rules()
    
    def evaluate_product_involvement_rule(self, event: QualityEvent) -> RuleResult:
        """Rule: Direct product involvement indicates GxP classification"""
        if event.product_involvement and event.manufacturing_impact:
            return RuleResult(
                rule_name="direct_product_involvement",
                result=True,
                weight=0.40,
                rationale="Event directly affects product manufacturing"
            )
        return RuleResult(rule_name="direct_product_involvement", result=False, weight=0.0)
    
    def evaluate_quality_system_rule(self, event: QualityEvent) -> RuleResult:
        """Rule: Quality system impact requires GxP consideration"""
        if event.quality_system_impact:
            affected_gxp_systems = self._check_gxp_system_involvement(event.affected_systems)
            if affected_gxp_systems:
                return RuleResult(
                    rule_name="quality_system_impact",
                    result=True,
                    weight=0.30,
                    rationale=f"Affects GxP systems: {', '.join(affected_gxp_systems)}"
                )
        return RuleResult(rule_name="quality_system_impact", result=False, weight=0.0)
    
    def evaluate_regulatory_context_rule(self, event: QualityEvent) -> RuleResult:
        """Rule: Regulatory context determines classification scope"""
        if event.regulatory_context:
            if event.regulatory_context.get('gmp_applicable', False):
                return RuleResult(
                    rule_name="regulatory_context",
                    result=True,
                    weight=0.20,
                    rationale="Event occurs in GMP-regulated environment"
                )
        return RuleResult(rule_name="regulatory_context", result=False, weight=0.0)
    
    def evaluate_patient_safety_rule(self, event: QualityEvent) -> RuleResult:
        """Rule: Patient safety risk elevates to GxP classification"""
        if event.patient_safety_risk:
            return RuleResult(
                rule_name="patient_safety_risk",
                result=True,
                weight=0.35,
                rationale="Event poses potential patient safety risk"
            )
        return RuleResult(rule_name="patient_safety_risk", result=False, weight=0.0)
```

#### Confidence Scoring Algorithm
```python
# Confidence Calculation Logic
class ConfidenceScoring:
    def __init__(self):
        self.base_weights = {
            'product_involvement': 0.35,
            'manufacturing_impact': 0.25,
            'quality_system_impact': 0.20,
            'regulatory_context': 0.15,
            'patient_safety_risk': 0.05
        }
    
    def calculate_classification_confidence(self, rule_results: List[RuleResult]) -> float:
        """Calculate confidence score based on rule evaluation results"""
        total_weight = 0.0
        weighted_score = 0.0
        
        for rule_result in rule_results:
            if rule_result.result:
                weighted_score += rule_result.weight * rule_result.confidence
                total_weight += rule_result.weight
        
        if total_weight == 0:
            return 0.0
        
        base_confidence = weighted_score / total_weight
        
        # Apply confidence adjustments
        adjusted_confidence = self._apply_confidence_adjustments(base_confidence, rule_results)
        
        return min(max(adjusted_confidence, 0.0), 1.0)
    
    def _apply_confidence_adjustments(self, base_confidence: float, rule_results: List[RuleResult]) -> float:
        """Apply adjustments for ambiguous or conflicting indicators"""
        # Reduce confidence for ambiguous cases
        ambiguity_penalty = self._calculate_ambiguity_penalty(rule_results)
        
        # Boost confidence for clear-cut cases
        clarity_bonus = self._calculate_clarity_bonus(rule_results)
        
        return base_confidence - ambiguity_penalty + clarity_bonus
```

#### Override Management
```python
# Classification Override Logic
class ClassificationOverrideManager:
    def __init__(self, authorization_service: AuthorizationService):
        self.auth_service = authorization_service
    
    async def process_override_request(self, event_id: str, override_data: ClassificationOverride) -> OverrideResult:
        # Step 1: Validate override authorization
        is_authorized = await self.auth_service.validate_override_permission(
            override_data.overridden_by,
            override_data.new_classification
        )
        
        if not is_authorized:
            raise OverrideAuthorizationException(
                user_role=override_data.overridden_by,
                required_role="quality_manager"
            )
        
        # Step 2: Validate override justification
        justification_valid = self._validate_override_justification(override_data)
        if not justification_valid:
            raise ValueError("Override justification insufficient")
        
        # Step 3: Create override record
        override_record = ClassificationOverrideRecord(
            event_id=event_id,
            original_classification=override_data.original_classification,
            new_classification=override_data.new_classification,
            override_reason=override_data.override_reason,
            justification=override_data.override_justification,
            overridden_by=override_data.overridden_by,
            overridden_at=datetime.utcnow(),
            requires_approval=override_data.requires_approval
        )
        
        # Step 4: Update classification
        await self.repository.save_override_record(override_record)
        await self.repository.update_event_classification(event_id, override_data.new_classification)
        
        # Step 5: Trigger approval workflow if required
        if override_data.requires_approval:
            await self.trigger_approval_workflow(override_record)
        
        return OverrideResult(
            override_id=override_record.override_id,
            status="pending_approval" if override_data.requires_approval else "approved",
            message="Override processed successfully"
        )
```

### 1.5 Service Integrations

#### Regulatory Database Integration
```python
# Regulatory Compliance Database Integration
class RegulatoryComplianceService:
    def __init__(self, compliance_db_url: str, api_key: str):
        self.compliance_db_url = compliance_db_url
        self.api_key = api_key
    
    async def get_fda_21cfr_requirements(self, event_type: str, facility_type: str) -> List[str]:
        """Retrieve applicable FDA 21 CFR requirements"""
        payload = {
            "event_type": event_type,
            "facility_type": facility_type,
            "regulation": "21_CFR"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.compliance_db_url}/requirements/lookup",
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            return response.json()["requirements"]
    
    async def validate_gmp_applicability(self, event_context: Dict[str, Any]) -> bool:
        """Validate if GMP regulations apply to the event context"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.compliance_db_url}/gmp/validate",
                json=event_context,
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()["gmp_applicable"]
```

#### Machine Learning Model Integration
```python
# ML Model Integration for Classification Enhancement
class MLClassificationEnhancer:
    def __init__(self, model_service_url: str):
        self.model_service_url = model_service_url
    
    async def enhance_classification_confidence(self, event_data: QualityEvent, rule_based_result: ClassificationResult) -> float:
        """Use ML model to enhance confidence scoring"""
        ml_input = {
            "event_features": self._extract_features(event_data),
            "rule_based_classification": rule_based_result.classification,
            "rule_based_confidence": rule_based_result.confidence_score
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.model_service_url}/enhance-confidence",
                json=ml_input
            )
            response.raise_for_status()
            return response.json()["enhanced_confidence"]
    
    def _extract_features(self, event: QualityEvent) -> Dict[str, Any]:
        """Extract features for ML model input"""
        return {
            "event_type_encoded": self._encode_event_type(event.event_type),
            "system_count": len(event.affected_systems),
            "has_product_involvement": event.product_involvement,
            "has_manufacturing_impact": event.manufacturing_impact,
            "has_quality_system_impact": event.quality_system_impact,
            "lifecycle_stage_encoded": self._encode_lifecycle_stage(event.lifecycle_stage)
        }
```

## 2. Frontend React Details

### 2.1 UI Architecture

#### Component Structure
```typescript
// Component Hierarchy
GxPClassificationPage
├── ClassificationRequestForm
│   ├── EventDetailsSection
│   ├── ProductImpactSection
│   ├── RegulatoryContextSection
│   └── ClassificationTrigger
├── ClassificationResultDisplay
│   ├── ClassificationBadge
│   ├── ConfidenceIndicator
│   ├── DecisionRationale
│   └── ComplianceFlags
├── OverrideManagement
│   ├── OverrideRequestForm
│   ├── OverrideJustification
│   └── ApprovalWorkflow
└── ClassificationHistory
    ├── HistoryTimeline
    ├── OverrideLog
    └── AuditTrail
```

#### State Management
```typescript
// Redux Store Structure
interface GxPClassificationState {
  classification: {
    currentRequest: ClassificationRequest | null;
    result: ClassificationResult | null;
    isClassifying: boolean;
    error: string | null;
  };
  override: {
    overrideRequest: OverrideRequest | null;
    isProcessing: boolean;
    approvalStatus: ApprovalStatus | null;
  };
  history: {
    classifications: ClassificationHistory[];
    overrides: OverrideHistory[];
    isLoading: boolean;
  };
}
```

### 2.2 UI Specifications

#### Classification Request Form
```typescript
// Classification Form Interface
interface ClassificationFormProps {
  onSubmit: (request: ClassificationRequest) => void;
  isProcessing: boolean;
  validationErrors: ValidationError[];
}

interface ClassificationRequest {
  eventId: string;
  eventType: string;
  productInvolvement: boolean;
  manufacturingImpact: boolean;
  qualitySystemImpact: boolean;
  patientSafetyRisk: boolean;
  lifecycleStage: string;
  regulatoryContext: RegulatoryContext;
}

// Form Component
const ClassificationRequestForm: React.FC<ClassificationFormProps> = ({
  onSubmit,
  isProcessing,
  validationErrors
}) => {
  const [formData, setFormData] = useState<ClassificationRequest>(initialFormData);
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="classification-form">
      <EventDetailsSection 
        eventId={formData.eventId}
        eventType={formData.eventType}
        onChange={(field, value) => setFormData({...formData, [field]: value})}
      />
      
      <ProductImpactSection
        productInvolvement={formData.productInvolvement}
        manufacturingImpact={formData.manufacturingImpact}
        onChange={(field, value) => setFormData({...formData, [field]: value})}
      />
      
      <RegulatoryContextSection
        regulatoryContext={formData.regulatoryContext}
        onChange={(context) => setFormData({...formData, regulatoryContext: context})}
      />
      
      <button 
        type="submit" 
        disabled={isProcessing}
        className="classify-button"
      >
        {isProcessing ? 'Classifying...' : 'Classify Event'}
      </button>
    </form>
  );
};
```

#### Classification Result Display
```typescript
// Result Display Component
const ClassificationResultDisplay: React.FC<{
  result: ClassificationResult;
  onOverrideRequest: () => void;
}> = ({ result, onOverrideRequest }) => {
  return (
    <div className="classification-result">
      <div className="result-header">
        <ClassificationBadge 
          classification={result.classification}
          confidence={result.confidenceScore}
        />
        <ConfidenceIndicator score={result.confidenceScore} />
      </div>
      
      <div className="result-details">
        <DecisionRationale rationale={result.decisionRationale} />
        <ComplianceFlags flags={result.complianceFlags} />
        <RequiredDocumentation documents={result.requiredDocumentation} />
      </div>
      
      <div className="result-actions">
        <button onClick={onOverrideRequest} className="override-button">
          Request Override
        </button>
        <button className="export-button">
          Export Classification Report
        </button>
      </div>
    </div>
  );
};
```

### 2.3 API Integration

#### Classification API Service
```typescript
// API Service Implementation
class GxPClassificationApiService {
  private baseUrl: string;
  private httpClient: HttpClient;

  async classifyEvent(request: ClassificationRequest): Promise<ClassificationResult> {
    const response = await this.httpClient.post<ClassificationResult>(
      '/api/v1/gxp-classification/classify',
      request
    );
    return response.data;
  }

  async batchClassifyEvents(events: ClassificationRequest[]): Promise<BatchClassificationResult> {
    const response = await this.httpClient.post<BatchClassificationResult>(
      '/api/v1/gxp-classification/batch-classify',
      { events }
    );
    return response.data;
  }

  async requestOverride(eventId: string, overrideData: OverrideRequest): Promise<OverrideResult> {
    const response = await this.httpClient.put<OverrideResult>(
      `/api/v1/gxp-classification/override/${eventId}`,
      overrideData
    );
    return response.data;
  }

  async getClassificationHistory(eventId: string): Promise<ClassificationHistory[]> {
    const response = await this.httpClient.get<ClassificationHistory[]>(
      `/api/v1/gxp-classification/history/${eventId}`
    );
    return response.data;
  }
}
```

#### React Hooks Integration
```typescript
// Custom Hooks for GxP Classification
const useGxPClassification = () => {
  const [isClassifying, setIsClassifying] = useState(false);
  const [result, setResult] = useState<ClassificationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const classifyEvent = async (request: ClassificationRequest) => {
    setIsClassifying(true);
    setError(null);
    
    try {
      const classificationResult = await gxpClassificationApi.classifyEvent(request);
      setResult(classificationResult);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsClassifying(false);
    }
  };

  const requestOverride = async (eventId: string, overrideData: OverrideRequest) => {
    try {
      const overrideResult = await gxpClassificationApi.requestOverride(eventId, overrideData);
      return overrideResult;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  return {
    classifyEvent,
    requestOverride,
    isClassifying,
    result,
    error
  };
};
```

## 3. Database Details

### 3.1 ER Diagram

```mermaid
erDiagram
    GXP_CLASSIFICATIONS {
        string classification_id PK
        string event_id FK
        string classification
        float confidence_score
        text decision_rationale
        json compliance_flags
        json required_documentation
        json analysis_details
        datetime classified_at
        string classified_by
        string model_version
    }
    
    CLASSIFICATION_RULES {
        string rule_id PK
        string rule_name
        text rule_description
        json rule_logic
        float rule_weight
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    
    CLASSIFICATION_OVERRIDES {
        string override_id PK
        string event_id FK
        string classification_id FK
        string original_classification
        string new_classification
        text override_reason
        text override_justification
        string overridden_by
        datetime overridden_at
        boolean requires_approval
        string approval_status
        string approved_by
        datetime approved_at
    }
    
    REGULATORY_CONTEXT {
        string context_id PK
        string event_id FK
        string facility_type
        string product_class
        string regulatory_body
        boolean gmp_applicable
        json compliance_requirements
        datetime created_at
    }
    
    AUDIT_TRAIL {
        string audit_id PK
        string event_id FK
        string action_type
        string performed_by
        json action_details
        datetime action_timestamp
        string ip_address
        string user_agent
    }
    
    GXP_CLASSIFICATIONS ||--o{ CLASSIFICATION_OVERRIDES : "can_have"
    GXP_CLASSIFICATIONS ||--|| REGULATORY_CONTEXT : "has"
    GXP_CLASSIFICATIONS ||--o{ AUDIT_TRAIL : "generates"
    CLASSIFICATION_OVERRIDES ||--o{ AUDIT_TRAIL : "generates"
```

### 3.2 Database Validations

#### Table Constraints
```sql
-- GxP Classifications Table
CREATE TABLE gxp_classifications (
    classification_id VARCHAR(50) PRIMARY KEY,
    event_id VARCHAR(50) NOT NULL,
    classification VARCHAR(20) NOT NULL CHECK (classification IN ('GxP', 'Non-GxP')),
    confidence_score DECIMAL(3,2) NOT NULL CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
    decision_rationale TEXT NOT NULL,
    compliance_flags JSON NOT NULL,
    required_documentation JSON NOT NULL,
    analysis_details JSON NOT NULL,
    classified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    classified_by VARCHAR(100) NOT NULL,
    model_version VARCHAR(20) NOT NULL,
    UNIQUE KEY uk_event_classification (event_id, classified_at)
);

-- Classification Overrides Table
CREATE TABLE classification_overrides (
    override_id VARCHAR(50) PRIMARY KEY,
    event_id VARCHAR(50) NOT NULL,
    classification_id VARCHAR(50) NOT NULL,
    original_classification VARCHAR(20) NOT NULL CHECK (original_classification IN ('GxP', 'Non-GxP')),
    new_classification VARCHAR(20) NOT NULL CHECK (new_classification IN ('GxP', 'Non-GxP')),
    override_reason TEXT NOT NULL CHECK (LENGTH(override_reason) >= 10),
    override_justification TEXT NOT NULL CHECK (LENGTH(override_justification) >= 20),
    overridden_by VARCHAR(100) NOT NULL,
    overridden_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    requires_approval BOOLEAN DEFAULT TRUE,
    approval_status VARCHAR(20) DEFAULT 'pending' CHECK (approval_status IN ('pending', 'approved', 'rejected')),
    approved_by VARCHAR(100),
    approved_at TIMESTAMP,
    FOREIGN KEY (classification_id) REFERENCES gxp_classifications(classification_id)
);

-- Indexes
CREATE INDEX idx_gxp_classifications_event_id ON gxp_classifications(event_id);
CREATE INDEX idx_gxp_classifications_classification ON gxp_classifications(classification);
CREATE INDEX idx_gxp_classifications_confidence ON gxp_classifications(confidence_score);
CREATE INDEX idx_classification_overrides_event_id ON classification_overrides(event_id);
CREATE INDEX idx_classification_overrides_status ON classification_overrides(approval_status);
```

#### Business Rule Constraints
```sql
-- Confidence score validation for production classifications
ALTER TABLE gxp_classifications ADD CONSTRAINT chk_production_confidence 
CHECK (
    (model_version NOT LIKE '%dev%') OR 
    (model_version LIKE '%dev%' AND confidence_score >= 0.7)
);

-- Override approval requirement for GxP to Non-GxP changes
ALTER TABLE classification_overrides ADD CONSTRAINT chk_gxp_override_approval 
CHECK (
    (original_classification != 'GxP' OR new_classification != 'Non-GxP') OR 
    (original_classification = 'GxP' AND new_classification = 'Non-GxP' AND requires_approval = TRUE)
);

-- Approval timestamp consistency
ALTER TABLE classification_overrides ADD CONSTRAINT chk_approval_timestamp 
CHECK (
    (approval_status = 'pending' AND approved_at IS NULL) OR
    (approval_status IN ('approved', 'rejected') AND approved_at IS NOT NULL)
);
```

## 4. Non-Functional Requirements

### 4.1 Performance

#### Classification Performance Requirements
- Classification response time: < 3 seconds for single event
- Batch classification: < 10 seconds for 50 events
- Confidence calculation: < 1 second
- Override processing: < 2 seconds

#### Performance Optimization
```python
# Caching Strategy for Classification Rules
from redis import Redis
import json

class ClassificationRulesCache:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.cache_ttl = 3600  # 1 hour
    
    async def get_cached_rules(self, rule_type: str) -> Optional[List[Dict]]:
        cache_key = f"classification_rules:{rule_type}"
        cached_rules = await self.redis.get(cache_key)
        return json.loads(cached_rules) if cached_rules else None
    
    async def cache_rules(self, rule_type: str, rules: List[Dict]) -> None:
        cache_key = f"classification_rules:{rule_type}"
        await self.redis.setex(cache_key, self.cache_ttl, json.dumps(rules))

# Async Processing for Batch Classifications
class BatchClassificationProcessor:
    async def process_batch_async(self, events: List[QualityEvent]) -> BatchClassificationResult:
        # Process events in parallel using asyncio
        tasks = [self.classify_single_event(event) for event in events]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful_results = []
        failed_results = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed_results.append({
                    'event_id': events[i].event_id,
                    'error': str(result)
                })
            else:
                successful_results.append(result)
        
        return BatchClassificationResult(
            successful_results=successful_results,
            failed_results=failed_results,
            processing_time=time.time() - start_time
        )
```

### 4.2 Security

#### Classification Data Security
```python
# Secure Classification Processing
from cryptography.fernet import Fernet
import hashlib

class SecureClassificationProcessor:
    def __init__(self, encryption_key: bytes):
        self.cipher_suite = Fernet(encryption_key)
    
    def encrypt_sensitive_classification_data(self, classification_result: ClassificationResult) -> ClassificationResult:
        """Encrypt sensitive fields in classification results"""
        encrypted_result = classification_result.copy()
        
        # Encrypt decision rationale if it contains sensitive information
        if self._contains_sensitive_info(classification_result.decision_rationale):
            encrypted_result.decision_rationale = self.cipher_suite.encrypt(
                classification_result.decision_rationale.encode()
            ).decode()
        
        return encrypted_result
    
    def hash_event_data_for_audit(self, event_data: QualityEvent) -> str:
        """Generate hash of event data for audit trail integrity"""
        event_string = json.dumps(event_data.dict(), sort_keys=True)
        return hashlib.sha256(event_string.encode()).hexdigest()

# Role-based Access Control for Overrides
class OverrideAuthorizationService:
    def __init__(self):
        self.role_permissions = {
            'quality_analyst': ['view_classifications'],
            'quality_manager': ['view_classifications', 'request_override'],
            'quality_director': ['view_classifications', 'request_override', 'approve_override'],
            'regulatory_affairs': ['view_classifications', 'approve_gxp_overrides']
        }
    
    async def validate_override_permission(self, user_id: str, override_type: str) -> bool:
        user_role = await self.get_user_role(user_id)
        required_permission = self._get_required_permission(override_type)
        return required_permission in self.role_permissions.get(user_role, [])
```

### 4.3 Logging and Monitoring

#### Classification Audit Logging
```python
# Comprehensive Audit Logging
import structlog
from datetime import datetime

class GxPClassificationAuditor:
    def __init__(self):
        self.logger = structlog.get_logger()
    
    async def log_classification_decision(self, event_id: str, result: ClassificationResult, user_id: str):
        self.logger.info(
            "gxp_classification_completed",
            event_id=event_id,
            classification=result.classification,
            confidence_score=result.confidence_score,
            model_version=result.classified_by,
            user_id=user_id,
            timestamp=datetime.utcnow().isoformat(),
            compliance_flags=result.compliance_flags
        )
    
    async def log_override_request(self, override_data: ClassificationOverride):
        self.logger.warning(
            "gxp_classification_override_requested",
            event_id=override_data.event_id,
            original_classification=override_data.original_classification,
            new_classification=override_data.new_classification,
            overridden_by=override_data.overridden_by,
            override_reason=override_data.override_reason,
            requires_approval=override_data.requires_approval,
            timestamp=datetime.utcnow().isoformat()
        )
    
    async def log_low_confidence_classification(self, event_id: str, confidence_score: float):
        self.logger.warning(
            "gxp_classification_low_confidence",
            event_id=event_id,
            confidence_score=confidence_score,
            threshold=0.7,
            recommendation="manual_review_required",
            timestamp=datetime.utcnow().isoformat()
        )
```

#### Performance Monitoring
```python
# Performance Metrics Collection
from prometheus_client import Counter, Histogram, Gauge

# Metrics
gxp_classifications_total = Counter('gxp_classifications_total', 'Total GxP classifications', ['classification_type'])
classification_duration = Histogram('gxp_classification_duration_seconds', 'Classification processing time')
classification_confidence = Histogram('gxp_classification_confidence', 'Classification confidence scores')
override_requests_total = Counter('gxp_override_requests_total', 'Total override requests', ['override_type'])

class ClassificationMetricsCollector:
    @staticmethod
    def record_classification(classification: str, duration: float, confidence: float):
        gxp_classifications_total.labels(classification_type=classification).inc()
        classification_duration.observe(duration)
        classification_confidence.observe(confidence)
    
    @staticmethod
    def record_override_request(override_type: str):
        override_requests_total.labels(override_type=override_type).inc()
```

## 5. Dependencies

### 5.1 Backend Dependencies
```python
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
alembic==1.13.0
asyncpg==0.29.0
redis==5.0.1
httpx==0.25.2
python-jose[cryptography]==3.3.0
scikit-learn==1.3.2
numpy==1.24.3
pandas==2.0.3
structlog==23.2.0
prometheus-client==0.19.0
cryptography==41.0.8
dependency-injector==4.41.0
pytest==7.4.3
pytest-asyncio==0.21.1
```

### 5.2 Frontend Dependencies
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "@reduxjs/toolkit": "^1.9.1",
    "react-redux": "^8.0.5",
    "axios": "^1.3.0",
    "react-hook-form": "^7.43.0",
    "yup": "^1.0.0",
    "@hookform/resolvers": "^2.9.10",
    "react-query": "^3.39.3",
    "material-ui": "^5.11.0",
    "recharts": "^2.5.0",
    "typescript": "^4.9.4"
  }
}
```

### 5.3 Infrastructure Dependencies
- PostgreSQL 15+ (with JSON support)
- Redis 7+ (for caching and session management)
- Docker & Docker Compose
- Kubernetes (for production deployment)
- Prometheus & Grafana (monitoring)
- ELK Stack (logging and audit trail)

## 6. Assumptions

1. **Regulatory Database Access**
   - Access to current FDA 21 CFR Part 11 and Part 211 requirements
   - Regulatory compliance database is maintained and up-to-date
   - API access to regulatory guidance documents

2. **Event Data Quality**
   - Quality events contain sufficient context for accurate classification
   - Event data structure is consistent across different source systems
   - Required regulatory fields are populated when applicable

3. **Classification Rules**
   - GxP determination rules are validated by regulatory affairs team
   - Classification logic aligns with current FDA guidance
   - Rules engine is regularly updated to reflect regulatory changes

4. **User Authorization**
   - User roles and permissions are managed by upstream identity system
   - Override authorization workflows are defined by quality management
   - Approval processes are documented and enforced

5. **Performance Requirements**
   - Classification accuracy requirements are defined by business stakeholders
   - Confidence thresholds are validated through historical data analysis
   - Performance benchmarks are established based on operational needs

6. **Audit and Compliance**
   - Audit trail requirements comply with 21 CFR Part 11
   - Data retention policies are established for classification records
   - Electronic signature requirements are defined for overrides

7. **Integration Dependencies**
   - Machine learning models are available for confidence enhancement
   - Regulatory compliance services provide real-time validation
   - Notification systems support priority alerting for GxP events