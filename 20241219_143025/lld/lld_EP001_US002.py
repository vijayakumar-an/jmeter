# Low Level Design Document

## Epic ID: EP001
## User Story ID: US002
## Title: System Event Evaluation and Decision Making

---

## 1. Objective

Design and implement an automated system event evaluation engine that processes quality events for GxP classification, severity assessment, and change control requirements with high accuracy and regulatory compliance.

---

## 2. Backend Spring Boot API Details

### 2.1 API Model

```java
// System Event Evaluation Model
@Entity
@Table(name = "system_evaluations")
public class SystemEvaluation {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull
    @Column(name = "evaluation_id")
    private String evaluationId;
    
    @NotNull
    @Column(name = "event_id")
    private String eventId;
    
    @NotNull
    @Column(name = "gxp_classification")
    @Enumerated(EnumType.STRING)
    private GxPClassification gxpClassification;
    
    @NotNull
    @Column(name = "severity_level")
    @Enumerated(EnumType.STRING)
    private SeverityLevel severityLevel;
    
    @NotNull
    @Column(name = "change_control_required")
    private Boolean changeControlRequired;
    
    @Column(name = "confidence_score")
    private Double confidenceScore;
    
    @Column(name = "evaluation_rationale", columnDefinition = "TEXT")
    private String evaluationRationale;
    
    @Column(name = "regulatory_references", columnDefinition = "JSON")
    private String regulatoryReferences;
    
    @NotNull
    @Column(name = "evaluation_status")
    @Enumerated(EnumType.STRING)
    private EvaluationStatus evaluationStatus;
    
    @NotNull
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "evaluation_timestamp")
    private Date evaluationTimestamp;
    
    @Column(name = "processing_time_ms")
    private Long processingTimeMs;
    
    @Column(name = "evaluation_engine_version")
    private String evaluationEngineVersion;
    
    // Getters and Setters
}

// Evaluation Request Model
public class SystemEvaluationRequest {
    @NotNull
    private String eventId;
    @NotNull
    private String eventType;
    @NotNull
    private String description;
    @NotNull
    private String sourceSystem;
    private String productLine;
    private String regulatoryRegion;
    private String impactArea;
    private Map<String, Object> additionalContext;
    
    // Getters and Setters
}

// Evaluation Response Model
public class SystemEvaluationResponse {
    private String evaluationId;
    private String eventId;
    private GxPClassification gxpClassification;
    private SeverityLevel severityLevel;
    private Boolean changeControlRequired;
    private Double confidenceScore;
    private String evaluationRationale;
    private List<String> regulatoryReferences;
    private EvaluationStatus evaluationStatus;
    private Date evaluationTimestamp;
    private Long processingTimeMs;
    private List<String> flaggedForReview;
    
    // Getters and Setters
}

// Enums
public enum GxPClassification {
    GXP, NON_GXP, REQUIRES_REVIEW
}

public enum SeverityLevel {
    CRITICAL, MAJOR, MINOR, NEGLIGIBLE
}

public enum EvaluationStatus {
    COMPLETED, PENDING_REVIEW, FAILED, IN_PROGRESS
}
```

### 2.2 API Details

```java
@RestController
@RequestMapping("/api/v1/system-evaluation")
@Validated
public class SystemEvaluationController {
    
    @Autowired
    private SystemEvaluationService systemEvaluationService;
    
    @PostMapping("/evaluate")
    @ResponseStatus(HttpStatus.OK)
    public ResponseEntity<SystemEvaluationResponse> evaluateEvent(
            @Valid @RequestBody SystemEvaluationRequest request) {
        
        SystemEvaluationResponse response = systemEvaluationService.evaluateEvent(request);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/batch-evaluate")
    public ResponseEntity<List<SystemEvaluationResponse>> batchEvaluateEvents(
            @Valid @RequestBody List<SystemEvaluationRequest> requests) {
        
        List<SystemEvaluationResponse> responses = systemEvaluationService.batchEvaluateEvents(requests);
        return ResponseEntity.ok(responses);
    }
    
    @GetMapping("/evaluation/{evaluationId}")
    public ResponseEntity<SystemEvaluationResponse> getEvaluation(
            @PathVariable String evaluationId) {
        
        SystemEvaluationResponse response = systemEvaluationService.getEvaluationById(evaluationId);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/evaluations/pending-review")
    public ResponseEntity<Page<SystemEvaluationResponse>> getPendingReviewEvaluations(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        
        Pageable pageable = PageRequest.of(page, size);
        Page<SystemEvaluationResponse> responses = systemEvaluationService.getPendingReviewEvaluations(pageable);
        return ResponseEntity.ok(responses);
    }
    
    @PutMapping("/evaluation/{evaluationId}/approve")
    public ResponseEntity<SystemEvaluationResponse> approveEvaluation(
            @PathVariable String evaluationId,
            @RequestBody ApprovalRequest approvalRequest) {
        
        SystemEvaluationResponse response = systemEvaluationService.approveEvaluation(evaluationId, approvalRequest);
        return ResponseEntity.ok(response);
    }
}
```

### 2.3 Exceptions

