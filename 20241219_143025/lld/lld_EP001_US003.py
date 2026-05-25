# Low Level Design Document

## Epic ID: EP001
## User Story ID: US003
## Title: Impact Assessment and Recommendation Generation

---

## 1. Objective

Design and implement a comprehensive impact assessment and recommendation generation system that analyzes quality events to provide multi-dimensional impact assessments and actionable recommendations with clear timelines and rationale.

---

## 2. Backend Spring Boot API Details

### 2.1 API Model

```java
// Impact Assessment Model
@Entity
@Table(name = "impact_assessments")
public class ImpactAssessment {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull
    @Column(name = "assessment_id")
    private String assessmentId;
    
    @NotNull
    @Column(name = "event_id")
    private String eventId;
    
    @Column(name = "operational_impact", columnDefinition = "JSON")
    private String operationalImpact;
    
    @Column(name = "regulatory_impact", columnDefinition = "JSON")
    private String regulatoryImpact;
    
    @Column(name = "financial_impact", columnDefinition = "JSON")
    private String financialImpact;
    
    @Column(name = "reputational_impact", columnDefinition = "JSON")
    private String reputationalImpact;
    
    @Column(name = "patient_safety_impact", columnDefinition = "JSON")
    private String patientSafetyImpact;
    
    @NotNull
    @Column(name = "overall_risk_score")
    private Double overallRiskScore;
    
    @Column(name = "impact_rationale", columnDefinition = "TEXT")
    private String impactRationale;
    
    @NotNull
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "assessment_timestamp")
    private Date assessmentTimestamp;
    
    @Column(name = "assessment_version")
    private String assessmentVersion;
    
    // Getters and Setters
}

// Recommendation Model
@Entity
@Table(name = "recommendations")
public class Recommendation {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull
    @Column(name = "recommendation_id")
    private String recommendationId;
    
    @NotNull
    @Column(name = "assessment_id")
    private String assessmentId;
    
    @NotNull
    @Column(name = "action_title")
    private String actionTitle;
    
    @NotNull
    @Column(name = "action_description", columnDefinition = "TEXT")
    private String actionDescription;
    
    @NotNull
    @Column(name = "priority_level")
    @Enumerated(EnumType.STRING)
    private PriorityLevel priorityLevel;
    
    @NotNull
    @Column(name = "category")
    @Enumerated(EnumType.STRING)
    private ActionCategory category;
    
    @Column(name = "assigned_role")
    private String assignedRole;
    
    @Column(name = "estimated_effort_hours")
    private Integer estimatedEffortHours;
    
    @Column(name = "estimated_cost")
    private BigDecimal estimatedCost;
    
    @Column(name = "target_completion_days")
    private Integer targetCompletionDays;
    
    @Column(name = "success_criteria", columnDefinition = "TEXT")
    private String successCriteria;
    
    @Column(name = "rationale", columnDefinition = "TEXT")
    private String rationale;
    
    @Column(name = "dependencies", columnDefinition = "JSON")
    private String dependencies;
    
    @Column(name = "risk_mitigation_score")
    private Double riskMitigationScore;
    
    @NotNull
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "created_timestamp")
    private Date createdTimestamp;
    
    // Getters and Setters
}

// Assessment Request Model
public class ImpactAssessmentRequest {
    @NotNull
    private String eventId;
    @NotNull
    private String eventType;
    @NotNull
    private String severity;
    @NotNull
    private String gxpClassification;
    private String description;
    private String productLine;
    private String affectedSystems;
    private String regulatoryRegion;
    private Map<String, Object> eventContext;
    
    // Getters and Setters
}

// Assessment Response Model
public class ImpactAssessmentResponse {
    private String assessmentId;
    private String eventId;
    private OperationalImpact operationalImpact;
    private RegulatoryImpact regulatoryImpact;
    private FinancialImpact financialImpact;
    private ReputationalImpact reputationalImpact;
    private PatientSafetyImpact patientSafetyImpact;
    private Double overallRiskScore;
    private String impactRationale;
    private List<RecommendationResponse> recommendations;
    private Date assessmentTimestamp;
    
    // Getters and Setters
}

// Enums
public enum PriorityLevel {
    CRITICAL, HIGH, MEDIUM, LOW
}

public enum ActionCategory {
    IMMEDIATE_ACTION, INVESTIGATION, CORRECTIVE_ACTION, PREVENTIVE_ACTION, 
    REGULATORY_NOTIFICATION, DOCUMENTATION, TRAINING, SYSTEM_UPDATE
}
```

### 2.2 API Details

```java
@RestController
@RequestMapping("/api/v1/impact-assessment")
@Validated
public class ImpactAssessmentController {
    
    @Autowired
    private ImpactAssessmentService impactAssessmentService;
    
    @PostMapping("/generate")
    @ResponseStatus(HttpStatus.OK)
    public ResponseEntity<ImpactAssessmentResponse> generateAssessment(
            @Valid @RequestBody ImpactAssessmentRequest request) {
        
        ImpactAssessmentResponse response = impactAssessmentService.generateAssessment(request);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/assessment/{assessmentId}")
    public ResponseEntity<ImpactAssessmentResponse> getAssessment(
            @PathVariable String assessmentId) {
        
        ImpactAssessmentResponse response = impactAssessmentService.getAssessmentById(assessmentId);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/event/{eventId}/assessment")
    public ResponseEntity<ImpactAssessmentResponse> getAssessmentByEventId(
            @PathVariable String eventId) {
        
        ImpactAssessmentResponse response = impactAssessmentService.getAssessmentByEventId(eventId);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/recommendations/generate")
    public ResponseEntity<List<RecommendationResponse>> generateRecommendations(
            @Valid @RequestBody RecommendationRequest request) {
        
        List<RecommendationResponse> recommendations = impactAssessmentService.generateRecommendations(request);
        return ResponseEntity.ok(recommendations);
    }
    
    @PutMapping("/recommendation/{recommendationId}/update-status")
    public ResponseEntity<RecommendationResponse> updateRecommendationStatus(
            @PathVariable String recommendationId,
            @RequestBody StatusUpdateRequest statusUpdate) {
        
        RecommendationResponse response = impactAssessmentService.updateRecommendationStatus(recommendationId, statusUpdate);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/templates")
    public ResponseEntity<List<RecommendationTemplate>> getRecommendationTemplates(
            @RequestParam(required = false) String eventType,
            @RequestParam(required = false) String severity) {
        
        List<RecommendationTemplate> templates = impactAssessmentService.getRecommendationTemplates(eventType, severity);
        return ResponseEntity.ok(templates);
    }
}
```

