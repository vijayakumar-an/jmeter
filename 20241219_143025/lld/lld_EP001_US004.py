# Low Level Design Document

## Epic ID: EP001
## User Story ID: US004
## Title: Decision Rationale Explanation System

---

## 1. Objective

Design and implement a comprehensive decision rationale explanation system that provides clear, transparent, and auditable explanations for all AI-driven decisions and recommendations with regulatory compliance and user comprehension focus.

---

## 2. Backend Spring Boot API Details

### 2.1 API Model

```java
// Decision Rationale Model
@Entity
@Table(name = "decision_rationales")
public class DecisionRationale {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull
    @Column(name = "rationale_id")
    private String rationaleId;
    
    @NotNull
    @Column(name = "decision_id")
    private String decisionId;
    
    @NotNull
    @Column(name = "decision_type")
    @Enumerated(EnumType.STRING)
    private DecisionType decisionType;
    
    @NotNull
    @Column(name = "primary_decision")
    private String primaryDecision;
    
    @Column(name = "confidence_score")
    private Double confidenceScore;
    
    @Column(name = "summary_explanation", columnDefinition = "TEXT")
    private String summaryExplanation;
    
    @Column(name = "detailed_explanation", columnDefinition = "TEXT")
    private String detailedExplanation;
    
    @Column(name = "technical_explanation", columnDefinition = "TEXT")
    private String technicalExplanation;
    
    @Column(name = "decision_factors", columnDefinition = "JSON")
    private String decisionFactors;
    
    @Column(name = "regulatory_references", columnDefinition = "JSON")
    private String regulatoryReferences;
    
    @Column(name = "assumptions_made", columnDefinition = "JSON")
    private String assumptionsMade;
    
    @Column(name = "alternative_scenarios", columnDefinition = "JSON")
    private String alternativeScenarios;
    
    @Column(name = "data_limitations", columnDefinition = "JSON")
    private String dataLimitations;
    
    @Column(name = "decision_tree_path", columnDefinition = "JSON")
    private String decisionTreePath;
    
    @NotNull
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "generated_timestamp")
    private Date generatedTimestamp;
    
    @Column(name = "explanation_version")
    private String explanationVersion;
    
    @Column(name = "reading_level_score")
    private Integer readingLevelScore;
    
    // Getters and Setters
}

// Decision Factor Model
@Entity
@Table(name = "decision_factors")
public class DecisionFactor {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull
    @Column(name = "factor_id")
    private String factorId;
    
    @NotNull
    @Column(name = "rationale_id")
    private String rationaleId;
    
    @NotNull
    @Column(name = "factor_name")
    private String factorName;
    
    @NotNull
    @Column(name = "factor_category")
    @Enumerated(EnumType.STRING)
    private FactorCategory factorCategory;
    
    @NotNull
    @Column(name = "weight_percentage")
    private Double weightPercentage;
    
    @NotNull
    @Column(name = "influence_score")
    private Double influenceScore;
    
    @Column(name = "factor_description", columnDefinition = "TEXT")
    private String factorDescription;
    
    @Column(name = "supporting_evidence", columnDefinition = "TEXT")
    private String supportingEvidence;
    
    @Column(name = "regulatory_basis", columnDefinition = "TEXT")
    private String regulatoryBasis;
    
    @NotNull
    @Column(name = "factor_rank")
    private Integer factorRank;
    
    // Getters and Setters
}

// Explanation Request Model
public class ExplanationRequest {
    @NotNull
    private String decisionId;
    @NotNull
    private DecisionType decisionType;
    @NotNull
    private ExplanationLevel explanationLevel;
    private String userId;
    private String userRole;
    private List<String> requestedSections;
    private String outputFormat;
    
    // Getters and Setters
}

// Explanation Response Model
public class ExplanationResponse {
    private String rationaleId;
    private String decisionId;
    private DecisionType decisionType;
    private String primaryDecision;
    private Double confidenceScore;
    private String explanation;
    private List<DecisionFactorResponse> decisionFactors;
    private List<RegulatoryReference> regulatoryReferences;
    private List<String> assumptionsMade;
    private List<AlternativeScenario> alternativeScenarios;
    private List<String> dataLimitations;
    private DecisionTreeVisualization decisionTree;
    private Date generatedTimestamp;
    private Integer readingLevelScore;
    
    // Getters and Setters
}

// Enums
public enum DecisionType {
    GXP_CLASSIFICATION, SEVERITY_ASSESSMENT, CHANGE_CONTROL_EVALUATION, 
    IMPACT_ASSESSMENT, RECOMMENDATION_GENERATION
}

public enum ExplanationLevel {
    SUMMARY, DETAILED, TECHNICAL
}

public enum FactorCategory {
    REGULATORY_COMPLIANCE, PATIENT_SAFETY, OPERATIONAL_IMPACT, 
    FINANCIAL_IMPACT, HISTORICAL_PRECEDENT, SYSTEM_CONTEXT
}
```

### 2.2 API Details

```java
@RestController
@RequestMapping("/api/v1/decision-rationale")
@Validated
public class DecisionRationaleController {
    
    @Autowired
    private DecisionRationaleService rationaleService;
    
    @PostMapping("/explain")
    @ResponseStatus(HttpStatus.OK)
    public ResponseEntity<ExplanationResponse> explainDecision(
            @Valid @RequestBody ExplanationRequest request) {
        
        ExplanationResponse response = rationaleService.generateExplanation(request);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/rationale/{rationaleId}")
    public ResponseEntity<ExplanationResponse> getRationale(
            @PathVariable String rationaleId,
            @RequestParam(defaultValue = "DETAILED") ExplanationLevel level) {
        
        ExplanationResponse response = rationaleService.getRationaleById(rationaleId, level);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/decision/{decisionId}/rationale")
    public ResponseEntity<ExplanationResponse> getRationaleByDecisionId(
            @PathVariable String decisionId,
            @RequestParam(defaultValue = "DETAILED") ExplanationLevel level) {
        
        ExplanationResponse response = rationaleService.getRationaleByDecisionId(decisionId, level);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/batch-explain")
    public ResponseEntity<List<ExplanationResponse>> batchExplainDecisions(
            @Valid @RequestBody List<ExplanationRequest> requests) {
        
        List<ExplanationResponse> responses = rationaleService.batchGenerateExplanations(requests);
        return ResponseEntity.ok(responses);
    }
    
    @GetMapping("/export/{rationaleId}")
    public ResponseEntity<byte[]> exportExplanation(
            @PathVariable String rationaleId,
            @RequestParam(defaultValue = "PDF") String format) {
        
        byte[] exportData = rationaleService.exportExplanation(rationaleId, format);
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
        headers.setContentDispositionFormData("attachment", "rationale_" + rationaleId + "." + format.toLowerCase());
        
        return ResponseEntity.ok().headers(headers).body(exportData);
    }
    
    @PostMapping("/feedback")
    public ResponseEntity<Void> submitFeedback(
            @Valid @RequestBody ExplanationFeedback feedback) {
        
        rationaleService.processFeedback(feedback);
        return ResponseEntity.ok().build();
    }
    
    @GetMapping("/templates")
    public ResponseEntity<List<ExplanationTemplate>> getExplanationTemplates(
            @RequestParam(required = false) DecisionType decisionType,
            @RequestParam(required = false) ExplanationLevel level) {
        
        List<ExplanationTemplate> templates = rationaleService.getExplanationTemplates(decisionType, level);
        return ResponseEntity.ok(templates);
    }
}
```