```java
@ResponseStatus(HttpStatus.BAD_REQUEST)
public class InvalidEvaluationRequestException extends RuntimeException {
    public InvalidEvaluationRequestException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
public class EvaluationEngineUnavailableException extends RuntimeException {
    public EvaluationEngineUnavailableException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.NOT_FOUND)
public class EvaluationNotFoundException extends RuntimeException {
    public EvaluationNotFoundException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.CONFLICT)
public class EvaluationConflictException extends RuntimeException {
    public EvaluationConflictException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
public class RegulatoryDataAccessException extends RuntimeException {
    public RegulatoryDataAccessException(String message) {
        super(message);
    }
}

@ControllerAdvice
public class SystemEvaluationExceptionHandler {
    
    @ExceptionHandler(InvalidEvaluationRequestException.class)
    public ResponseEntity<ErrorResponse> handleInvalidRequest(InvalidEvaluationRequestException ex) {
        ErrorResponse error = new ErrorResponse("INVALID_EVALUATION_REQUEST", ex.getMessage());
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(EvaluationEngineUnavailableException.class)
    public ResponseEntity<ErrorResponse> handleEngineUnavailable(EvaluationEngineUnavailableException ex) {
        ErrorResponse error = new ErrorResponse("EVALUATION_ENGINE_UNAVAILABLE", ex.getMessage());
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(error);
    }
    
    @ExceptionHandler(RegulatoryDataAccessException.class)
    public ResponseEntity<ErrorResponse> handleRegulatoryDataAccess(RegulatoryDataAccessException ex) {
        ErrorResponse error = new ErrorResponse("REGULATORY_DATA_ACCESS_ERROR", ex.getMessage());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

### 2.4 Functional Design

```mermaid
graph TD
    A[System Evaluation Request] --> B[Input Validation]
    B --> C{Validation Passed?}
    C -->|No| D[Return Validation Error]
    C -->|Yes| E[Load Regulatory Context]
    E --> F[GxP Classification Engine]
    F --> G[Severity Assessment Engine]
    G --> H[Change Control Evaluator]
    H --> I[Confidence Score Calculator]
    I --> J{Confidence > Threshold?}
    J -->|No| K[Flag for Manual Review]
    J -->|Yes| L[Generate Evaluation Response]
    K --> M[Queue for Review]
    L --> N[Audit Trail Creation]
    M --> N
    N --> O[Return Evaluation Result]
```

### 2.5 Class Diagram

```mermaid
classDiagram
    class SystemEvaluationController {
        +evaluateEvent(request)
        +batchEvaluateEvents(requests)
        +getEvaluation(evaluationId)
        +getPendingReviewEvaluations(page, size)
        +approveEvaluation(evaluationId, approval)
    }
    
    class SystemEvaluationService {
        +evaluateEvent(request)
        +batchEvaluateEvents(requests)
        +getEvaluationById(evaluationId)
        +getPendingReviewEvaluations(pageable)
        +approveEvaluation(evaluationId, approval)
    }
    
    class GxPClassificationEngine {
        +classifyEvent(event)
        +loadRegulatoryRules()
        +applyFDAGuidelines(event)
        +applyEMAGuidelines(event)
        +calculateConfidence(classification)
    }
    
    class SeverityAssessmentEngine {
        +assessSeverity(event, classification)
        +evaluatePatientSafetyImpact(event)
        +evaluateProductQualityImpact(event)
        +evaluateRegulatoryImpact(event)
    }
    
    class ChangeControlEvaluator {
        +evaluateChangeControlRequirement(event, severity)
        +assessImpactScope(event)
        +determineApprovalLevel(impact)
    }
    
    class RegulatoryKnowledgeService {
        +getRegulatoryGuidelines(region)
        +getClassificationRules(productType)
        +validateCompliance(event, rules)
    }
    
    class EvaluationRepository {
        +save(evaluation)
        +findByEvaluationId(evaluationId)
        +findPendingReview(pageable)
        +findByEventId(eventId)
    }
    
    class AuditTrailService {
        +logEvaluation(evaluation)
        +logApproval(evaluationId, approval)
        +logSystemDecision(decision)
    }
    
    SystemEvaluationController --> SystemEvaluationService
    SystemEvaluationService --> GxPClassificationEngine
    SystemEvaluationService --> SeverityAssessmentEngine
    SystemEvaluationService --> ChangeControlEvaluator
    SystemEvaluationService --> RegulatoryKnowledgeService
    SystemEvaluationService --> EvaluationRepository
    SystemEvaluationService --> AuditTrailService
```

### 2.6 Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    participant GxPEngine
    participant SeverityEngine
    participant ChangeControlEval
    participant RegulatoryService
    participant Repository
    participant AuditService
    
    Client->>Controller: POST /api/v1/system-evaluation/evaluate
    Controller->>Service: evaluateEvent(request)
    Service->>Service: validateRequest(request)
    Service->>RegulatoryService: getRegulatoryContext(event)
    RegulatoryService-->>Service: RegulatoryContext
    Service->>GxPEngine: classifyEvent(event, context)
    GxPEngine->>GxPEngine: applyClassificationRules()
    GxPEngine-->>Service: GxPClassification + Confidence
    Service->>SeverityEngine: assessSeverity(event, classification)
    SeverityEngine->>SeverityEngine: evaluateImpacts()
    SeverityEngine-->>Service: SeverityLevel
    Service->>ChangeControlEval: evaluateRequirement(event, severity)
    ChangeControlEval-->>Service: ChangeControlRequired
    Service->>Service: calculateOverallConfidence()
    Service->>Repository: save(evaluation)
    Service->>AuditService: logEvaluation(evaluation)
    Service-->>Controller: SystemEvaluationResponse
    Controller-->>Client: HTTP 200 OK + Response
```

### 2.7 Components

