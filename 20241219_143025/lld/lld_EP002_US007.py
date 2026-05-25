# Low Level Design Document

## Epic ID: EP002
## User Story ID: US007
## Title: Context-Backed Decision Rationale System

---

## 1. Objective

Design and implement a comprehensive context-backed decision rationale system that provides AI recommendations with detailed rationale including regulatory citations, historical precedents, and contextual evidence with role-based access controls and audit capabilities.

---

## 2. Backend Spring Boot API Details

### 2.1 API Model

```java
// Context-Backed Rationale Model
@Entity
@Table(name = "context_backed_rationales")
public class ContextBackedRationale {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull
    @Column(name = "rationale_id")
    private String rationaleId;
    
    @NotNull
    @Column(name = "recommendation_id")
    private String recommendationId;
    
    @NotNull
    @Column(name = "event_id")
    private String eventId;
    
    @NotNull
    @Column(name = "rationale_type")
    @Enumerated(EnumType.STRING)
    private RationaleType rationaleType;
    
    @Column(name = "executive_summary", columnDefinition = "TEXT")
    private String executiveSummary;
    
    @Column(name = "detailed_analysis", columnDefinition = "TEXT")
    private String detailedAnalysis;
    
    @Column(name = "technical_rationale", columnDefinition = "TEXT")
    private String technicalRationale;
    
    @Column(name = "regulatory_citations", columnDefinition = "JSON")
    private String regulatoryCitations;
    
    @Column(name = "historical_precedents", columnDefinition = "JSON")
    private String historicalPrecedents;
    
    @Column(name = "contextual_factors", columnDefinition = "JSON")
    private String contextualFactors;
    
    @Column(name = "confidence_indicators", columnDefinition = "JSON")
    private String confidenceIndicators;
    
    @Column(name = "data_limitations", columnDefinition = "JSON")
    private String dataLimitations;
    
    @Column(name = "validation_steps", columnDefinition = "JSON")
    private String validationSteps;
    
    @NotNull
    @Column(name = "overall_confidence_score")
    private Double overallConfidenceScore;
    
    @NotNull
    @Column(name = "access_level")
    @Enumerated(EnumType.STRING)
    private AccessLevel accessLevel;
    
    @NotNull
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "generated_timestamp")
    private Date generatedTimestamp;
    
    @Column(name = "last_modified_timestamp")
    @Temporal(TemporalType.TIMESTAMP)
    private Date lastModifiedTimestamp;
    
    @Column(name = "generated_by")
    private String generatedBy;
    
    @Column(name = "reviewed_by")
    private String reviewedBy;
    
    @Column(name = "review_status")
    @Enumerated(EnumType.STRING)
    private ReviewStatus reviewStatus;
    
    // Getters and Setters
}

// Regulatory Citation Model
@Entity
@Table(name = "regulatory_citations")
public class RegulatoryCitation {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull
    @Column(name = "citation_id")
    private String citationId;
    
    @NotNull
    @Column(name = "rationale_id")
    private String rationaleId;
    
    @NotNull
    @Column(name = "regulation_title")
    private String regulationTitle;
    
    @NotNull
    @Column(name = "regulation_number")
    private String regulationNumber;
    
    @NotNull
    @Column(name = "issuing_authority")
    private String issuingAuthority;
    
    @Column(name = "section_reference")
    private String sectionReference;
    
    @Column(name = "specific_clause", columnDefinition = "TEXT")
    private String specificClause;
    
    @NotNull
    @Column(name = "relevance_score")
    private Double relevanceScore;
    
    @NotNull
    @Column(name = "citation_type")
    @Enumerated(EnumType.STRING)
    private CitationType citationType;
    
    @Column(name = "source_url")
    private String sourceUrl;
    
    @Column(name = "effective_date")
    @Temporal(TemporalType.DATE)
    private Date effectiveDate;
    
    @Column(name = "is_primary_source")
    private Boolean isPrimarySource;
    
    // Getters and Setters
}

// Rationale Request Model
public class RationaleRequest {
    @NotNull
    private String recommendationId;
    @NotNull
    private String eventId;
    @NotNull
    private RationaleType rationaleType;
    private String userId;
    private String userRole;
    private AccessLevel requestedAccessLevel;
    private List<String> requestedSections;
    private Boolean includeHistoricalPrecedents;
    private Boolean includeRegulatoryCitations;
    private Boolean includeContextualFactors;
    
    // Getters and Setters
}

// Rationale Response Model
public class RationaleResponse {
    private String rationaleId;
    private String recommendationId;
    private String eventId;
    private RationaleType rationaleType;
    private String rationale;
    private List<RegulatoryCitationResponse> regulatoryCitations;
    private List<HistoricalPrecedentResponse> historicalPrecedents;
    private List<ContextualFactorResponse> contextualFactors;
    private ConfidenceIndicators confidenceIndicators;
    private List<String> dataLimitations;
    private List<String> validationSteps;
    private Double overallConfidenceScore;
    private AccessLevel accessLevel;
    private Date generatedTimestamp;
    private ReviewStatus reviewStatus;
    
    // Getters and Setters
}

// Enums
public enum RationaleType {
    EXECUTIVE_SUMMARY, DETAILED_ANALYSIS, TECHNICAL_RATIONALE, COMPLIANCE_FOCUSED
}

public enum AccessLevel {
    PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
}

public enum ReviewStatus {
    PENDING, IN_REVIEW, APPROVED, REJECTED, REQUIRES_REVISION
}

public enum CitationType {
    PRIMARY_REGULATION, SUPPORTING_GUIDELINE, INDUSTRY_STANDARD, PRECEDENT_CASE
}
```

### 2.2 API Details

```java
@RestController
@RequestMapping("/api/v1/context-rationale")
@Validated
public class ContextRationaleController {
    
    @Autowired
    private ContextRationaleService rationaleService;
    
    @PostMapping("/generate")
    @ResponseStatus(HttpStatus.OK)
    public ResponseEntity<RationaleResponse> generateRationale(
            @Valid @RequestBody RationaleRequest request) {
        
        RationaleResponse response = rationaleService.generateContextBackedRationale(request);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/rationale/{rationaleId}")
    public ResponseEntity<RationaleResponse> getRationale(
            @PathVariable String rationaleId,
            @RequestParam(required = false) String userId,
            @RequestParam(required = false) String userRole) {
        
        RationaleResponse response = rationaleService.getRationaleById(rationaleId, userId, userRole);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/recommendation/{recommendationId}/rationale")
    public ResponseEntity<RationaleResponse> getRationaleByRecommendation(
            @PathVariable String recommendationId,
            @RequestParam(defaultValue = "DETAILED_ANALYSIS") RationaleType rationaleType,
            @RequestParam(required = false) String userId,
            @RequestParam(required = false) String userRole) {
        
        RationaleResponse response = rationaleService.getRationaleByRecommendationId(
            recommendationId, rationaleType, userId, userRole);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/citations/validate")
    public ResponseEntity<CitationValidationResponse> validateCitations(
            @Valid @RequestBody CitationValidationRequest request) {
        
        CitationValidationResponse response = rationaleService.validateCitations(request);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/export")
    public ResponseEntity<byte[]> exportRationale(
            @Valid @RequestBody RationaleExportRequest request) {
        
        byte[] exportData = rationaleService.exportRationale(request);
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
        headers.setContentDispositionFormData("attachment", 
            "rationale_" + request.getRationaleId() + "." + request.getFormat().toLowerCase());
        
        return ResponseEntity.ok().headers(headers).body(exportData);
    }
    
    @PostMapping("/annotations")
    public ResponseEntity<AnnotationResponse> addAnnotation(
            @Valid @RequestBody AnnotationRequest request) {
        
        AnnotationResponse response = rationaleService.addAnnotation(request);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/annotations/{rationaleId}")
    public ResponseEntity<List<AnnotationResponse>> getAnnotations(
            @PathVariable String rationaleId,
            @RequestParam(required = false) String userId) {
        
        List<AnnotationResponse> annotations = rationaleService.getAnnotations(rationaleId, userId);
        return ResponseEntity.ok(annotations);
    }
    
    @PostMapping("/review")
    public ResponseEntity<ReviewResponse> submitReview(
            @Valid @RequestBody ReviewRequest request) {
        
        ReviewResponse response = rationaleService.submitReview(request);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/confidence/breakdown/{rationaleId}")
    public ResponseEntity<ConfidenceBreakdownResponse> getConfidenceBreakdown(
            @PathVariable String rationaleId) {
        
        ConfidenceBreakdownResponse response = rationaleService.getConfidenceBreakdown(rationaleId);
        return ResponseEntity.ok(response);
    }
}
```

### 2.3 Exceptions

```java
@ResponseStatus(HttpStatus.BAD_REQUEST)
public class InvalidRationaleRequestException extends RuntimeException {
    public InvalidRationaleRequestException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.NOT_FOUND)
public class RationaleNotFoundException extends RuntimeException {
    public RationaleNotFoundException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.FORBIDDEN)
public class RationaleAccessDeniedException extends RuntimeException {
    public RationaleAccessDeniedException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
public class ContextRetrievalException extends RuntimeException {
    public ContextRetrievalException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.CONFLICT)
public class CitationValidationException extends RuntimeException {
    public CitationValidationException(String message) {
        super(message);
    }
}

@ControllerAdvice
public class ContextRationaleExceptionHandler {
    
    @ExceptionHandler(InvalidRationaleRequestException.class)
    public ResponseEntity<ErrorResponse> handleInvalidRequest(InvalidRationaleRequestException ex) {
        ErrorResponse error = new ErrorResponse("INVALID_RATIONALE_REQUEST", ex.getMessage());
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(RationaleNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleRationaleNotFound(RationaleNotFoundException ex) {
        ErrorResponse error = new ErrorResponse("RATIONALE_NOT_FOUND", ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
    
    @ExceptionHandler(RationaleAccessDeniedException.class)
    public ResponseEntity<ErrorResponse> handleAccessDenied(RationaleAccessDeniedException ex) {
        ErrorResponse error = new ErrorResponse("RATIONALE_ACCESS_DENIED", ex.getMessage());
        return ResponseEntity.status(HttpStatus.FORBIDDEN).body(error);
    }
    
    @ExceptionHandler(ContextRetrievalException.class)
    public ResponseEntity<ErrorResponse> handleContextRetrieval(ContextRetrievalException ex) {
        ErrorResponse error = new ErrorResponse("CONTEXT_RETRIEVAL_ERROR", ex.getMessage());
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(error);
    }
}
```