### 2.3 Exceptions

```java
@ResponseStatus(HttpStatus.BAD_REQUEST)
public class InvalidAssessmentRequestException extends RuntimeException {
    public InvalidAssessmentRequestException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
public class AssessmentEngineUnavailableException extends RuntimeException {
    public AssessmentEngineUnavailableException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.NOT_FOUND)
public class AssessmentNotFoundException extends RuntimeException {
    public AssessmentNotFoundException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.CONFLICT)
public class RecommendationConflictException extends RuntimeException {
    public RecommendationConflictException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
public class TemplateProcessingException extends RuntimeException {
    public TemplateProcessingException(String message) {
        super(message);
    }
}

@ControllerAdvice
public class ImpactAssessmentExceptionHandler {
    
    @ExceptionHandler(InvalidAssessmentRequestException.class)
    public ResponseEntity<ErrorResponse> handleInvalidRequest(InvalidAssessmentRequestException ex) {
        ErrorResponse error = new ErrorResponse("INVALID_ASSESSMENT_REQUEST", ex.getMessage());
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(AssessmentEngineUnavailableException.class)
    public ResponseEntity<ErrorResponse> handleEngineUnavailable(AssessmentEngineUnavailableException ex) {
        ErrorResponse error = new ErrorResponse("ASSESSMENT_ENGINE_UNAVAILABLE", ex.getMessage());
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(error);
    }
    
    @ExceptionHandler(TemplateProcessingException.class)
    public ResponseEntity<ErrorResponse> handleTemplateProcessing(TemplateProcessingException ex) {
        ErrorResponse error = new ErrorResponse("TEMPLATE_PROCESSING_ERROR", ex.getMessage());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

### 2.4 Functional Design

```mermaid
graph TD
    A[Impact Assessment Request] --> B[Input Validation]
    B --> C{Validation Passed?}
    C -->|No| D[Return Validation Error]
    C -->|Yes| E[Load Event Context]
    E --> F[Operational Impact Analysis]
    F --> G[Regulatory Impact Analysis]
    G --> H[Financial Impact Analysis]
    H --> I[Reputational Impact Analysis]
    I --> J[Patient Safety Impact Analysis]
    J --> K[Calculate Overall Risk Score]
    K --> L[Generate Recommendation Templates]
    L --> M[Customize Recommendations]
    M --> N[Prioritize Actions]
    N --> O[Calculate Timelines & Costs]
    O --> P[Generate Assessment Response]
    P --> Q[Save Assessment & Recommendations]
    Q --> R[Return Complete Assessment]
```

### 2.5 Class Diagram

```mermaid
classDiagram
    class ImpactAssessmentController {
        +generateAssessment(request)
        +getAssessment(assessmentId)
        +getAssessmentByEventId(eventId)
        +generateRecommendations(request)
        +updateRecommendationStatus(recommendationId, status)
        +getRecommendationTemplates(eventType, severity)
    }
    
    class ImpactAssessmentService {
        +generateAssessment(request)
        +getAssessmentById(assessmentId)
        +getAssessmentByEventId(eventId)
        +generateRecommendations(request)
        +updateRecommendationStatus(recommendationId, status)
        +getRecommendationTemplates(eventType, severity)
    }
    
    class OperationalImpactAnalyzer {
        +analyzeOperationalImpact(event)
        +assessSystemDowntime(event)
        +evaluateProcessDisruption(event)
        +calculateProductionImpact(event)
    }
    
    class RegulatoryImpactAnalyzer {
        +analyzeRegulatoryImpact(event, region)
        +assessComplianceRisk(event)
        +evaluateReportingRequirements(event)
        +calculateRegulatoryPenalties(event)
    }
    
    class FinancialImpactAnalyzer {
        +analyzeFinancialImpact(event)
        +calculateDirectCosts(event)
        +estimateIndirectCosts(event)
        +assessRevenueImpact(event)
    }
    
    class RecommendationEngine {
        +generateRecommendations(assessment)
        +loadTemplates(eventType, severity)
        +customizeRecommendations(templates, context)
        +prioritizeActions(recommendations)
        +calculateTimelines(recommendations)
    }
    
    class TemplateService {
        +getTemplatesByCategory(category)
        +processTemplate(template, context)
        +validateTemplate(template)
        +updateTemplate(template)
    }
    
    class RiskScoreCalculator {
        +calculateOverallRisk(impacts)
        +weightImpactFactors(impacts)
        +normalizeScores(scores)
    }
    
    ImpactAssessmentController --> ImpactAssessmentService
    ImpactAssessmentService --> OperationalImpactAnalyzer
    ImpactAssessmentService --> RegulatoryImpactAnalyzer
    ImpactAssessmentService --> FinancialImpactAnalyzer
    ImpactAssessmentService --> RecommendationEngine
    ImpactAssessmentService --> RiskScoreCalculator
    RecommendationEngine --> TemplateService
```

### 2.6 Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    participant OpAnalyzer
    participant RegAnalyzer
    participant FinAnalyzer
    participant RecommendationEngine
    participant TemplateService
    participant Repository
    
    Client->>Controller: POST /api/v1/impact-assessment/generate
    Controller->>Service: generateAssessment(request)
    Service->>Service: validateRequest(request)
    Service->>OpAnalyzer: analyzeOperationalImpact(event)
    OpAnalyzer-->>Service: OperationalImpact
    Service->>RegAnalyzer: analyzeRegulatoryImpact(event)
    RegAnalyzer-->>Service: RegulatoryImpact
    Service->>FinAnalyzer: analyzeFinancialImpact(event)
    FinAnalyzer-->>Service: FinancialImpact
    Service->>Service: calculateOverallRiskScore(impacts)
    Service->>RecommendationEngine: generateRecommendations(assessment)
    RecommendationEngine->>TemplateService: getTemplates(eventType, severity)
    TemplateService-->>RecommendationEngine: Templates
    RecommendationEngine->>RecommendationEngine: customizeRecommendations()
    RecommendationEngine-->>Service: Recommendations
    Service->>Repository: saveAssessment(assessment, recommendations)
    Service-->>Controller: ImpactAssessmentResponse
    Controller-->>Client: HTTP 200 OK + Response
```

