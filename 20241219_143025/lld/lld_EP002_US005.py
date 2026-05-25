# Low Level Design Document

## Epic ID: EP002
## User Story ID: US005
## Title: Regulatory Knowledge Retrieval System

---

## 1. Objective

Design and implement a comprehensive regulatory knowledge retrieval system that automatically fetches, indexes, and provides relevant regulations, GMP rules, and SOPs based on quality event context with semantic search capabilities and real-time updates.

---

## 2. Backend Spring Boot API Details

### 2.1 API Model

```java
// Regulatory Document Model
@Entity
@Table(name = "regulatory_documents")
public class RegulatoryDocument {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull
    @Column(name = "document_id")
    private String documentId;
    
    @NotNull
    @Column(name = "document_type")
    @Enumerated(EnumType.STRING)
    private DocumentType documentType;
    
    @NotNull
    @Column(name = "title")
    private String title;
    
    @Column(name = "regulation_number")
    private String regulationNumber;
    
    @NotNull
    @Column(name = "issuing_authority")
    private String issuingAuthority;
    
    @NotNull
    @Column(name = "jurisdiction")
    private String jurisdiction;
    
    @Column(name = "content", columnDefinition = "LONGTEXT")
    private String content;
    
    @Column(name = "summary", columnDefinition = "TEXT")
    private String summary;
    
    @Column(name = "keywords", columnDefinition = "JSON")
    private String keywords;
    
    @Column(name = "sections", columnDefinition = "JSON")
    private String sections;
    
    @NotNull
    @Temporal(TemporalType.DATE)
    @Column(name = "effective_date")
    private Date effectiveDate;
    
    @Temporal(TemporalType.DATE)
    @Column(name = "expiration_date")
    private Date expirationDate;
    
    @NotNull
    @Column(name = "version")
    private String version;
    
    @Column(name = "source_url")
    private String sourceUrl;
    
    @Column(name = "checksum")
    private String checksum;
    
    @NotNull
    @Column(name = "is_active")
    private Boolean isActive;
    
    @NotNull
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "last_updated")
    private Date lastUpdated;
    
    @Column(name = "search_vector", columnDefinition = "TEXT")
    private String searchVector;
    
    // Getters and Setters
}

// Knowledge Search Request Model
public class KnowledgeSearchRequest {
    @NotNull
    private String query;
    private String eventType;
    private String jurisdiction;
    private DocumentType documentType;
    private String productCategory;
    private List<String> keywords;
    private Integer maxResults;
    private Double relevanceThreshold;
    private Boolean includeExpired;
    
    // Getters and Setters
}

// Knowledge Search Response Model
public class KnowledgeSearchResponse {
    private String searchId;
    private String query;
    private List<RegulatoryDocumentResult> results;
    private Integer totalResults;
    private Double searchTime;
    private List<String> suggestedQueries;
    private List<ConflictAlert> conflicts;
    private Date searchTimestamp;
    
    // Getters and Setters
}

// Document Result Model
public class RegulatoryDocumentResult {
    private String documentId;
    private String title;
    private String regulationNumber;
    private String issuingAuthority;
    private String jurisdiction;
    private DocumentType documentType;
    private Double relevanceScore;
    private List<DocumentSection> relevantSections;
    private String summary;
    private Date effectiveDate;
    private Date expirationDate;
    private String version;
    private List<String> highlightedText;
    
    // Getters and Setters
}

// Document Section Model
public class DocumentSection {
    private String sectionId;
    private String sectionNumber;
    private String title;
    private String content;
    private Double relevanceScore;
    private List<String> applicableScenarios;
    
    // Getters and Setters
}

// Enums
public enum DocumentType {
    FDA_REGULATION, EMA_GUIDELINE, ICH_GUIDELINE, SOP, POLICY, 
    GMP_RULE, INDUSTRY_STANDARD, INTERNAL_PROCEDURE
}

public enum SearchType {
    SEMANTIC, KEYWORD, HYBRID, CITATION
}
```

### 2.2 API Details

```java
@RestController
@RequestMapping("/api/v1/regulatory-knowledge")
@Validated
public class RegulatoryKnowledgeController {
    
    @Autowired
    private RegulatoryKnowledgeService knowledgeService;
    
    @PostMapping("/search")
    @ResponseStatus(HttpStatus.OK)
    public ResponseEntity<KnowledgeSearchResponse> searchRegulations(
            @Valid @RequestBody KnowledgeSearchRequest request) {
        
        KnowledgeSearchResponse response = knowledgeService.searchRegulations(request);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/document/{documentId}")
    public ResponseEntity<RegulatoryDocumentResult> getDocument(
            @PathVariable String documentId,
            @RequestParam(defaultValue = "false") Boolean includeFullContent) {
        
        RegulatoryDocumentResult document = knowledgeService.getDocumentById(documentId, includeFullContent);
        return ResponseEntity.ok(document);
    }
    
    @GetMapping("/document/{documentId}/sections")
    public ResponseEntity<List<DocumentSection>> getDocumentSections(
            @PathVariable String documentId,
            @RequestParam(required = false) String sectionFilter) {
        
        List<DocumentSection> sections = knowledgeService.getDocumentSections(documentId, sectionFilter);
        return ResponseEntity.ok(sections);
    }
    
    @PostMapping("/context-search")
    public ResponseEntity<KnowledgeSearchResponse> searchByContext(
            @Valid @RequestBody EventContextRequest contextRequest) {
        
        KnowledgeSearchResponse response = knowledgeService.searchByEventContext(contextRequest);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/jurisdictions")
    public ResponseEntity<List<JurisdictionInfo>> getSupportedJurisdictions() {
        
        List<JurisdictionInfo> jurisdictions = knowledgeService.getSupportedJurisdictions();
        return ResponseEntity.ok(jurisdictions);
    }
    
    @GetMapping("/updates/recent")
    public ResponseEntity<List<DocumentUpdateInfo>> getRecentUpdates(
            @RequestParam(defaultValue = "7") Integer days,
            @RequestParam(required = false) String jurisdiction) {
        
        List<DocumentUpdateInfo> updates = knowledgeService.getRecentUpdates(days, jurisdiction);
        return ResponseEntity.ok(updates);
    }
    
    @PostMapping("/validate-compliance")
    public ResponseEntity<ComplianceValidationResponse> validateCompliance(
            @Valid @RequestBody ComplianceValidationRequest request) {
        
        ComplianceValidationResponse response = knowledgeService.validateCompliance(request);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/conflicts/detect")
    public ResponseEntity<List<ConflictAlert>> detectConflicts(
            @RequestParam String eventType,
            @RequestParam String jurisdiction) {
        
        List<ConflictAlert> conflicts = knowledgeService.detectRegulatoryConflicts(eventType, jurisdiction);
        return ResponseEntity.ok(conflicts);
    }
}
```

### 2.3 Exceptions