### 2.4 Functional Design

```mermaid
graph TD
    A[Rationale Request] --> B[Input Validation]
    B --> C{Validation Passed?}
    C -->|No| D[Return Validation Error]
    C -->|Yes| E[Access Control Check]
    E --> F{Access Authorized?}
    F -->|No| G[Return Access Denied]
    F -->|Yes| H[Load Recommendation Context]
    H --> I[Retrieve Regulatory Citations]
    I --> J[Fetch Historical Precedents]
    J --> K[Analyze Contextual Factors]
    K --> L[Generate Base Rationale]
    L --> M[Apply Access Level Filtering]
    M --> N[Calculate Confidence Scores]
    N --> O[Validate Citations]
    O --> P[Format Response]
    P --> Q[Save Rationale]
    Q --> R[Create Audit Trail]
    R --> S[Return Context-Backed Rationale]
```

### 2.5 Class Diagram

```mermaid
classDiagram
    class ContextRationaleController {
        +generateRationale(request)
        +getRationale(rationaleId, userId, userRole)
        +getRationaleByRecommendation(recommendationId, type, userId, userRole)
        +validateCitations(request)
        +exportRationale(request)
        +addAnnotation(request)
        +getAnnotations(rationaleId, userId)
        +submitReview(request)
        +getConfidenceBreakdown(rationaleId)
    }
    
    class ContextRationaleService {
        +generateContextBackedRationale(request)
        +getRationaleById(rationaleId, userId, userRole)
        +getRationaleByRecommendationId(recommendationId, type, userId, userRole)
        +validateCitations(request)
        +exportRationale(request)
        +addAnnotation(request)
        +getAnnotations(rationaleId, userId)
        +submitReview(request)
        +getConfidenceBreakdown(rationaleId)
    }
    
    class RegulatoryContextProvider {
        +retrieveRegulatoryCitations(eventContext)
        +validateCitationAccuracy(citations)
        +rankCitationsByRelevance(citations, context)
        +resolveConflictingGuidance(citations)
    }
    
    class HistoricalPrecedentAnalyzer {
        +findSimilarPrecedents(eventContext)
        +analyzeOutcomes(precedents)
        +calculateRelevanceScores(precedents, context)
        +extractLessonsLearned(precedents)
    }
    
    class ContextualFactorExtractor {
        +identifyContextualFactors(event, recommendation)
        +analyzeFactorInfluence(factors)
        +calculateFactorWeights(factors)
        +generateFactorExplanations(factors)
    }
    
    class RationaleGenerator {
        +generateExecutiveSummary(context, citations, precedents)
        +generateDetailedAnalysis(context, citations, precedents)
        +generateTechnicalRationale(context, citations, precedents)
        +formatRationale(content, type, accessLevel)
    }
    
    class AccessControlManager {
        +validateAccess(userId, userRole, accessLevel)
        +filterSensitiveContent(rationale, userRole)
        +determineAccessLevel(content, context)
        +applyRedactionRules(content, accessLevel)
    }
    
    class ConfidenceCalculator {
        +calculateOverallConfidence(citations, precedents, factors)
        +calculateCitationConfidence(citations)
        +calculatePrecedentConfidence(precedents)
        +calculateContextConfidence(factors)
    }
    
    ContextRationaleController --> ContextRationaleService
    ContextRationaleService --> RegulatoryContextProvider
    ContextRationaleService --> HistoricalPrecedentAnalyzer
    ContextRationaleService --> ContextualFactorExtractor
    ContextRationaleService --> RationaleGenerator
    ContextRationaleService --> AccessControlManager
    ContextRationaleService --> ConfidenceCalculator
```

### 2.6 Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    participant RegProvider
    participant HistAnalyzer
    participant ContextExtractor
    participant RationaleGen
    participant AccessMgr
    participant Repository
    
    Client->>Controller: POST /api/v1/context-rationale/generate
    Controller->>Service: generateContextBackedRationale(request)
    Service->>Service: validateRequest(request)
    Service->>AccessMgr: validateAccess(userId, userRole, accessLevel)
    AccessMgr-->>Service: AccessValidation
    Service->>RegProvider: retrieveRegulatoryCitations(eventContext)
    RegProvider-->>Service: RegulatoryCitations
    Service->>HistAnalyzer: findSimilarPrecedents(eventContext)
    HistAnalyzer-->>Service: HistoricalPrecedents
    Service->>ContextExtractor: identifyContextualFactors(event, recommendation)
    ContextExtractor-->>Service: ContextualFactors
    Service->>RationaleGen: generateRationale(context, citations, precedents, type)
    RationaleGen-->>Service: GeneratedRationale
    Service->>AccessMgr: filterSensitiveContent(rationale, userRole)
    AccessMgr-->>Service: FilteredRationale
    Service->>Service: calculateConfidenceScores(citations, precedents, factors)
    Service->>Repository: saveRationale(rationale)
    Service-->>Controller: RationaleResponse
    Controller-->>Client: HTTP 200 OK + Response
```

### 2.7 Components

```java
@Component
public class RationaleRequestValidator {
    
    public void validateRationaleRequest(RationaleRequest request) {
        if (request.getRecommendationId() == null || request.getRecommendationId().trim().isEmpty()) {
            throw new InvalidRationaleRequestException("Recommendation ID is required");
        }
        
        if (request.getEventId() == null || request.getEventId().trim().isEmpty()) {
            throw new InvalidRationaleRequestException("Event ID is required");
        }
        
        if (request.getRationaleType() == null) {
            throw new InvalidRationaleRequestException("Rationale type is required");
        }
        
        validateRationaleType(request.getRationaleType());
        validateAccessLevel(request.getRequestedAccessLevel());
        validateUserCredentials(request.getUserId(), request.getUserRole());
    }
    
    private void validateRationaleType(RationaleType rationaleType) {
        List<RationaleType> validTypes = Arrays.asList(RationaleType.values());
        if (!validTypes.contains(rationaleType)) {
            throw new InvalidRationaleRequestException("Invalid rationale type: " + rationaleType);
        }
    }
    
    private void validateAccessLevel(AccessLevel accessLevel) {
        if (accessLevel != null) {
            List<AccessLevel> validLevels = Arrays.asList(AccessLevel.values());
            if (!validLevels.contains(accessLevel)) {
                throw new InvalidRationaleRequestException("Invalid access level: " + accessLevel);
            }
        }
    }
    
    private void validateUserCredentials(String userId, String userRole) {
        if (userId != null && (userRole == null || userRole.trim().isEmpty())) {
            throw new InvalidRationaleRequestException("User role is required when user ID is provided");
        }
    }
}

@Component
public class RationaleAccessController {
    
    private static final Map<String, List<AccessLevel>> ROLE_ACCESS_LEVELS = Map.of(
        "QUALITY_MANAGER", Arrays.asList(AccessLevel.values()),
        "REGULATORY_SPECIALIST", Arrays.asList(AccessLevel.PUBLIC, AccessLevel.INTERNAL, AccessLevel.CONFIDENTIAL),
        "QUALITY_ANALYST", Arrays.asList(AccessLevel.PUBLIC, AccessLevel.INTERNAL),
        "AUDITOR", Arrays.asList(AccessLevel.PUBLIC, AccessLevel.INTERNAL, AccessLevel.CONFIDENTIAL),
        "EXTERNAL_USER", Arrays.asList(AccessLevel.PUBLIC)
    );
    
    public boolean hasAccess(String userRole, AccessLevel accessLevel) {
        if (userRole == null || accessLevel == null) {
            return false;
        }
        
        List<AccessLevel> allowedLevels = ROLE_ACCESS_LEVELS.get(userRole);
        return allowedLevels != null && allowedLevels.contains(accessLevel);
    }
    
    public AccessLevel determineMaxAccessLevel(String userRole) {
        List<AccessLevel> allowedLevels = ROLE_ACCESS_LEVELS.get(userRole);
        if (allowedLevels == null || allowedLevels.isEmpty()) {
            return AccessLevel.PUBLIC;
        }
        
        // Return highest access level allowed for the role
        if (allowedLevels.contains(AccessLevel.RESTRICTED)) return AccessLevel.RESTRICTED;
        if (allowedLevels.contains(AccessLevel.CONFIDENTIAL)) return AccessLevel.CONFIDENTIAL;
        if (allowedLevels.contains(AccessLevel.INTERNAL)) return AccessLevel.INTERNAL;
        return AccessLevel.PUBLIC;
    }
    
    public void validateAccess(String userId, String userRole, AccessLevel requestedLevel) {
        if (!hasAccess(userRole, requestedLevel)) {
            throw new RationaleAccessDeniedException(
                "User " + userId + " with role " + userRole + 
                " does not have access to " + requestedLevel + " level rationale"
            );
        }
    }
    
    public String filterSensitiveContent(String content, String userRole) {
        AccessLevel maxLevel = determineMaxAccessLevel(userRole);
        
        switch (maxLevel) {
            case PUBLIC:
                return applyPublicRedaction(content);
            case INTERNAL:
                return applyInternalRedaction(content);
            case CONFIDENTIAL:
                return applyConfidentialRedaction(content);
            case RESTRICTED:
                return content; // No redaction for restricted access
            default:
                return applyPublicRedaction(content);
        }
    }
    