### 2.3 Exceptions

```java
@ResponseStatus(HttpStatus.BAD_REQUEST)
public class InvalidExplanationRequestException extends RuntimeException {
    public InvalidExplanationRequestException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.NOT_FOUND)
public class RationaleNotFoundException extends RuntimeException {
    public RationaleNotFoundException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
public class ExplanationEngineUnavailableException extends RuntimeException {
    public ExplanationEngineUnavailableException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.FORBIDDEN)
public class ExplanationAccessDeniedException extends RuntimeException {
    public ExplanationAccessDeniedException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
public class ExplanationGenerationException extends RuntimeException {
    public ExplanationGenerationException(String message) {
        super(message);
    }
}

@ControllerAdvice
public class DecisionRationaleExceptionHandler {
    
    @ExceptionHandler(InvalidExplanationRequestException.class)
    public ResponseEntity<ErrorResponse> handleInvalidRequest(InvalidExplanationRequestException ex) {
        ErrorResponse error = new ErrorResponse("INVALID_EXPLANATION_REQUEST", ex.getMessage());
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(RationaleNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleRationaleNotFound(RationaleNotFoundException ex) {
        ErrorResponse error = new ErrorResponse("RATIONALE_NOT_FOUND", ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
    
    @ExceptionHandler(ExplanationAccessDeniedException.class)
    public ResponseEntity<ErrorResponse> handleAccessDenied(ExplanationAccessDeniedException ex) {
        ErrorResponse error = new ErrorResponse("EXPLANATION_ACCESS_DENIED", ex.getMessage());
        return ResponseEntity.status(HttpStatus.FORBIDDEN).body(error);
    }
    
    @ExceptionHandler(ExplanationEngineUnavailableException.class)
    public ResponseEntity<ErrorResponse> handleEngineUnavailable(ExplanationEngineUnavailableException ex) {
        ErrorResponse error = new ErrorResponse("EXPLANATION_ENGINE_UNAVAILABLE", ex.getMessage());
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(error);
    }
}
```

### 2.4 Functional Design

```mermaid
graph TD
    A[Explanation Request] --> B[Input Validation]
    B --> C{Validation Passed?}
    C -->|No| D[Return Validation Error]
    C -->|Yes| E[Load Decision Context]
    E --> F[Access Control Check]
    F --> G{Access Authorized?}
    G -->|No| H[Return Access Denied]
    G -->|Yes| I[Extract Decision Factors]
    I --> J[Rank Factor Importance]
    J --> K[Load Regulatory References]
    K --> L[Generate Base Explanation]
    L --> M[Apply Explanation Level]
    M --> N[Check Reading Level]
    N --> O{Reading Level OK?}
    O -->|No| P[Simplify Language]
    O -->|Yes| Q[Add Visual Elements]
    P --> Q
    Q --> R[Apply Security Redaction]
    R --> S[Generate Final Response]
    S --> T[Save Rationale]
    T --> U[Return Explanation]
```

### 2.5 Class Diagram

```mermaid
classDiagram
    class DecisionRationaleController {
        +explainDecision(request)
        +getRationale(rationaleId, level)
        +getRationaleByDecisionId(decisionId, level)
        +batchExplainDecisions(requests)
        +exportExplanation(rationaleId, format)
        +submitFeedback(feedback)
        +getExplanationTemplates(decisionType, level)
    }
    
    class DecisionRationaleService {
        +generateExplanation(request)
        +getRationaleById(rationaleId, level)
        +getRationaleByDecisionId(decisionId, level)
        +batchGenerateExplanations(requests)
        +exportExplanation(rationaleId, format)
        +processFeedback(feedback)
        +getExplanationTemplates(decisionType, level)
    }
    
    class ExplanationGenerator {
        +generateSummaryExplanation(decision, factors)
        +generateDetailedExplanation(decision, factors)
        +generateTechnicalExplanation(decision, factors)
        +formatExplanation(content, level)
    }
    
    class DecisionFactorAnalyzer {
        +extractDecisionFactors(decision)
        +rankFactorsByImportance(factors)
        +calculateFactorWeights(factors)
        +analyzeFactorInfluence(factors)
    }
    
    class RegulatoryReferenceService {
        +loadRegulatoryReferences(decision)
        +validateReferences(references)
        +formatRegulatoryContext(references)
    }
    
    class ReadabilityAnalyzer {
        +calculateReadingLevel(text)
        +simplifyLanguage(text, targetLevel)
        +validateReadability(text)
    }
    
    class ExplanationTemplateEngine {
        +loadTemplate(decisionType, level)
        +processTemplate(template, context)
        +customizeExplanation(template, factors)
    }
    
    class SecurityRedactionService {
        +applyRedaction(explanation, userRole)
        +identifySensitiveContent(content)
        +redactContent(content, rules)
    }
    
    class DecisionTreeVisualizer {
        +generateDecisionTree(factors, path)
        +createVisualization(tree)
        +exportTreeDiagram(tree, format)
    }
    
    DecisionRationaleController --> DecisionRationaleService
    DecisionRationaleService --> ExplanationGenerator
    DecisionRationaleService --> DecisionFactorAnalyzer
    DecisionRationaleService --> RegulatoryReferenceService
    DecisionRationaleService --> ReadabilityAnalyzer
    DecisionRationaleService --> ExplanationTemplateEngine
    DecisionRationaleService --> SecurityRedactionService
    DecisionRationaleService --> DecisionTreeVisualizer
```

### 2.6 Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    participant FactorAnalyzer
    participant ExplanationGenerator
    participant RegulatoryService
    participant ReadabilityAnalyzer
    participant SecurityService
    participant Repository
    
    Client->>Controller: POST /api/v1/decision-rationale/explain
    Controller->>Service: generateExplanation(request)
    Service->>Service: validateRequest(request)
    Service->>Service: checkAccessControl(userId, decisionId)
    Service->>FactorAnalyzer: extractDecisionFactors(decision)
    FactorAnalyzer-->>Service: DecisionFactors
    Service->>FactorAnalyzer: rankFactorsByImportance(factors)
    FactorAnalyzer-->>Service: RankedFactors
    Service->>RegulatoryService: loadRegulatoryReferences(decision)
    RegulatoryService-->>Service: RegulatoryReferences
    Service->>ExplanationGenerator: generateExplanation(factors, level)
    ExplanationGenerator-->>Service: BaseExplanation
    Service->>ReadabilityAnalyzer: checkReadingLevel(explanation)
    ReadabilityAnalyzer-->>Service: ReadingLevelScore
    Service->>SecurityService: applyRedaction(explanation, userRole)
    SecurityService-->>Service: RedactedExplanation
    Service->>Repository: saveRationale(rationale)
    Service-->>Controller: ExplanationResponse
    Controller-->>Client: HTTP 200 OK + Response
```

### 2.7 Components

```java
@Component
public class ExplanationRequestValidator {
    