```java
@ResponseStatus(HttpStatus.BAD_REQUEST)
public class InvalidSearchRequestException extends RuntimeException {
    public InvalidSearchRequestException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.NOT_FOUND)
public class DocumentNotFoundException extends RuntimeException {
    public DocumentNotFoundException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
public class RegulatoryDatabaseUnavailableException extends RuntimeException {
    public RegulatoryDatabaseUnavailableException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
public class SearchEngineException extends RuntimeException {
    public SearchEngineException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.CONFLICT)
public class DocumentVersionConflictException extends RuntimeException {
    public DocumentVersionConflictException(String message) {
        super(message);
    }
}

@ControllerAdvice
public class RegulatoryKnowledgeExceptionHandler {
    
    @ExceptionHandler(InvalidSearchRequestException.class)
    public ResponseEntity<ErrorResponse> handleInvalidSearchRequest(InvalidSearchRequestException ex) {
        ErrorResponse error = new ErrorResponse("INVALID_SEARCH_REQUEST", ex.getMessage());
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(DocumentNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleDocumentNotFound(DocumentNotFoundException ex) {
        ErrorResponse error = new ErrorResponse("DOCUMENT_NOT_FOUND", ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
    
    @ExceptionHandler(RegulatoryDatabaseUnavailableException.class)
    public ResponseEntity<ErrorResponse> handleDatabaseUnavailable(RegulatoryDatabaseUnavailableException ex) {
        ErrorResponse error = new ErrorResponse("REGULATORY_DATABASE_UNAVAILABLE", ex.getMessage());
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(error);
    }
    
    @ExceptionHandler(SearchEngineException.class)
    public ResponseEntity<ErrorResponse> handleSearchEngineError(SearchEngineException ex) {
        ErrorResponse error = new ErrorResponse("SEARCH_ENGINE_ERROR", ex.getMessage());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

### 2.4 Functional Design

```mermaid
graph TD
    A[Knowledge Search Request] --> B[Input Validation]
    B --> C{Validation Passed?}
    C -->|No| D[Return Validation Error]
    C -->|Yes| E[Query Analysis]
    E --> F[Semantic Processing]
    F --> G[Index Search]
    G --> H[Relevance Scoring]
    H --> I[Result Ranking]
    I --> J[Conflict Detection]
    J --> K[Section Extraction]
    K --> L[Response Assembly]
    L --> M[Cache Results]
    M --> N[Return Search Response]
    
    O[Document Update Process] --> P[Source Monitoring]
    P --> Q[Change Detection]
    Q --> R[Content Validation]
    R --> S[Index Update]
    S --> T[Version Management]
    T --> U[Notification]
```

### 2.5 Class Diagram

```mermaid
classDiagram
    class RegulatoryKnowledgeController {
        +searchRegulations(request)
        +getDocument(documentId, includeFullContent)
        +getDocumentSections(documentId, sectionFilter)
        +searchByContext(contextRequest)
        +getSupportedJurisdictions()
        +getRecentUpdates(days, jurisdiction)
        +validateCompliance(request)
        +detectConflicts(eventType, jurisdiction)
    }
    
    class RegulatoryKnowledgeService {
        +searchRegulations(request)
        +getDocumentById(documentId, includeFullContent)
        +getDocumentSections(documentId, sectionFilter)
        +searchByEventContext(contextRequest)
        +getSupportedJurisdictions()
        +getRecentUpdates(days, jurisdiction)
        +validateCompliance(request)
        +detectRegulatoryConflicts(eventType, jurisdiction)
    }
    
    class SemanticSearchEngine {
        +performSemanticSearch(query, filters)
        +calculateRelevanceScore(document, query)
        +extractKeyPhrases(text)
        +generateEmbeddings(content)
    }
    
    class DocumentIndexer {
        +indexDocument(document)
        +updateIndex(documentId, content)
        +removeFromIndex(documentId)
        +rebuildIndex()
        +optimizeIndex()
    }
    
    class RegulatorySourceMonitor {
        +monitorSources()
        +detectChanges(source)
        +fetchUpdates(source)
        +validateContent(content)
    }
    
    class ConflictDetector {
        +detectConflicts(documents)
        +analyzeOverlaps(regulations)
        +identifyContradictions(rules)
        +generateConflictReport(conflicts)
    }
    
    class DocumentVersionManager {
        +createVersion(document)
        +compareVersions(oldVersion, newVersion)
        +archiveVersion(documentId, version)
        +getVersionHistory(documentId)
    }
    
    class ComplianceValidator {
        +validateCompliance(event, regulations)
        +checkRequirements(event, rules)
        +generateComplianceReport(validation)
    }
    
    RegulatoryKnowledgeController --> RegulatoryKnowledgeService
    RegulatoryKnowledgeService --> SemanticSearchEngine
    RegulatoryKnowledgeService --> DocumentIndexer
    RegulatoryKnowledgeService --> RegulatorySourceMonitor
    RegulatoryKnowledgeService --> ConflictDetector
    RegulatoryKnowledgeService --> DocumentVersionManager
    RegulatoryKnowledgeService --> ComplianceValidator
```

### 2.6 Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    participant SearchEngine
    participant IndexService
    participant ConflictDetector
    participant Cache
    participant Repository
    
    Client->>Controller: POST /api/v1/regulatory-knowledge/search
    Controller->>Service: searchRegulations(request)
    Service->>Service: validateSearchRequest(request)
    Service->>Cache: checkCache(queryHash)
    Cache-->>Service: CachedResults (if available)
    alt Cache Miss
        Service->>SearchEngine: performSemanticSearch(query, filters)
        SearchEngine->>IndexService: searchIndex(processedQuery)
        IndexService-->>SearchEngine: RawResults
        SearchEngine->>SearchEngine: calculateRelevanceScores()
        SearchEngine-->>Service: RankedResults
        Service->>ConflictDetector: detectConflicts(results)
        ConflictDetector-->>Service: ConflictAlerts
        Service->>Service: assembleResponse(results, conflicts)
        Service->>Cache: cacheResults(queryHash, response)
    end
    Service->>Repository: logSearch(searchRequest, results)
    Service-->>Controller: KnowledgeSearchResponse
    Controller-->>Client: HTTP 200 OK + Response
```

### 2.7 Components