### 2.7 Components

```java
@Component
public class AssessmentRequestValidator {
    
    public void validateAssessmentRequest(ImpactAssessmentRequest request) {
        if (request.getEventId() == null || request.getEventId().trim().isEmpty()) {
            throw new InvalidAssessmentRequestException("Event ID is required");
        }
        
        if (request.getEventType() == null) {
            throw new InvalidAssessmentRequestException("Event type is required");
        }
        
        if (request.getSeverity() == null) {
            throw new InvalidAssessmentRequestException("Severity level is required");
        }
        
        if (request.getGxpClassification() == null) {
            throw new InvalidAssessmentRequestException("GxP classification is required");
        }
        
        validateEventType(request.getEventType());
        validateSeverity(request.getSeverity());
        validateGxpClassification(request.getGxpClassification());
    }
    
    private void validateEventType(String eventType) {
        List<String> validTypes = Arrays.asList("DEVIATION", "CAPA", "CHANGE_CONTROL", "INCIDENT", "COMPLAINT", "OOS", "OOT");
        if (!validTypes.contains(eventType)) {
            throw new InvalidAssessmentRequestException("Invalid event type: " + eventType);
        }
    }
    
    private void validateSeverity(String severity) {
        List<String> validSeverities = Arrays.asList("CRITICAL", "MAJOR", "MINOR", "NEGLIGIBLE");
        if (!validSeverities.contains(severity)) {
            throw new InvalidAssessmentRequestException("Invalid severity level: " + severity);
        }
    }
    
    private void validateGxpClassification(String classification) {
        List<String> validClassifications = Arrays.asList("GXP", "NON_GXP");
        if (!validClassifications.contains(classification)) {
            throw new InvalidAssessmentRequestException("Invalid GxP classification: " + classification);
        }
    }
}

@Component
public class ImpactWeightingEngine {
    
    private static final Map<String, Double> IMPACT_WEIGHTS = Map.of(
        "PATIENT_SAFETY", 0.35,
        "REGULATORY", 0.25,
        "OPERATIONAL", 0.20,
        "FINANCIAL", 0.15,
        "REPUTATIONAL", 0.05
    );
    
    public double calculateWeightedRiskScore(Map<String, Double> impactScores) {
        double weightedScore = 0.0;
        
        for (Map.Entry<String, Double> entry : impactScores.entrySet()) {
            String impactType = entry.getKey();
            Double score = entry.getValue();
            Double weight = IMPACT_WEIGHTS.get(impactType);
            
            if (weight != null && score != null) {
                weightedScore += (score * weight);
            }
        }
        
        return Math.min(10.0, Math.max(0.0, weightedScore));
    }
    
    public Map<String, Double> adjustWeightsForContext(String eventType, String severity, String gxpClassification) {
        Map<String, Double> adjustedWeights = new HashMap<>(IMPACT_WEIGHTS);
        
        // Increase patient safety weight for GxP critical events
        if ("GXP".equals(gxpClassification) && "CRITICAL".equals(severity)) {
            adjustedWeights.put("PATIENT_SAFETY", 0.45);
            adjustedWeights.put("REGULATORY", 0.30);
            adjustedWeights.put("OPERATIONAL", 0.15);
            adjustedWeights.put("FINANCIAL", 0.08);
            adjustedWeights.put("REPUTATIONAL", 0.02);
        }
        
        // Increase regulatory weight for compliance-related events
        if ("CHANGE_CONTROL".equals(eventType) || "DEVIATION".equals(eventType)) {
            adjustedWeights.put("REGULATORY", adjustedWeights.get("REGULATORY") + 0.10);
            adjustedWeights.put("OPERATIONAL", adjustedWeights.get("OPERATIONAL") - 0.05);
            adjustedWeights.put("FINANCIAL", adjustedWeights.get("FINANCIAL") - 0.05);
        }
        
        return adjustedWeights;
    }
}
```

### 2.8 Service Layer Business Logic