```java
@Component
public class EvaluationRequestValidator {
    
    public void validateEvaluationRequest(SystemEvaluationRequest request) {
        if (request.getEventId() == null || request.getEventId().trim().isEmpty()) {
            throw new InvalidEvaluationRequestException("Event ID is required");
        }
        
        if (request.getDescription() == null || request.getDescription().length() < 10) {
            throw new InvalidEvaluationRequestException("Event description must be at least 10 characters");
        }
        
        if (request.getEventType() == null) {
            throw new InvalidEvaluationRequestException("Event type is required");
        }
        
        validateEventTypeFormat(request.getEventType());
        validateSourceSystem(request.getSourceSystem());
    }
    
    private void validateEventTypeFormat(String eventType) {
        List<String> validTypes = Arrays.asList("DEVIATION", "CAPA", "CHANGE_CONTROL", "INCIDENT", "COMPLAINT", "OOS", "OOT");
        if (!validTypes.contains(eventType)) {
            throw new InvalidEvaluationRequestException("Invalid event type: " + eventType);
        }
    }
    
    private void validateSourceSystem(String sourceSystem) {
        if (sourceSystem == null || sourceSystem.trim().isEmpty()) {
            throw new InvalidEvaluationRequestException("Source system is required");
        }
    }
}

@Component
public class ConfidenceScoreCalculator {
    
    public double calculateOverallConfidence(
            double gxpConfidence, 
            double severityConfidence, 
            double changeControlConfidence,
            boolean hasRegulatoryContext) {
        
        double baseConfidence = (gxpConfidence + severityConfidence + changeControlConfidence) / 3.0;
        
        // Adjust confidence based on regulatory context availability
        if (hasRegulatoryContext) {
            baseConfidence += 0.1;
        } else {
            baseConfidence -= 0.15;
        }
        
        // Ensure confidence is within valid range
        return Math.max(0.0, Math.min(1.0, baseConfidence));
    }
    
    public boolean requiresManualReview(double confidence, GxPClassification classification, SeverityLevel severity) {
        double threshold = getConfidenceThreshold(classification, severity);
        return confidence < threshold;
    }
    
    private double getConfidenceThreshold(GxPClassification classification, SeverityLevel severity) {
        if (classification == GxPClassification.GXP && severity == SeverityLevel.CRITICAL) {
            return 0.95;
        } else if (classification == GxPClassification.GXP) {
            return 0.85;
        } else if (severity == SeverityLevel.CRITICAL) {
            return 0.90;
        }
        return 0.75;
    }
}
```

### 2.8 Service Layer Business Logic

```java
@Service
@Transactional
public class SystemEvaluationServiceImpl implements SystemEvaluationService {
    
    @Autowired
    private GxPClassificationEngine gxpEngine;
    
    @Autowired
    private SeverityAssessmentEngine severityEngine;
    
    @Autowired
    private ChangeControlEvaluator changeControlEvaluator;
    
    @Autowired
    private RegulatoryKnowledgeService regulatoryService;
    
    @Autowired
    private EvaluationRepository evaluationRepository;
    
    @Autowired
    private EvaluationRequestValidator validator;
    
    @Autowired
    private ConfidenceScoreCalculator confidenceCalculator;
    
    @Autowired
    private AuditTrailService auditService;
    
    @Override
    public SystemEvaluationResponse evaluateEvent(SystemEvaluationRequest request) {
        long startTime = System.currentTimeMillis();
        
        try {
            // Validate input
            validator.validateEvaluationRequest(request);
            
            // Generate evaluation ID
            String evaluationId = generateEvaluationId();
            
            // Load regulatory context
            RegulatoryContext context = regulatoryService.getRegulatoryContext(
                request.getEventType(), 
                request.getRegulatoryRegion()
            );
            
            // Perform GxP classification
            ClassificationResult gxpResult = gxpEngine.classifyEvent(request, context);
            
            // Assess severity
            SeverityResult severityResult = severityEngine.assessSeverity(request, gxpResult);
            
            // Evaluate change control requirement
            ChangeControlResult changeControlResult = changeControlEvaluator.evaluateRequirement(
                request, gxpResult, severityResult
            );
            
            // Calculate overall confidence
            double overallConfidence = confidenceCalculator.calculateOverallConfidence(
                gxpResult.getConfidence(),
                severityResult.getConfidence(),
                changeControlResult.getConfidence(),
                context != null
            );
            
            // Determine if manual review is required
            boolean requiresReview = confidenceCalculator.requiresManualReview(
                overallConfidence, 
                gxpResult.getClassification(), 
                severityResult.getSeverity()
            );
            
            // Create evaluation entity
            SystemEvaluation evaluation = createEvaluation(
                evaluationId, request, gxpResult, severityResult, 
                changeControlResult, overallConfidence, requiresReview
            );
            
            evaluation.setProcessingTimeMs(System.currentTimeMillis() - startTime);
            
            // Save evaluation
            evaluation = evaluationRepository.save(evaluation);
            
            // Create audit trail
            auditService.logEvaluation(evaluation);
            
            // Convert to response
            return convertToResponse(evaluation);
            
        } catch (Exception e) {
            auditService.logEvaluationError(request.getEventId(), e.getMessage());
            throw e;
        }
    }
    
    @Override
    public List<SystemEvaluationResponse> batchEvaluateEvents(List<SystemEvaluationRequest> requests) {
        List<SystemEvaluationResponse> responses = new ArrayList<>();
        
        for (SystemEvaluationRequest request : requests) {
            try {
                SystemEvaluationResponse response = evaluateEvent(request);
                responses.add(response);
            } catch (Exception e) {
                // Log error but continue with other events
                auditService.logEvaluationError(request.getEventId(), e.getMessage());
                
                // Create error response
                SystemEvaluationResponse errorResponse = createErrorResponse(request, e.getMessage());
                responses.add(errorResponse);
            }
        }
        
        return responses;
    }
    
    private String generateEvaluationId() {
        return "EVAL-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 8);
    }
}
```

### 2.9 Validation Rules