```java
@Component
public class SearchRequestValidator {
    
    private static final int MAX_QUERY_LENGTH = 1000;
    private static final int MAX_RESULTS = 100;
    private static final double MIN_RELEVANCE_THRESHOLD = 0.1;
    
    public void validateSearchRequest(KnowledgeSearchRequest request) {
        if (request.getQuery() == null || request.getQuery().trim().isEmpty()) {
            throw new InvalidSearchRequestException("Search query is required");
        }
        
        if (request.getQuery().length() > MAX_QUERY_LENGTH) {
            throw new InvalidSearchRequestException("Query length exceeds maximum: " + MAX_QUERY_LENGTH);
        }
        
        if (request.getMaxResults() != null && request.getMaxResults() > MAX_RESULTS) {
            throw new InvalidSearchRequestException("Max results exceeds limit: " + MAX_RESULTS);
        }
        
        if (request.getRelevanceThreshold() != null && 
            request.getRelevanceThreshold() < MIN_RELEVANCE_THRESHOLD) {
            throw new InvalidSearchRequestException("Relevance threshold too low: " + MIN_RELEVANCE_THRESHOLD);
        }
        
        validateJurisdiction(request.getJurisdiction());
        validateDocumentType(request.getDocumentType());
    }
    
    private void validateJurisdiction(String jurisdiction) {
        if (jurisdiction != null) {
            List<String> validJurisdictions = Arrays.asList("FDA", "EMA", "PMDA", "HC", "TGA", "ANVISA");
            if (!validJurisdictions.contains(jurisdiction)) {
                throw new InvalidSearchRequestException("Invalid jurisdiction: " + jurisdiction);
            }
        }
    }
    
    private void validateDocumentType(DocumentType documentType) {
        if (documentType != null) {
            List<DocumentType> validTypes = Arrays.asList(DocumentType.values());
            if (!validTypes.contains(documentType)) {
                throw new InvalidSearchRequestException("Invalid document type: " + documentType);
            }
        }
    }
}

@Component
public class QueryProcessor {
    
    @Autowired
    private NaturalLanguageProcessor nlpProcessor;
    
    public ProcessedQuery processQuery(String rawQuery, KnowledgeSearchRequest request) {
        ProcessedQuery processed = new ProcessedQuery();
        
        // Clean and normalize query
        String cleanedQuery = cleanQuery(rawQuery);
        processed.setCleanedQuery(cleanedQuery);
        
        // Extract key phrases
        List<String> keyPhrases = nlpProcessor.extractKeyPhrases(cleanedQuery);
        processed.setKeyPhrases(keyPhrases);
        
        // Identify entities (regulations, sections, etc.)
        List<NamedEntity> entities = nlpProcessor.extractNamedEntities(cleanedQuery);
        processed.setNamedEntities(entities);
        
        // Generate synonyms and related terms
        List<String> expandedTerms = generateExpandedTerms(keyPhrases);
        processed.setExpandedTerms(expandedTerms);
        
        // Create search vectors
        double[] queryVector = nlpProcessor.generateEmbedding(cleanedQuery);
        processed.setQueryVector(queryVector);
        
        return processed;
    }
    
    private String cleanQuery(String query) {
        // Remove special characters, normalize whitespace
        return query.replaceAll("[^a-zA-Z0-9\\s\\-\\.]", "")
                   .replaceAll("\\s+", " ")
                   .trim()
                   .toLowerCase();
    }
    
    private List<String> generateExpandedTerms(List<String> keyPhrases) {
        List<String> expanded = new ArrayList<>(keyPhrases);
        
        // Add regulatory synonyms
        Map<String, List<String>> synonyms = Map.of(
            "gmp", Arrays.asList("good manufacturing practice", "manufacturing standards"),
            "validation", Arrays.asList("qualification", "verification", "testing"),
            "deviation", Arrays.asList("non-conformance", "discrepancy", "variance"),
            "capa", Arrays.asList("corrective action", "preventive action", "improvement")
        );
        
        for (String phrase : keyPhrases) {
            String lowerPhrase = phrase.toLowerCase();
            synonyms.entrySet().stream()
                .filter(entry -> lowerPhrase.contains(entry.getKey()))
                .forEach(entry -> expanded.addAll(entry.getValue()));
        }
        
        return expanded.stream().distinct().collect(Collectors.toList());
    }
}
```

### 2.8 Service Layer Business Logic

```java
@Service
@Transactional
public class RegulatoryKnowledgeServiceImpl implements RegulatoryKnowledgeService {
    
    @Autowired
    private SemanticSearchEngine searchEngine;
    
    @Autowired
    private DocumentIndexer documentIndexer;
    
    @Autowired
    private ConflictDetector conflictDetector;
    
    @Autowired
    private RegulatoryDocumentRepository documentRepository;
    
    @Autowired
    private SearchRequestValidator validator;
    
    @Autowired
    private QueryProcessor queryProcessor;
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    @Override
    public KnowledgeSearchResponse searchRegulations(KnowledgeSearchRequest request) {
        long startTime = System.currentTimeMillis();
        
        try {
            // Validate request
            validator.validateSearchRequest(request);
            
            // Generate search ID
            String searchId = generateSearchId();
            
            // Check cache
            String cacheKey = generateCacheKey(request);
            KnowledgeSearchResponse cachedResponse = (KnowledgeSearchResponse) redisTemplate.opsForValue().get(cacheKey);
            if (cachedResponse != null) {
                cachedResponse.setSearchId(searchId);
                return cachedResponse;
            }
            
            // Process query
            ProcessedQuery processedQuery = queryProcessor.processQuery(request.getQuery(), request);
            
            // Perform search
            List<RegulatoryDocumentResult> searchResults = searchEngine.performSemanticSearch(processedQuery, request);
            
            // Apply filters
            List<RegulatoryDocumentResult> filteredResults = applyFilters(searchResults, request);
            
            // Detect conflicts
            List<ConflictAlert> conflicts = conflictDetector.detectConflicts(filteredResults);
            
            // Generate suggestions
            List<String> suggestedQueries = generateSuggestedQueries(processedQuery, filteredResults);
            
            // Create response
            KnowledgeSearchResponse response = new KnowledgeSearchResponse();
            response.setSearchId(searchId);
            response.setQuery(request.getQuery());
            response.setResults(filteredResults);
            response.setTotalResults(filteredResults.size());
            response.setSearchTime((double)(System.currentTimeMillis() - startTime) / 1000.0);
            response.setSuggestedQueries(suggestedQueries);
            response.setConflicts(conflicts);
            response.setSearchTimestamp(new Date());
            
            // Cache response
            redisTemplate.opsForValue().set(cacheKey, response, Duration.ofHours(1));
            
            // Log search
            logSearch(request, response);
            
            return response;
            
        } catch (Exception e) {
            throw new SearchEngineException("Failed to perform regulatory search: " + e.getMessage());
        }
    }
    
    @Override
    public KnowledgeSearchResponse searchByEventContext(EventContextRequest contextRequest) {
        try {
            // Convert event context to search query
            String contextQuery = buildContextQuery(contextRequest);
            
            // Create search request
            KnowledgeSearchRequest searchRequest = new KnowledgeSearchRequest();
            searchRequest.setQuery(contextQuery);
            searchRequest.setEventType(contextRequest.getEventType());
            searchRequest.setJurisdiction(contextRequest.getJurisdiction());
            searchRequest.setProductCategory(contextRequest.getProductCategory());
            searchRequest.setMaxResults(20);
            searchRequest.setRelevanceThreshold(0.6);
            
            // Perform search
            return searchRegulations(searchRequest);
            
        } catch (Exception e) {
            throw new SearchEngineException("Failed to search by event context: " + e.getMessage());
        }
    }
    
    @Override
    public List<ConflictAlert> detectRegulatoryConflicts(String eventType, String jurisdiction) {
        try {
            // Get relevant regulations for event type
            KnowledgeSearchRequest request = new KnowledgeSearchRequest();
            request.setQuery(eventType);
            request.setJurisdiction(jurisdiction);
            request.setMaxResults(50);
            
            KnowledgeSearchResponse searchResponse = searchRegulations(request);
            
            // Detect conflicts among results
            return conflictDetector.detectConflicts(searchResponse.getResults());
            
        } catch (Exception e) {
            throw new SearchEngineException("Failed to detect regulatory conflicts: " + e.getMessage());
        }
    }
    
    private List<RegulatoryDocumentResult> applyFilters(List<RegulatoryDocumentResult> results, KnowledgeSearchRequest request) {
        Stream<RegulatoryDocumentResult> stream = results.stream();
        
        // Filter by document type
        if (request.getDocumentType() != null) {
            stream = stream.filter(result -> result.getDocumentType() == request.getDocumentType());
        }
        
        // Filter by jurisdiction
        if (request.getJurisdiction() != null) {
            stream = stream.filter(result -> request.getJurisdiction().equals(result.getJurisdiction()));
        }
        
        // Filter by relevance threshold
        if (request.getRelevanceThreshold() != null) {
            stream = stream.filter(result -> result.getRelevanceScore() >= request.getRelevanceThreshold());
        }
        
        // Filter expired documents
        if (request.getIncludeExpired() == null || !request.getIncludeExpired()) {
            Date now = new Date();
            stream = stream.filter(result -> 
                result.getExpirationDate() == null || result.getExpirationDate().after(now)
            );
        }
        
        // Limit results
        if (request.getMaxResults() != null) {
            stream = stream.limit(request.getMaxResults());
        }
        
        return stream.collect(Collectors.toList());
    }
    
    private String buildContextQuery(EventContextRequest contextRequest) {
        StringBuilder queryBuilder = new StringBuilder();
        
        queryBuilder.append(contextRequest.getEventType()).append(" ");
        
        if (contextRequest.getEventDescription() != null) {
            queryBuilder.append(contextRequest.getEventDescription()).append(" ");
        }
        
        if (contextRequest.getProductCategory() != null) {
            queryBuilder.append(contextRequest.getProductCategory()).append(" ");
        }
        
        if (contextRequest.getProcessArea() != null) {
            queryBuilder.append(contextRequest.getProcessArea()).append(" ");
        }
        
        return queryBuilder.toString().trim();
    }
    
    private String generateSearchId() {
        return "SEARCH-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 8);
    }
    
    private String generateCacheKey(KnowledgeSearchRequest request) {
        return "search:" + DigestUtils.md5Hex(
            request.getQuery() + 
            Optional.ofNullable(request.getJurisdiction()).orElse("") +
            Optional.ofNullable(request.getDocumentType()).map(Enum::name).orElse("") +
            Optional.ofNullable(request.getMaxResults()).map(String::valueOf).orElse("")
        );
    }
}
```