    private String applyPublicRedaction(String content) {
        // Redact sensitive information for public access
        return content.replaceAll("\\[CONFIDENTIAL\\].*?\\[/CONFIDENTIAL\\]", "[REDACTED]")
                     .replaceAll("\\[INTERNAL\\].*?\\[/INTERNAL\\]", "[REDACTED]")
                     .replaceAll("\\[RESTRICTED\\].*?\\[/RESTRICTED\\]", "[REDACTED]");
    }
    
    private String applyInternalRedaction(String content) {
        // Redact only confidential and restricted information
        return content.replaceAll("\\[CONFIDENTIAL\\].*?\\[/CONFIDENTIAL\\]", "[REDACTED]")
                     .replaceAll("\\[RESTRICTED\\].*?\\[/RESTRICTED\\]", "[REDACTED]");
    }
    
    private String applyConfidentialRedaction(String content) {
        // Redact only restricted information
        return content.replaceAll("\\[RESTRICTED\\].*?\\[/RESTRICTED\\]", "[REDACTED]");
    }
}
```

### 2.8 Service Layer Business Logic

```java
@Service
@Transactional
public class ContextRationaleServiceImpl implements ContextRationaleService {
    
    @Autowired
    private RegulatoryContextProvider regulatoryProvider;
    
    @Autowired
    private HistoricalPrecedentAnalyzer precedentAnalyzer;
    
    @Autowired
    private ContextualFactorExtractor factorExtractor;
    
    @Autowired
    private RationaleGenerator rationaleGenerator;
    
    @Autowired
    private AccessControlManager accessControlManager;
    
    @Autowired
    private ConfidenceCalculator confidenceCalculator;
    
    @Autowired
    private ContextBackedRationaleRepository rationaleRepository;
    
    @Autowired
    private RationaleRequestValidator validator;
    
    @Autowired
    private RationaleAccessController accessController;
    
    @Override
    public RationaleResponse generateContextBackedRationale(RationaleRequest request) {
        long startTime = System.currentTimeMillis();
        
        try {
            // Validate request
            validator.validateRationaleRequest(request);
            
            // Validate access permissions
            AccessLevel requestedLevel = request.getRequestedAccessLevel() != null ? 
                request.getRequestedAccessLevel() : 
                accessController.determineMaxAccessLevel(request.getUserRole());
            
            accessController.validateAccess(request.getUserId(), request.getUserRole(), requestedLevel);
            
            // Generate rationale ID
            String rationaleId = generateRationaleId();
            
            // Load event and recommendation context
            EventRecommendationContext context = loadEventRecommendationContext(
                request.getEventId(), request.getRecommendationId()
            );
            
            // Retrieve regulatory citations
            List<RegulatoryCitation> citations = Collections.emptyList();
            if (request.getIncludeRegulatoryCitations() == null || request.getIncludeRegulatoryCitations()) {
                citations = regulatoryProvider.retrieveRegulatoryCitations(context);
            }
            
            // Find historical precedents
            List<HistoricalPrecedent> precedents = Collections.emptyList();
            if (request.getIncludeHistoricalPrecedents() == null || request.getIncludeHistoricalPrecedents()) {
                precedents = precedentAnalyzer.findSimilarPrecedents(context);
            }
            
            // Extract contextual factors
            List<ContextualFactor> factors = Collections.emptyList();
            if (request.getIncludeContextualFactors() == null || request.getIncludeContextualFactors()) {
                factors = factorExtractor.identifyContextualFactors(context);
            }
            
            // Generate rationale content
            String rationaleContent = rationaleGenerator.generateRationale(
                context, citations, precedents, factors, request.getRationaleType()
            );
            
            // Apply access control filtering
            String filteredContent = accessController.filterSensitiveContent(
                rationaleContent, request.getUserRole()
            );
            
            // Calculate confidence scores
            ConfidenceIndicators confidenceIndicators = confidenceCalculator.calculateConfidenceScores(
                citations, precedents, factors, context
            );
            
            // Identify data limitations and validation steps
            List<String> dataLimitations = identifyDataLimitations(citations, precedents, factors);
            List<String> validationSteps = generateValidationSteps(context, confidenceIndicators);
            
            // Create rationale entity
            ContextBackedRationale rationale = createRationale(
                rationaleId, request, context, filteredContent, citations, 
                precedents, factors, confidenceIndicators, dataLimitations, 
                validationSteps, requestedLevel
            );
            
            rationale.setProcessingTimeMs(System.currentTimeMillis() - startTime);
            
            // Save rationale
            rationale = rationaleRepository.save(rationale);
            
            // Create audit trail
            createAuditTrail(rationale, request);
            
            // Convert to response
            RationaleResponse response = convertToResponse(rationale, citations, precedents, factors);
            
            return response;
            
        } catch (Exception e) {
            throw new ContextRetrievalException("Failed to generate context-backed rationale: " + e.getMessage());
        }
    }
    
    @Override
    public CitationValidationResponse validateCitations(CitationValidationRequest request) {
        try {
            List<CitationValidationResult> validationResults = new ArrayList<>();
            
            for (String citationId : request.getCitationIds()) {
                CitationValidationResult result = validateSingleCitation(citationId);
                validationResults.add(result);
            }
            
            // Calculate overall validation score
            double overallScore = validationResults.stream()
                .mapToDouble(CitationValidationResult::getValidationScore)
                .average()
                .orElse(0.0);
            
            // Identify broken links or invalid references
            List<String> brokenLinks = validationResults.stream()
                .filter(r -> !r.isLinkValid())
                .map(CitationValidationResult::getCitationId)
                .collect(Collectors.toList());
            
            CitationValidationResponse response = new CitationValidationResponse();
            response.setValidationId(generateValidationId());
            response.setValidationResults(validationResults);
            response.setOverallValidationScore(overallScore);
            response.setBrokenLinks(brokenLinks);
            response.setValidationTimestamp(new Date());
            
            return response;
            
        } catch (Exception e) {
            throw new CitationValidationException("Failed to validate citations: " + e.getMessage());
        }
    }
    
    @Override
    public byte[] exportRationale(RationaleExportRequest request) {
        try {
            ContextBackedRationale rationale = rationaleRepository.findByRationaleId(request.getRationaleId())
                .orElseThrow(() -> new RationaleNotFoundException("Rationale not found: " + request.getRationaleId()));
            
            // Validate access
            accessController.validateAccess(request.getUserId(), request.getUserRole(), rationale.getAccessLevel());
            
            switch (request.getFormat().toUpperCase()) {
                case "PDF":
                    return generatePdfExport(rationale, request);
                case "DOCX":
                    return generateDocxExport(rationale, request);
                case "HTML":
                    return generateHtmlExport(rationale, request).getBytes();
                case "JSON":
                    return generateJsonExport(rationale, request).getBytes();
                default:
                    throw new InvalidRationaleRequestException("Unsupported export format: " + request.getFormat());
            }
            
        } catch (Exception e) {
            throw new ContextRetrievalException("Failed to export rationale: " + e.getMessage());
        }
    }
    
    private EventRecommendationContext loadEventRecommendationContext(String eventId, String recommendationId) {
        // Load event details
        QualityEvent event = eventRepository.findByEventId(eventId)
            .orElseThrow(() -> new RationaleNotFoundException("Event not found: " + eventId));
        
        // Load recommendation details
        Recommendation recommendation = recommendationRepository.findByRecommendationId(recommendationId)
            .orElseThrow(() -> new RationaleNotFoundException("Recommendation not found: " + recommendationId));
        
        // Create context object
        EventRecommendationContext context = new EventRecommendationContext();
        context.setEvent(event);
        context.setRecommendation(recommendation);
        context.setEventType(event.getEventType());
        context.setProductLine(event.getProductLine());
        context.setProcessArea(event.getProcessArea());
        context.setSeverityLevel(event.getSeverityLevel());
        context.setGxpClassification(event.getGxpClassification());
        
        return context;
    }
    
    private List<String> identifyDataLimitations(
            List<RegulatoryCitation> citations, 
            List<HistoricalPrecedent> precedents, 
            List<ContextualFactor> factors) {
        
        List<String> limitations = new ArrayList<>();
        
        if (citations.isEmpty()) {
            limitations.add("No regulatory citations available for this event type");
        } else if (citations.size() < 3) {
            limitations.add("Limited regulatory guidance available - only " + citations.size() + " relevant citations found");
        }
        
        if (precedents.isEmpty()) {
            limitations.add("No similar historical precedents found");
        } else if (precedents.size() < 5) {
            limitations.add("Limited historical data - only " + precedents.size() + " similar cases found");
        }
        
        if (factors.isEmpty()) {
            limitations.add("Limited contextual factors identified");
        }
        
        // Check for outdated citations
        long outdatedCitations = citations.stream()
            .filter(c -> c.getEffectiveDate() != null)
            .filter(c -> ChronoUnit.YEARS.between(c.getEffectiveDate().toInstant(), Instant.now()) > 5)
            .count();
        
        if (outdatedCitations > 0) {
            limitations.add(outdatedCitations + " citations are more than 5 years old");
        }
        
        return limitations;
    }
    
    private List<String> generateValidationSteps(EventRecommendationContext context, ConfidenceIndicators confidence) {
        List<String> steps = new ArrayList<>();
        
        if (confidence.getOverallConfidence() < 0.8) {
            steps.add("Seek expert review due to low confidence score (" + 
                String.format("%.1f%%", confidence.getOverallConfidence() * 100) + ")");
        }
        
        if (confidence.getRegulatoryConfidence() < 0.7) {
            steps.add("Consult regulatory affairs team for additional guidance");
        }
        
        if (confidence.getHistoricalConfidence() < 0.6) {
            steps.add("Review additional historical cases for similar events");
        }
        
        if (context.getEvent().getSeverityLevel() == SeverityLevel.CRITICAL) {
            steps.add("Mandatory review by quality management team for critical events");
        }
        
        if (context.getEvent().getGxpClassification() == GxPClassification.GXP) {
            steps.add("Regulatory compliance review required for GxP events");
        }
        
        return steps;
    }
    
    private String generateRationaleId() {
        return "RATIONALE-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 8);
    }
}
```

### 2.9 Validation Rules

```java
@Component
public class ContextRationaleValidationRules {
    