```java
@Component
public class SystemEvaluationValidationRules {
    
    private static final Map<String, List<String>> PRODUCT_LINE_REGULATIONS = Map.of(
        "PHARMACEUTICAL", Arrays.asList("FDA_21CFR211", "EMA_GMP", "ICH_Q7"),
        "MEDICAL_DEVICE", Arrays.asList("FDA_21CFR820", "ISO_13485", "MDR_EU"),
        "BIOLOGICS", Arrays.asList("FDA_21CFR600", "EMA_ATMP", "ICH_Q5")
    );
    
    public void validateRegulatoryCompliance(SystemEvaluationRequest request, RegulatoryContext context) {
        String productLine = request.getProductLine();
        
        if (productLine != null && PRODUCT_LINE_REGULATIONS.containsKey(productLine)) {
            List<String> requiredRegulations = PRODUCT_LINE_REGULATIONS.get(productLine);
            
            if (context == null || !context.hasRequiredRegulations(requiredRegulations)) {
                throw new RegulatoryDataAccessException(
                    "Missing required regulatory context for product line: " + productLine
                );
            }
        }
    }
    
    public void validateClassificationConsistency(
            GxPClassification classification, 
            SeverityLevel severity, 
            String eventType) {
        
        // Critical events in pharmaceutical context must be GxP
        if (severity == SeverityLevel.CRITICAL && 
            eventType.equals("DEVIATION") && 
            classification != GxPClassification.GXP) {
            
            throw new EvaluationConflictException(
                "Critical pharmaceutical deviations must be classified as GxP"
            );
        }
        
        // Medical device incidents with patient impact must be GxP
        if (eventType.equals("INCIDENT") && 
            severity == SeverityLevel.CRITICAL && 
            classification == GxPClassification.NON_GXP) {
            
            throw new EvaluationConflictException(
                "Critical medical device incidents must be classified as GxP"
            );
        }
    }
    
    public void validateChangeControlLogic(
            ChangeControlResult result, 
            SeverityLevel severity, 
            GxPClassification classification) {
        
        // All GxP critical events require change control
        if (classification == GxPClassification.GXP && 
            severity == SeverityLevel.CRITICAL && 
            !result.isRequired()) {
            
            throw new EvaluationConflictException(
                "GxP critical events must require change control"
            );
        }
    }
}
```

### 2.10 Service Integrations

```java
@Service
public class RegulatoryKnowledgeServiceImpl implements RegulatoryKnowledgeService {
    
    @Value("${regulatory.database.url}")
    private String regulatoryDatabaseUrl;
    
    @Value("${regulatory.api.key}")
    private String regulatoryApiKey;
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    @Override
    public RegulatoryContext getRegulatoryContext(String eventType, String region) {
        String cacheKey = "regulatory_context:" + eventType + ":" + region;
        
        // Try cache first
        RegulatoryContext cachedContext = (RegulatoryContext) redisTemplate.opsForValue().get(cacheKey);
        if (cachedContext != null) {
            return cachedContext;
        }
        
        try {
            // Fetch from regulatory database
            HttpHeaders headers = new HttpHeaders();
            headers.set("Authorization", "Bearer " + regulatoryApiKey);
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            String url = regulatoryDatabaseUrl + "/context?eventType=" + eventType + "&region=" + region;
            
            HttpEntity<String> entity = new HttpEntity<>(headers);
            ResponseEntity<RegulatoryContext> response = restTemplate.exchange(
                url, HttpMethod.GET, entity, RegulatoryContext.class
            );
            
            RegulatoryContext context = response.getBody();
            
            // Cache for 1 hour
            redisTemplate.opsForValue().set(cacheKey, context, Duration.ofHours(1));
            
            return context;
            
        } catch (Exception e) {
            throw new RegulatoryDataAccessException("Failed to retrieve regulatory context: " + e.getMessage());
        }
    }
    
    @Override
    public List<ClassificationRule> getClassificationRules(String productType, String region) {
        String cacheKey = "classification_rules:" + productType + ":" + region;
        
        List<ClassificationRule> cachedRules = (List<ClassificationRule>) redisTemplate.opsForValue().get(cacheKey);
        if (cachedRules != null) {
            return cachedRules;
        }
        
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.set("Authorization", "Bearer " + regulatoryApiKey);
            
            String url = regulatoryDatabaseUrl + "/rules?productType=" + productType + "&region=" + region;
            
            HttpEntity<String> entity = new HttpEntity<>(headers);
            ResponseEntity<ClassificationRule[]> response = restTemplate.exchange(
                url, HttpMethod.GET, entity, ClassificationRule[].class
            );
            
            List<ClassificationRule> rules = Arrays.asList(response.getBody());
            
            // Cache for 4 hours
            redisTemplate.opsForValue().set(cacheKey, rules, Duration.ofHours(4));
            
            return rules;
            
        } catch (Exception e) {
            throw new RegulatoryDataAccessException("Failed to retrieve classification rules: " + e.getMessage());
        }
    }
}
```

---

## 3. Frontend React Details

### 3.1 UI Architecture