### 2.9 Validation Rules

```java
@Component
public class RegulatoryKnowledgeValidationRules {
    
    public void validateDocumentContent(RegulatoryDocument document) {
        if (document.getTitle() == null || document.getTitle().trim().isEmpty()) {
            throw new DocumentValidationException("Document title is required");
        }
        
        if (document.getContent() == null || document.getContent().trim().isEmpty()) {
            throw new DocumentValidationException("Document content is required");
        }
        
        if (document.getIssuingAuthority() == null || document.getIssuingAuthority().trim().isEmpty()) {
            throw new DocumentValidationException("Issuing authority is required");
        }
        
        validateEffectiveDates(document);
        validateDocumentStructure(document);
        validateContentIntegrity(document);
    }
    
    private void validateEffectiveDates(RegulatoryDocument document) {
        if (document.getEffectiveDate() == null) {
            throw new DocumentValidationException("Effective date is required");
        }
        
        if (document.getExpirationDate() != null && 
            document.getExpirationDate().before(document.getEffectiveDate())) {
            throw new DocumentValidationException("Expiration date cannot be before effective date");
        }
        
        // Warn if effective date is in the future
        if (document.getEffectiveDate().after(new Date())) {
            // Log warning but don't fail validation
        }
    }
    
    private void validateDocumentStructure(RegulatoryDocument document) {
        if (document.getSections() != null) {
            try {
                ObjectMapper mapper = new ObjectMapper();
                JsonNode sectionsNode = mapper.readTree(document.getSections());
                
                if (!sectionsNode.isArray()) {
                    throw new DocumentValidationException("Document sections must be an array");
                }
                
                for (JsonNode section : sectionsNode) {
                    if (!section.has("sectionId") || !section.has("title")) {
                        throw new DocumentValidationException("Each section must have sectionId and title");
                    }
                }
                
            } catch (JsonProcessingException e) {
                throw new DocumentValidationException("Invalid sections JSON format");
            }
        }
    }
    
    private void validateContentIntegrity(RegulatoryDocument document) {
        if (document.getChecksum() != null) {
            String calculatedChecksum = calculateChecksum(document.getContent());
            if (!document.getChecksum().equals(calculatedChecksum)) {
                throw new DocumentValidationException("Document content checksum mismatch");
            }
        }
    }
    
    public void validateSearchResults(List<RegulatoryDocumentResult> results, KnowledgeSearchRequest request) {
        if (results.isEmpty() && isRequiredSearch(request)) {
            throw new SearchValidationException("No results found for required regulatory search");
        }
        
        // Validate relevance scores
        for (RegulatoryDocumentResult result : results) {
            if (result.getRelevanceScore() < 0.0 || result.getRelevanceScore() > 1.0) {
                throw new SearchValidationException("Invalid relevance score: " + result.getRelevanceScore());
            }
        }
        
        // Validate result ordering (should be by relevance descending)
        for (int i = 1; i < results.size(); i++) {
            if (results.get(i).getRelevanceScore() > results.get(i-1).getRelevanceScore()) {
                throw new SearchValidationException("Search results not properly ordered by relevance");
            }
        }
    }
    
    private boolean isRequiredSearch(KnowledgeSearchRequest request) {
        // Certain event types require regulatory context
        List<String> requiredEventTypes = Arrays.asList("DEVIATION", "CAPA", "CHANGE_CONTROL");
        return request.getEventType() != null && requiredEventTypes.contains(request.getEventType());
    }
    
    private String calculateChecksum(String content) {
        return DigestUtils.sha256Hex(content);
    }
}
```

### 2.10 Service Integrations

```java
@Service
public class RegulatorySourceIntegrationService {
    
    @Value("${regulatory.fda.api.url}")
    private String fdaApiUrl;
    
    @Value("${regulatory.ema.api.url}")
    private String emaApiUrl;
    
    @Value("${regulatory.api.key}")
    private String apiKey;
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Autowired
    private DocumentVersionManager versionManager;
    
    @Scheduled(cron = "0 0 2 * * ?") // Daily at 2 AM
    public void synchronizeRegulatoryUpdates() {
        try {
            synchronizeFDAUpdates();
            synchronizeEMAUpdates();
            synchronizeICHUpdates();
            
        } catch (Exception e) {
            throw new RegulatoryDatabaseUnavailableException("Failed to synchronize regulatory updates: " + e.getMessage());
        }
    }
    
    private void synchronizeFDAUpdates() {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.set("Authorization", "Bearer " + apiKey);
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            // Get updates since last sync
            String lastSyncDate = getLastSyncDate("FDA");
            String url = fdaApiUrl + "/updates?since=" + lastSyncDate;
            
            HttpEntity<String> entity = new HttpEntity<>(headers);
            ResponseEntity<FDAUpdateResponse> response = restTemplate.exchange(
                url, HttpMethod.GET, entity, FDAUpdateResponse.class
            );
            
            FDAUpdateResponse updateResponse = response.getBody();
            if (updateResponse != null && updateResponse.getUpdates() != null) {
                for (FDADocumentUpdate update : updateResponse.getUpdates()) {
                    processDocumentUpdate(update);
                }
                
                updateLastSyncDate("FDA", new Date());
            }
            
        } catch (Exception e) {
            throw new RegulatoryDatabaseUnavailableException("Failed to sync FDA updates: " + e.getMessage());
        }
    }
    
    private void synchronizeEMAUpdates() {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.set("Authorization", "Bearer " + apiKey);
            
            String lastSyncDate = getLastSyncDate("EMA");
            String url = emaApiUrl + "/guidelines/updates?since=" + lastSyncDate;
            
            HttpEntity<String> entity = new HttpEntity<>(headers);
            ResponseEntity<EMAUpdateResponse> response = restTemplate.exchange(
                url, HttpMethod.GET, entity, EMAUpdateResponse.class
            );
            
            EMAUpdateResponse updateResponse = response.getBody();
            if (updateResponse != null && updateResponse.getGuidelines() != null) {
                for (EMAGuidelineUpdate update : updateResponse.getGuidelines()) {
                    processGuidelineUpdate(update);
                }
                
                updateLastSyncDate("EMA", new Date());
            }
            
        } catch (Exception e) {
            throw new RegulatoryDatabaseUnavailableException("Failed to sync EMA updates: " + e.getMessage());
        }
    }
    
    private void processDocumentUpdate(FDADocumentUpdate update) {
        try {
            // Check if document exists
            Optional<RegulatoryDocument> existingDoc = documentRepository.findByRegulationNumber(update.getRegulationNumber());
            
            if (existingDoc.isPresent()) {
                // Update existing document
                RegulatoryDocument document = existingDoc.get();
                
                // Create new version if content changed
                if (!document.getVersion().equals(update.getVersion())) {
                    versionManager.createVersion(document);
                    
                    document.setContent(update.getContent());
                    document.setVersion(update.getVersion());
                    document.setLastUpdated(new Date());
                    document.setChecksum(calculateChecksum(update.getContent()));
                    
                    documentRepository.save(document);
                    documentIndexer.updateIndex(document.getDocumentId(), document.getContent());
                }
            } else {
                // Create new document
                RegulatoryDocument newDocument = createDocumentFromUpdate(update);
                documentRepository.save(newDocument);
                documentIndexer.indexDocument(newDocument);
            }
            
        } catch (Exception e) {
            throw new RegulatoryDatabaseUnavailableException("Failed to process document update: " + e.getMessage());
        }
    }
    
    public ComplianceValidationResponse validateCompliance(ComplianceValidationRequest request) {
        try {
            // Search for applicable regulations
            KnowledgeSearchRequest searchRequest = new KnowledgeSearchRequest();
            searchRequest.setQuery(request.getEventDescription());
            searchRequest.setEventType(request.getEventType());
            searchRequest.setJurisdiction(request.getJurisdiction());
            searchRequest.setMaxResults(10);
            
            KnowledgeSearchResponse searchResponse = searchRegulations(searchRequest);
            
            // Analyze compliance against found regulations
            ComplianceAnalysis analysis = analyzeCompliance(request, searchResponse.getResults());
            
            // Generate compliance report
            ComplianceValidationResponse response = new ComplianceValidationResponse();
            response.setValidationId(generateValidationId());
            response.setEventId(request.getEventId());
            response.setComplianceStatus(analysis.getOverallStatus());
            response.setApplicableRegulations(analysis.getApplicableRegulations());
            response.setComplianceGaps(analysis.getComplianceGaps());
            response.setRecommendations(analysis.getRecommendations());
            response.setValidationTimestamp(new Date());
            
            return response;
            
        } catch (Exception e) {
            throw new SearchEngineException("Failed to validate compliance: " + e.getMessage());
        }
    }
    
    private String getLastSyncDate(String source) {
        // Retrieve from configuration or database
        return "2024-01-01"; // Placeholder
    }
    
    private void updateLastSyncDate(String source, Date date) {
        // Update in configuration or database
    }
    
    private String calculateChecksum(String content) {
        return DigestUtils.sha256Hex(content);
    }
}
```