```java
@Service
@Transactional
public class ImpactAssessmentServiceImpl implements ImpactAssessmentService {
    
    @Autowired
    private OperationalImpactAnalyzer operationalAnalyzer;
    
    @Autowired
    private RegulatoryImpactAnalyzer regulatoryAnalyzer;
    
    @Autowired
    private FinancialImpactAnalyzer financialAnalyzer;
    
    @Autowired
    private ReputationalImpactAnalyzer reputationalAnalyzer;
    
    @Autowired
    private PatientSafetyImpactAnalyzer patientSafetyAnalyzer;
    
    @Autowired
    private RecommendationEngine recommendationEngine;
    
    @Autowired
    private RiskScoreCalculator riskCalculator;
    
    @Autowired
    private ImpactAssessmentRepository assessmentRepository;
    
    @Autowired
    private AssessmentRequestValidator validator;
    
    @Autowired
    private ImpactWeightingEngine weightingEngine;
    
    @Override
    public ImpactAssessmentResponse generateAssessment(ImpactAssessmentRequest request) {
        long startTime = System.currentTimeMillis();
        
        try {
            // Validate input
            validator.validateAssessmentRequest(request);
            
            // Generate assessment ID
            String assessmentId = generateAssessmentId();
            
            // Perform impact analyses
            OperationalImpact operationalImpact = operationalAnalyzer.analyzeOperationalImpact(request);
            RegulatoryImpact regulatoryImpact = regulatoryAnalyzer.analyzeRegulatoryImpact(request);
            FinancialImpact financialImpact = financialAnalyzer.analyzeFinancialImpact(request);
            ReputationalImpact reputationalImpact = reputationalAnalyzer.analyzeReputationalImpact(request);
            PatientSafetyImpact patientSafetyImpact = patientSafetyAnalyzer.analyzePatientSafetyImpact(request);
            
            // Calculate overall risk score
            Map<String, Double> impactScores = Map.of(
                "OPERATIONAL", operationalImpact.getRiskScore(),
                "REGULATORY", regulatoryImpact.getRiskScore(),
                "FINANCIAL", financialImpact.getRiskScore(),
                "REPUTATIONAL", reputationalImpact.getRiskScore(),
                "PATIENT_SAFETY", patientSafetyImpact.getRiskScore()
            );
            
            double overallRiskScore = weightingEngine.calculateWeightedRiskScore(impactScores);
            
            // Generate recommendations
            List<RecommendationResponse> recommendations = recommendationEngine.generateRecommendations(
                assessmentId, request, operationalImpact, regulatoryImpact, financialImpact, 
                reputationalImpact, patientSafetyImpact, overallRiskScore
            );
            
            // Create assessment entity
            ImpactAssessment assessment = createAssessment(
                assessmentId, request, operationalImpact, regulatoryImpact, 
                financialImpact, reputationalImpact, patientSafetyImpact, overallRiskScore
            );
            
            // Save assessment
            assessment = assessmentRepository.save(assessment);
            
            // Create response
            ImpactAssessmentResponse response = convertToResponse(assessment, recommendations);
            response.setProcessingTimeMs(System.currentTimeMillis() - startTime);
            
            return response;
            
        } catch (Exception e) {
            throw new AssessmentEngineUnavailableException("Failed to generate impact assessment: " + e.getMessage());
        }
    }
    
    @Override
    public List<RecommendationResponse> generateRecommendations(RecommendationRequest request) {
        try {
            // Load existing assessment
            ImpactAssessment assessment = assessmentRepository.findByAssessmentId(request.getAssessmentId())
                .orElseThrow(() -> new AssessmentNotFoundException("Assessment not found: " + request.getAssessmentId()));
            
            // Generate new recommendations based on updated context
            return recommendationEngine.generateCustomRecommendations(assessment, request);
            
        } catch (Exception e) {
            throw new AssessmentEngineUnavailableException("Failed to generate recommendations: " + e.getMessage());
        }
    }
    
    private String generateAssessmentId() {
        return "ASSESS-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 8);
    }
    
    private ImpactAssessment createAssessment(
            String assessmentId, ImpactAssessmentRequest request,
            OperationalImpact operationalImpact, RegulatoryImpact regulatoryImpact,
            FinancialImpact financialImpact, ReputationalImpact reputationalImpact,
            PatientSafetyImpact patientSafetyImpact, double overallRiskScore) {
        
        ImpactAssessment assessment = new ImpactAssessment();
        assessment.setAssessmentId(assessmentId);
        assessment.setEventId(request.getEventId());
        assessment.setOperationalImpact(convertToJson(operationalImpact));
        assessment.setRegulatoryImpact(convertToJson(regulatoryImpact));
        assessment.setFinancialImpact(convertToJson(financialImpact));
        assessment.setReputationalImpact(convertToJson(reputationalImpact));
        assessment.setPatientSafetyImpact(convertToJson(patientSafetyImpact));
        assessment.setOverallRiskScore(overallRiskScore);
        assessment.setImpactRationale(generateImpactRationale(operationalImpact, regulatoryImpact, financialImpact, reputationalImpact, patientSafetyImpact));
        assessment.setAssessmentTimestamp(new Date());
        assessment.setAssessmentVersion("1.0");
        
        return assessment;
    }
}
```

### 2.9 Validation Rules

```java
@Component
public class ImpactAssessmentValidationRules {
    
    public void validateImpactScores(Map<String, Double> impactScores) {
        for (Map.Entry<String, Double> entry : impactScores.entrySet()) {
            String impactType = entry.getKey();
            Double score = entry.getValue();
            
            if (score == null) {
                throw new InvalidAssessmentRequestException("Missing impact score for: " + impactType);
            }
            
            if (score < 0.0 || score > 10.0) {
                throw new InvalidAssessmentRequestException("Invalid impact score for " + impactType + ": " + score + " (must be 0.0-10.0)");
            }
        }
    }
    
    public void validateRecommendationPriorities(List<RecommendationResponse> recommendations) {
        long criticalCount = recommendations.stream()
            .filter(r -> r.getPriorityLevel() == PriorityLevel.CRITICAL)
            .count();
        
        if (criticalCount > 5) {
            throw new RecommendationConflictException("Too many critical recommendations: " + criticalCount + " (maximum 5 allowed)");
        }
        
        // Validate that critical recommendations have appropriate timelines
        recommendations.stream()
            .filter(r -> r.getPriorityLevel() == PriorityLevel.CRITICAL)
            .forEach(r -> {
                if (r.getTargetCompletionDays() == null || r.getTargetCompletionDays() > 7) {
                    throw new RecommendationConflictException("Critical recommendations must have completion timeline ≤ 7 days");
                }
            });
    }
    
    public void validateRecommendationConsistency(List<RecommendationResponse> recommendations, double overallRiskScore) {
        boolean hasImmediateAction = recommendations.stream()
            .anyMatch(r -> r.getCategory() == ActionCategory.IMMEDIATE_ACTION);
        
        // High-risk events must have immediate actions
        if (overallRiskScore >= 8.0 && !hasImmediateAction) {
            throw new RecommendationConflictException("High-risk events (score ≥ 8.0) must include immediate actions");
        }
        
        // Validate cost estimates are reasonable
        BigDecimal totalCost = recommendations.stream()
            .filter(r -> r.getEstimatedCost() != null)
            .map(RecommendationResponse::getEstimatedCost)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        if (totalCost.compareTo(new BigDecimal("1000000")) > 0) { // $1M threshold
            throw new RecommendationConflictException("Total recommendation cost exceeds threshold: $" + totalCost);
        }
    }
}
```

### 2.10 Service Integrations