    public void validateExplanationRequest(ExplanationRequest request) {
        if (request.getDecisionId() == null || request.getDecisionId().trim().isEmpty()) {
            throw new InvalidExplanationRequestException("Decision ID is required");
        }
        
        if (request.getDecisionType() == null) {
            throw new InvalidExplanationRequestException("Decision type is required");
        }
        
        if (request.getExplanationLevel() == null) {
            throw new InvalidExplanationRequestException("Explanation level is required");
        }
        
        validateDecisionType(request.getDecisionType());
        validateExplanationLevel(request.getExplanationLevel());
        validateOutputFormat(request.getOutputFormat());
    }
    
    private void validateDecisionType(DecisionType decisionType) {
        List<DecisionType> validTypes = Arrays.asList(DecisionType.values());
        if (!validTypes.contains(decisionType)) {
            throw new InvalidExplanationRequestException("Invalid decision type: " + decisionType);
        }
    }
    
    private void validateExplanationLevel(ExplanationLevel level) {
        List<ExplanationLevel> validLevels = Arrays.asList(ExplanationLevel.values());
        if (!validLevels.contains(level)) {
            throw new InvalidExplanationRequestException("Invalid explanation level: " + level);
        }
    }
    
    private void validateOutputFormat(String format) {
        if (format != null) {
            List<String> validFormats = Arrays.asList("JSON", "HTML", "PDF", "DOCX");
            if (!validFormats.contains(format.toUpperCase())) {
                throw new InvalidExplanationRequestException("Invalid output format: " + format);
            }
        }
    }
}

@Component
public class ExplanationAccessController {
    
    private static final Map<String, List<DecisionType>> ROLE_PERMISSIONS = Map.of(
        "QUALITY_MANAGER", Arrays.asList(DecisionType.values()),
        "REGULATORY_SPECIALIST", Arrays.asList(DecisionType.GXP_CLASSIFICATION, DecisionType.CHANGE_CONTROL_EVALUATION),
        "QUALITY_ANALYST", Arrays.asList(DecisionType.SEVERITY_ASSESSMENT, DecisionType.IMPACT_ASSESSMENT),
        "SYSTEM_USER", Arrays.asList(DecisionType.RECOMMENDATION_GENERATION)
    );
    
    public boolean hasAccess(String userRole, DecisionType decisionType, ExplanationLevel level) {
        if (userRole == null || decisionType == null) {
            return false;
        }
        
        List<DecisionType> allowedTypes = ROLE_PERMISSIONS.get(userRole);
        if (allowedTypes == null || !allowedTypes.contains(decisionType)) {
            return false;
        }
        
        // Technical explanations require elevated privileges
        if (level == ExplanationLevel.TECHNICAL && 
            !Arrays.asList("QUALITY_MANAGER", "REGULATORY_SPECIALIST").contains(userRole)) {
            return false;
        }
        
        return true;
    }
    
    public void validateAccess(String userId, String userRole, DecisionType decisionType, ExplanationLevel level) {
        if (!hasAccess(userRole, decisionType, level)) {
            throw new ExplanationAccessDeniedException(
                "User " + userId + " with role " + userRole + " does not have access to " + 
                decisionType + " explanations at " + level + " level"
            );
        }
    }
}
```

### 2.8 Service Layer Business Logic

```java
@Service
@Transactional
public class DecisionRationaleServiceImpl implements DecisionRationaleService {
    
    @Autowired
    private ExplanationGenerator explanationGenerator;
    
    @Autowired
    private DecisionFactorAnalyzer factorAnalyzer;
    
    @Autowired
    private RegulatoryReferenceService regulatoryService;
    
    @Autowired
    private ReadabilityAnalyzer readabilityAnalyzer;
    
    @Autowired
    private ExplanationTemplateEngine templateEngine;
    
    @Autowired
    private SecurityRedactionService redactionService;
    
    @Autowired
    private DecisionTreeVisualizer treeVisualizer;
    
    @Autowired
    private DecisionRationaleRepository rationaleRepository;
    
    @Autowired
    private ExplanationRequestValidator validator;
    
    @Autowired
    private ExplanationAccessController accessController;
    
    @Override
    public ExplanationResponse generateExplanation(ExplanationRequest request) {
        long startTime = System.currentTimeMillis();
        
        try {
            // Validate request
            validator.validateExplanationRequest(request);
            
            // Check access permissions
            accessController.validateAccess(
                request.getUserId(), 
                request.getUserRole(), 
                request.getDecisionType(), 
                request.getExplanationLevel()
            );
            
            // Generate rationale ID
            String rationaleId = generateRationaleId();
            
            // Load decision context
            DecisionContext decisionContext = loadDecisionContext(request.getDecisionId(), request.getDecisionType());
            
            // Extract and analyze decision factors
            List<DecisionFactor> factors = factorAnalyzer.extractDecisionFactors(decisionContext);
            List<DecisionFactor> rankedFactors = factorAnalyzer.rankFactorsByImportance(factors);
            
            // Load regulatory references
            List<RegulatoryReference> regulatoryRefs = regulatoryService.loadRegulatoryReferences(decisionContext);
            
            // Generate base explanation
            String baseExplanation = explanationGenerator.generateExplanation(
                decisionContext, rankedFactors, regulatoryRefs, request.getExplanationLevel()
            );
            
            // Check and adjust reading level
            int readingLevel = readabilityAnalyzer.calculateReadingLevel(baseExplanation);
            if (readingLevel > 12 && request.getExplanationLevel() != ExplanationLevel.TECHNICAL) {
                baseExplanation = readabilityAnalyzer.simplifyLanguage(baseExplanation, 12);
                readingLevel = readabilityAnalyzer.calculateReadingLevel(baseExplanation);
            }
            
            // Apply security redaction
            String finalExplanation = redactionService.applyRedaction(baseExplanation, request.getUserRole());
            
            // Generate decision tree visualization
            DecisionTreeVisualization decisionTree = treeVisualizer.generateDecisionTree(rankedFactors, decisionContext.getDecisionPath());
            
            // Create rationale entity
            DecisionRationale rationale = createRationale(
                rationaleId, request, decisionContext, rankedFactors, 
                regulatoryRefs, finalExplanation, readingLevel
            );
            
            // Save rationale
            rationale = rationaleRepository.save(rationale);
            
            // Create response
            ExplanationResponse response = convertToResponse(rationale, rankedFactors, regulatoryRefs, decisionTree);
            response.setProcessingTimeMs(System.currentTimeMillis() - startTime);
            
            return response;
            
        } catch (Exception e) {
            throw new ExplanationGenerationException("Failed to generate explanation: " + e.getMessage());
        }
    }
    
    @Override
    public List<ExplanationResponse> batchGenerateExplanations(List<ExplanationRequest> requests) {
        List<ExplanationResponse> responses = new ArrayList<>();
        
        for (ExplanationRequest request : requests) {
            try {
                ExplanationResponse response = generateExplanation(request);
                responses.add(response);
            } catch (Exception e) {
                // Log error but continue with other requests
                ExplanationResponse errorResponse = createErrorResponse(request, e.getMessage());
                responses.add(errorResponse);
            }
        }
        
        return responses;
    }
    
    @Override
    public byte[] exportExplanation(String rationaleId, String format) {
        try {
            DecisionRationale rationale = rationaleRepository.findByRationaleId(rationaleId)
                .orElseThrow(() -> new RationaleNotFoundException("Rationale not found: " + rationaleId));
            
            switch (format.toUpperCase()) {
                case "PDF":
                    return generatePdfExport(rationale);
                case "DOCX":
                    return generateDocxExport(rationale);
                case "HTML":
                    return generateHtmlExport(rationale).getBytes();
                default:
                    throw new InvalidExplanationRequestException("Unsupported export format: " + format);
            }
            
        } catch (Exception e) {
            throw new ExplanationGenerationException("Failed to export explanation: " + e.getMessage());
        }
    }
    