---

## 3. Frontend React Details

### 3.1 UI Architecture

```jsx
// Regulatory Knowledge Dashboard Component
import React, { useState, useEffect } from 'react';
import { RegulatorySearch } from './RegulatorySearch';
import { SearchResults } from './SearchResults';
import { DocumentViewer } from './DocumentViewer';
import { ConflictAlerts } from './ConflictAlerts';
import { RecentUpdates } from './RecentUpdates';

const RegulatoryKnowledgeDashboard = () => {
    const [searchResults, setSearchResults] = useState(null);
    const [selectedDocument, setSelectedDocument] = useState(null);
    const [conflicts, setConflicts] = useState([]);
    const [recentUpdates, setRecentUpdates] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('search');

    useEffect(() => {
        loadRecentUpdates();
    }, []);

    const loadRecentUpdates = async () => {
        try {
            const response = await fetch('/api/v1/regulatory-knowledge/updates/recent?days=7');
            const updates = await response.json();
            setRecentUpdates(updates);
        } catch (err) {
            console.error('Failed to load recent updates:', err);
        }
    };

    const handleSearch = async (searchRequest) => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await fetch('/api/v1/regulatory-knowledge/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                },
                body: JSON.stringify(searchRequest)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const results = await response.json();
            setSearchResults(results);
            setConflicts(results.conflicts || []);
            
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="regulatory-knowledge-dashboard">
            <header className="dashboard-header">
                <h1>Regulatory Knowledge System</h1>
                <div className="dashboard-stats">
                    <div className="stat-card">
                        <span className="stat-value">{recentUpdates.length}</span>
                        <span className="stat-label">Recent Updates</span>
                    </div>
                    <div className="stat-card">
                        <span className="stat-value">{conflicts.length}</span>
                        <span className="stat-label">Conflicts Detected</span>
                    </div>
                    <div className="stat-card">
                        <span className="stat-value">
                            {searchResults ? searchResults.totalResults : 0}
                        </span>
                        <span className="stat-label">Search Results</span>
                    </div>
                </div>
            </header>

            <nav className="dashboard-nav">
                <button 
                    className={activeTab === 'search' ? 'active' : ''}
                    onClick={() => setActiveTab('search')}
                >
                    Search Regulations
                </button>
                <button 
                    className={activeTab === 'results' ? 'active' : ''}
                    onClick={() => setActiveTab('results')}
                    disabled={!searchResults}
                >
                    Search Results
                </button>
                <button 
                    className={activeTab === 'conflicts' ? 'active' : ''}
                    onClick={() => setActiveTab('conflicts')}
                    disabled={conflicts.length === 0}
                >
                    Conflicts ({conflicts.length})
                </button>
                <button 
                    className={activeTab === 'updates' ? 'active' : ''}
                    onClick={() => setActiveTab('updates')}
                >
                    Recent Updates
                </button>
            </nav>

            <div className="dashboard-content">
                {error && (
                    <div className="error-alert">
                        <strong>Error:</strong> {error}
                        <button onClick={() => setError(null)}>×</button>
                    </div>
                )}

                {activeTab === 'search' && (
                    <RegulatorySearch 
                        onSearch={handleSearch}
                        loading={loading}
                    />
                )}

                {activeTab === 'results' && searchResults && (
                    <SearchResults 
                        results={searchResults}
                        onDocumentSelect={setSelectedDocument}
                        loading={loading}
                    />
                )}

                {activeTab === 'conflicts' && (
                    <ConflictAlerts 
                        conflicts={conflicts}
                        onResolve={(conflictId) => {
                            setConflicts(conflicts.filter(c => c.id !== conflictId));
                        }}
                    />
                )}

                {activeTab === 'updates' && (
                    <RecentUpdates 
                        updates={recentUpdates}
                        onRefresh={loadRecentUpdates}
                    />
                )}
            </div>

            {selectedDocument && (
                <DocumentViewer 
                    document={selectedDocument}
                    onClose={() => setSelectedDocument(null)}
                />
            )}
        </div>
    );
};
```

### 3.2 UI Specifications