    private static final double MIN_CONFIDENCE_THRESHOLD = 0.5;
    private static final int MAX_RATIONALE_LENGTH = 50000;
    private static final int MIN_CITATIONS_FOR_HIGH_CONFIDENCE = 3;
    
    public void validateRationaleContent(String content, RationaleType type) {
        if (content == null || content.trim().isEmpty()) {
            throw new InvalidRationaleRequestException("Rationale content cannot be empty");
        }
        
        if (content.length() > MAX_RATIONALE_LENGTH) {
            throw new InvalidRationaleRequestException("Rationale content exceeds maximum length: " + MAX_RATIONALE_LENGTH);
        }
        
        validateRationaleStructure(content, type);
        validateRequiredSections(content, type);
    }
    
    private void validateRationaleStructure(String content, RationaleType type) {
        switch (type) {
            case EXECUTIVE_SUMMARY:
                validateExecutiveSummaryStructure(content);
                break;
            case DETAILED_ANALYSIS:
                validateDetailedAnalysisStructure(content);
                break;
            case TECHNICAL_RATIONALE:
                validateTechnicalRationaleStructure(content);
                break;
            case COMPLIANCE_FOCUSED:
                validateComplianceFocusedStructure(content);
                break;
        }
    }
    
    private void validateExecutiveSummaryStructure(String content) {
        List<String> requiredSections = Arrays.asList("Recommendation", "Key Factors", "Confidence");
        
        for (String section : requiredSections) {
            if (!content.toLowerCase().contains(section.toLowerCase())) {
                throw new InvalidRationaleRequestException("Executive summary missing required section: " + section);
            }
        }
    }
    
    private void validateDetailedAnalysisStructure(String content) {
        List<String> requiredSections = Arrays.asList(
            "Recommendation", "Regulatory Context", "Historical Precedents", 
            "Contextual Factors", "Risk Assessment", "Confidence Analysis"
        );
        
        for (String section : requiredSections) {
            if (!content.toLowerCase().contains(section.toLowerCase())) {
                throw new InvalidRationaleRequestException("Detailed analysis missing required section: " + section);
            }
        }
    }
    
    private void validateTechnicalRationaleStructure(String content) {
        List<String> requiredElements = Arrays.asList(
            "algorithm", "model", "data", "confidence", "validation"
        );
        
        boolean hasTechnicalContent = requiredElements.stream()
            .anyMatch(element -> content.toLowerCase().contains(element));
        
        if (!hasTechnicalContent) {
            throw new InvalidRationaleRequestException("Technical rationale missing technical details");
        }
    }
    
    private void validateComplianceFocusedStructure(String content) {
        List<String> requiredElements = Arrays.asList("regulation", "compliance", "requirement");
        
        boolean hasComplianceContent = requiredElements.stream()
            .anyMatch(element -> content.toLowerCase().contains(element));
        
        if (!hasComplianceContent) {
            throw new InvalidRationaleRequestException("Compliance-focused rationale missing regulatory content");
        }
    }
    
    public void validateCitations(List<RegulatoryCitation> citations) {
        for (RegulatoryCitation citation : citations) {
            validateSingleCitation(citation);
        }
        
        // Check for duplicate citations
        Set<String> citationNumbers = new HashSet<>();
        for (RegulatoryCitation citation : citations) {
            if (!citationNumbers.add(citation.getRegulationNumber())) {
                throw new CitationValidationException("Duplicate citation found: " + citation.getRegulationNumber());
            }
        }
    }
    
    private void validateSingleCitation(RegulatoryCitation citation) {
        if (citation.getRegulationTitle() == null || citation.getRegulationTitle().trim().isEmpty()) {
            throw new CitationValidationException("Citation title is required");
        }
        
        if (citation.getRegulationNumber() == null || citation.getRegulationNumber().trim().isEmpty()) {
            throw new CitationValidationException("Citation regulation number is required");
        }
        
        if (citation.getIssuingAuthority() == null || citation.getIssuingAuthority().trim().isEmpty()) {
            throw new CitationValidationException("Citation issuing authority is required");
        }
        
        if (citation.getRelevanceScore() == null || citation.getRelevanceScore() < 0.0 || citation.getRelevanceScore() > 1.0) {
            throw new CitationValidationException("Invalid relevance score: " + citation.getRelevanceScore());
        }
        
        // Validate URL format if provided
        if (citation.getSourceUrl() != null && !isValidUrl(citation.getSourceUrl())) {
            throw new CitationValidationException("Invalid source URL: " + citation.getSourceUrl());
        }
    }
    
    public void validateConfidenceScores(ConfidenceIndicators confidence) {
        if (confidence.getOverallConfidence() < 0.0 || confidence.getOverallConfidence() > 1.0) {
            throw new InvalidRationaleRequestException("Invalid overall confidence score: " + confidence.getOverallConfidence());
        }
        
        if (confidence.getRegulatoryConfidence() < 0.0 || confidence.getRegulatoryConfidence() > 1.0) {
            throw new InvalidRationaleRequestException("Invalid regulatory confidence score: " + confidence.getRegulatoryConfidence());
        }
        
        if (confidence.getHistoricalConfidence() < 0.0 || confidence.getHistoricalConfidence() > 1.0) {
            throw new InvalidRationaleRequestException("Invalid historical confidence score: " + confidence.getHistoricalConfidence());
        }
        
        if (confidence.getContextualConfidence() < 0.0 || confidence.getContextualConfidence() > 1.0) {
            throw new InvalidRationaleRequestException("Invalid contextual confidence score: " + confidence.getContextualConfidence());
        }
    }
    
    public void validateRationaleConsistency(
            ContextBackedRationale rationale, 
            List<RegulatoryCitation> citations, 
            List<HistoricalPrecedent> precedents) {
        
        // High confidence rationale should have sufficient supporting evidence
        if (rationale.getOverallConfidenceScore() > 0.8) {
            if (citations.size() < MIN_CITATIONS_FOR_HIGH_CONFIDENCE) {
                throw new InvalidRationaleRequestException(
                    "High confidence rationale requires at least " + MIN_CITATIONS_FOR_HIGH_CONFIDENCE + " citations"
                );
            }
        }
        
        // Rationale should mention key citations
        String rationaleContent = getRationaleContent(rationale);
        for (RegulatoryCitation citation : citations) {
            if (citation.getRelevanceScore() > 0.8 && 
                !rationaleContent.contains(citation.getRegulationNumber())) {
                throw new InvalidRationaleRequestException(
                    "High-relevance citation not mentioned in rationale: " + citation.getRegulationNumber()
                );
            }
        }
        
        // Check consistency between confidence score and content
        if (rationale.getOverallConfidenceScore() < MIN_CONFIDENCE_THRESHOLD && 
            !rationaleContent.toLowerCase().contains("limitation")) {
            throw new InvalidRationaleRequestException(
                "Low confidence rationale should mention limitations or uncertainties"
            );
        }
    }
    
    private String getRationaleContent(ContextBackedRationale rationale) {
        StringBuilder content = new StringBuilder();
        if (rationale.getExecutiveSummary() != null) content.append(rationale.getExecutiveSummary());
        if (rationale.getDetailedAnalysis() != null) content.append(rationale.getDetailedAnalysis());
        if (rationale.getTechnicalRationale() != null) content.append(rationale.getTechnicalRationale());
        return content.toString();
    }
    
    private boolean isValidUrl(String url) {
        try {
            new URL(url);
            return true;
        } catch (MalformedURLException e) {
            return false;
        }
    }
}
```

### 2.10 Service Integrations

```java
@Service
public class RegulatoryContextProviderImpl implements RegulatoryContextProvider {
    
    @Value("${regulatory.knowledge.service.url}")
    private String regulatoryServiceUrl;
    
    @Value("${regulatory.api.key}")
    private String regulatoryApiKey;
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    @Override
    public List<RegulatoryCitation> retrieveRegulatoryCitations(EventRecommendationContext context) {
        String cacheKey = "regulatory_citations:" + generateContextHash(context);
        
        // Try cache first
        List<RegulatoryCitation> cachedCitations = (List<RegulatoryCitation>) redisTemplate.opsForValue().get(cacheKey);
        if (cachedCitations != null) {
            return cachedCitations;
        }
        
        try {
            // Build search request
            RegulatorySearchRequest searchRequest = new RegulatorySearchRequest();
            searchRequest.setEventType(context.getEventType());
            searchRequest.setProductLine(context.getProductLine());
            searchRequest.setGxpClassification(context.getGxpClassification());
            searchRequest.setSeverityLevel(context.getSeverityLevel());
            searchRequest.setMaxResults(20);
            
            // Call regulatory knowledge service
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("Authorization", "Bearer " + regulatoryApiKey);
            
            HttpEntity<RegulatorySearchRequest> entity = new HttpEntity<>(searchRequest, headers);
            
            ResponseEntity<RegulatorySearchResponse> response = restTemplate.postForEntity(
                regulatoryServiceUrl + "/search/citations", entity, RegulatorySearchResponse.class
            );
            
            RegulatorySearchResponse searchResponse = response.getBody();
            if (searchResponse == null || searchResponse.getCitations() == null) {
                return Collections.emptyList();
            }
            
            // Convert to internal format
            List<RegulatoryCitation> citations = searchResponse.getCitations().stream()
                .map(this::convertToRegulatoryCitation)
                .collect(Collectors.toList());
            
            // Rank by relevance
            citations = rankCitationsByRelevance(citations, context);
            
            // Cache for 2 hours
            redisTemplate.opsForValue().set(cacheKey, citations, Duration.ofHours(2));
            
            return citations;
            
        } catch (Exception e) {
            throw new ContextRetrievalException("Failed to retrieve regulatory citations: " + e.getMessage());
        }
    }
    