```jsx
// System Evaluation Dashboard Component
import React, { useState, useEffect } from 'react';
import { SystemEvaluationForm } from './SystemEvaluationForm';
import { EvaluationResults } from './EvaluationResults';
import { PendingReviewQueue } from './PendingReviewQueue';
import { BatchEvaluationUpload } from './BatchEvaluationUpload';

const SystemEvaluationDashboard = () => {
    const [activeTab, setActiveTab] = useState('single-evaluation');
    const [evaluationResult, setEvaluationResult] = useState(null);
    const [pendingReviews, setPendingReviews] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (activeTab === 'pending-reviews') {
            loadPendingReviews();
        }
    }, [activeTab]);

    const loadPendingReviews = async () => {
        setLoading(true);
        try {
            const response = await fetch('/api/v1/system-evaluation/evaluations/pending-review');
            const data = await response.json();
            setPendingReviews(data.content || []);
        } catch (err) {
            setError('Failed to load pending reviews');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="system-evaluation-dashboard">
            <header className="dashboard-header">
                <h1>System Event Evaluation</h1>
                <div className="dashboard-stats">
                    <div className="stat-card">
                        <span className="stat-value">{pendingReviews.length}</span>
                        <span className="stat-label">Pending Reviews</span>
                    </div>
                </div>
            </header>

            <nav className="dashboard-nav">
                <button 
                    className={activeTab === 'single-evaluation' ? 'active' : ''}
                    onClick={() => setActiveTab('single-evaluation')}
                >
                    Single Evaluation
                </button>
                <button 
                    className={activeTab === 'batch-evaluation' ? 'active' : ''}
                    onClick={() => setActiveTab('batch-evaluation')}
                >
                    Batch Evaluation
                </button>
                <button 
                    className={activeTab === 'pending-reviews' ? 'active' : ''}
                    onClick={() => setActiveTab('pending-reviews')}
                >
                    Pending Reviews ({pendingReviews.length})
                </button>
            </nav>

            <div className="dashboard-content">
                {error && (
                    <div className="error-alert">
                        <strong>Error:</strong> {error}
                        <button onClick={() => setError(null)}>×</button>
                    </div>
                )}

                {activeTab === 'single-evaluation' && (
                    <SystemEvaluationForm 
                        onEvaluationComplete={setEvaluationResult}
                        loading={loading}
                        setLoading={setLoading}
                        setError={setError}
                    />
                )}

                {activeTab === 'batch-evaluation' && (
                    <BatchEvaluationUpload 
                        setLoading={setLoading}
                        setError={setError}
                    />
                )}

                {activeTab === 'pending-reviews' && (
                    <PendingReviewQueue 
                        pendingReviews={pendingReviews}
                        onReviewComplete={loadPendingReviews}
                        loading={loading}
                    />
                )}

                {evaluationResult && (
                    <EvaluationResults 
                        result={evaluationResult} 
                        onClose={() => setEvaluationResult(null)}
                    />
                )}
            </div>
        </div>
    );
};
```

### 3.2 UI Specifications

```jsx
// System Evaluation Form Component
import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const SystemEvaluationForm = ({ onEvaluationComplete, loading, setLoading, setError }) => {
    const validationSchema = Yup.object({
        eventId: Yup.string()
            .matches(/^[A-Z]{2,3}\d{6,10}$/, 'Invalid event ID format')
            .required('Event ID is required'),
        eventType: Yup.string()
            .oneOf(['DEVIATION', 'CAPA', 'CHANGE_CONTROL', 'INCIDENT', 'COMPLAINT', 'OOS', 'OOT'])
            .required('Event type is required'),
        description: Yup.string()
            .min(10, 'Description must be at least 10 characters')
            .max(5000, 'Description must be less than 5000 characters')
            .required('Description is required'),
        sourceSystem: Yup.string().required('Source system is required'),
        productLine: Yup.string().oneOf(['PHARMACEUTICAL', 'MEDICAL_DEVICE', 'BIOLOGICS']),
        regulatoryRegion: Yup.string().oneOf(['FDA', 'EMA', 'PMDA', 'HC']),
        impactArea: Yup.string()
    });

    const handleSubmit = async (values, { setSubmitting, resetForm }) => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await fetch('/api/v1/system-evaluation/evaluate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                },
                body: JSON.stringify({
                    ...values,
                    additionalContext: {
                        submittedBy: getCurrentUser(),
                        submissionTimestamp: new Date().toISOString()
                    }
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            onEvaluationComplete(result);
            resetForm();
            
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
            setSubmitting(false);
        }
    };

    return (
        <div className="system-evaluation-form">
            <h2>System Event Evaluation</h2>
            <p className="form-description">
                Submit an event for automated GxP classification, severity assessment, and change control evaluation.
            </p>
            
            <Formik
                initialValues={{
                    eventId: '',
                    eventType: '',
                    description: '',
                    sourceSystem: '',
                    productLine: '',
                    regulatoryRegion: '',
                    impactArea: ''
                }}
                validationSchema={validationSchema}
                onSubmit={handleSubmit}
            >
                {({ isSubmitting, values }) => (
                    <Form className="evaluation-form">
                        <div className="form-section">
                            <h3>Event Information</h3>
                            
                            <div className="form-row">
                                <div className="form-group col-md-6">
                                    <label htmlFor="eventId">Event ID *</label>
                                    <Field 
                                        type="text" 
                                        name="eventId" 
                                        placeholder="e.g., DEV123456"
                                        className="form-control"
                                    />
                                    <ErrorMessage name="eventId" component="div" className="error-message" />
                                </div>

                                <div className="form-group col-md-6">
                                    <label htmlFor="eventType">Event Type *</label>
                                    <Field as="select" name="eventType" className="form-control">
                                        <option value="">Select Event Type</option>
                                        <option value="DEVIATION">Deviation</option>
                                        <option value="CAPA">CAPA</option>
                                        <option value="CHANGE_CONTROL">Change Control</option>
                                        <option value="INCIDENT">Incident</option>
                                        <option value="COMPLAINT">Complaint</option>
                                        <option value="OOS">Out of Specification</option>
                                        <option value="OOT">Out of Trend</option>
                                    </Field>
                                    <ErrorMessage name="eventType" component="div" className="error-message" />
                                </div>
                            </div>

                            <div className="form-group">
                                <label htmlFor="description">Event Description *</label>
                                <Field 
                                    as="textarea" 
                                    name="description" 
                                    rows="4"
                                    placeholder="Provide detailed description of the event..."
                                    className="form-control"
                                />
                                <div className="character-count">
                                    {values.description.length}/5000 characters
                                </div>
                                <ErrorMessage name="description" component="div" className="error-message" />
                            </div>

                            <div className="form-group">
                                <label htmlFor="sourceSystem">Source System *</label>
                                <Field 
                                    type="text" 
                                    name="sourceSystem" 
                                    placeholder="e.g., Manufacturing Execution System"
                                    className="form-control"
                                />
                                <ErrorMessage name="sourceSystem" component="div" className="error-message" />
                            </div>
                        </div>

                        <div className="form-section">
                            <h3>Regulatory Context</h3>
                            
                            <div className="form-row">
                                <div className="form-group col-md-6">
                                    <label htmlFor="productLine">Product Line</label>
                                    <Field as="select" name="productLine" className="form-control">
                                        <option value="">Select Product Line</option>
                                        <option value="PHARMACEUTICAL">Pharmaceutical</option>
                                        <option value="MEDICAL_DEVICE">Medical Device</option>
                                        <option value="BIOLOGICS">Biologics</option>
                                    </Field>
                                </div>

                                <div className="form-group col-md-6">
                                    <label htmlFor="regulatoryRegion">Regulatory Region</label>
                                    <Field as="select" name="regulatoryRegion" className="form-control">
                                        <option value="">Select Region</option>
                                        <option value="FDA">FDA (United States)</option>
                                        <option value="EMA">EMA (European Union)</option>
                                        <option value="PMDA">PMDA (Japan)</option>
                                        <option value="HC">Health Canada</option>
                                    </Field>
                                </div>
                            </div>

                            <div className="form-group">
                                <label htmlFor="impactArea">Impact Area</label>
                                <Field 
                                    type="text" 
                                    name="impactArea" 
                                    placeholder="e.g., Patient Safety, Product Quality, Data Integrity"
                                    className="form-control"
                                />
                            </div>
                        </div>

                        <div className="form-actions">
                            <button 
                                type="submit" 
                                disabled={isSubmitting || loading}
                                className="btn btn-primary btn-lg"
                            >
                                {loading ? (
                                    <>
                                        <span className="spinner"></span>
                                        Evaluating Event...
                                    </>
                                ) : (
                                    'Evaluate Event'
                                )}
                            </button>
                        </div>
                    </Form>
                )}
            </Formik>
        </div>
    );
};
```