    private String generateRationaleId() {
        return "RAT-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 8);
    }
    
    private DecisionContext loadDecisionContext(String decisionId, DecisionType decisionType) {
        // Load decision context based on decision type
        switch (decisionType) {
            case GXP_CLASSIFICATION:
                return loadGxPClassificationContext(decisionId);
            case SEVERITY_ASSESSMENT:
                return loadSeverityAssessmentContext(decisionId);
            case CHANGE_CONTROL_EVALUATION:
                return loadChangeControlContext(decisionId);
            case IMPACT_ASSESSMENT:
                return loadImpactAssessmentContext(decisionId);
            case RECOMMENDATION_GENERATION:
                return loadRecommendationContext(decisionId);
            default:
                throw new InvalidExplanationRequestException("Unsupported decision type: " + decisionType);
        }
    }
}
```

### 2.9 Validation Rules

```java
@Component
public class ExplanationValidationRules {
    
    private static final int MAX_READING_LEVEL = 16;
    private static final int MIN_EXPLANATION_LENGTH = 100;
    private static final int MAX_EXPLANATION_LENGTH = 10000;
    
    public void validateExplanationQuality(String explanation, ExplanationLevel level) {
        if (explanation == null || explanation.trim().isEmpty()) {
            throw new ExplanationGenerationException("Generated explanation is empty");
        }
        
        if (explanation.length() < MIN_EXPLANATION_LENGTH) {
            throw new ExplanationGenerationException("Generated explanation is too short: " + explanation.length() + " characters");
        }
        
        if (explanation.length() > MAX_EXPLANATION_LENGTH) {
            throw new ExplanationGenerationException("Generated explanation is too long: " + explanation.length() + " characters");
        }
        
        validateExplanationStructure(explanation, level);
        validateRegulatoryReferences(explanation);
    }
    
    private void validateExplanationStructure(String explanation, ExplanationLevel level) {
        switch (level) {
            case SUMMARY:
                validateSummaryStructure(explanation);
                break;
            case DETAILED:
                validateDetailedStructure(explanation);
                break;
            case TECHNICAL:
                validateTechnicalStructure(explanation);
                break;
        }
    }
    
    private void validateSummaryStructure(String explanation) {
        // Summary should contain decision statement and key factors
        if (!explanation.contains("Decision:") && !explanation.contains("Classification:")) {
            throw new ExplanationGenerationException("Summary explanation missing decision statement");
        }
        
        if (!explanation.contains("Key factors:") && !explanation.contains("Primary reasons:")) {
            throw new ExplanationGenerationException("Summary explanation missing key factors");
        }
    }
    
    private void validateDetailedStructure(String explanation) {
        // Detailed should contain decision, factors, rationale, and references
        List<String> requiredSections = Arrays.asList("Decision", "Factors", "Rationale", "References");
        
        for (String section : requiredSections) {
            if (!explanation.toLowerCase().contains(section.toLowerCase())) {
                throw new ExplanationGenerationException("Detailed explanation missing required section: " + section);
            }
        }
    }
    
    private void validateTechnicalStructure(String explanation) {
        // Technical should contain algorithms, weights, and confidence scores
        List<String> technicalElements = Arrays.asList("algorithm", "weight", "confidence", "score");
        
        boolean hasTechnicalContent = technicalElements.stream()
            .anyMatch(element -> explanation.toLowerCase().contains(element));
        
        if (!hasTechnicalContent) {
            throw new ExplanationGenerationException("Technical explanation missing technical details");
        }
    }
    
    private void validateRegulatoryReferences(String explanation) {
        // Check for valid regulatory reference patterns
        Pattern regulatoryPattern = Pattern.compile("(21 CFR|ICH|FDA|EMA|ISO)\\s+\\d+", Pattern.CASE_INSENSITIVE);
        
        if (explanation.toLowerCase().contains("regulation") || explanation.toLowerCase().contains("guideline")) {
            if (!regulatoryPattern.matcher(explanation).find()) {
                throw new ExplanationGenerationException("Explanation mentions regulations but lacks specific references");
            }
        }
    }
    
    public void validateDecisionFactorConsistency(List<DecisionFactor> factors, String explanation) {
        // Ensure all high-weight factors are mentioned in explanation
        List<DecisionFactor> highWeightFactors = factors.stream()
            .filter(f -> f.getWeightPercentage() > 20.0)
            .collect(Collectors.toList());
        
        for (DecisionFactor factor : highWeightFactors) {
            if (!explanation.toLowerCase().contains(factor.getFactorName().toLowerCase())) {
                throw new ExplanationGenerationException("High-weight factor not mentioned in explanation: " + factor.getFactorName());
            }
        }
        
        // Validate weight percentages sum to approximately 100%
        double totalWeight = factors.stream()
            .mapToDouble(DecisionFactor::getWeightPercentage)
            .sum();
        
        if (Math.abs(totalWeight - 100.0) > 5.0) {
            throw new ExplanationGenerationException("Decision factor weights do not sum to 100%: " + totalWeight);
        }
    }
}
```

### 2.10 Service Integrations

```java
@Service
public class RegulatoryReferenceServiceImpl implements RegulatoryReferenceService {
    
    @Value("${regulatory.database.url}")
    private String regulatoryDatabaseUrl;
    
    @Value("${regulatory.api.key}")
    private String regulatoryApiKey;
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    @Override
    public List<RegulatoryReference> loadRegulatoryReferences(DecisionContext context) {
        String cacheKey = "regulatory_refs:" + context.getDecisionType() + ":" + context.getEventType();
        
        // Try cache first
        List<RegulatoryReference> cachedRefs = (List<RegulatoryReference>) redisTemplate.opsForValue().get(cacheKey);
        if (cachedRefs != null) {
            return cachedRefs;
        }
        
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.set("Authorization", "Bearer " + regulatoryApiKey);
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            Map<String, Object> requestBody = Map.of(
                "decisionType", context.getDecisionType().toString(),
                "eventType", context.getEventType(),
                "region", context.getRegulatoryRegion(),
                "productType", context.getProductType()
            );
            
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);
            
            ResponseEntity<RegulatoryReference[]> response = restTemplate.postForEntity(
                regulatoryDatabaseUrl + "/references/search", entity, RegulatoryReference[].class
            );
            
            List<RegulatoryReference> references = Arrays.asList(response.getBody());
            
            // Cache for 2 hours
            redisTemplate.opsForValue().set(cacheKey, references, Duration.ofHours(2));
            