    @Override
    public List<RegulatoryCitation> rankCitationsByRelevance(List<RegulatoryCitation> citations, EventRecommendationContext context) {
        // Calculate relevance scores based on context
        for (RegulatoryCitation citation : citations) {
            double relevanceScore = calculateRelevanceScore(citation, context);
            citation.setRelevanceScore(relevanceScore);
        }
        
        // Sort by relevance score descending
        return citations.stream()
            .sorted((c1, c2) -> Double.compare(c2.getRelevanceScore(), c1.getRelevanceScore()))
            .collect(Collectors.toList());
    }
    
    @Override
    public List<ConflictResolution> resolveConflictingGuidance(List<RegulatoryCitation> citations) {
        List<ConflictResolution> resolutions = new ArrayList<>();
        
        // Group citations by topic/area
        Map<String, List<RegulatoryCitation>> citationsByTopic = groupCitationsByTopic(citations);
        
        for (Map.Entry<String, List<RegulatoryCitation>> entry : citationsByTopic.entrySet()) {
            List<RegulatoryCitation> topicCitations = entry.getValue();
            
            if (topicCitations.size() > 1) {
                // Check for conflicts
                ConflictAnalysis analysis = analyzeConflicts(topicCitations);
                
                if (analysis.hasConflicts()) {
                    ConflictResolution resolution = new ConflictResolution();
                    resolution.setTopic(entry.getKey());
                    resolution.setConflictingCitations(topicCitations);
                    resolution.setConflictDescription(analysis.getConflictDescription());
                    resolution.setResolutionStrategy(determineResolutionStrategy(topicCitations));
                    resolution.setRecommendedCitation(selectPrimaryCitation(topicCitations));
                    
                    resolutions.add(resolution);
                }
            }
        }
        
        return resolutions;
    }
    
    private double calculateRelevanceScore(RegulatoryCitation citation, EventRecommendationContext context) {
        double score = 0.0;
        
        // Base score from citation type
        switch (citation.getCitationType()) {
            case PRIMARY_REGULATION: score += 0.4; break;
            case SUPPORTING_GUIDELINE: score += 0.3; break;
            case INDUSTRY_STANDARD: score += 0.2; break;
            case PRECEDENT_CASE: score += 0.1; break;
        }
        
        // Adjust for event type match
        if (citationAppliesToEventType(citation, context.getEventType())) {
            score += 0.3;
        }
        
        // Adjust for GxP classification
        if (context.getGxpClassification() == GxPClassification.GXP && 
            citation.getRegulationTitle().toLowerCase().contains("gmp")) {
            score += 0.2;
        }
        
        // Adjust for recency
        if (citation.getEffectiveDate() != null) {
            long yearsSinceEffective = ChronoUnit.YEARS.between(
                citation.getEffectiveDate().toInstant(), Instant.now()
            );
            
            if (yearsSinceEffective <= 2) {
                score += 0.1;
            } else if (yearsSinceEffective > 5) {
                score -= 0.1;
            }
        }
        
        return Math.min(1.0, Math.max(0.0, score));
    }
    
    private boolean citationAppliesToEventType(RegulatoryCitation citation, String eventType) {
        String title = citation.getRegulationTitle().toLowerCase();
        String clause = citation.getSpecificClause() != null ? citation.getSpecificClause().toLowerCase() : "";
        
        switch (eventType) {
            case "DEVIATION":
                return title.contains("deviation") || title.contains("non-conformance") || 
                       clause.contains("deviation") || clause.contains("non-conformance");
            case "CAPA":
                return title.contains("corrective") || title.contains("preventive") || 
                       clause.contains("capa") || clause.contains("corrective action");
            case "CHANGE_CONTROL":
                return title.contains("change") || title.contains("modification") || 
                       clause.contains("change control") || clause.contains("change management");
            default:
                return false;
        }
    }
    
    private String generateContextHash(EventRecommendationContext context) {
        String hashInput = context.getEventType() + ":" + 
                          context.getProductLine() + ":" + 
                          context.getGxpClassification() + ":" + 
                          context.getSeverityLevel();
        return DigestUtils.md5Hex(hashInput);
    }
    
    private RegulatoryCitation convertToRegulatoryCitation(ExternalCitation external) {
        RegulatoryCitation citation = new RegulatoryCitation();
        citation.setCitationId(generateCitationId());
        citation.setRegulationTitle(external.getTitle());
        citation.setRegulationNumber(external.getNumber());
        citation.setIssuingAuthority(external.getAuthority());
        citation.setSectionReference(external.getSection());
        citation.setSpecificClause(external.getClause());
        citation.setSourceUrl(external.getUrl());
        citation.setEffectiveDate(external.getEffectiveDate());
        citation.setIsPrimarySource(external.getIsPrimary());
        citation.setCitationType(mapCitationType(external.getType()));
        return citation;
    }
    
    private CitationType mapCitationType(String externalType) {
        switch (externalType.toUpperCase()) {
            case "REGULATION": return CitationType.PRIMARY_REGULATION;
            case "GUIDELINE": return CitationType.SUPPORTING_GUIDELINE;
            case "STANDARD": return CitationType.INDUSTRY_STANDARD;
            case "PRECEDENT": return CitationType.PRECEDENT_CASE;
            default: return CitationType.SUPPORTING_GUIDELINE;
        }
    }
    
    private String generateCitationId() {
        return "CIT-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 6);
    }
}
```

---

## 3. Frontend React Details

### 3.1 UI Architecture

```jsx
// Context-Backed Rationale Dashboard Component
import React, { useState, useEffect } from 'react';
import { RationaleViewer } from './RationaleViewer';
import { CitationBrowser } from './CitationBrowser';
import { HistoricalPrecedents } from './HistoricalPrecedents';
import { ContextualFactors } from './ContextualFactors';
import { ConfidenceIndicators } from './ConfidenceIndicators';
import { RationaleExport } from './RationaleExport';
import { CollaborativeAnnotations } from './CollaborativeAnnotations';