### 3.3 API Integration

```jsx
// System Evaluation API Service
class SystemEvaluationAPI {
    constructor() {
        this.baseURL = process.env.REACT_APP_API_BASE_URL || '/api/v1';
        this.timeout = 45000; // 45 seconds for system evaluation
    }

    async evaluateEvent(eventData) {
        const response = await this.makeRequest('/system-evaluation/evaluate', {
            method: 'POST',
            body: JSON.stringify(eventData)
        });
        return response;
    }

    async batchEvaluateEvents(eventsData) {
        const response = await this.makeRequest('/system-evaluation/batch-evaluate', {
            method: 'POST',
            body: JSON.stringify(eventsData)
        });
        return response;
    }

    async getEvaluation(evaluationId) {
        const response = await this.makeRequest(`/system-evaluation/evaluation/${evaluationId}`, {
            method: 'GET'
        });
        return response;
    }

    async getPendingReviewEvaluations(page = 0, size = 20) {
        const queryParams = new URLSearchParams({
            page: page.toString(),
            size: size.toString()
        });
        
        const response = await this.makeRequest(`/system-evaluation/evaluations/pending-review?${queryParams}`, {
            method: 'GET'
        });
        return response;
    }

    async approveEvaluation(evaluationId, approvalData) {
        const response = await this.makeRequest(`/system-evaluation/evaluation/${evaluationId}/approve`, {
            method: 'PUT',
            body: JSON.stringify(approvalData)
        });
        return response;
    }

    async makeRequest(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const defaultHeaders = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.getAuthToken()}`
        };

        const config = {
            ...options,
            headers: {
                ...defaultHeaders,
                ...options.headers
            }
        };

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), this.timeout);
            
            const response = await fetch(url, {
                ...config,
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('Request timeout - evaluation taking longer than expected');
            }
            throw error;
        }
    }

    getAuthToken() {
        return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
    }
}