            return references;
            
        } catch (Exception e) {
            throw new ExplanationGenerationException("Failed to load regulatory references: " + e.getMessage());
        }
    }
    
    @Override
    public void validateReferences(List<RegulatoryReference> references) {
        for (RegulatoryReference ref : references) {
            if (ref.getReferenceId() == null || ref.getTitle() == null) {
                throw new ExplanationGenerationException("Invalid regulatory reference: missing required fields");
            }
            
            if (ref.getEffectiveDate() != null && ref.getEffectiveDate().after(new Date())) {
                throw new ExplanationGenerationException("Regulatory reference not yet effective: " + ref.getReferenceId());
            }
            
            if (ref.getExpirationDate() != null && ref.getExpirationDate().before(new Date())) {
                throw new ExplanationGenerationException("Regulatory reference expired: " + ref.getReferenceId());
            }
        }
    }
    
    @Override
    public String formatRegulatoryContext(List<RegulatoryReference> references) {
        if (references.isEmpty()) {
            return "No specific regulatory references apply to this decision.";
        }
        
        StringBuilder context = new StringBuilder();
        context.append("This decision is based on the following regulatory guidelines:\n\n");
        
        for (RegulatoryReference ref : references) {
            context.append("• ").append(ref.getTitle())
                   .append(" (").append(ref.getReferenceId()).append(")")
                   .append("\n  ").append(ref.getDescription())
                   .append("\n  Effective: ").append(formatDate(ref.getEffectiveDate()))
                   .append("\n\n");
        }
        
        return context.toString();
    }
    
    private String formatDate(Date date) {
        if (date == null) return "Not specified";
        SimpleDateFormat formatter = new SimpleDateFormat("MMM dd, yyyy");
        return formatter.format(date);
    }
}
```

---

## 3. Frontend React Details

### 3.1 UI Architecture

```jsx
// Decision Rationale Dashboard Component
import React, { useState, useEffect } from 'react';
import { ExplanationViewer } from './ExplanationViewer';
import { DecisionTreeVisualization } from './DecisionTreeVisualization';
import { RegulatoryReferences } from './RegulatoryReferences';
import { ExplanationExport } from './ExplanationExport';
import { FeedbackForm } from './FeedbackForm';