const ContextRationaleDashboard = ({ recommendationId, eventId }) => {
    const [rationale, setRationale] = useState(null);
    const [rationaleType, setRationaleType] = useState('DETAILED_ANALYSIS');
    const [activeTab, setActiveTab] = useState('rationale');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [userRole, setUserRole] = useState(null);

    useEffect(() => {
        if (recommendationId && eventId) {
            loadRationale();
        }
        loadUserRole();
    }, [recommendationId, eventId, rationaleType]);

    const loadUserRole = () => {
        const role = localStorage.getItem('userRole') || 'QUALITY_ANALYST';
        setUserRole(role);
    };

    const loadRationale = async () => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await fetch('/api/v1/context-rationale/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                },
                body: JSON.stringify({
                    recommendationId,
                    eventId,
                    rationaleType,
                    userId: getCurrentUserId(),
                    userRole: userRole,
                    includeRegulatoryCitations: true,
                    includeHistoricalPrecedents: true,
                    includeContextualFactors: true
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            setRationale(result);
            
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="context-rationale-dashboard">
            <header className="dashboard-header">
                <h1>Context-Backed Decision Rationale</h1>
                <div className="rationale-controls">
                    <select 
                        value={rationaleType} 
                        onChange={(e) => setRationaleType(e.target.value)}
                        className="rationale-type-selector"
                    >
                        <option value="EXECUTIVE_SUMMARY">Executive Summary</option>
                        <option value="DETAILED_ANALYSIS">Detailed Analysis</option>
                        <option value="TECHNICAL_RATIONALE">Technical Rationale</option>
                        <option value="COMPLIANCE_FOCUSED">Compliance Focused</option>
                    </select>
                    
                    {rationale && (
                        <div className="confidence-display">
                            <span className="confidence-label">Overall Confidence:</span>
                            <span className={`confidence-score ${getConfidenceClass(rationale.overallConfidenceScore)}`}>
                                {(rationale.overallConfidenceScore * 100).toFixed(1)}%
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
                    Generating context-backed rationale...
                </div>
            )}

            {rationale && (
                <>
                    <nav className="rationale-nav">
                        <button 
                            className={activeTab === 'rationale' ? 'active' : ''}
                            onClick={() => setActiveTab('rationale')}
                        >
                            Rationale
                        </button>
                        <button 
                            className={activeTab === 'citations' ? 'active' : ''}
                            onClick={() => setActiveTab('citations')}
                        >
                            Citations ({rationale.regulatoryCitations?.length || 0})
                        </button>
                        <button 
                            className={activeTab === 'precedents' ? 'active' : ''}
                            onClick={() => setActiveTab('precedents')}
                        >
                            Precedents ({rationale.historicalPrecedents?.length || 0})
                        </button>
                        <button 
                            className={activeTab === 'factors' ? 'active' : ''}
                            onClick={() => setActiveTab('factors')}
                        >
                            Context Factors ({rationale.contextualFactors?.length || 0})
                        </button>
                        <button 
                            className={activeTab === 'confidence' ? 'active' : ''}
                            onClick={() => setActiveTab('confidence')}
                        >
                            Confidence Analysis
                        </button>
                        <button 
                            className={activeTab === 'annotations' ? 'active' : ''}
                            onClick={() => setActiveTab('annotations')}
                        >
                            Annotations
                        </button>
                        <button 
                            className={activeTab === 'export' ? 'active' : ''}
                            onClick={() => setActiveTab('export')}
                        >
                            Export
                        </button>
                    </nav>

                    <div className="rationale-content">
                        {activeTab === 'rationale' && (
                            <RationaleViewer 
                                rationale={rationale}
                                rationaleType={rationaleType}
                                userRole={userRole}
                            />
                        )}

                        {activeTab === 'citations' && (
                            <CitationBrowser 
                                citations={rationale.regulatoryCitations}
                                onCitationClick={(citation) => {/* Handle citation click */}}
                            />
                        )}

                        {activeTab === 'precedents' && (
                            <HistoricalPrecedents 
                                precedents={rationale.historicalPrecedents}
                                onPrecedentAnalyze={(precedent) => {/* Handle precedent analysis */}}
                            />
                        )}

                        {activeTab === 'factors' && (
                            <ContextualFactors 
                                factors={rationale.contextualFactors}
                                onFactorDrillDown={(factor) => {/* Handle factor drill-down */}}
                            />
                        )}

                        {activeTab === 'confidence' && (
                            <ConfidenceIndicators 
                                confidenceData={rationale.confidenceIndicators}
                                overallScore={rationale.overallConfidenceScore}
                                dataLimitations={rationale.dataLimitations}
                                validationSteps={rationale.validationSteps}
                            />
                        )}

                        {activeTab === 'annotations' && (
                            <CollaborativeAnnotations 
                                rationaleId={rationale.rationaleId}
                                userRole={userRole}
                                onAnnotationAdded={() => {/* Handle annotation added */}}
                            />
                        )}

                        {activeTab === 'export' && (
                            <RationaleExport 
                                rationaleId={rationale.rationaleId}
                                userRole={userRole}
                                onExportComplete={() => {/* Handle export complete */}}
                            />
                        )}
                    </div>
                </>
            )}
        </div>
    );
};

const getConfidenceClass = (score) => {
    if (score >= 0.8) return 'high-confidence';
    if (score >= 0.6) return 'medium-confidence';
    return 'low-confidence';
};

const getCurrentUserId = () => {
    return localStorage.getItem('userId') || 'anonymous';
};
```

### 3.2 UI Specifications

```jsx
// Rationale Viewer Component
import React, { useState } from 'react';
import { marked } from 'marked';

const RationaleViewer = ({ rationale, rationaleType, userRole }) => {
    const [expandedSections, setExpandedSections] = useState(new Set(['main-content']));

    const toggleSection = (sectionId) => {
        const newExpanded = new Set(expandedSections);
        if (newExpanded.has(sectionId)) {
            newExpanded.delete(sectionId);
        } else {
            newExpanded.add(sectionId);
        }
        setExpandedSections(newExpanded);
    };

    const getRationaleContent = () => {
        switch (rationaleType) {
            case 'EXECUTIVE_SUMMARY':
                return rationale.rationale; // Assuming this contains the executive summary
            case 'DETAILED_ANALYSIS':
                return rationale.rationale; // Detailed analysis content
            case 'TECHNICAL_RATIONALE':
                return rationale.rationale; // Technical rationale content
            case 'COMPLIANCE_FOCUSED':
                return rationale.rationale; // Compliance-focused content
            default:
                return rationale.rationale;
        }
    };

    return (
        <div className="rationale-viewer">
            <div className="rationale-header">
                <h2>Decision Rationale - {rationaleType.replace('_', ' ')}</h2>
                <div className="rationale-meta">
                    <div className="meta-item">
                        <label>Generated:</label>
                        <span>{new Date(rationale.generatedTimestamp).toLocaleString()}</span>
                    </div>
                    <div className="meta-item">
                        <label>Access Level:</label>
                        <span className={`access-level ${rationale.accessLevel.toLowerCase()}`}>
                            {rationale.accessLevel}
                        </span>
                    </div>
                    <div className="meta-item">
                        <label>Review Status:</label>
                        <span className={`review-status ${rationale.reviewStatus?.toLowerCase()}`}>
                            {rationale.reviewStatus || 'Pending'}
                        </span>
                    </div>
                </div>
            </div>

            <div className="rationale-sections">
                <div className="section">
                    <h3 
                        className="section-header clickable"
                        onClick={() => toggleSection('main-content')}
                    >
                        Rationale Content
                        <span className={`expand-icon ${expandedSections.has('main-content') ? 'expanded' : ''}`}>
                            ▼
                        </span>
                    </h3>
                    {expandedSections.has('main-content') && (
                        <div className="section-content">
                            <div 
                                className="rationale-content"
                                dangerouslySetInnerHTML={{ __html: marked(getRationaleContent()) }}
                            />
                        </div>
                    )}
                </div>

                {rationale.dataLimitations && rationale.dataLimitations.length > 0 && (
                    <div className="section">
                        <h3 
                            className="section-header clickable"
                            onClick={() => toggleSection('limitations')}
                        >
                            Data Limitations
                            <span className={`expand-icon ${expandedSections.has('limitations') ? 'expanded' : ''}`}>
                                ▼
                            </span>
                        </h3>
                        {expandedSections.has('limitations') && (
                            <div className="section-content">
                                <div className="limitations-list">
                                    {rationale.dataLimitations.map((limitation, index) => (
                                        <div key={index} className="limitation-item">
                                            <span className="limitation-icon">⚠️</span>
                                            <span className="limitation-text">{limitation}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {rationale.validationSteps && rationale.validationSteps.length > 0 && (
                    <div className="section">
                        <h3 
                            className="section-header clickable"
                            onClick={() => toggleSection('validation')}
                        >
                            Recommended Validation Steps
                            <span className={`expand-icon ${expandedSections.has('validation') ? 'expanded' : ''}`}>
                                ▼
                            </span>
                        </h3>
                        {expandedSections.has('validation') && (
                            <div className="section-content">
                                <div className="validation-steps">
                                    {rationale.validationSteps.map((step, index) => (
                                        <div key={index} className="validation-step">
                                            <span className="step-number">{index + 1}</span>
                                            <span className="step-text">{step}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

// Citation Browser Component
const CitationBrowser = ({ citations, onCitationClick }) => {
    const [sortBy, setSortBy] = useState('relevance');
    const [filterBy, setFilterBy] = useState('all');

    const sortedCitations = [...citations].sort((a, b) => {
        switch (sortBy) {
            case 'relevance':
                return b.relevanceScore - a.relevanceScore;
            case 'date':
                return new Date(b.effectiveDate) - new Date(a.effectiveDate);
            case 'authority':
                return a.issuingAuthority.localeCompare(b.issuingAuthority);
            default:
                return 0;
        }
    });

    const filteredCitations = sortedCitations.filter(citation => {
        if (filterBy === 'all') return true;
        if (filterBy === 'primary') return citation.isPrimarySource;
        if (filterBy === 'high-relevance') return citation.relevanceScore >= 0.8;
        return true;
    });

    return (
        <div className="citation-browser">
            <div className="citation-controls">
                <div className="control-group">
                    <label>Sort by:</label>
                    <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
                        <option value="relevance">Relevance Score</option>
                        <option value="date">Effective Date</option>
                        <option value="authority">Issuing Authority</option>
                    </select>
                </div>
                
                <div className="control-group">
                    <label>Filter:</label>
                    <select value={filterBy} onChange={(e) => setFilterBy(e.target.value)}>
                        <option value="all">All Citations</option>
                        <option value="primary">Primary Sources Only</option>
                        <option value="high-relevance">High Relevance (≥80%)</option>
                    </select>
                </div>
            </div>

            <div className="citations-list">
                {filteredCitations.map((citation, index) => (
                    <div 
                        key={citation.citationId} 
                        className="citation-card"
                        onClick={() => onCitationClick(citation)}
                    >
                        <div className="citation-header">
                            <h4>{citation.regulationTitle}</h4>
                            <div className="citation-badges">
                                <span className="regulation-number">{citation.regulationNumber}</span>
                                <span className={`relevance-score ${getRelevanceClass(citation.relevanceScore)}`}>
                                    {(citation.relevanceScore * 100).toFixed(0)}% relevant
                                </span>
                                {citation.isPrimarySource && (
                                    <span className="primary-source-badge">Primary Source</span>
                                )}
                            </div>
                        </div>

                        <div className="citation-details">
                            <div className="detail-row">
                                <span className="label">Authority:</span>
                                <span className="value">{citation.issuingAuthority}</span>
                            </div>
                            
                            {citation.sectionReference && (
                                <div className="detail-row">
                                    <span className="label">Section:</span>
                                    <span className="value">{citation.sectionReference}</span>
                                </div>
                            )}
                            
                            {citation.effectiveDate && (
                                <div className="detail-row">
                                    <span className="label">Effective Date:</span>
                                    <span className="value">
                                        {new Date(citation.effectiveDate).toLocaleDateString()}
                                    </span>
                                </div>
                            )}
                        </div>

                        {citation.specificClause && (
                            <div className="citation-clause">
                                <h5>Relevant Clause:</h5>
                                <p>{citation.specificClause}</p>
                            </div>
                        )}

                        {citation.sourceUrl && (
                            <div className="citation-actions">
                                <a 
                                    href={citation.sourceUrl} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="source-link"
                                    onClick={(e) => e.stopPropagation()}
                                >
                                    View Source Document →
                                </a>
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {filteredCitations.length === 0 && (
                <div className="no-citations">
                    <p>No citations match the current filter criteria.</p>
                </div>
            )}
        </div>
    );
};

const getRelevanceClass = (score) => {
    if (score >= 0.8) return 'high-relevance';
    if (score >= 0.6) return 'medium-relevance';
    return 'low-relevance';
};
```

### 3.3 API Integration

```jsx
// Context Rationale API Service
class ContextRationaleAPI {
    constructor() {
        this.baseURL = process.env.REACT_APP_API_BASE_URL || '/api/v1';
        this.timeout = 45000; // 45 seconds for context rationale generation
    }

    async generateRationale(rationaleRequest) {
        const response = await this.makeRequest('/context-rationale/generate', {
            method: 'POST',
            body: JSON.stringify(rationaleRequest)
        });
        return response;
    }

    async getRationale(rationaleId, userId = null, userRole = null) {
        const queryParams = new URLSearchParams();
        if (userId) queryParams.append('userId', userId);
        if (userRole) queryParams.append('userRole', userRole);
        
        const response = await this.makeRequest(`/context-rationale/rationale/${rationaleId}?${queryParams}`, {
            method: 'GET'
        });
        return response;
    }

    async getRationaleByRecommendation(recommendationId, rationaleType = 'DETAILED_ANALYSIS', userId = null, userRole = null) {
        const queryParams = new URLSearchParams({ rationaleType });
        if (userId) queryParams.append('userId', userId);
        if (userRole) queryParams.append('userRole', userRole);
        
        const response = await this.makeRequest(`/context-rationale/recommendation/${recommendationId}/rationale?${queryParams}`, {
            method: 'GET'
        });
        return response;
    }

    async validateCitations(citationIds) {
        const response = await this.makeRequest('/context-rationale/citations/validate', {
            method: 'POST',
            body: JSON.stringify({ citationIds })
        });
        return response;
    }

    async exportRationale(rationaleId, format = 'PDF', userId = null, userRole = null) {
        const response = await fetch(`${this.baseURL}/context-rationale/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.getAuthToken()}`
            },
            body: JSON.stringify({
                rationaleId,
                format,
                userId,
                userRole
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.blob();
    }

    async addAnnotation(annotationData) {
        const response = await this.makeRequest('/context-rationale/annotations', {
            method: 'POST',
            body: JSON.stringify(annotationData)
        });
        return response;
    }

    async getAnnotations(rationaleId, userId = null) {
        const queryParams = new URLSearchParams();
        if (userId) queryParams.append('userId', userId);
        
        const response = await this.makeRequest(`/context-rationale/annotations/${rationaleId}?${queryParams}`, {
            method: 'GET'
        });
        return response;
    }

    async submitReview(reviewData) {
        const response = await this.makeRequest('/context-rationale/review', {
            method: 'POST',
            body: JSON.stringify(reviewData)
        });
        return response;
    }

    async getConfidenceBreakdown(rationaleId) {
        const response = await this.makeRequest(`/context-rationale/confidence/breakdown/${rationaleId}`, {
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
                throw new Error('Request timeout - rationale generation taking longer than expected');
            }
            throw error;
        }
    }

    getAuthToken() {
        return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
    }
}

export default new ContextRationaleAPI();
```

---

## 4. Database Details

### 4.1 ER Diagram

```mermaid
erDiagram
    CONTEXT_BACKED_RATIONALES {
        BIGINT id PK
        VARCHAR rationale_id UK
        VARCHAR recommendation_id FK
        VARCHAR event_id FK
        ENUM rationale_type
        TEXT executive_summary
        TEXT detailed_analysis
        TEXT technical_rationale
        JSON regulatory_citations
        JSON historical_precedents
        JSON contextual_factors
        JSON confidence_indicators
        JSON data_limitations
        JSON validation_steps
        DECIMAL overall_confidence_score
        ENUM access_level
        TIMESTAMP generated_timestamp
        TIMESTAMP last_modified_timestamp
        VARCHAR generated_by
        VARCHAR reviewed_by
        ENUM review_status
    }
    
    REGULATORY_CITATIONS {
        BIGINT id PK
        VARCHAR citation_id UK
        VARCHAR rationale_id FK
        VARCHAR regulation_title
        VARCHAR regulation_number
        VARCHAR issuing_authority
        VARCHAR section_reference
        TEXT specific_clause
        DECIMAL relevance_score
        ENUM citation_type
        VARCHAR source_url
        DATE effective_date
        BOOLEAN is_primary_source
    }
    
    HISTORICAL_PRECEDENTS {
        BIGINT id PK
        VARCHAR precedent_id UK
        VARCHAR rationale_id FK
        VARCHAR case_reference
        TEXT case_description
        VARCHAR event_type
        VARCHAR outcome
        DECIMAL similarity_score
        DATE case_date
        VARCHAR lessons_learned
        VARCHAR resolution_approach
    }
    
    CONTEXTUAL_FACTORS {
        BIGINT id PK
        VARCHAR factor_id UK
        VARCHAR rationale_id FK
        VARCHAR factor_name
        VARCHAR factor_category
        TEXT factor_description
        DECIMAL influence_weight
        VARCHAR supporting_evidence
        BOOLEAN is_key_factor
    }
    
    RATIONALE_ANNOTATIONS {
        BIGINT id PK
        VARCHAR annotation_id UK
        VARCHAR rationale_id FK
        VARCHAR user_id
        VARCHAR annotation_type
        TEXT annotation_content
        VARCHAR section_reference
        TIMESTAMP created_at
        TIMESTAMP updated_at
        BOOLEAN is_resolved
    }
    
    RATIONALE_REVIEWS {
        BIGINT id PK
        VARCHAR review_id UK
        VARCHAR rationale_id FK
        VARCHAR reviewer_id
        ENUM review_status
        TEXT review_comments
        JSON review_criteria_scores
        TIMESTAMP review_date
        VARCHAR review_outcome
    }
    
    CITATION_VALIDATIONS {
        BIGINT id PK
        VARCHAR validation_id UK
        VARCHAR citation_id FK
        BOOLEAN is_link_valid
        BOOLEAN is_content_accurate
        DECIMAL validation_score
        TIMESTAMP last_validated
        VARCHAR validation_notes
    }
    
    CONTEXT_BACKED_RATIONALES ||--o{ REGULATORY_CITATIONS : "contains"
    CONTEXT_BACKED_RATIONALES ||--o{ HISTORICAL_PRECEDENTS : "references"
    CONTEXT_BACKED_RATIONALES ||--o{ CONTEXTUAL_FACTORS : "analyzes"
    CONTEXT_BACKED_RATIONALES ||--o{ RATIONALE_ANNOTATIONS : "receives"
    CONTEXT_BACKED_RATIONALES ||--o{ RATIONALE_REVIEWS : "undergoes"
    REGULATORY_CITATIONS ||--o{ CITATION_VALIDATIONS : "validated_by"
```

### 4.2 Database Validations

```sql
-- Context-Backed Rationales Table
CREATE TABLE context_backed_rationales (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    rationale_id VARCHAR(100) NOT NULL UNIQUE,
    recommendation_id VARCHAR(100) NOT NULL,
    event_id VARCHAR(100) NOT NULL,
    rationale_type ENUM('EXECUTIVE_SUMMARY', 'DETAILED_ANALYSIS', 'TECHNICAL_RATIONALE', 'COMPLIANCE_FOCUSED') NOT NULL,
    executive_summary TEXT,
    detailed_analysis TEXT,
    technical_rationale TEXT,
    regulatory_citations JSON,
    historical_precedents JSON,
    contextual_factors JSON,
    confidence_indicators JSON,
    data_limitations JSON,
    validation_steps JSON,
    overall_confidence_score DECIMAL(4,3) NOT NULL CHECK (overall_confidence_score >= 0.000 AND overall_confidence_score <= 1.000),
    access_level ENUM('PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED') NOT NULL DEFAULT 'INTERNAL',
    generated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    generated_by VARCHAR(100),
    reviewed_by VARCHAR(100),
    review_status ENUM('PENDING', 'IN_REVIEW', 'APPROVED', 'REJECTED', 'REQUIRES_REVISION') DEFAULT 'PENDING',
    INDEX idx_rationale_id (rationale_id),
    INDEX idx_recommendation_id (recommendation_id),
    INDEX idx_event_id (event_id),
    INDEX idx_rationale_type (rationale_type),
    INDEX idx_access_level (access_level),
    INDEX idx_overall_confidence_score (overall_confidence_score),
    INDEX idx_generated_timestamp (generated_timestamp),
    INDEX idx_review_status (review_status),
    CONSTRAINT chk_rationale_content CHECK (
        executive_summary IS NOT NULL OR 
        detailed_analysis IS NOT NULL OR 
        technical_rationale IS NOT NULL
    )
);

-- Regulatory Citations Table
CREATE TABLE regulatory_citations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    citation_id VARCHAR(100) NOT NULL UNIQUE,
    rationale_id VARCHAR(100) NOT NULL,
    regulation_title VARCHAR(500) NOT NULL,
    regulation_number VARCHAR(100) NOT NULL,
    issuing_authority VARCHAR(200) NOT NULL,
    section_reference VARCHAR(100),
    specific_clause TEXT,
    relevance_score DECIMAL(4,3) NOT NULL CHECK (relevance_score >= 0.000 AND relevance_score <= 1.000),
    citation_type ENUM('PRIMARY_REGULATION', 'SUPPORTING_GUIDELINE', 'INDUSTRY_STANDARD', 'PRECEDENT_CASE') NOT NULL,
    source_url VARCHAR(1000),
    effective_date DATE,
    is_primary_source BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (rationale_id) REFERENCES context_backed_rationales(rationale_id) ON DELETE CASCADE,
    INDEX idx_citation_id (citation_id),
    INDEX idx_rationale_id (rationale_id),
    INDEX idx_regulation_number (regulation_number),
    INDEX idx_issuing_authority (issuing_authority),
    INDEX idx_relevance_score (relevance_score),
    INDEX idx_citation_type (citation_type),
    INDEX idx_effective_date (effective_date),
    INDEX idx_is_primary_source (is_primary_source)
);

-- Historical Precedents Table
CREATE TABLE historical_precedents (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    precedent_id VARCHAR(100) NOT NULL UNIQUE,
    rationale_id VARCHAR(100) NOT NULL,
    case_reference VARCHAR(200) NOT NULL,
    case_description TEXT NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    outcome VARCHAR(200),
    similarity_score DECIMAL(4,3) NOT NULL CHECK (similarity_score >= 0.000 AND similarity_score <= 1.000),
    case_date DATE,
    lessons_learned TEXT,
    resolution_approach TEXT,
    FOREIGN KEY (rationale_id) REFERENCES context_backed_rationales(rationale_id) ON DELETE CASCADE,
    INDEX idx_precedent_id (precedent_id),
    INDEX idx_rationale_id (rationale_id),
    INDEX idx_event_type (event_type),
    INDEX idx_similarity_score (similarity_score),
    INDEX idx_case_date (case_date)
);

-- Contextual Factors Table
CREATE TABLE contextual_factors (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    factor_id VARCHAR(100) NOT NULL UNIQUE,
    rationale_id VARCHAR(100) NOT NULL,
    factor_name VARCHAR(200) NOT NULL,
    factor_category VARCHAR(100) NOT NULL,
    factor_description TEXT,
    influence_weight DECIMAL(4,3) NOT NULL CHECK (influence_weight >= 0.000 AND influence_weight <= 1.000),
    supporting_evidence TEXT,
    is_key_factor BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (rationale_id) REFERENCES context_backed_rationales(rationale_id) ON DELETE CASCADE,
    INDEX idx_factor_id (factor_id),
    INDEX idx_rationale_id (rationale_id),
    INDEX idx_factor_category (factor_category),
    INDEX idx_influence_weight (influence_weight),
    INDEX idx_is_key_factor (is_key_factor)
);

-- Rationale Annotations Table
CREATE TABLE rationale_annotations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    annotation_id VARCHAR(100) NOT NULL UNIQUE,
    rationale_id VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    annotation_type VARCHAR(50) NOT NULL,
    annotation_content TEXT NOT NULL,
    section_reference VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_resolved BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (rationale_id) REFERENCES context_backed_rationales(rationale_id) ON DELETE CASCADE,
    INDEX idx_annotation_id (annotation_id),
    INDEX idx_rationale_id (rationale_id),
    INDEX idx_user_id (user_id),
    INDEX idx_annotation_type (annotation_type),
    INDEX idx_created_at (created_at),
    INDEX idx_is_resolved (is_resolved)
);

-- Rationale Reviews Table
CREATE TABLE rationale_reviews (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    review_id VARCHAR(100) NOT NULL UNIQUE,
    rationale_id VARCHAR(100) NOT NULL,
    reviewer_id VARCHAR(100) NOT NULL,
    review_status ENUM('PENDING', 'IN_PROGRESS', 'COMPLETED', 'ESCALATED') NOT NULL DEFAULT 'PENDING',
    review_comments TEXT,
    review_criteria_scores JSON,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    review_outcome VARCHAR(100),
    FOREIGN KEY (rationale_id) REFERENCES context_backed_rationales(rationale_id) ON DELETE CASCADE,
    INDEX idx_review_id (review_id),
    INDEX idx_rationale_id (rationale_id),
    INDEX idx_reviewer_id (reviewer_id),
    INDEX idx_review_status (review_status),
    INDEX idx_review_date (review_date)
);

-- Citation Validations Table
CREATE TABLE citation_validations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    validation_id VARCHAR(100) NOT NULL UNIQUE,
    citation_id VARCHAR(100) NOT NULL,
    is_link_valid BOOLEAN NOT NULL DEFAULT TRUE,
    is_content_accurate BOOLEAN NOT NULL DEFAULT TRUE,
    validation_score DECIMAL(4,3) NOT NULL CHECK (validation_score >= 0.000 AND validation_score <= 1.000),
    last_validated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validation_notes TEXT,
    FOREIGN KEY (citation_id) REFERENCES regulatory_citations(citation_id) ON DELETE CASCADE,
    INDEX idx_validation_id (validation_id),
    INDEX idx_citation_id (citation_id),
    INDEX idx_is_link_valid (is_link_valid),
    INDEX idx_validation_score (validation_score),
    INDEX idx_last_validated (last_validated)
);
```

---

## 5. Non Functional Requirements

### 5.1 Performance

```yaml
Performance Requirements:
  Rationale Generation:
    - Executive Summary: < 2 seconds (95th percentile)
    - Detailed Analysis: < 4 seconds (95th percentile)
    - Technical Rationale: < 6 seconds (95th percentile)
    - Compliance Focused: < 3 seconds (95th percentile)
    
  Context Retrieval:
    - Regulatory Citations: < 1 second for 20 citations
    - Historical Precedents: < 2 seconds for 10 precedents
    - Contextual Factors: < 500ms for factor analysis
    
  Citation Validation:
    - Link Validation: < 200ms per citation
    - Content Accuracy Check: < 1 second per citation
    - Batch Validation: < 30 seconds for 50 citations
    
  Export Operations:
    - PDF Export: < 10 seconds for detailed rationale
    - DOCX Export: < 8 seconds for detailed rationale
    - HTML Export: < 3 seconds for any format
    
  Resource Utilization:
    - CPU: < 75% during rationale generation
    - Memory: < 80% heap utilization
    - Database: < 85% connection pool usage
    - Cache Hit Ratio: > 90% for regulatory citations
```

### 5.2 Security

```yaml
Security Requirements:
  Access Control:
    - Role-based rationale access (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED)
    - Citation-level access controls
    - Annotation permission management
    
  Data Protection:
    - Rationale content encryption at rest
    - Sensitive information redaction based on user role
    - Secure transmission of regulatory citations
    
  Audit Requirements:
    - Complete rationale generation audit trail
    - Citation access logging
    - Annotation and review activity tracking
    
  Compliance:
    - Regulatory compliance for citation handling
    - Data retention policies for audit requirements
    - Privacy controls for collaborative features
```

### 5.3 Logging

```java
@Component
public class ContextRationaleLogger {
    
    private static final Logger logger = LoggerFactory.getLogger(ContextRationaleLogger.class);
    private static final Logger auditLogger = LoggerFactory.getLogger("CONTEXT_RATIONALE_AUDIT");
    private static final Logger performanceLogger = LoggerFactory.getLogger("CONTEXT_RATIONALE_PERFORMANCE");
    private static final Logger accessLogger = LoggerFactory.getLogger("RATIONALE_ACCESS");
    
    public void logRationaleGeneration(String rationaleId, String recommendationId, String eventId, 
                                     RationaleType type, long processingTime, double confidenceScore) {
        auditLogger.info("Rationale generated - RationaleId: {}, RecommendationId: {}, EventId: {}, " +
            "Type: {}, ProcessingTime: {}ms, Confidence: {}", 
            rationaleId, recommendationId, eventId, type, processingTime, confidenceScore);
        
        if (processingTime > getPerformanceThreshold(type)) {
            performanceLogger.warn("Slow rationale generation - RationaleId: {}, Type: {}, ProcessingTime: {}ms", 
                rationaleId, type, processingTime);
        }
    }
    
    public void logRationaleAccess(String rationaleId, String userId, String userRole, AccessLevel accessLevel) {
        accessLogger.info("Rationale accessed - RationaleId: {}, UserId: {}, UserRole: {}, AccessLevel: {}", 
            rationaleId, userId, userRole, accessLevel);
    }
    
    public void logCitationValidation(String citationId, boolean isValid, double validationScore) {
        auditLogger.info("Citation validated - CitationId: {}, IsValid: {}, ValidationScore: {}", 
            citationId, isValid, validationScore);
        
        if (!isValid) {
            logger.warn("Invalid citation detected - CitationId: {}, ValidationScore: {}", 
                citationId, validationScore);
        }
    }
    
    public void logAnnotationActivity(String annotationId, String rationaleId, String userId, String action) {
        auditLogger.info("Annotation activity - AnnotationId: {}, RationaleId: {}, UserId: {}, Action: {}", 
            annotationId, rationaleId, userId, action);
    }
    
    public void logReviewActivity(String reviewId, String rationaleId, String reviewerId, String status) {
        auditLogger.info("Review activity - ReviewId: {}, RationaleId: {}, ReviewerId: {}, Status: {}", 
            reviewId, rationaleId, reviewerId, status);
    }
    
    public void logExportActivity(String rationaleId, String format, String userId, boolean success) {
        auditLogger.info("Rationale export - RationaleId: {}, Format: {}, UserId: {}, Success: {}", 
            rationaleId, format, userId, success);
        
        if (!success) {
            logger.error("Rationale export failed - RationaleId: {}, Format: {}, UserId: {}", 
                rationaleId, format, userId);
        }
    }
    
    public void logAccessDenied(String userId, String userRole, String rationaleId, AccessLevel requiredLevel) {
        accessLogger.warn("Rationale access denied - UserId: {}, UserRole: {}, RationaleId: {}, RequiredLevel: {}", 
            userId, userRole, rationaleId, requiredLevel);
    }
    
    private long getPerformanceThreshold(RationaleType type) {
        switch (type) {
            case EXECUTIVE_SUMMARY: return 2000;
            case DETAILED_ANALYSIS: return 4000;
            case TECHNICAL_RATIONALE: return 6000;
            case COMPLIANCE_FOCUSED: return 3000;
            default: return 4000;
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
  Jsoup: 1.16.1

Frontend Dependencies:
  React: 18.2.0
  React Router: 6.11.0
  Marked: 5.1.0
  Material-UI: 5.13.0
  React Query: 4.29.0
  React PDF Viewer: 3.12.0
  React Highlight Words: 0.20.0
  File-saver: 2.0.5
  React Virtualized: 9.22.0

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
  Regulatory Knowledge Service: v2.1
  Historical Data Service: v1.8
  Document Generation Service: v2.0
  Citation Validation Service: v1.5
  Natural Language Processing API: v1.3
```

---

## 7. Assumptions

```yaml
Technical Assumptions:
  - Regulatory knowledge service provides current and accurate citations
  - Historical data service maintains comprehensive precedent database
  - Citation validation service can verify link accuracy and content
  - Document generation service supports multiple export formats
  - Natural language processing can extract contextual factors effectively

Business Assumptions:
  - Users require different levels of rationale detail based on their roles
  - Regulatory citations are essential for compliance and audit purposes
  - Historical precedents provide valuable context for decision validation
  - Collaborative annotations improve rationale quality over time
  - Expert reviews enhance rationale accuracy and completeness

Operational Assumptions:
  - 24/7 availability for rationale generation and access
  - Automated backup of rationale data and citations
  - Performance monitoring and alerting for slow operations
  - Regular validation of citation links and content accuracy
  - Integration with existing quality management and audit systems

Data Assumptions:
  - Regulatory citation data is current and accessible
  - Historical precedent data is complete and accurate
  - Contextual factor extraction provides meaningful insights
  - Confidence calculations reflect actual decision reliability
  - Access control requirements are clearly defined and enforced

Regulatory Assumptions:
  - Citation accuracy requirements are clearly defined
  - Audit trail requirements meet regulatory standards
  - Data retention policies comply with regulatory requirements
  - Access controls satisfy data protection and privacy regulations
  - Export formats meet regulatory submission requirements
```