export default new SystemEvaluationAPI();
```

---

## 4. Database Details

### 4.1 ER Diagram

```mermaid
erDiagram
    SYSTEM_EVALUATIONS {
        BIGINT id PK
        VARCHAR evaluation_id UK
        VARCHAR event_id FK
        ENUM gxp_classification
        ENUM severity_level
        BOOLEAN change_control_required
        DECIMAL confidence_score
        TEXT evaluation_rationale
        JSON regulatory_references
        ENUM evaluation_status
        TIMESTAMP evaluation_timestamp
        BIGINT processing_time_ms
        VARCHAR evaluation_engine_version
    }
    
    REGULATORY_CONTEXTS {
        BIGINT id PK
        VARCHAR context_id UK
        VARCHAR event_type
        VARCHAR regulatory_region
        VARCHAR product_line
        JSON classification_rules
        JSON severity_criteria
        JSON change_control_rules
        TIMESTAMP last_updated
        VARCHAR version
    }
    
    EVALUATION_AUDIT_TRAIL {
        BIGINT id PK
        VARCHAR evaluation_id FK
        VARCHAR action_type
        TEXT action_details
        VARCHAR performed_by
        TIMESTAMP action_timestamp
        VARCHAR ip_address
        JSON before_state
        JSON after_state
    }
    
    MANUAL_REVIEW_QUEUE {
        BIGINT id PK
        VARCHAR evaluation_id FK
        VARCHAR review_reason
        VARCHAR assigned_reviewer
        ENUM review_status
        TIMESTAMP queued_at
        TIMESTAMP reviewed_at
        TEXT review_comments
        VARCHAR final_decision
    }
    
    BATCH_EVALUATIONS {
        BIGINT id PK
        VARCHAR batch_id UK
        VARCHAR uploaded_by
        INTEGER total_events
        INTEGER processed_events
        INTEGER failed_events
        ENUM batch_status
        TIMESTAMP started_at
        TIMESTAMP completed_at
        TEXT error_summary
    }
    
    SYSTEM_EVALUATIONS ||--|| REGULATORY_CONTEXTS : "uses"
    SYSTEM_EVALUATIONS ||--o{ EVALUATION_AUDIT_TRAIL : "generates"
    SYSTEM_EVALUATIONS ||--o| MANUAL_REVIEW_QUEUE : "may_require"
    BATCH_EVALUATIONS ||--o{ SYSTEM_EVALUATIONS : "contains"
```

### 4.2 Database Validations

```sql
-- System Evaluations Table
CREATE TABLE system_evaluations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    evaluation_id VARCHAR(100) NOT NULL UNIQUE,
    event_id VARCHAR(50) NOT NULL,
    gxp_classification ENUM('GXP', 'NON_GXP', 'REQUIRES_REVIEW') NOT NULL,
    severity_level ENUM('CRITICAL', 'MAJOR', 'MINOR', 'NEGLIGIBLE') NOT NULL,
    change_control_required BOOLEAN NOT NULL DEFAULT FALSE,
    confidence_score DECIMAL(4,3) CHECK (confidence_score >= 0.000 AND confidence_score <= 1.000),
    evaluation_rationale TEXT,
    regulatory_references JSON,
    evaluation_status ENUM('COMPLETED', 'PENDING_REVIEW', 'FAILED', 'IN_PROGRESS') NOT NULL DEFAULT 'IN_PROGRESS',
    evaluation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_time_ms BIGINT CHECK (processing_time_ms >= 0),
    evaluation_engine_version VARCHAR(20),
    INDEX idx_evaluation_id (evaluation_id),
    INDEX idx_event_id (event_id),
    INDEX idx_gxp_classification (gxp_classification),
    INDEX idx_severity_level (severity_level),
    INDEX idx_evaluation_status (evaluation_status),
    INDEX idx_evaluation_timestamp (evaluation_timestamp),
    INDEX idx_confidence_score (confidence_score)
);

-- Regulatory Contexts Table
CREATE TABLE regulatory_contexts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    context_id VARCHAR(100) NOT NULL UNIQUE,
    event_type VARCHAR(50) NOT NULL,
    regulatory_region VARCHAR(20) NOT NULL,
    product_line VARCHAR(50),
    classification_rules JSON NOT NULL,
    severity_criteria JSON NOT NULL,
    change_control_rules JSON NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    version VARCHAR(20) NOT NULL,
    UNIQUE KEY uk_context (event_type, regulatory_region, product_line),
    INDEX idx_event_type (event_type),
    INDEX idx_regulatory_region (regulatory_region),
    INDEX idx_product_line (product_line),
    INDEX idx_last_updated (last_updated)
);

-- Evaluation Audit Trail Table
CREATE TABLE evaluation_audit_trail (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    evaluation_id VARCHAR(100) NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    action_details TEXT,
    performed_by VARCHAR(100),
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    before_state JSON,
    after_state JSON,
    FOREIGN KEY (evaluation_id) REFERENCES system_evaluations(evaluation_id) ON DELETE CASCADE,
    INDEX idx_evaluation_id (evaluation_id),
    INDEX idx_action_type (action_type),
    INDEX idx_action_timestamp (action_timestamp),
    INDEX idx_performed_by (performed_by)
);

-- Manual Review Queue Table
CREATE TABLE manual_review_queue (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    evaluation_id VARCHAR(100) NOT NULL,
    review_reason VARCHAR(200) NOT NULL,
    assigned_reviewer VARCHAR(100),
    review_status ENUM('PENDING', 'IN_REVIEW', 'COMPLETED', 'ESCALATED') NOT NULL DEFAULT 'PENDING',
    queued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP NULL,
    review_comments TEXT,
    final_decision VARCHAR(100),
    FOREIGN KEY (evaluation_id) REFERENCES system_evaluations(evaluation_id) ON DELETE CASCADE,
    INDEX idx_evaluation_id (evaluation_id),
    INDEX idx_review_status (review_status),
    INDEX idx_assigned_reviewer (assigned_reviewer),
    INDEX idx_queued_at (queued_at)
);

-- Batch Evaluations Table
CREATE TABLE batch_evaluations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    batch_id VARCHAR(100) NOT NULL UNIQUE,
    uploaded_by VARCHAR(100) NOT NULL,
    total_events INTEGER NOT NULL CHECK (total_events > 0),
    processed_events INTEGER NOT NULL DEFAULT 0 CHECK (processed_events >= 0),
    failed_events INTEGER NOT NULL DEFAULT 0 CHECK (failed_events >= 0),
    batch_status ENUM('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', 'CANCELLED') NOT NULL DEFAULT 'PENDING',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    error_summary TEXT,
    INDEX idx_batch_id (batch_id),
    INDEX idx_uploaded_by (uploaded_by),
    INDEX idx_batch_status (batch_status),
    INDEX idx_started_at (started_at),
    CONSTRAINT chk_processed_total CHECK (processed_events <= total_events),
    CONSTRAINT chk_failed_total CHECK (failed_events <= total_events),
    CONSTRAINT chk_processed_failed CHECK (processed_events + failed_events <= total_events)
);
```

---

## 5. Non Functional Requirements

### 5.1 Performance

```yaml
Performance Requirements:
  Processing Capacity:
    - Single Event: < 2 seconds (95th percentile)
    - Batch Processing: 10,000+ events per hour
    - Concurrent Evaluations: 500+ simultaneous
    
  Throughput Targets:
    - Peak Load: 15,000 events per hour
    - Sustained Load: 8,000 events per hour
    - Batch Size: Up to 1,000 events per batch
    
  Response Times:
    - Simple Events: < 1 second
    - Complex Events: < 3 seconds
    - Regulatory Context Loading: < 500ms
    
  Resource Utilization:
    - CPU: < 75% under peak load
    - Memory: < 85% heap utilization
    - Database: < 90% connection pool usage
    - Cache Hit Ratio: > 90% for regulatory data