const DecisionRationaleDashboard = ({ decisionId, decisionType }) => {
    const [explanation, setExplanation] = useState(null);
    const [explanationLevel, setExplanationLevel] = useState('DETAILED');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('explanation');

    useEffect(() => {
        if (decisionId && decisionType) {
            loadExplanation();
        }
    }, [decisionId, decisionType, explanationLevel]);

    const loadExplanation = async () => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await fetch('/api/v1/decision-rationale/explain', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                },
                body: JSON.stringify({
                    decisionId,
                    decisionType,
                    explanationLevel,
                    userId: getCurrentUserId(),
                    userRole: getCurrentUserRole()
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            setExplanation(result);
            
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="decision-rationale-dashboard">
            <header className="dashboard-header">
                <h1>Decision Rationale</h1>
                <div className="explanation-controls">
                    <select 
                        value={explanationLevel} 
                        onChange={(e) => setExplanationLevel(e.target.value)}
                        className="level-selector"
                    >
                        <option value="SUMMARY">Summary</option>
                        <option value="DETAILED">Detailed</option>
                        <option value="TECHNICAL">Technical</option>
                    </select>
                    
                    {explanation && (
                        <div className="confidence-indicator">
                            <span className="confidence-label">Confidence:</span>
                            <span className={`confidence-score ${getConfidenceClass(explanation.confidenceScore)}`}>
                                {(explanation.confidenceScore * 100).toFixed(1)}%
                            </span>
                        </div>
                    )}
                </div>
            </header>

            {error && (
                <div className="error-alert">
                    <strong>Error:</strong> {error}
                    <button onClick={() => setError(null)}>×</button>
                </div>
            )}

            {loading && (
                <div className="loading-indicator">
                    <span className="spinner"></span>
                    Generating explanation...
                </div>
            )}

            {explanation && (
                <>
                    <nav className="explanation-nav">
                        <button 
                            className={activeTab === 'explanation' ? 'active' : ''}
                            onClick={() => setActiveTab('explanation')}
                        >
                            Explanation
                        </button>
                        <button 
                            className={activeTab === 'factors' ? 'active' : ''}
                            onClick={() => setActiveTab('factors')}
                        >
                            Decision Factors
                        </button>
                        <button 
                            className={activeTab === 'tree' ? 'active' : ''}
                            onClick={() => setActiveTab('tree')}
                        >
                            Decision Tree
                        </button>
                        <button 
                            className={activeTab === 'references' ? 'active' : ''}
                            onClick={() => setActiveTab('references')}
                        >
                            Regulatory References
                        </button>
                        <button 
                            className={activeTab === 'export' ? 'active' : ''}
                            onClick={() => setActiveTab('export')}
                        >
                            Export
                        </button>
                    </nav>

                    <div className="explanation-content">
                        {activeTab === 'explanation' && (
                            <ExplanationViewer 
                                explanation={explanation}
                                level={explanationLevel}
                            />
                        )}

                        {activeTab === 'factors' && (
                            <DecisionFactorsView 
                                factors={explanation.decisionFactors}
                                totalConfidence={explanation.confidenceScore}
                            />
                        )}

                        {activeTab === 'tree' && explanation.decisionTree && (
                            <DecisionTreeVisualization 
                                decisionTree={explanation.decisionTree}
                            />
                        )}

                        {activeTab === 'references' && (
                            <RegulatoryReferences 
                                references={explanation.regulatoryReferences}
                            />
                        )}

                        {activeTab === 'export' && (
                            <ExplanationExport 
                                rationaleId={explanation.rationaleId}
                                decisionId={decisionId}
                            />
                        )}
                    </div>

                    <FeedbackForm 
                        rationaleId={explanation.rationaleId}
                        onFeedbackSubmitted={() => {/* Handle feedback */}}
                    />
                </>
            )}
        </div>
    );
};

const getConfidenceClass = (score) => {
    if (score >= 0.9) return 'high-confidence';
    if (score >= 0.7) return 'medium-confidence';
    return 'low-confidence';
};
```

### 3.2 UI Specifications

```jsx
// Explanation Viewer Component
import React, { useState } from 'react';
import { marked } from 'marked';

const ExplanationViewer = ({ explanation, level }) => {
    const [expandedSections, setExpandedSections] = useState(new Set());

    const toggleSection = (sectionId) => {
        const newExpanded = new Set(expandedSections);
        if (newExpanded.has(sectionId)) {
            newExpanded.delete(sectionId);
        } else {
            newExpanded.add(sectionId);
        }
        setExpandedSections(newExpanded);
    };

    const renderExplanation = () => {
        switch (level) {
            case 'SUMMARY':
                return renderSummaryExplanation();
            case 'DETAILED':
                return renderDetailedExplanation();
            case 'TECHNICAL':
                return renderTechnicalExplanation();
            default:
                return renderDetailedExplanation();
        }
    };

    const renderSummaryExplanation = () => (
        <div className="summary-explanation">
            <div className="decision-summary">
                <h3>Decision Summary</h3>
                <div className="primary-decision">
                    <strong>Classification:</strong> {explanation.primaryDecision}
                </div>
                <div className="confidence-score">
                    <strong>Confidence:</strong> {(explanation.confidenceScore * 100).toFixed(1)}%
                </div>
            </div>

            <div className="key-factors">
                <h3>Key Factors</h3>
                <ul>
                    {explanation.decisionFactors
                        .filter(factor => factor.weightPercentage > 15)
                        .map(factor => (
                            <li key={factor.factorId}>
                                <strong>{factor.factorName}:</strong> {factor.factorDescription}
                                <span className="factor-weight">({factor.weightPercentage.toFixed(1)}% influence)</span>
                            </li>
                        ))}
                </ul>
            </div>

            <div className="explanation-text">
                <div dangerouslySetInnerHTML={{ __html: marked(explanation.explanation) }} />
            </div>
        </div>
    );

    const renderDetailedExplanation = () => (
        <div className="detailed-explanation">
            <div className="decision-overview">
                <h3>Decision Overview</h3>
                <div className="decision-details">
                    <div className="detail-item">
                        <label>Primary Decision:</label>
                        <span>{explanation.primaryDecision}</span>
                    </div>
                    <div className="detail-item">
                        <label>Decision Type:</label>
                        <span>{explanation.decisionType}</span>
                    </div>
                    <div className="detail-item">
                        <label>Confidence Score:</label>
                        <span className={getConfidenceClass(explanation.confidenceScore)}>
                            {(explanation.confidenceScore * 100).toFixed(1)}%
                        </span>
                    </div>
                    <div className="detail-item">
                        <label>Generated:</label>
                        <span>{new Date(explanation.generatedTimestamp).toLocaleString()}</span>
                    </div>
                </div>
            </div>

            <div className="explanation-sections">
                <div className="section">
                    <h4 
                        className="section-header clickable"
                        onClick={() => toggleSection('main-explanation')}
                    >
                        Detailed Explanation
                        <span className={`expand-icon ${expandedSections.has('main-explanation') ? 'expanded' : ''}`}>
                            ▼
                        </span>
                    </h4>
                    {expandedSections.has('main-explanation') && (
                        <div className="section-content">
                            <div dangerouslySetInnerHTML={{ __html: marked(explanation.explanation) }} />
                        </div>
                    )}
                </div>

                {explanation.assumptionsMade && explanation.assumptionsMade.length > 0 && (
                    <div className="section">
                        <h4 
                            className="section-header clickable"
                            onClick={() => toggleSection('assumptions')}
                        >
                            Assumptions Made
                            <span className={`expand-icon ${expandedSections.has('assumptions') ? 'expanded' : ''}`}>
                                ▼
                            </span>
                        </h4>
                        {expandedSections.has('assumptions') && (
                            <div className="section-content">
                                <ul>
                                    {explanation.assumptionsMade.map((assumption, index) => (
                                        <li key={index}>{assumption}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                )}

                {explanation.dataLimitations && explanation.dataLimitations.length > 0 && (
                    <div className="section">
                        <h4 
                            className="section-header clickable"
                            onClick={() => toggleSection('limitations')}
                        >
                            Data Limitations
                            <span className={`expand-icon ${expandedSections.has('limitations') ? 'expanded' : ''}`}>
                                ▼
                            </span>
                        </h4>
                        {expandedSections.has('limitations') && (
                            <div className="section-content">
                                <ul>
                                    {explanation.dataLimitations.map((limitation, index) => (
                                        <li key={index}>{limitation}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                )}

                {explanation.alternativeScenarios && explanation.alternativeScenarios.length > 0 && (
                    <div className="section">
                        <h4 
                            className="section-header clickable"
                            onClick={() => toggleSection('alternatives')}
                        >
                            Alternative Scenarios
                            <span className={`expand-icon ${expandedSections.has('alternatives') ? 'expanded' : ''}`}>
                                ▼
                            </span>
                        </h4>
                        {expandedSections.has('alternatives') && (
                            <div className="section-content">
                                {explanation.alternativeScenarios.map((scenario, index) => (
                                    <div key={index} className="alternative-scenario">
                                        <h5>{scenario.scenarioName}</h5>
                                        <p>{scenario.description}</p>
                                        <div className="scenario-impact">
                                            <strong>Potential Impact:</strong> {scenario.potentialImpact}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );

    const renderTechnicalExplanation = () => (
        <div className="technical-explanation">
            <div className="technical-overview">
                <h3>Technical Analysis</h3>
                <div className="technical-metrics">
                    <div className="metric">
                        <label>Algorithm Version:</label>
                        <span>v{explanation.explanationVersion}</span>
                    </div>
                    <div className="metric">
                        <label>Processing Time:</label>
                        <span>{explanation.processingTimeMs}ms</span>
                    </div>
                    <div className="metric">
                        <label>Reading Level:</label>
                        <span>Grade {explanation.readingLevelScore}</span>
                    </div>
                </div>
            </div>

            <div className="algorithm-details">
                <h4>Algorithm Details</h4>
                <div dangerouslySetInnerHTML={{ __html: marked(explanation.explanation) }} />
            </div>

            <div className="factor-weights">
                <h4>Factor Weight Analysis</h4>
                <div className="weight-chart">
                    {explanation.decisionFactors.map(factor => (
                        <div key={factor.factorId} className="weight-bar">
                            <div className="factor-label">
                                {factor.factorName}
                            </div>
                            <div className="weight-visualization">
                                <div 
                                    className="weight-fill"
                                    style={{ width: `${factor.weightPercentage}%` }}
                                ></div>
                                <span className="weight-value">
                                    {factor.weightPercentage.toFixed(1)}%
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );

    return (
        <div className="explanation-viewer">
            {renderExplanation()}
        </div>
    );
};
```

### 3.3 API Integration

```jsx
// Decision Rationale API Service
class DecisionRationaleAPI {
    constructor() {
        this.baseURL = process.env.REACT_APP_API_BASE_URL || '/api/v1';
        this.timeout = 30000; // 30 seconds for explanation generation
    }

    async explainDecision(explanationRequest) {
        const response = await this.makeRequest('/decision-rationale/explain', {
            method: 'POST',
            body: JSON.stringify(explanationRequest)
        });
        return response;
    }

    async getRationale(rationaleId, level = 'DETAILED') {
        const queryParams = new URLSearchParams({ level });
        const response = await this.makeRequest(`/decision-rationale/rationale/${rationaleId}?${queryParams}`, {
            method: 'GET'
        });
        return response;
    }

    async getRationaleByDecisionId(decisionId, level = 'DETAILED') {
        const queryParams = new URLSearchParams({ level });
        const response = await this.makeRequest(`/decision-rationale/decision/${decisionId}/rationale?${queryParams}`, {
            method: 'GET'
        });
        return response;
    }

    async batchExplainDecisions(explanationRequests) {
        const response = await this.makeRequest('/decision-rationale/batch-explain', {
            method: 'POST',
            body: JSON.stringify(explanationRequests)
        });
        return response;
    }

    async exportExplanation(rationaleId, format = 'PDF') {
        const queryParams = new URLSearchParams({ format });
        const response = await fetch(`${this.baseURL}/decision-rationale/export/${rationaleId}?${queryParams}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${this.getAuthToken()}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.blob();
    }

    async submitFeedback(feedback) {
        const response = await this.makeRequest('/decision-rationale/feedback', {
            method: 'POST',
            body: JSON.stringify(feedback)
        });
        return response;
    }

    async getExplanationTemplates(decisionType = null, level = null) {
        const queryParams = new URLSearchParams();
        if (decisionType) queryParams.append('decisionType', decisionType);
        if (level) queryParams.append('level', level);
        
        const response = await this.makeRequest(`/decision-rationale/templates?${queryParams}`, {
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
                throw new Error('Request timeout - explanation generation taking longer than expected');
            }
            throw error;
        }
    }

    getAuthToken() {
        return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
    }
}

export default new DecisionRationaleAPI();
```

---

## 4. Database Details

### 4.1 ER Diagram

```mermaid
erDiagram
    DECISION_RATIONALES {
        BIGINT id PK
        VARCHAR rationale_id UK
        VARCHAR decision_id FK
        ENUM decision_type
        VARCHAR primary_decision
        DECIMAL confidence_score
        TEXT summary_explanation
        TEXT detailed_explanation
        TEXT technical_explanation
        JSON decision_factors
        JSON regulatory_references
        JSON assumptions_made
        JSON alternative_scenarios
        JSON data_limitations
        JSON decision_tree_path
        TIMESTAMP generated_timestamp
        VARCHAR explanation_version
        INTEGER reading_level_score
    }
    
    DECISION_FACTORS {
        BIGINT id PK
        VARCHAR factor_id UK
        VARCHAR rationale_id FK
        VARCHAR factor_name
        ENUM factor_category
        DECIMAL weight_percentage
        DECIMAL influence_score
        TEXT factor_description
        TEXT supporting_evidence
        TEXT regulatory_basis
        INTEGER factor_rank
    }
    
    REGULATORY_REFERENCES {
        BIGINT id PK
        VARCHAR reference_id UK
        VARCHAR title
        VARCHAR regulation_number
        VARCHAR issuing_authority
        TEXT description
        VARCHAR region
        DATE effective_date
        DATE expiration_date
        VARCHAR url
        BOOLEAN is_active
    }
    
    EXPLANATION_FEEDBACK {
        BIGINT id PK
        VARCHAR feedback_id UK
        VARCHAR rationale_id FK
        VARCHAR user_id
        INTEGER helpfulness_rating
        INTEGER clarity_rating
        INTEGER accuracy_rating
        TEXT comments
        JSON improvement_suggestions
        TIMESTAMP submitted_at
    }
    
    EXPLANATION_TEMPLATES {
        BIGINT id PK
        VARCHAR template_id UK
        VARCHAR template_name
        ENUM decision_type
        ENUM explanation_level
        TEXT template_content
        JSON template_variables
        BOOLEAN is_active
        TIMESTAMP created_at
        TIMESTAMP last_updated
        VARCHAR created_by
    }
    
    DECISION_RATIONALES ||--o{ DECISION_FACTORS : "contains"
    DECISION_RATIONALES ||--o{ EXPLANATION_FEEDBACK : "receives"
    EXPLANATION_TEMPLATES ||--o{ DECISION_RATIONALES : "generates"
    REGULATORY_REFERENCES ||--o{ DECISION_RATIONALES : "references"
```

### 4.2 Database Validations

```sql
-- Decision Rationales Table
CREATE TABLE decision_rationales (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    rationale_id VARCHAR(100) NOT NULL UNIQUE,
    decision_id VARCHAR(100) NOT NULL,
    decision_type ENUM('GXP_CLASSIFICATION', 'SEVERITY_ASSESSMENT', 'CHANGE_CONTROL_EVALUATION', 
                       'IMPACT_ASSESSMENT', 'RECOMMENDATION_GENERATION') NOT NULL,
    primary_decision VARCHAR(200) NOT NULL,
    confidence_score DECIMAL(4,3) CHECK (confidence_score >= 0.000 AND confidence_score <= 1.000),
    summary_explanation TEXT,
    detailed_explanation TEXT,
    technical_explanation TEXT,
    decision_factors JSON,
    regulatory_references JSON,
    assumptions_made JSON,
    alternative_scenarios JSON,
    data_limitations JSON,
    decision_tree_path JSON,
    generated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    explanation_version VARCHAR(10) NOT NULL DEFAULT '1.0',
    reading_level_score INTEGER CHECK (reading_level_score >= 1 AND reading_level_score <= 20),
    INDEX idx_rationale_id (rationale_id),
    INDEX idx_decision_id (decision_id),
    INDEX idx_decision_type (decision_type),
    INDEX idx_generated_timestamp (generated_timestamp),
    INDEX idx_confidence_score (confidence_score)
);

-- Decision Factors Table
CREATE TABLE decision_factors (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    factor_id VARCHAR(100) NOT NULL UNIQUE,
    rationale_id VARCHAR(100) NOT NULL,
    factor_name VARCHAR(200) NOT NULL,
    factor_category ENUM('REGULATORY_COMPLIANCE', 'PATIENT_SAFETY', 'OPERATIONAL_IMPACT', 
                         'FINANCIAL_IMPACT', 'HISTORICAL_PRECEDENT', 'SYSTEM_CONTEXT') NOT NULL,
    weight_percentage DECIMAL(5,2) NOT NULL CHECK (weight_percentage >= 0.00 AND weight_percentage <= 100.00),
    influence_score DECIMAL(4,3) NOT NULL CHECK (influence_score >= 0.000 AND influence_score <= 1.000),
    factor_description TEXT,
    supporting_evidence TEXT,
    regulatory_basis TEXT,
    factor_rank INTEGER NOT NULL CHECK (factor_rank > 0),
    FOREIGN KEY (rationale_id) REFERENCES decision_rationales(rationale_id) ON DELETE CASCADE,
    INDEX idx_factor_id (factor_id),
    INDEX idx_rationale_id (rationale_id),
    INDEX idx_factor_category (factor_category),
    INDEX idx_weight_percentage (weight_percentage),
    INDEX idx_factor_rank (factor_rank)
);

-- Regulatory References Table
CREATE TABLE regulatory_references (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    reference_id VARCHAR(100) NOT NULL UNIQUE,
    title VARCHAR(500) NOT NULL,
    regulation_number VARCHAR(50),
    issuing_authority VARCHAR(100) NOT NULL,
    description TEXT,
    region VARCHAR(50) NOT NULL,
    effective_date DATE,
    expiration_date DATE,
    url VARCHAR(1000),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    INDEX idx_reference_id (reference_id),
    INDEX idx_regulation_number (regulation_number),
    INDEX idx_issuing_authority (issuing_authority),
    INDEX idx_region (region),
    INDEX idx_effective_date (effective_date),
    INDEX idx_is_active (is_active),
    CONSTRAINT chk_dates CHECK (expiration_date IS NULL OR expiration_date > effective_date)
);

-- Explanation Feedback Table
CREATE TABLE explanation_feedback (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    feedback_id VARCHAR(100) NOT NULL UNIQUE,
    rationale_id VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    helpfulness_rating INTEGER CHECK (helpfulness_rating >= 1 AND helpfulness_rating <= 5),
    clarity_rating INTEGER CHECK (clarity_rating >= 1 AND clarity_rating <= 5),
    accuracy_rating INTEGER CHECK (accuracy_rating >= 1 AND accuracy_rating <= 5),
    comments TEXT,
    improvement_suggestions JSON,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rationale_id) REFERENCES decision_rationales(rationale_id) ON DELETE CASCADE,
    INDEX idx_feedback_id (feedback_id),
    INDEX idx_rationale_id (rationale_id),
    INDEX idx_user_id (user_id),
    INDEX idx_submitted_at (submitted_at)
);

-- Explanation Templates Table
CREATE TABLE explanation_templates (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    template_id VARCHAR(100) NOT NULL UNIQUE,
    template_name VARCHAR(200) NOT NULL,
    decision_type ENUM('GXP_CLASSIFICATION', 'SEVERITY_ASSESSMENT', 'CHANGE_CONTROL_EVALUATION', 
                       'IMPACT_ASSESSMENT', 'RECOMMENDATION_GENERATION') NOT NULL,
    explanation_level ENUM('SUMMARY', 'DETAILED', 'TECHNICAL') NOT NULL,
    template_content TEXT NOT NULL,
    template_variables JSON,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    INDEX idx_template_id (template_id),
    INDEX idx_decision_type (decision_type),
    INDEX idx_explanation_level (explanation_level),
    INDEX idx_is_active (is_active),
    UNIQUE KEY uk_template (decision_type, explanation_level, template_name)
);
```

---

## 5. Non Functional Requirements

### 5.1 Performance

```yaml
Performance Requirements:
  Explanation Generation:
    - Summary Level: < 2 seconds (95th percentile)
    - Detailed Level: < 3 seconds (95th percentile)
    - Technical Level: < 5 seconds (95th percentile)
    
  Throughput Targets:
    - Concurrent Explanations: 300+ simultaneous
    - Explanations per Hour: 8,000+
    - Batch Processing: 100+ explanations per batch
    
  Response Times:
    - Factor Analysis: < 1 second
    - Regulatory Reference Loading: < 500ms
    - Reading Level Analysis: < 200ms
    - Template Processing: < 300ms
    
  Resource Utilization:
    - CPU: < 75% under peak load
    - Memory: < 80% heap utilization
    - Database: < 85% connection pool usage
    - Cache Hit Ratio: > 95% for templates and references
```

### 5.2 Security

```yaml
Security Requirements:
  Data Protection:
    - Explanation content encryption at rest
    - Secure transmission of sensitive rationale data
    - Regulatory reference access control
    
  Access Control:
    - Role-based explanation level access
    - Decision-specific viewing permissions
    - Audit trail for explanation access
    
  Content Redaction:
    - Automatic sensitive information masking
    - Role-based content filtering
    - Regulatory compliance redaction rules
    
  Audit Requirements:
    - Complete explanation generation audit trail
    - User access logging
    - Feedback submission tracking
```

### 5.3 Logging

```java
@Component
public class DecisionRationaleLogger {
    
    private static final Logger logger = LoggerFactory.getLogger(DecisionRationaleLogger.class);
    private static final Logger auditLogger = LoggerFactory.getLogger("DECISION_RATIONALE_AUDIT");
    private static final Logger performanceLogger = LoggerFactory.getLogger("DECISION_RATIONALE_PERFORMANCE");
    private static final Logger usageLogger = LoggerFactory.getLogger("EXPLANATION_USAGE");
    
    public void logExplanationGeneration(String rationaleId, String decisionId, DecisionType decisionType, 
                                       ExplanationLevel level, long processingTime) {
        auditLogger.info("Explanation generated - RationaleId: {}, DecisionId: {}, Type: {}, Level: {}, ProcessingTime: {}ms", 
            rationaleId, decisionId, decisionType, level, processingTime);
        
        if (processingTime > getPerformanceThreshold(level)) {
            performanceLogger.warn("Slow explanation generation - RationaleId: {}, Level: {}, ProcessingTime: {}ms", 
                rationaleId, level, processingTime);
        }
    }
    
    public void logExplanationAccess(String rationaleId, String userId, String userRole, ExplanationLevel level) {
        auditLogger.info("Explanation accessed - RationaleId: {}, UserId: {}, UserRole: {}, Level: {}", 
            rationaleId, userId, userRole, level);
        
        usageLogger.info("Explanation usage - RationaleId: {}, Level: {}, AccessTime: {}", 
            rationaleId, level, Instant.now());
    }
    
    public void logFeedbackSubmission(String feedbackId, String rationaleId, String userId, 
                                    int helpfulnessRating, int clarityRating, int accuracyRating) {
        auditLogger.info("Feedback submitted - FeedbackId: {}, RationaleId: {}, UserId: {}, " +
            "Helpfulness: {}, Clarity: {}, Accuracy: {}", 
            feedbackId, rationaleId, userId, helpfulnessRating, clarityRating, accuracyRating);
        
        if (clarityRating <= 2 || accuracyRating <= 2) {
            logger.warn("Low-quality explanation feedback - RationaleId: {}, Clarity: {}, Accuracy: {}", 
                rationaleId, clarityRating, accuracyRating);
        }
    }
    
    public void logRegulatoryReferenceUsage(String referenceId, String decisionType, String region) {
        usageLogger.info("Regulatory reference used - ReferenceId: {}, DecisionType: {}, Region: {}", 
            referenceId, decisionType, region);
    }
    
    public void logExplanationExport(String rationaleId, String format, String userId) {
        auditLogger.info("Explanation exported - RationaleId: {}, Format: {}, UserId: {}", 
            rationaleId, format, userId);
    }
    
    private long getPerformanceThreshold(ExplanationLevel level) {
        switch (level) {
            case SUMMARY: return 2000;
            case DETAILED: return 3000;
            case TECHNICAL: return 5000;
            default: return 3000;
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
  Apache Commons Text: 1.10.0
  Freemarker: 2.3.32
  iText PDF: 7.2.5
  Apache POI: 5.2.4

Frontend Dependencies:
  React: 18.2.0
  React Router: 6.11.0
  Marked: 5.1.0
  D3.js: 7.8.0
  Chart.js: 4.3.0
  Material-UI: 5.13.0
  React Query: 4.29.0
  React PDF: 6.2.0
  File-saver: 2.0.5

Infrastructure Dependencies:
  MySQL: 8.0.33
  Redis: 7.0.11
  Nginx: 1.24.0
  Docker: 24.0.0
  Kubernetes: 1.27.0
  Prometheus: 2.45.0
  Grafana: 10.0.0
  Elasticsearch: 8.8.0

External Services:
  Regulatory Database API: v2.1
  Natural Language Processing API: v1.3
  Document Generation Service: v2.0
  Notification Service: v1.5
  Authentication Service: OAuth 2.0
```

---

## 7. Assumptions

```yaml
Technical Assumptions:
  - Decision logic is transparent and can be explained algorithmically
  - Natural language processing capabilities are available for readability analysis
  - Template engine supports dynamic content generation with variables
  - Regulatory database provides current and accurate reference information
  - Export functionality supports multiple output formats (PDF, DOCX, HTML)

Business Assumptions:
  - Users require different levels of explanation detail based on their roles
  - Regulatory references are essential for compliance and audit purposes
  - Explanation quality can be measured through user feedback
  - Decision factors can be ranked and weighted quantitatively
  - Alternative scenarios provide valuable context for decision understanding

Operational Assumptions:
  - 24/7 availability for explanation generation
  - Automated backup of explanation data and templates
  - Performance monitoring and alerting for slow explanations
  - Regular updates to explanation templates based on feedback
  - Integration with existing audit and compliance systems

Data Assumptions:
  - Decision data contains sufficient information for meaningful explanations
  - Regulatory references are maintained and updated regularly
  - Historical explanation data is available for improvement analysis
  - User feedback is collected and analyzed for system enhancement
  - Template effectiveness is measured and optimized over time

Regulatory Assumptions:
  - AI transparency requirements are clearly defined and documented
  - Explanation retention periods comply with regulatory requirements
  - Audit trails meet regulatory standards for traceability
  - Access controls satisfy data protection and privacy regulations
  - Export formats meet regulatory submission requirements
```