```java
@Service
public class ProjectManagementIntegrationService {
    
    @Value("${project.management.api.url}")
    private String projectManagementApiUrl;
    
    @Value("${project.management.api.key}")
    private String apiKey;
    
    @Autowired
    private RestTemplate restTemplate;
    
    public String createProjectTask(RecommendationResponse recommendation) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("Authorization", "Bearer " + apiKey);
            
            Map<String, Object> taskData = new HashMap<>();
            taskData.put("title", recommendation.getActionTitle());
            taskData.put("description", recommendation.getActionDescription());
            taskData.put("priority", mapPriorityLevel(recommendation.getPriorityLevel()));
            taskData.put("assignedRole", recommendation.getAssignedRole());
            taskData.put("dueDate", calculateDueDate(recommendation.getTargetCompletionDays()));
            taskData.put("estimatedHours", recommendation.getEstimatedEffortHours());
            taskData.put("tags", Arrays.asList("quality-event", "impact-assessment"));
            
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(taskData, headers);
            
            ResponseEntity<Map> response = restTemplate.postForEntity(
                projectManagementApiUrl + "/tasks", entity, Map.class
            );
            
            Map<String, Object> responseBody = response.getBody();
            return (String) responseBody.get("taskId");
            
        } catch (Exception e) {
            throw new RuntimeException("Failed to create project task: " + e.getMessage());
        }
    }
    
    public void updateTaskStatus(String taskId, String status) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("Authorization", "Bearer " + apiKey);
            
            Map<String, Object> statusUpdate = Map.of("status", status);
            
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(statusUpdate, headers);
            
            restTemplate.exchange(
                projectManagementApiUrl + "/tasks/" + taskId + "/status",
                HttpMethod.PUT,
                entity,
                Void.class
            );
            
        } catch (Exception e) {
            throw new RuntimeException("Failed to update task status: " + e.getMessage());
        }
    }
    
    private String mapPriorityLevel(PriorityLevel priority) {
        switch (priority) {
            case CRITICAL: return "urgent";
            case HIGH: return "high";
            case MEDIUM: return "medium";
            case LOW: return "low";
            default: return "medium";
        }
    }
    
    private String calculateDueDate(Integer targetCompletionDays) {
        if (targetCompletionDays == null) {
            targetCompletionDays = 30; // Default 30 days
        }
        
        LocalDate dueDate = LocalDate.now().plusDays(targetCompletionDays);
        return dueDate.toString();
    }
}
```

---

## 3. Frontend React Details

### 3.1 UI Architecture

```jsx
// Impact Assessment Dashboard Component
import React, { useState, useEffect } from 'react';
import { ImpactAssessmentForm } from './ImpactAssessmentForm';
import { AssessmentResults } from './AssessmentResults';
import { RecommendationTracker } from './RecommendationTracker';
import { AssessmentHistory } from './AssessmentHistory';

const ImpactAssessmentDashboard = () => {
    const [activeTab, setActiveTab] = useState('generate-assessment');
    const [assessmentResult, setAssessmentResult] = useState(null);
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    return (
        <div className="impact-assessment-dashboard">
            <header className="dashboard-header">
                <h1>Impact Assessment & Recommendations</h1>
                <div className="dashboard-metrics">
                    <div className="metric-card">
                        <span className="metric-value">{recommendations.length}</span>
                        <span className="metric-label">Active Recommendations</span>
                    </div>
                    <div className="metric-card">
                        <span className="metric-value">
                            {assessmentResult ? assessmentResult.overallRiskScore.toFixed(1) : 'N/A'}
                        </span>
                        <span className="metric-label">Risk Score</span>
                    </div>
                </div>
            </header>

            <nav className="dashboard-nav">
                <button 
                    className={activeTab === 'generate-assessment' ? 'active' : ''}
                    onClick={() => setActiveTab('generate-assessment')}
                >
                    Generate Assessment
                </button>
                <button 
                    className={activeTab === 'view-results' ? 'active' : ''}
                    onClick={() => setActiveTab('view-results')}
                    disabled={!assessmentResult}
                >
                    View Results
                </button>
                <button 
                    className={activeTab === 'track-recommendations' ? 'active' : ''}
                    onClick={() => setActiveTab('track-recommendations')}
                >
                    Track Recommendations
                </button>
                <button 
                    className={activeTab === 'history' ? 'active' : ''}
                    onClick={() => setActiveTab('history')}
                >
                    Assessment History
                </button>
            </nav>

            <div className="dashboard-content">
                {error && (
                    <div className="error-alert">
                        <strong>Error:</strong> {error}
                        <button onClick={() => setError(null)}>×</button>
                    </div>
                )}

                {activeTab === 'generate-assessment' && (
                    <ImpactAssessmentForm 
                        onAssessmentComplete={setAssessmentResult}
                        onRecommendationsGenerated={setRecommendations}
                        loading={loading}
                        setLoading={setLoading}
                        setError={setError}
                    />
                )}

                {activeTab === 'view-results' && assessmentResult && (
                    <AssessmentResults 
                        assessment={assessmentResult}
                        recommendations={recommendations}
                    />
                )}

                {activeTab === 'track-recommendations' && (
                    <RecommendationTracker 
                        recommendations={recommendations}
                        onStatusUpdate={setRecommendations}
                    />
                )}

                {activeTab === 'history' && (
                    <AssessmentHistory />
                )}
            </div>
        </div>
    );
};
```

### 3.2 UI Specifications