```jsx
// Regulatory Search Component
import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const RegulatorySearch = ({ onSearch, loading }) => {
    const validationSchema = Yup.object({
        query: Yup.string()
            .min(3, 'Query must be at least 3 characters')
            .max(1000, 'Query must be less than 1000 characters')
            .required('Search query is required'),
        jurisdiction: Yup.string(),
        documentType: Yup.string(),
        maxResults: Yup.number()
            .min(1, 'Must be at least 1')
            .max(100, 'Cannot exceed 100'),
        relevanceThreshold: Yup.number()
            .min(0.1, 'Must be at least 0.1')
            .max(1.0, 'Cannot exceed 1.0')
    });

    const handleSubmit = (values, { setSubmitting }) => {
        const searchRequest = {
            ...values,
            maxResults: values.maxResults || 20,
            relevanceThreshold: values.relevanceThreshold || 0.5,
            includeExpired: values.includeExpired || false
        };
        
        onSearch(searchRequest);
        setSubmitting(false);
    };

    return (
        <div className="regulatory-search">
            <h2>Search Regulatory Knowledge Base</h2>
            <p className="search-description">
                Search through FDA regulations, EMA guidelines, ICH standards, and organizational SOPs.
            </p>
            
            <Formik
                initialValues={{
                    query: '',
                    jurisdiction: '',
                    documentType: '',
                    eventType: '',
                    productCategory: '',
                    maxResults: 20,
                    relevanceThreshold: 0.5,
                    includeExpired: false
                }}
                validationSchema={validationSchema}
                onSubmit={handleSubmit}
            >
                {({ isSubmitting, values, setFieldValue }) => (
                    <Form className="search-form">
                        <div className="form-section">
                            <h3>Search Query</h3>
                            
                            <div className="form-group">
                                <label htmlFor="query">Search Terms *</label>
                                <Field 
                                    type="text" 
                                    name="query" 
                                    placeholder="e.g., GMP validation requirements, deviation reporting"
                                    className="form-control search-input"
                                />
                                <ErrorMessage name="query" component="div" className="error-message" />
                            </div>

                            <div className="quick-searches">
                                <span className="quick-search-label">Quick searches:</span>
                                <button 
                                    type="button" 
                                    className="quick-search-btn"
                                    onClick={() => setFieldValue('query', 'GMP validation requirements')}
                                >
                                    GMP Validation
                                </button>
                                <button 
                                    type="button" 
                                    className="quick-search-btn"
                                    onClick={() => setFieldValue('query', 'deviation reporting requirements')}
                                >
                                    Deviation Reporting
                                </button>
                                <button 
                                    type="button" 
                                    className="quick-search-btn"
                                    onClick={() => setFieldValue('query', 'change control procedures')}
                                >
                                    Change Control
                                </button>
                            </div>
                        </div>

                        <div className="form-section">
                            <h3>Search Filters</h3>
                            
                            <div className="form-row">
                                <div className="form-group col-md-6">
                                    <label htmlFor="jurisdiction">Jurisdiction</label>
                                    <Field as="select" name="jurisdiction" className="form-control">
                                        <option value="">All Jurisdictions</option>
                                        <option value="FDA">FDA (United States)</option>
                                        <option value="EMA">EMA (European Union)</option>
                                        <option value="PMDA">PMDA (Japan)</option>
                                        <option value="HC">Health Canada</option>
                                        <option value="TGA">TGA (Australia)</option>
                                        <option value="ANVISA">ANVISA (Brazil)</option>
                                    </Field>
                                </div>

                                <div className="form-group col-md-6">
                                    <label htmlFor="documentType">Document Type</label>
                                    <Field as="select" name="documentType" className="form-control">
                                        <option value="">All Document Types</option>
                                        <option value="FDA_REGULATION">FDA Regulation</option>
                                        <option value="EMA_GUIDELINE">EMA Guideline</option>
                                        <option value="ICH_GUIDELINE">ICH Guideline</option>
                                        <option value="SOP">Standard Operating Procedure</option>
                                        <option value="POLICY">Policy</option>
                                        <option value="GMP_RULE">GMP Rule</option>
                                        <option value="INDUSTRY_STANDARD">Industry Standard</option>
                                    </Field>
                                </div>
                            </div>

                            <div className="form-row">
                                <div className="form-group col-md-6">
                                    <label htmlFor="eventType">Event Type</label>
                                    <Field as="select" name="eventType" className="form-control">
                                        <option value="">All Event Types</option>
                                        <option value="DEVIATION">Deviation</option>
                                        <option value="CAPA">CAPA</option>
                                        <option value="CHANGE_CONTROL">Change Control</option>
                                        <option value="INCIDENT">Incident</option>
                                        <option value="COMPLAINT">Complaint</option>
                                        <option value="OOS">Out of Specification</option>
                                        <option value="OOT">Out of Trend</option>
                                    </Field>
                                </div>

                                <div className="form-group col-md-6">
                                    <label htmlFor="productCategory">Product Category</label>
                                    <Field 
                                        type="text" 
                                        name="productCategory" 
                                        placeholder="e.g., Pharmaceuticals, Medical Devices"
                                        className="form-control"
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="form-section">
                            <h3>Search Options</h3>
                            
                            <div className="form-row">
                                <div className="form-group col-md-4">
                                    <label htmlFor="maxResults">Max Results</label>
                                    <Field 
                                        type="number" 
                                        name="maxResults" 
                                        min="1" 
                                        max="100"
                                        className="form-control"
                                    />
                                    <ErrorMessage name="maxResults" component="div" className="error-message" />
                                </div>

                                <div className="form-group col-md-4">
                                    <label htmlFor="relevanceThreshold">Relevance Threshold</label>
                                    <Field 
                                        type="number" 
                                        name="relevanceThreshold" 
                                        min="0.1" 
                                        max="1.0" 
                                        step="0.1"
                                        className="form-control"
                                    />
                                    <ErrorMessage name="relevanceThreshold" component="div" className="error-message" />
                                </div>

                                <div className="form-group col-md-4">
                                    <div className="checkbox-group">
                                        <Field 
                                            type="checkbox" 
                                            name="includeExpired" 
                                            id="includeExpired"
                                        />
                                        <label htmlFor="includeExpired">Include Expired Documents</label>
                                    </div>
                                </div>
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
                                        Searching...
                                    </>
                                ) : (
                                    'Search Regulations'
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
// Regulatory Knowledge API Service
class RegulatoryKnowledgeAPI {
    constructor() {
        this.baseURL = process.env.REACT_APP_API_BASE_URL || '/api/v1';
        this.timeout = 15000; // 15 seconds for regulatory search
    }

    async searchRegulations(searchRequest) {
        const response = await this.makeRequest('/regulatory-knowledge/search', {
            method: 'POST',
            body: JSON.stringify(searchRequest)
        });
        return response;
    }

    async getDocument(documentId, includeFullContent = false) {
        const queryParams = new URLSearchParams({ includeFullContent: includeFullContent.toString() });
        const response = await this.makeRequest(`/regulatory-knowledge/document/${documentId}?${queryParams}`, {
            method: 'GET'
        });
        return response;
    }

    async getDocumentSections(documentId, sectionFilter = null) {
        const queryParams = new URLSearchParams();
        if (sectionFilter) queryParams.append('sectionFilter', sectionFilter);
        
        const response = await this.makeRequest(`/regulatory-knowledge/document/${documentId}/sections?${queryParams}`, {
            method: 'GET'
        });
        return response;
    }

    async searchByContext(contextRequest) {
        const response = await this.makeRequest('/regulatory-knowledge/context-search', {
            method: 'POST',
            body: JSON.stringify(contextRequest)
        });
        return response;
    }

    async getSupportedJurisdictions() {
        const response = await this.makeRequest('/regulatory-knowledge/jurisdictions', {
            method: 'GET'
        });
        return response;
    }

    async getRecentUpdates(days = 7, jurisdiction = null) {
        const queryParams = new URLSearchParams({ days: days.toString() });
        if (jurisdiction) queryParams.append('jurisdiction', jurisdiction);
        
        const response = await this.makeRequest(`/regulatory-knowledge/updates/recent?${queryParams}`, {
            method: 'GET'
        });
        return response;
    }

    async validateCompliance(validationRequest) {
        const response = await this.makeRequest('/regulatory-knowledge/validate-compliance', {
            method: 'POST',
            body: JSON.stringify(validationRequest)
        });
        return response;
    }

    async detectConflicts(eventType, jurisdiction) {
        const queryParams = new URLSearchParams({ eventType, jurisdiction });
        const response = await this.makeRequest(`/regulatory-knowledge/conflicts/detect?${queryParams}`, {
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
                throw new Error('Request timeout - regulatory search taking longer than expected');
            }
            throw error;
        }
    }

    getAuthToken() {
        return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
    }
}

export default new RegulatoryKnowledgeAPI();
```