```

### 5.2 Security

```yaml
Security Requirements:
  Access Control:
    - Role-based evaluation permissions
    - API endpoint authorization
    - Evaluation result access control
    
  Data Protection:
    - Evaluation data encryption at rest
    - Secure transmission of regulatory data
    - PII masking in audit logs
    
  Regulatory Compliance:
    - 21 CFR Part 11 compliance for audit trails
    - GDPR compliance for data handling
    - SOX compliance for financial impact events
    
  Authentication:
    - Multi-factor authentication for reviewers
    - Service-to-service authentication
    - Token-based API access
```

### 5.3 Logging

```java
@Component
public class SystemEvaluationLogger {
    
    private static final Logger logger = LoggerFactory.getLogger(SystemEvaluationLogger.class);
    private static final Logger auditLogger = LoggerFactory.getLogger("SYSTEM_EVALUATION_AUDIT");
    private static final Logger performanceLogger = LoggerFactory.getLogger("SYSTEM_EVALUATION_PERFORMANCE");
    private static final Logger regulatoryLogger = LoggerFactory.getLogger("REGULATORY_COMPLIANCE");
    
    public void logEvaluationStart(String evaluationId, String eventId, String eventType) {
        auditLogger.info("Evaluation started - EvaluationId: {}, EventId: {}, EventType: {}, Timestamp: {}", 
            evaluationId, eventId, eventType, Instant.now());
    }
    
    public void logEvaluationComplete(String evaluationId, GxPClassification classification, 
                                    SeverityLevel severity, double confidence, long processingTime) {
        auditLogger.info("Evaluation completed - EvaluationId: {}, Classification: {}, Severity: {}, " +
            "Confidence: {}, ProcessingTime: {}ms", 
            evaluationId, classification, severity, confidence, processingTime);
        
        if (processingTime > 2000) {
            performanceLogger.warn("Slow evaluation detected - EvaluationId: {}, ProcessingTime: {}ms", 
                evaluationId, processingTime);
        }
    }
    
    public void logManualReviewRequired(String evaluationId, String reason, double confidence) {
        auditLogger.warn("Manual review required - EvaluationId: {}, Reason: {}, Confidence: {}", 
            evaluationId, reason, confidence);
    }
    
    public void logRegulatoryContextAccess(String eventType, String region, boolean success) {
        regulatoryLogger.info("Regulatory context access - EventType: {}, Region: {}, Success: {}", 
            eventType, region, success);
    }
    
    public void logBatchEvaluationProgress(String batchId, int processed, int total, int failed) {
        logger.info("Batch evaluation progress - BatchId: {}, Processed: {}/{}, Failed: {}", 
            batchId, processed, total, failed);
    }
}
```

---

## 6. Dependencies

```yaml
Backend Dependencies:
  Spring Boot: 3.1.0
  Spring Security: 6.1.0
  Spring Data JPA: 3.1.0
  Spring Cache: 6.0.0
  MySQL Connector: 8.0.33
  Redis: 7.0.11
  Jackson: 2.15.0
  Validation API: 3.0.2
  Micrometer: 1.11.0
  Logback: 1.4.7
  Apache Commons: 3.12.0

Frontend Dependencies:
  React: 18.2.0
  React Router: 6.11.0
  Formik: 2.4.0
  Yup: 1.2.0
  Axios: 1.4.0
  Material-UI: 5.13.0
  React Query: 4.29.0
  Chart.js: 4.3.0

Infrastructure Dependencies:
  MySQL: 8.0.33
  Redis: 7.0.11
  Nginx: 1.24.0
  Docker: 24.0.0
  Kubernetes: 1.27.0
  Prometheus: 2.45.0

External Services:
  Regulatory Database API: v2.1
  Authentication Service: OAuth 2.0
  Notification Service: v1.5
  Document Management: v3.2
```

---

## 7. Assumptions

```yaml
Technical Assumptions:
  - Regulatory database maintains 99.9% availability
  - Network latency to regulatory services < 300ms
  - Database supports up to 500 concurrent connections
  - Redis cache cluster available for high availability
  - Load balancer handles SSL termination and routing

Business Assumptions:
  - Regulatory guidelines are updated monthly
  - Classification rules are version-controlled
  - Manual reviewers available during business hours
  - Escalation procedures defined for critical events
  - Audit requirements clearly documented

Operational Assumptions:
  - 24/7 monitoring for system evaluations
  - Automated backup of evaluation data
  - Disaster recovery procedures tested quarterly
  - Performance baselines established and monitored
  - Incident response team available

Data Assumptions:
  - Event data quality validated at source
  - Regulatory data synchronized daily
  - Historical evaluation data retained for 7 years
  - Data privacy requirements documented
  - Integration with quality management systems established

Regulatory Assumptions:
  - FDA and EMA guidelines remain stable
  - Classification criteria are well-defined
  - Change control processes are established
  - Audit trail requirements are documented
  - Compliance validation procedures are in place
```