```jsx
// Impact Assessment Form Component
import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const ImpactAssessmentForm = ({ onAssessmentComplete, onRecommendationsGenerated, loading, setLoading, setError }) => {
    const validationSchema = Yup.object({
        eventId: Yup.string()
            .matches(/^[A-Z]{2,3}\d{6,10}$/, 'Invalid event ID format')
            .required('Event ID is required'),
        eventType: Yup.string()
            .oneOf(['DEVIATION', 'CAPA', 'CHANGE_CONTROL', 'INCIDENT', 'COMPLAINT', 'OOS', 'OOT'])
            .required('Event type is required'),
        severity: Yup.string()
            .oneOf(['CRITICAL', 'MAJOR', 'MINOR', 'NEGLIGIBLE'])
            .required('Severity level is required'),
        gxpClassification: Yup.string()
            .oneOf(['GXP', 'NON_GXP'])
            .required('GxP classification is required'),
        description: Yup.string()
            .min(20, 'Description must be at least 20 characters')
            .max(2000, 'Description must be less than 2000 characters')
            .required('Description is required'),
        productLine: Yup.string(),
        affectedSystems: Yup.string(),
        regulatoryRegion: Yup.string()
    });

    const handleSubmit = async (values, { setSubmitting, resetForm }) => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await fetch('/api/v1/impact-assessment/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                },
                body: JSON.stringify({
                    ...values,
                    eventContext: {
                        submittedBy: getCurrentUser(),
                        submissionTimestamp: new Date().toISOString(),
                        sourceApplication: 'Impact Assessment Dashboard'
                    }
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            onAssessmentComplete(result);
            onRecommendationsGenerated(result.recommendations || []);
            
            // Show success message
            setError(null);
            
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
            setSubmitting(false);
        }
    };

    return (
        <div className="impact-assessment-form">
            <h2>Generate Impact Assessment</h2>
            <p className="form-description">
                Provide event details to generate a comprehensive impact assessment and actionable recommendations.
            </p>
            
            <Formik
                initialValues={{
                    eventId: '',
                    eventType: '',
                    severity: '',
                    gxpClassification: '',
                    description: '',
                    productLine: '',
                    affectedSystems: '',
                    regulatoryRegion: ''
                }}
                validationSchema={validationSchema}
                onSubmit={handleSubmit}
            >
                {({ isSubmitting, values }) => (
                    <Form className="assessment-form">
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

                            <div className="form-row">
                                <div className="form-group col-md-6">
                                    <label htmlFor="severity">Severity Level *</label>
                                    <Field as="select" name="severity" className="form-control">
                                        <option value="">Select Severity</option>
                                        <option value="CRITICAL">Critical</option>
                                        <option value="MAJOR">Major</option>
                                        <option value="MINOR">Minor</option>
                                        <option value="NEGLIGIBLE">Negligible</option>
                                    </Field>
                                    <ErrorMessage name="severity" component="div" className="error-message" />
                                </div>

                                <div className="form-group col-md-6">
                                    <label htmlFor="gxpClassification">GxP Classification *</label>
                                    <Field as="select" name="gxpClassification" className="form-control">
                                        <option value="">Select Classification</option>
                                        <option value="GXP">GxP</option>
                                        <option value="NON_GXP">Non-GxP</option>
                                    </Field>
                                    <ErrorMessage name="gxpClassification" component="div" className="error-message" />
                                </div>
                            </div>

                            <div className="form-group">
                                <label htmlFor="description">Event Description *</label>
                                <Field 
                                    as="textarea" 
                                    name="description" 
                                    rows="4"
                                    placeholder="Provide detailed description of the event and its context..."
                                    className="form-control"
                                />
                                <div className="character-count">
                                    {values.description.length}/2000 characters
                                </div>
                                <ErrorMessage name="description" component="div" className="error-message" />
                            </div>
                        </div>

                        <div className="form-section">
                            <h3>Additional Context</h3>
                            
                            <div className="form-row">
                                <div className="form-group col-md-6">
                                    <label htmlFor="productLine">Product Line</label>
                                    <Field 
                                        type="text" 
                                        name="productLine" 
                                        placeholder="e.g., Pharmaceuticals, Medical Devices"
                                        className="form-control"
                                    />
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
                                <label htmlFor="affectedSystems">Affected Systems</label>
                                <Field 
                                    type="text" 
                                    name="affectedSystems" 
                                    placeholder="e.g., Manufacturing System, Quality Management System"
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
                                        Generating Assessment...
                                    </>
                                ) : (
                                    'Generate Impact Assessment'
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
// Impact Assessment API Service
class ImpactAssessmentAPI {
    constructor() {
        this.baseURL = process.env.REACT_APP_API_BASE_URL || '/api/v1';
        this.timeout = 60000; // 60 seconds for impact assessment
    }

    async generateAssessment(assessmentData) {
        const response = await this.makeRequest('/impact-assessment/generate', {
            method: 'POST',
            body: JSON.stringify(assessmentData)
        });
        return response;
    }

    async getAssessment(assessmentId) {
        const response = await this.makeRequest(`/impact-assessment/assessment/${assessmentId}`, {
            method: 'GET'
        });
        return response;
    }

    async getAssessmentByEventId(eventId) {
        const response = await this.makeRequest(`/impact-assessment/event/${eventId}/assessment`, {
            method: 'GET'
        });
        return response;
    }

    async generateRecommendations(recommendationData) {
        const response = await this.makeRequest('/impact-assessment/recommendations/generate', {
            method: 'POST',
            body: JSON.stringify(recommendationData)
        });
        return response;
    }

    async updateRecommendationStatus(recommendationId, statusData) {
        const response = await this.makeRequest(`/impact-assessment/recommendation/${recommendationId}/update-status`, {
            method: 'PUT',
            body: JSON.stringify(statusData)
        });
        return response;
    }

    async getRecommendationTemplates(eventType = null, severity = null) {
        const queryParams = new URLSearchParams();
        if (eventType) queryParams.append('eventType', eventType);
        if (severity) queryParams.append('severity', severity);
        
        const response = await this.makeRequest(`/impact-assessment/templates?${queryParams}`, {
            method: 'GET'
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
                throw new Error('Request timeout - assessment generation taking longer than expected');
            }
            throw error;
        }
    }

    getAuthToken() {
        return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
    }
}

export default new ImpactAssessmentAPI();
```

---

## 4. Database Details

### 4.1 ER Diagram