---

## 4. Database Details

### 4.1 ER Diagram

```mermaid
erDiagram
    REGULATORY_DOCUMENTS {
        BIGINT id PK
        VARCHAR document_id UK
        ENUM document_type
        VARCHAR title
        VARCHAR regulation_number
        VARCHAR issuing_authority
        VARCHAR jurisdiction
        LONGTEXT content
        TEXT summary
        JSON keywords
        JSON sections
        DATE effective_date
        DATE expiration_date
        VARCHAR version
        VARCHAR source_url
        VARCHAR checksum
        BOOLEAN is_active
        TIMESTAMP last_updated
        TEXT search_vector
    }
    
    DOCUMENT_SECTIONS {
        BIGINT id PK
        VARCHAR section_id UK
        VARCHAR document_id FK
        VARCHAR section_number
        VARCHAR title
        TEXT content
        JSON applicable_scenarios
        INTEGER display_order
        BOOLEAN is_active
    }
    
    SEARCH_HISTORY {
        BIGINT id PK
        VARCHAR search_id UK
        VARCHAR user_id
        TEXT query
        JSON search_filters
        INTEGER results_count
        DECIMAL search_time
        TIMESTAMP search_timestamp
        JSON results_summary
    }
    
    DOCUMENT_VERSIONS {
        BIGINT id PK
        VARCHAR version_id UK
        VARCHAR document_id FK
        VARCHAR version_number
        LONGTEXT content
        VARCHAR checksum
        TIMESTAMP created_at
        VARCHAR created_by
        TEXT change_summary
    }
    
    REGULATORY_SOURCES {
        BIGINT id PK
        VARCHAR source_id UK
        VARCHAR source_name
        VARCHAR jurisdiction
        VARCHAR api_endpoint
        VARCHAR authentication_type
        JSON sync_configuration
        TIMESTAMP last_sync
        BOOLEAN is_active
    }
    
    CONFLICT_ALERTS {
        BIGINT id PK
        VARCHAR conflict_id UK
        VARCHAR document_id_1 FK
        VARCHAR document_id_2 FK
        ENUM conflict_type
        TEXT conflict_description
        ENUM severity_level
        ENUM status
        TIMESTAMP detected_at
        TIMESTAMP resolved_at
        VARCHAR resolved_by
    }
    
    REGULATORY_DOCUMENTS ||--o{ DOCUMENT_SECTIONS : "contains"
    REGULATORY_DOCUMENTS ||--o{ DOCUMENT_VERSIONS : "has_versions"
    REGULATORY_DOCUMENTS ||--o{ CONFLICT_ALERTS : "involved_in"
    REGULATORY_SOURCES ||--o{ REGULATORY_DOCUMENTS : "provides"
    SEARCH_HISTORY ||--o{ REGULATORY_DOCUMENTS : "finds"
```

### 4.2 Database Validations

```sql
-- Regulatory Documents Table
CREATE TABLE regulatory_documents (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    document_id VARCHAR(100) NOT NULL UNIQUE,
    document_type ENUM('FDA_REGULATION', 'EMA_GUIDELINE', 'ICH_GUIDELINE', 'SOP', 'POLICY', 
                       'GMP_RULE', 'INDUSTRY_STANDARD', 'INTERNAL_PROCEDURE') NOT NULL,
    title VARCHAR(500) NOT NULL,
    regulation_number VARCHAR(100),
    issuing_authority VARCHAR(200) NOT NULL,
    jurisdiction VARCHAR(50) NOT NULL,
    content LONGTEXT,
    summary TEXT,
    keywords JSON,
    sections JSON,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    version VARCHAR(20) NOT NULL,
    source_url VARCHAR(1000),
    checksum VARCHAR(64),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    search_vector TEXT,
    INDEX idx_document_id (document_id),
    INDEX idx_document_type (document_type),
    INDEX idx_regulation_number (regulation_number),
    INDEX idx_jurisdiction (jurisdiction),
    INDEX idx_effective_date (effective_date),
    INDEX idx_is_active (is_active),
    INDEX idx_last_updated (last_updated),
    FULLTEXT idx_search_content (title, content, summary),
    CONSTRAINT chk_dates CHECK (expiration_date IS NULL OR expiration_date > effective_date)
);

-- Document Sections Table
CREATE TABLE document_sections (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    section_id VARCHAR(100) NOT NULL UNIQUE,
    document_id VARCHAR(100) NOT NULL,
    section_number VARCHAR(50),
    title VARCHAR(300) NOT NULL,
    content TEXT,
    applicable_scenarios JSON,
    display_order INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (document_id) REFERENCES regulatory_documents(document_id) ON DELETE CASCADE,
    INDEX idx_section_id (section_id),
    INDEX idx_document_id (document_id),
    INDEX idx_section_number (section_number),
    INDEX idx_display_order (display_order),
    INDEX idx_is_active (is_active),
    FULLTEXT idx_section_content (title, content)
);

-- Search History Table
CREATE TABLE search_history (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    search_id VARCHAR(100) NOT NULL UNIQUE,
    user_id VARCHAR(100),
    query TEXT NOT NULL,
    search_filters JSON,
    results_count INTEGER NOT NULL DEFAULT 0,
    search_time DECIMAL(8,3) NOT NULL,
    search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    results_summary JSON,
    INDEX idx_search_id (search_id),
    INDEX idx_user_id (user_id),
    INDEX idx_search_timestamp (search_timestamp),
    INDEX idx_results_count (results_count)
);

-- Document Versions Table
CREATE TABLE document_versions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    version_id VARCHAR(100) NOT NULL UNIQUE,
    document_id VARCHAR(100) NOT NULL,
    version_number VARCHAR(20) NOT NULL,
    content LONGTEXT,
    checksum VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    change_summary TEXT,
    FOREIGN KEY (document_id) REFERENCES regulatory_documents(document_id) ON DELETE CASCADE,
    INDEX idx_version_id (version_id),
    INDEX idx_document_id (document_id),
    INDEX idx_version_number (version_number),
    INDEX idx_created_at (created_at),
    UNIQUE KEY uk_document_version (document_id, version_number)
);

-- Regulatory Sources Table
CREATE TABLE regulatory_sources (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    source_id VARCHAR(100) NOT NULL UNIQUE,
    source_name VARCHAR(200) NOT NULL,
    jurisdiction VARCHAR(50) NOT NULL,
    api_endpoint VARCHAR(500),
    authentication_type VARCHAR(50),
    sync_configuration JSON,
    last_sync TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    INDEX idx_source_id (source_id),
    INDEX idx_jurisdiction (jurisdiction),
    INDEX idx_last_sync (last_sync),
    INDEX idx_is_active (is_active)
);

-- Conflict Alerts Table
CREATE TABLE conflict_alerts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    conflict_id VARCHAR(100) NOT NULL UNIQUE,
    document_id_1 VARCHAR(100) NOT NULL,
    document_id_2 VARCHAR(100) NOT NULL,
    conflict_type ENUM('CONTRADICTION', 'OVERLAP', 'SUPERSEDED', 'INCONSISTENCY') NOT NULL,
    conflict_description TEXT,
    severity_level ENUM('HIGH', 'MEDIUM', 'LOW') NOT NULL,
    status ENUM('OPEN', 'INVESTIGATING', 'RESOLVED', 'DISMISSED') NOT NULL DEFAULT 'OPEN',
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    resolved_by VARCHAR(100),
    FOREIGN KEY (document_id_1) REFERENCES regulatory_documents(document_id) ON DELETE CASCADE,
    FOREIGN KEY (document_id_2) REFERENCES regulatory_documents(document_id) ON DELETE CASCADE,
    INDEX idx_conflict_id (conflict_id),
    INDEX idx_document_id_1 (document_id_1),
    INDEX idx_document_id_2 (document_id_2),
    INDEX idx_conflict_type (conflict_type),
    INDEX idx_severity_level (severity_level),
    INDEX idx_status (status),
    INDEX idx_detected_at (detected_at)
);
```