```mermaid
erDiagram
    IMPACT_ASSESSMENTS {
        BIGINT id PK
        VARCHAR assessment_id UK
        VARCHAR event_id FK
        JSON operational_impact
        JSON regulatory_impact
        JSON financial_impact
        JSON reputational_impact
        JSON patient_safety_impact
        DECIMAL overall_risk_score
        TEXT impact_rationale
        TIMESTAMP assessment_timestamp
        VARCHAR assessment_version
    }
    
    RECOMMENDATIONS {
        BIGINT id PK
        VARCHAR recommendation_id UK
        VARCHAR assessment_id FK
        VARCHAR action_title
        TEXT action_description
        ENUM priority_level
        ENUM category
        VARCHAR assigned_role
        INTEGER estimated_effort_hours
        DECIMAL estimated_cost
        INTEGER target_completion_days
        TEXT success_criteria
        TEXT rationale
        JSON dependencies
        DECIMAL risk_mitigation_score
        TIMESTAMP created_timestamp
    }
    
    RECOMMENDATION_TEMPLATES {
        BIGINT id PK
        VARCHAR template_id UK
        VARCHAR template_name
        VARCHAR event_type
        VARCHAR severity_level
        VARCHAR gxp_classification
        JSON template_content
        BOOLEAN is_active
        TIMESTAMP created_at
        TIMESTAMP last_updated
        VARCHAR created_by
    }
    
    RECOMMENDATION_STATUS_HISTORY {
        BIGINT id PK
        VARCHAR recommendation_id FK
        ENUM status
        VARCHAR updated_by
        TIMESTAMP updated_at
        TEXT comments
        VARCHAR external_task_id
    }
    
    IMPACT_FACTORS {
        BIGINT id PK
        VARCHAR factor_id UK
        VARCHAR factor_name
        VARCHAR impact_category
        DECIMAL weight_factor
        JSON calculation_rules
        BOOLEAN is_active
        TIMESTAMP last_updated
    }
    
    IMPACT_ASSESSMENTS ||--o{ RECOMMENDATIONS : "generates"
    RECOMMENDATIONS ||--o{ RECOMMENDATION_STATUS_HISTORY : "tracks"
    RECOMMENDATION_TEMPLATES ||--o{ RECOMMENDATIONS : "based_on"
    IMPACT_FACTORS ||--o{ IMPACT_ASSESSMENTS : "influences"
```

### 4.2 Database Validations

```sql
-- Impact Assessments Table
CREATE TABLE impact_assessments (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    assessment_id VARCHAR(100) NOT NULL UNIQUE,
    event_id VARCHAR(50) NOT NULL,
    operational_impact JSON NOT NULL,
    regulatory_impact JSON NOT NULL,
    financial_impact JSON NOT NULL,
    reputational_impact JSON NOT NULL,
    patient_safety_impact JSON NOT NULL,
    overall_risk_score DECIMAL(4,2) NOT NULL CHECK (overall_risk_score >= 0.00 AND overall_risk_score <= 10.00),
    impact_rationale TEXT,
    assessment_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assessment_version VARCHAR(10) NOT NULL DEFAULT '1.0',
    INDEX idx_assessment_id (assessment_id),
    INDEX idx_event_id (event_id),
    INDEX idx_overall_risk_score (overall_risk_score),
    INDEX idx_assessment_timestamp (assessment_timestamp)
);

-- Recommendations Table
CREATE TABLE recommendations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    recommendation_id VARCHAR(100) NOT NULL UNIQUE,
    assessment_id VARCHAR(100) NOT NULL,
    action_title VARCHAR(200) NOT NULL,
    action_description TEXT NOT NULL,
    priority_level ENUM('CRITICAL', 'HIGH', 'MEDIUM', 'LOW') NOT NULL,
    category ENUM('IMMEDIATE_ACTION', 'INVESTIGATION', 'CORRECTIVE_ACTION', 'PREVENTIVE_ACTION', 
                  'REGULATORY_NOTIFICATION', 'DOCUMENTATION', 'TRAINING', 'SYSTEM_UPDATE') NOT NULL,
    assigned_role VARCHAR(100),
    estimated_effort_hours INTEGER CHECK (estimated_effort_hours > 0),
    estimated_cost DECIMAL(12,2) CHECK (estimated_cost >= 0),
    target_completion_days INTEGER CHECK (target_completion_days > 0),
    success_criteria TEXT,
    rationale TEXT,
    dependencies JSON,
    risk_mitigation_score DECIMAL(4,2) CHECK (risk_mitigation_score >= 0.00 AND risk_mitigation_score <= 10.00),
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES impact_assessments(assessment_id) ON DELETE CASCADE,
    INDEX idx_recommendation_id (recommendation_id),
    INDEX idx_assessment_id (assessment_id),
    INDEX idx_priority_level (priority_level),
    INDEX idx_category (category),
    INDEX idx_assigned_role (assigned_role),
    INDEX idx_created_timestamp (created_timestamp)
);

-- Recommendation Templates Table
CREATE TABLE recommendation_templates (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    template_id VARCHAR(100) NOT NULL UNIQUE,
    template_name VARCHAR(200) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    severity_level VARCHAR(20),
    gxp_classification VARCHAR(20),
    template_content JSON NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    INDEX idx_template_id (template_id),
    INDEX idx_event_type (event_type),
    INDEX idx_severity_level (severity_level),
    INDEX idx_gxp_classification (gxp_classification),
    INDEX idx_is_active (is_active)
);

-- Recommendation Status History Table
CREATE TABLE recommendation_status_history (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    recommendation_id VARCHAR(100) NOT NULL,
    status ENUM('PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', 'ON_HOLD') NOT NULL,
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comments TEXT,
    external_task_id VARCHAR(100),
    FOREIGN KEY (recommendation_id) REFERENCES recommendations(recommendation_id) ON DELETE CASCADE,
    INDEX idx_recommendation_id (recommendation_id),
    INDEX idx_status (status),
    INDEX idx_updated_at (updated_at),
    INDEX idx_updated_by (updated_by)
);

-- Impact Factors Table
CREATE TABLE impact_factors (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    factor_id VARCHAR(100) NOT NULL UNIQUE,
    factor_name VARCHAR(200) NOT NULL,
    impact_category VARCHAR(50) NOT NULL CHECK (impact_category IN ('OPERATIONAL', 'REGULATORY', 'FINANCIAL', 'REPUTATIONAL', 'PATIENT_SAFETY')),
    weight_factor DECIMAL(4,3) NOT NULL CHECK (weight_factor >= 0.000 AND weight_factor <= 1.000),
    calculation_rules JSON NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_factor_id (factor_id),
    INDEX idx_impact_category (impact_category),
    INDEX idx_is_active (is_active)
);
```

---

## 5. Non Functional Requirements

### 5.1 Performance

```yaml
Performance Requirements:
  Assessment Generation:
    - Standard Assessment: < 5 seconds (95th percentile)
    - Complex Multi-Impact Assessment: < 10 seconds
    - Recommendation Generation: < 3 seconds
    
  Throughput Targets:
    - Concurrent Assessments: 200+ simultaneous
    - Assessments per Hour: 5,000+
    - Template Processing: 1,000+ per minute
    
  Response Times:
    - Impact Analysis: < 2 seconds per dimension
    - Risk Score Calculation: < 500ms
    - Template Loading: < 200ms
    
  Resource Utilization:
    - CPU: < 80% under peak load
    - Memory: < 85% heap utilization
    - Database: < 85% connection pool usage
    - Cache Hit Ratio: > 95% for templates
```

### 5.2 Security

```yaml
Security Requirements:
  Data Protection:
    - Impact assessment data encryption
    - Recommendation access control
    - Sensitive financial data masking
    
  Access Control:
    - Role-based recommendation visibility
    - Assessment approval workflows
    - Template modification permissions
    
  Audit Requirements:
    - Complete assessment audit trail
    - Recommendation status tracking
    - Template change logging
    
  Compliance:
    - SOX compliance for financial impacts
    - GDPR compliance for personal data
    - Industry-specific regulatory compliance
```

### 5.3 Logging

```java
@Component
public class ImpactAssessmentLogger {
    
    private static final Logger logger = LoggerFactory.getLogger(ImpactAssessmentLogger.class);
    private static final Logger auditLogger = LoggerFactory.getLogger("IMPACT_ASSESSMENT_AUDIT");
    private static final Logger performanceLogger = LoggerFactory.getLogger("IMPACT_ASSESSMENT_PERFORMANCE");
    private static final Logger businessLogger = LoggerFactory.getLogger("BUSINESS_IMPACT");
    
    public void logAssessmentGeneration(String assessmentId, String eventId, double riskScore, long processingTime) {
        auditLogger.info("Assessment generated - AssessmentId: {}, EventId: {}, RiskScore: {}, ProcessingTime: {}ms", 
            assessmentId, eventId, riskScore, processingTime);
        
        if (riskScore >= 8.0) {
            businessLogger.warn("High-risk assessment generated - AssessmentId: {}, RiskScore: {}", 
                assessmentId, riskScore);
        }
        
        if (processingTime > 5000) {
            performanceLogger.warn("Slow assessment generation - AssessmentId: {}, ProcessingTime: {}ms", 
                assessmentId, processingTime);
        }
    }
    
    public void logRecommendationGeneration(String assessmentId, int recommendationCount, int criticalCount) {
        auditLogger.info("Recommendations generated - AssessmentId: {}, Total: {}, Critical: {}", 
            assessmentId, recommendationCount, criticalCount);
        
        if (criticalCount > 3) {
            businessLogger.warn("High number of critical recommendations - AssessmentId: {}, Critical: {}", 
                assessmentId, criticalCount);
        }
    }
    
    public void logRecommendationStatusUpdate(String recommendationId, String oldStatus, String newStatus, String updatedBy) {
        auditLogger.info("Recommendation status updated - RecommendationId: {}, Status: {} -> {}, UpdatedBy: {}", 
            recommendationId, oldStatus, newStatus, updatedBy);
    }
    
    public void logFinancialImpact(String assessmentId, BigDecimal estimatedCost, String impactCategory) {
        businessLogger.info("Financial impact assessed - AssessmentId: {}, EstimatedCost: {}, Category: {}", 
            assessmentId, estimatedCost, impactCategory);
        
        if (estimatedCost.compareTo(new BigDecimal("100000")) > 0) {
            businessLogger.warn("High financial impact detected - AssessmentId: {}, Cost: {}", 
                assessmentId, estimatedCost);
        }
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
  Apache Commons Math: 3.6.1
  Freemarker: 2.3.32

Frontend Dependencies:
  React: 18.2.0
  React Router: 6.11.0
  Formik: 2.4.0
  Yup: 1.2.0
  Axios: 1.4.0
  Material-UI: 5.13.0
  React Query: 4.29.0
  Chart.js: 4.3.0
  React Table: 8.9.0

Infrastructure Dependencies:
  MySQL: 8.0.33
  Redis: 7.0.11
  Nginx: 1.24.0
  Docker: 24.0.0
  Kubernetes: 1.27.0
  Prometheus: 2.45.0
  Grafana: 10.0.0

External Services:
  Project Management API: v2.0
  Financial Systems API: v1.5
  Notification Service: v1.5
  Document Management: v3.2
  Regulatory Database: v2.1
```

---

## 7. Assumptions

```yaml
Technical Assumptions:
  - Impact calculation algorithms are well-defined and tested
  - Template system supports dynamic content generation
  - External project management systems have stable APIs
  - Database supports complex JSON queries efficiently
  - Caching layer provides sub-second response times

Business Assumptions:
  - Impact assessment criteria are regularly reviewed and updated
  - Recommendation templates are maintained by subject matter experts
  - Financial impact calculations use current cost models
  - Regulatory requirements are clearly documented and current
  - Stakeholders provide timely feedback on recommendation effectiveness

Operational Assumptions:
  - 24/7 availability for critical impact assessments
  - Automated backup of assessment data and templates
  - Performance monitoring and alerting in place
  - Disaster recovery procedures tested and documented
  - Integration with existing quality management systems

Data Assumptions:
  - Historical impact data available for trend analysis
  - Cost models and financial data are accurate and current
  - Regulatory guidelines are synchronized with external sources
  - Template effectiveness is measured and tracked
  - Assessment accuracy is validated through outcome tracking

Integration Assumptions:
  - Project management systems support task creation via API
  - Financial systems provide real-time cost data
  - Notification systems handle high-priority alerts
  - Document management systems store assessment artifacts
  - Audit systems capture complete activity trails
```