---

## 5. Non Functional Requirements

### 5.1 Performance

```yaml
Performance Requirements:
  Search Response Times:
    - Simple Keyword Search: < 500ms (95th percentile)
    - Semantic Search: < 1 second (95th percentile)
    - Complex Multi-Filter Search: < 2 seconds (95th percentile)
    
  Throughput Targets:
    - Concurrent Searches: 500+ simultaneous users
    - Searches per Hour: 50,000+
    - Document Indexing: 1,000+ documents per hour
    
  Database Performance:
    - Full-text Search: < 200ms for 100,000+ documents
    - Document Retrieval: < 100ms per document
    - Index Updates: < 5 seconds per document
    
  Resource Utilization:
    - CPU: < 70% under peak search load
    - Memory: < 80% heap utilization
    - Storage: Support 1TB+ of regulatory content
    - Search Index: < 50% of original content size
```

### 5.2 Security

```yaml
Security Requirements:
  Access Control:
    - Role-based document access permissions
    - Jurisdiction-specific content filtering
    - Audit trail for all document access
    
  Data Protection:
    - Regulatory content encryption at rest
    - Secure transmission of search results
    - Document integrity verification via checksums
    
  Authentication:
    - Multi-factor authentication for administrative functions
    - API key management for external integrations
    - Session management for concurrent users
    
  Compliance:
    - Data retention policies for search history
    - Privacy controls for user search data
    - Regulatory compliance for document handling
```

### 5.3 Logging

```java
@Component
public class RegulatoryKnowledgeLogger {
    
    private static final Logger logger = LoggerFactory.getLogger(RegulatoryKnowledgeLogger.class);
    private static final Logger auditLogger = LoggerFactory.getLogger("REGULATORY_KNOWLEDGE_AUDIT");
    private static final Logger performanceLogger = LoggerFactory.getLogger("REGULATORY_KNOWLEDGE_PERFORMANCE");
    private static final Logger syncLogger = LoggerFactory.getLogger("REGULATORY_SYNC");
    
    public void logSearch(String searchId, String userId, String query, int resultsCount, double searchTime) {
        auditLogger.info("Regulatory search performed - SearchId: {}, UserId: {}, Query: {}, Results: {}, Time: {}ms", 
            searchId, userId, query, resultsCount, searchTime);
        
        if (searchTime > 1000) {
            performanceLogger.warn("Slow regulatory search - SearchId: {}, Query: {}, Time: {}ms", 
                searchId, query, searchTime);
        }
    }
    
    public void logDocumentAccess(String documentId, String userId, boolean fullContent) {
        auditLogger.info("Document accessed - DocumentId: {}, UserId: {}, FullContent: {}", 
            documentId, userId, fullContent);
    }
    
    public void logDocumentUpdate(String documentId, String version, String source, String changeType) {
        syncLogger.info("Document updated - DocumentId: {}, Version: {}, Source: {}, ChangeType: {}", 
            documentId, version, source, changeType);
    }
    
    public void logConflictDetection(String conflictId, String documentId1, String documentId2, String conflictType) {
        auditLogger.warn("Regulatory conflict detected - ConflictId: {}, Document1: {}, Document2: {}, Type: {}", 
            conflictId, documentId1, documentId2, conflictType);
    }
    
    public void logSyncOperation(String source, int documentsProcessed, int documentsUpdated, int errors, long duration) {
        syncLogger.info("Sync completed - Source: {}, Processed: {}, Updated: {}, Errors: {}, Duration: {}ms", 
            source, documentsProcessed, documentsUpdated, errors, duration);
        
        if (errors > 0) {
            syncLogger.error("Sync errors detected - Source: {}, ErrorCount: {}", source, errors);
        }
    }
    
    public void logIndexOperation(String operation, String documentId, long duration, boolean success) {
        performanceLogger.info("Index operation - Operation: {}, DocumentId: {}, Duration: {}ms, Success: {}", 
            operation, documentId, duration, success);
        
        if (!success) {
            logger.error("Index operation failed - Operation: {}, DocumentId: {}", operation, documentId);
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
  Elasticsearch: 8.8.0
  Jackson: 2.15.0
  Validation API: 3.0.2
  Micrometer: 1.11.0
  Logback: 1.4.7
  Apache Tika: 2.8.0
  Apache Lucene: 9.7.0

Frontend Dependencies:
  React: 18.2.0
  React Router: 6.11.0
  Formik: 2.4.0
  Yup: 1.2.0
  Axios: 1.4.0
  Material-UI: 5.13.0
  React Query: 4.29.0
  React Highlight Words: 0.20.0
  React PDF Viewer: 3.12.0

Infrastructure Dependencies:
  MySQL: 8.0.33
  Elasticsearch: 8.8.0
  Redis: 7.0.11
  Nginx: 1.24.0
  Docker: 24.0.0
  Kubernetes: 1.27.0
  Prometheus: 2.45.0
  Grafana: 10.0.0

External Services:
  FDA API: v1.2
  EMA API: v2.0
  ICH Guidelines API: v1.1
  Document Processing Service: v2.5
  Natural Language Processing API: v1.3
```

---

## 7. Assumptions

```yaml
Technical Assumptions:
  - Elasticsearch cluster provides high-availability search capabilities
  - Regulatory authorities maintain stable API endpoints for data feeds
  - Document processing can handle multiple formats (PDF, HTML, XML, DOCX)
  - Network connectivity allows real-time synchronization with regulatory sources
  - Search index can be rebuilt without significant downtime

Business Assumptions:
  - Regulatory documents are available in structured, machine-readable formats
  - Document versioning follows consistent patterns across authorities
  - Search relevance can be measured and improved through user feedback
  - Conflict detection rules can be defined and maintained by regulatory experts
  - Users require both simple keyword and advanced semantic search capabilities

Operational Assumptions:
  - 24/7 availability for regulatory search functionality
  - Automated monitoring and alerting for sync failures
  - Regular backup of regulatory content and search indices
  - Disaster recovery procedures for search infrastructure
  - Performance monitoring and optimization processes in place

Data Assumptions:
  - Regulatory content quality is validated at source
  - Document metadata is complete and accurate
  - Historical versions of documents are preserved for audit purposes
  - Search analytics data is collected and analyzed for improvements
  - Content updates are published in predictable schedules

Integration Assumptions:
  - External regulatory APIs provide reliable data feeds
  - Authentication mechanisms are stable and well-documented
  - Data formats remain consistent across regulatory updates
  - API rate limits accommodate synchronization requirements
  - Error handling covers various failure scenarios
```