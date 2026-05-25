# Low Level Design Document

## Epic ID: EP002
## User Story ID: US006
## Title: Historical Deviation Learning System

---

## 1. Objective

Design and implement a machine learning-powered historical deviation learning system that analyzes past deviation patterns and outcomes to continuously improve AI decision-making accuracy through pattern recognition, similarity matching, and adaptive learning algorithms.

---

## 2. Backend Spring Boot API Details

### 2.1 API Model

```java
// Historical Deviation Model
@Entity
@Table(name = "historical_deviations")
public class HistoricalDeviation {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull
    @Column(name = "deviation_id")
    private String deviationId;
    
    @NotNull
    @Column(name = "event_type")
    @Enumerated(EnumType.STRING)
    private EventType eventType;
    
    @NotNull
    @Column(name = "description", columnDefinition = "TEXT")
    private String description;
    
    @Column(name = "root_cause", columnDefinition = "TEXT")
    private String rootCause;
    
    @Column(name = "corrective_actions", columnDefinition = "JSON")
    private String correctiveActions;
    
    @Column(name = "preventive_actions", columnDefinition = "JSON")
    private String preventiveActions;
    
    @NotNull
    @Column(name = "severity_level")
    @Enumerated(EnumType.STRING)
    private SeverityLevel severityLevel;
    
    @NotNull
    @Column(name = "gxp_classification")
    @Enumerated(EnumType.STRING)
    private GxPClassification gxpClassification;
    
    @Column(name = "product_line")
    private String productLine;
    
    @Column(name = "process_area")
    private String processArea;
    
    @Column(name = "equipment_involved")
    private String equipmentInvolved;
    
    @NotNull
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "occurrence_date")
    private Date occurrenceDate;
    
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "resolution_date")
    private Date resolutionDate;
    
    @Column(name = "resolution_effectiveness")
    @Enumerated(EnumType.STRING)
    private ResolutionEffectiveness resolutionEffectiveness;
    
    @Column(name = "recurrence_count")
    private Integer recurrenceCount;
    
    @Column(name = "cost_impact")
    private BigDecimal costImpact;
    
    @Column(name = "regulatory_impact")
    private String regulatoryImpact;
    
    @Column(name = "feature_vector", columnDefinition = "JSON")
    private String featureVector;
    
    @Column(name = "similarity_hash")
    private String similarityHash;
    
    @NotNull
    @Column(name = "data_quality_score")
    private Double dataQualityScore;
    
    @NotNull
    @Column(name = "is_training_data")
    private Boolean isTrainingData;
    
    // Getters and Setters
}

// Learning Model Configuration
@Entity
@Table(name = "learning_models")
public class LearningModel {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull
    @Column(name = "model_id")
    private String modelId;
    
    @NotNull
    @Column(name = "model_name")
    private String modelName;
    
    @NotNull
    @Column(name = "model_type")
    @Enumerated(EnumType.STRING)
    private ModelType modelType;
    
    @Column(name = "model_parameters", columnDefinition = "JSON")
    private String modelParameters;
    
    @Column(name = "training_data_size")
    private Integer trainingDataSize;
    
    @Column(name = "accuracy_score")
    private Double accuracyScore;
    
    @Column(name = "precision_score")
    private Double precisionScore;
    
    @Column(name = "recall_score")
    private Double recallScore;
    
    @Column(name = "f1_score")
    private Double f1Score;
    
    @NotNull
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "trained_at")
    private Date trainedAt;
    
    @NotNull
    @Column(name = "version")
    private String version;
    
    @NotNull
    @Column(name = "is_active")
    private Boolean isActive;
    
    @Column(name = "model_artifact_path")
    private String modelArtifactPath;
    
    // Getters and Setters
}

// Similarity Analysis Request
public class SimilarityAnalysisRequest {
    @NotNull
    private String currentEventId;
    @NotNull
    private String eventDescription;
    @NotNull
    private EventType eventType;
    private String productLine;
    private String processArea;
    private SeverityLevel severityLevel;
    private Integer maxSimilarEvents;
    private Double similarityThreshold;
    private Boolean includeOutcomes;
    
    // Getters and Setters
}

// Similarity Analysis Response
public class SimilarityAnalysisResponse {
    private String analysisId;
    private String currentEventId;
    private List<SimilarDeviationResult> similarDeviations;
    private PatternInsights patternInsights;
    private List<LearningRecommendation> learningRecommendations;
    private Double confidenceScore;
    private Date analysisTimestamp;
    
    // Getters and Setters
}

// Similar Deviation Result
public class SimilarDeviationResult {
    private String deviationId;
    private String description;
    private Double similarityScore;
    private EventType eventType;
    private SeverityLevel severityLevel;
    private String rootCause;
    private List<String> correctiveActions;
    private ResolutionEffectiveness resolutionEffectiveness;
    private Integer daysToresolve;
    private BigDecimal costImpact;
    private Date occurrenceDate;
    
    // Getters and Setters
}

// Enums
public enum EventType {
    DEVIATION, CAPA, CHANGE_CONTROL, INCIDENT, COMPLAINT, OOS, OOT, INVESTIGATION
}

public enum SeverityLevel {
    CRITICAL, MAJOR, MINOR, NEGLIGIBLE
}

public enum GxPClassification {
    GXP, NON_GXP
}

public enum ResolutionEffectiveness {
    HIGHLY_EFFECTIVE, EFFECTIVE, PARTIALLY_EFFECTIVE, INEFFECTIVE, UNKNOWN
}

public enum ModelType {
    SIMILARITY_MATCHING, CLASSIFICATION, RECOMMENDATION, PATTERN_RECOGNITION
}
```

### 2.2 API Details

```java
@RestController
@RequestMapping("/api/v1/historical-learning")
@Validated
public class HistoricalLearningController {
    
    @Autowired
    private HistoricalLearningService learningService;
    
    @PostMapping("/analyze-similarity")
    @ResponseStatus(HttpStatus.OK)
    public ResponseEntity<SimilarityAnalysisResponse> analyzeSimilarity(
            @Valid @RequestBody SimilarityAnalysisRequest request) {
        
        SimilarityAnalysisResponse response = learningService.analyzeSimilarity(request);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/learn-from-outcome")
    public ResponseEntity<LearningUpdateResponse> learnFromOutcome(
            @Valid @RequestBody OutcomeLearningRequest request) {
        
        LearningUpdateResponse response = learningService.learnFromOutcome(request);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/patterns/{eventType}")
    public ResponseEntity<PatternAnalysisResponse> getPatterns(
            @PathVariable EventType eventType,
            @RequestParam(defaultValue = "365") Integer daysPeriod,
            @RequestParam(required = false) String productLine) {
        
        PatternAnalysisResponse response = learningService.analyzePatterns(eventType, daysPeriod, productLine);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/models/train")
    public ResponseEntity<ModelTrainingResponse> trainModel(
            @Valid @RequestBody ModelTrainingRequest request) {
        
        ModelTrainingResponse response = learningService.trainModel(request);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/models/{modelId}/performance")
    public ResponseEntity<ModelPerformanceResponse> getModelPerformance(
            @PathVariable String modelId,
            @RequestParam(defaultValue = "30") Integer evaluationDays) {
        
        ModelPerformanceResponse response = learningService.getModelPerformance(modelId, evaluationDays);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/recommendations/feedback")
    public ResponseEntity<Void> submitRecommendationFeedback(
            @Valid @RequestBody RecommendationFeedback feedback) {
        
        learningService.processRecommendationFeedback(feedback);
        return ResponseEntity.ok().build();
    }
    
    @GetMapping("/insights/trends")
    public ResponseEntity<TrendInsightsResponse> getTrendInsights(
            @RequestParam(defaultValue = "90") Integer daysPeriod,
            @RequestParam(required = false) EventType eventType,
            @RequestParam(required = false) String productLine) {
        
        TrendInsightsResponse response = learningService.getTrendInsights(daysPeriod, eventType, productLine);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/data-quality/validate")
    public ResponseEntity<DataQualityReport> validateDataQuality(
            @Valid @RequestBody DataQualityRequest request) {
        
        DataQualityReport report = learningService.validateDataQuality(request);
        return ResponseEntity.ok(report);
    }
}
```

### 2.3 Exceptions

```java
@ResponseStatus(HttpStatus.BAD_REQUEST)
public class InvalidLearningRequestException extends RuntimeException {
    public InvalidLearningRequestException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.NOT_FOUND)
public class HistoricalDataNotFoundException extends RuntimeException {
    public HistoricalDataNotFoundException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
public class LearningEngineUnavailableException extends RuntimeException {
    public LearningEngineUnavailableException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
public class ModelTrainingException extends RuntimeException {
    public ModelTrainingException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.CONFLICT)
public class DataQualityException extends RuntimeException {
    public DataQualityException(String message) {
        super(message);
    }
}

@ControllerAdvice
public class HistoricalLearningExceptionHandler {
    
    @ExceptionHandler(InvalidLearningRequestException.class)
    public ResponseEntity<ErrorResponse> handleInvalidRequest(InvalidLearningRequestException ex) {
        ErrorResponse error = new ErrorResponse("INVALID_LEARNING_REQUEST", ex.getMessage());
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(HistoricalDataNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleDataNotFound(HistoricalDataNotFoundException ex) {
        ErrorResponse error = new ErrorResponse("HISTORICAL_DATA_NOT_FOUND", ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
    
    @ExceptionHandler(LearningEngineUnavailableException.class)
    public ResponseEntity<ErrorResponse> handleEngineUnavailable(LearningEngineUnavailableException ex) {
        ErrorResponse error = new ErrorResponse("LEARNING_ENGINE_UNAVAILABLE", ex.getMessage());
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(error);
    }
    
    @ExceptionHandler(ModelTrainingException.class)
    public ResponseEntity<ErrorResponse> handleModelTraining(ModelTrainingException ex) {
        ErrorResponse error = new ErrorResponse("MODEL_TRAINING_ERROR", ex.getMessage());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

### 2.4 Functional Design

```mermaid
graph TD
    A[Similarity Analysis Request] --> B[Input Validation]
    B --> C{Validation Passed?}
    C -->|No| D[Return Validation Error]
    C -->|Yes| E[Feature Extraction]
    E --> F[Historical Data Retrieval]
    F --> G[Similarity Calculation]
    G --> H[Pattern Recognition]
    H --> I[Outcome Analysis]
    I --> J[Learning Recommendations]
    J --> K[Confidence Scoring]
    K --> L[Response Assembly]
    L --> M[Model Update Trigger]
    M --> N[Return Analysis Response]
    
    O[Model Training Process] --> P[Data Preparation]
    P --> Q[Feature Engineering]
    Q --> R[Model Training]
    R --> S[Model Validation]
    S --> T[Performance Evaluation]
    T --> U[Model Deployment]
    U --> V[Performance Monitoring]
```

### 2.5 Class Diagram

```mermaid
classDiagram
    class HistoricalLearningController {
        +analyzeSimilarity(request)
        +learnFromOutcome(request)
        +getPatterns(eventType, daysPeriod, productLine)
        +trainModel(request)
        +getModelPerformance(modelId, evaluationDays)
        +submitRecommendationFeedback(feedback)
        +getTrendInsights(daysPeriod, eventType, productLine)
        +validateDataQuality(request)
    }
    
    class HistoricalLearningService {
        +analyzeSimilarity(request)
        +learnFromOutcome(request)
        +analyzePatterns(eventType, daysPeriod, productLine)
        +trainModel(request)
        +getModelPerformance(modelId, evaluationDays)
        +processRecommendationFeedback(feedback)
        +getTrendInsights(daysPeriod, eventType, productLine)
        +validateDataQuality(request)
    }
    
    class SimilarityEngine {
        +calculateSimilarity(currentEvent, historicalEvent)
        +extractFeatures(deviation)
        +generateFeatureVector(deviation)
        +findSimilarDeviations(features, threshold)
    }
    
    class PatternRecognitionEngine {
        +identifyPatterns(deviations)
        +analyzeOutcomes(patterns)
        +generateInsights(patterns)
        +detectAnomalies(deviations)
    }
    
    class MachineLearningEngine {
        +trainSimilarityModel(trainingData)
        +trainClassificationModel(trainingData)
        +trainRecommendationModel(trainingData)
        +evaluateModel(model, testData)
        +updateModel(model, newData)
    }
    
    class DataQualityValidator {
        +validateDataCompleteness(deviation)
        +validateDataAccuracy(deviation)
        +calculateQualityScore(deviation)
        +identifyDataGaps(deviations)
    }
    
    class OutcomeLearningProcessor {
        +processOutcome(deviation, outcome)
        +updateLearningModel(outcome)
        +calculateEffectiveness(actions, outcome)
        +generateLearningInsights(outcomes)
    }
    
    class TrendAnalyzer {
        +analyzeTrends(deviations, period)
        +identifySeasonalPatterns(deviations)
        +detectTrendChanges(trends)
        +generateTrendInsights(trends)
    }
    
    HistoricalLearningController --> HistoricalLearningService
    HistoricalLearningService --> SimilarityEngine
    HistoricalLearningService --> PatternRecognitionEngine
    HistoricalLearningService --> MachineLearningEngine
    HistoricalLearningService --> DataQualityValidator
    HistoricalLearningService --> OutcomeLearningProcessor
    HistoricalLearningService --> TrendAnalyzer
```

### 2.6 Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    participant SimilarityEngine
    participant PatternEngine
    participant MLEngine
    participant Repository
    participant Cache
    
    Client->>Controller: POST /api/v1/historical-learning/analyze-similarity
    Controller->>Service: analyzeSimilarity(request)
    Service->>Service: validateRequest(request)
    Service->>SimilarityEngine: extractFeatures(currentEvent)
    SimilarityEngine-->>Service: FeatureVector
    Service->>Cache: checkSimilarityCache(featureHash)
    Cache-->>Service: CachedResults (if available)
    alt Cache Miss
        Service->>Repository: findHistoricalDeviations(filters)
        Repository-->>Service: HistoricalDeviations
        Service->>SimilarityEngine: calculateSimilarities(features, historical)
        SimilarityEngine-->>Service: SimilarityScores
        Service->>PatternEngine: identifyPatterns(similarDeviations)
        PatternEngine-->>Service: PatternInsights
        Service->>MLEngine: generateRecommendations(patterns, outcomes)
        MLEngine-->>Service: LearningRecommendations
        Service->>Cache: cacheSimilarityResults(featureHash, results)
    end
    Service->>Service: assembleResponse(similarities, patterns, recommendations)
    Service-->>Controller: SimilarityAnalysisResponse
    Controller-->>Client: HTTP 200 OK + Response
```

### 2.7 Components

```java
@Component
public class LearningRequestValidator {
    
    private static final int MAX_DESCRIPTION_LENGTH = 5000;
    private static final int MAX_SIMILAR_EVENTS = 50;
    private static final double MIN_SIMILARITY_THRESHOLD = 0.1;
    
    public void validateSimilarityRequest(SimilarityAnalysisRequest request) {
        if (request.getCurrentEventId() == null || request.getCurrentEventId().trim().isEmpty()) {
            throw new InvalidLearningRequestException("Current event ID is required");
        }
        
        if (request.getEventDescription() == null || request.getEventDescription().trim().isEmpty()) {
            throw new InvalidLearningRequestException("Event description is required");
        }
        
        if (request.getEventDescription().length() > MAX_DESCRIPTION_LENGTH) {
            throw new InvalidLearningRequestException("Event description exceeds maximum length: " + MAX_DESCRIPTION_LENGTH);
        }
        
        if (request.getEventType() == null) {
            throw new InvalidLearningRequestException("Event type is required");
        }
        
        if (request.getMaxSimilarEvents() != null && request.getMaxSimilarEvents() > MAX_SIMILAR_EVENTS) {
            throw new InvalidLearningRequestException("Max similar events exceeds limit: " + MAX_SIMILAR_EVENTS);
        }
        
        if (request.getSimilarityThreshold() != null && request.getSimilarityThreshold() < MIN_SIMILARITY_THRESHOLD) {
            throw new InvalidLearningRequestException("Similarity threshold too low: " + MIN_SIMILARITY_THRESHOLD);
        }
    }
    
    public void validateModelTrainingRequest(ModelTrainingRequest request) {
        if (request.getModelType() == null) {
            throw new InvalidLearningRequestException("Model type is required");
        }
        
        if (request.getTrainingDataPeriod() != null && request.getTrainingDataPeriod() < 30) {
            throw new InvalidLearningRequestException("Training data period must be at least 30 days");
        }
        
        validateModelParameters(request.getModelParameters());
    }
    
    private void validateModelParameters(Map<String, Object> parameters) {
        if (parameters != null) {
            // Validate specific parameters based on model type
            if (parameters.containsKey("learningRate")) {
                Double learningRate = (Double) parameters.get("learningRate");
                if (learningRate <= 0 || learningRate > 1) {
                    throw new InvalidLearningRequestException("Learning rate must be between 0 and 1");
                }
            }
            
            if (parameters.containsKey("maxIterations")) {
                Integer maxIterations = (Integer) parameters.get("maxIterations");
                if (maxIterations <= 0 || maxIterations > 10000) {
                    throw new InvalidLearningRequestException("Max iterations must be between 1 and 10000");
                }
            }
        }
    }
}

@Component
public class FeatureExtractor {
    
    @Autowired
    private NaturalLanguageProcessor nlpProcessor;
    
    public FeatureVector extractFeatures(HistoricalDeviation deviation) {
        FeatureVector features = new FeatureVector();
        
        // Text-based features
        features.setDescriptionEmbedding(nlpProcessor.generateEmbedding(deviation.getDescription()));
        features.setKeywords(nlpProcessor.extractKeywords(deviation.getDescription()));
        features.setNamedEntities(nlpProcessor.extractNamedEntities(deviation.getDescription()));
        
        // Categorical features
        features.setEventType(deviation.getEventType().name());
        features.setSeverityLevel(deviation.getSeverityLevel().name());
        features.setGxpClassification(deviation.getGxpClassification().name());
        features.setProductLine(deviation.getProductLine());
        features.setProcessArea(deviation.getProcessArea());
        
        // Numerical features
        features.setOccurrenceMonth(extractMonth(deviation.getOccurrenceDate()));
        features.setOccurrenceQuarter(extractQuarter(deviation.getOccurrenceDate()));
        features.setRecurrenceCount(deviation.getRecurrenceCount());
        features.setCostImpactCategory(categorizeCostImpact(deviation.getCostImpact()));
        
        // Derived features
        features.setResolutionTimeCategory(calculateResolutionTimeCategory(deviation));
        features.setComplexityScore(calculateComplexityScore(deviation));
        features.setRiskScore(calculateRiskScore(deviation));
        
        return features;
    }
    
    public String generateSimilarityHash(FeatureVector features) {
        // Create hash based on key features for similarity grouping
        StringBuilder hashInput = new StringBuilder();
        hashInput.append(features.getEventType())
                 .append(features.getSeverityLevel())
                 .append(features.getProductLine())
                 .append(features.getProcessArea())
                 .append(features.getComplexityScore());
        
        return DigestUtils.md5Hex(hashInput.toString());
    }
    
    private int extractMonth(Date date) {
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        return cal.get(Calendar.MONTH) + 1;
    }
    
    private int extractQuarter(Date date) {
        return (extractMonth(date) - 1) / 3 + 1;
    }
    
    private String categorizeCostImpact(BigDecimal cost) {
        if (cost == null) return "UNKNOWN";
        if (cost.compareTo(new BigDecimal("10000")) < 0) return "LOW";
        if (cost.compareTo(new BigDecimal("100000")) < 0) return "MEDIUM";
        return "HIGH";
    }
    
    private String calculateResolutionTimeCategory(HistoricalDeviation deviation) {
        if (deviation.getResolutionDate() == null) return "UNRESOLVED";
        
        long days = ChronoUnit.DAYS.between(
            deviation.getOccurrenceDate().toInstant(),
            deviation.getResolutionDate().toInstant()
        );
        
        if (days <= 7) return "FAST";
        if (days <= 30) return "MEDIUM";
        return "SLOW";
    }
    
    private double calculateComplexityScore(HistoricalDeviation deviation) {
        double score = 0.0;
        
        // Base complexity from event type
        switch (deviation.getEventType()) {
            case DEVIATION: score += 0.6; break;
            case CAPA: score += 0.8; break;
            case INVESTIGATION: score += 0.9; break;
            default: score += 0.5; break;
        }
        
        // Adjust for severity
        switch (deviation.getSeverityLevel()) {
            case CRITICAL: score += 0.4; break;
            case MAJOR: score += 0.3; break;
            case MINOR: score += 0.1; break;
            default: score += 0.0; break;
        }
        
        // Adjust for recurrence
        if (deviation.getRecurrenceCount() != null && deviation.getRecurrenceCount() > 0) {
            score += Math.min(0.3, deviation.getRecurrenceCount() * 0.1);
        }
        
        return Math.min(1.0, score);
    }
    
    private double calculateRiskScore(HistoricalDeviation deviation) {
        double risk = 0.0;
        
        // GxP classification impact
        if (deviation.getGxpClassification() == GxPClassification.GXP) {
            risk += 0.5;
        }
        
        // Severity impact
        switch (deviation.getSeverityLevel()) {
            case CRITICAL: risk += 0.4; break;
            case MAJOR: risk += 0.3; break;
            case MINOR: risk += 0.1; break;
        }
        
        // Cost impact
        if (deviation.getCostImpact() != null) {
            if (deviation.getCostImpact().compareTo(new BigDecimal("100000")) > 0) {
                risk += 0.1;
            }
        }
        
        return Math.min(1.0, risk);
    }
}
```

### 2.8 Service Layer Business Logic

```java
@Service
@Transactional
public class HistoricalLearningServiceImpl implements HistoricalLearningService {
    
    @Autowired
    private SimilarityEngine similarityEngine;
    
    @Autowired
    private PatternRecognitionEngine patternEngine;
    
    @Autowired
    private MachineLearningEngine mlEngine;
    
    @Autowired
    private DataQualityValidator dataQualityValidator;
    
    @Autowired
    private OutcomeLearningProcessor outcomeLearningProcessor;
    
    @Autowired
    private HistoricalDeviationRepository deviationRepository;
    
    @Autowired
    private LearningModelRepository modelRepository;
    
    @Autowired
    private LearningRequestValidator validator;
    
    @Autowired
    private FeatureExtractor featureExtractor;
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    @Override
    public SimilarityAnalysisResponse analyzeSimilarity(SimilarityAnalysisRequest request) {
        long startTime = System.currentTimeMillis();
        
        try {
            // Validate request
            validator.validateSimilarityRequest(request);
            
            // Generate analysis ID
            String analysisId = generateAnalysisId();
            
            // Extract features from current event
            FeatureVector currentFeatures = extractCurrentEventFeatures(request);
            
            // Check cache for similar analysis
            String cacheKey = generateCacheKey(currentFeatures);
            SimilarityAnalysisResponse cachedResponse = (SimilarityAnalysisResponse) redisTemplate.opsForValue().get(cacheKey);
            if (cachedResponse != null) {
                cachedResponse.setAnalysisId(analysisId);
                return cachedResponse;
            }
            
            // Find similar historical deviations
            List<HistoricalDeviation> candidates = findCandidateDeviations(request);
            
            // Calculate similarity scores
            List<SimilarDeviationResult> similarDeviations = similarityEngine.findSimilarDeviations(
                currentFeatures, candidates, request.getSimilarityThreshold(), request.getMaxSimilarEvents()
            );
            
            // Analyze patterns in similar deviations
            PatternInsights patternInsights = patternEngine.analyzePatterns(similarDeviations);
            
            // Generate learning-based recommendations
            List<LearningRecommendation> recommendations = mlEngine.generateLearningRecommendations(
                currentFeatures, similarDeviations, patternInsights
            );
            
            // Calculate confidence score
            double confidenceScore = calculateConfidenceScore(similarDeviations, patternInsights);
            
            // Create response
            SimilarityAnalysisResponse response = new SimilarityAnalysisResponse();
            response.setAnalysisId(analysisId);
            response.setCurrentEventId(request.getCurrentEventId());
            response.setSimilarDeviations(similarDeviations);
            response.setPatternInsights(patternInsights);
            response.setLearningRecommendations(recommendations);
            response.setConfidenceScore(confidenceScore);
            response.setAnalysisTimestamp(new Date());
            response.setProcessingTimeMs(System.currentTimeMillis() - startTime);
            
            // Cache response
            redisTemplate.opsForValue().set(cacheKey, response, Duration.ofHours(2));
            
            // Log analysis
            logSimilarityAnalysis(request, response);
            
            return response;
            
        } catch (Exception e) {
            throw new LearningEngineUnavailableException("Failed to analyze similarity: " + e.getMessage());
        }
    }
    
    @Override
    public LearningUpdateResponse learnFromOutcome(OutcomeLearningRequest request) {
        try {
            // Validate outcome data
            validateOutcomeData(request);
            
            // Process outcome learning
            LearningUpdate update = outcomeLearningProcessor.processOutcome(request);
            
            // Update learning models
            mlEngine.updateModelsWithOutcome(update);
            
            // Update historical deviation record
            updateHistoricalDeviation(request);
            
            // Generate learning insights
            LearningInsights insights = generateLearningInsights(update);
            
            // Create response
            LearningUpdateResponse response = new LearningUpdateResponse();
            response.setUpdateId(generateUpdateId());
            response.setDeviationId(request.getDeviationId());
            response.setLearningInsights(insights);
            response.setModelUpdatesApplied(update.getModelUpdatesApplied());
            response.setUpdateTimestamp(new Date());
            
            return response;
            
        } catch (Exception e) {
            throw new LearningEngineUnavailableException("Failed to learn from outcome: " + e.getMessage());
        }
    }
    
    @Override
    public ModelTrainingResponse trainModel(ModelTrainingRequest request) {
        try {
            // Validate training request
            validator.validateModelTrainingRequest(request);
            
            // Prepare training data
            List<HistoricalDeviation> trainingData = prepareTrainingData(request);
            
            // Validate data quality
            DataQualityReport qualityReport = dataQualityValidator.validateTrainingData(trainingData);
            if (qualityReport.getOverallScore() < 0.8) {
                throw new DataQualityException("Training data quality insufficient: " + qualityReport.getOverallScore());
            }
            
            // Train model
            LearningModel trainedModel = mlEngine.trainModel(request.getModelType(), trainingData, request.getModelParameters());
            
            // Evaluate model performance
            ModelPerformanceMetrics performance = mlEngine.evaluateModel(trainedModel, trainingData);
            
            // Save model if performance is acceptable
            if (performance.getAccuracyScore() >= 0.75) {
                trainedModel = modelRepository.save(trainedModel);
                
                // Activate model if it's better than current active model
                activateModelIfBetter(trainedModel, performance);
            }
            
            // Create response
            ModelTrainingResponse response = new ModelTrainingResponse();
            response.setTrainingId(generateTrainingId());
            response.setModelId(trainedModel.getModelId());
            response.setPerformanceMetrics(performance);
            response.setDataQualityReport(qualityReport);
            response.setTrainingDuration(calculateTrainingDuration(trainedModel));
            response.setTrainingTimestamp(trainedModel.getTrainedAt());
            
            return response;
            
        } catch (Exception e) {
            throw new ModelTrainingException("Failed to train model: " + e.getMessage());
        }
    }
    
    private List<HistoricalDeviation> findCandidateDeviations(SimilarityAnalysisRequest request) {
        // Build search criteria
        HistoricalDeviationSearchCriteria criteria = new HistoricalDeviationSearchCriteria();
        criteria.setEventType(request.getEventType());
        criteria.setProductLine(request.getProductLine());
        criteria.setProcessArea(request.getProcessArea());
        criteria.setSeverityLevel(request.getSeverityLevel());
        criteria.setMinDataQualityScore(0.7);
        criteria.setIsTrainingData(true);
        criteria.setMaxResults(1000);
        
        return deviationRepository.findByCriteria(criteria);
    }
    
    private FeatureVector extractCurrentEventFeatures(SimilarityAnalysisRequest request) {
        // Create temporary deviation object for feature extraction
        HistoricalDeviation tempDeviation = new HistoricalDeviation();
        tempDeviation.setDescription(request.getEventDescription());
        tempDeviation.setEventType(request.getEventType());
        tempDeviation.setProductLine(request.getProductLine());
        tempDeviation.setProcessArea(request.getProcessArea());
        tempDeviation.setSeverityLevel(request.getSeverityLevel());
        tempDeviation.setOccurrenceDate(new Date());
        
        return featureExtractor.extractFeatures(tempDeviation);
    }
    
    private double calculateConfidenceScore(List<SimilarDeviationResult> similarDeviations, PatternInsights patterns) {
        if (similarDeviations.isEmpty()) {
            return 0.0;
        }
        
        // Base confidence from similarity scores
        double avgSimilarity = similarDeviations.stream()
            .mapToDouble(SimilarDeviationResult::getSimilarityScore)
            .average()
            .orElse(0.0);
        
        // Adjust for number of similar deviations
        double countFactor = Math.min(1.0, similarDeviations.size() / 10.0);
        
        // Adjust for pattern strength
        double patternFactor = patterns.getPatternStrength();
        
        // Adjust for outcome consistency
        double outcomeFactor = calculateOutcomeConsistency(similarDeviations);
        
        return (avgSimilarity * 0.4 + countFactor * 0.2 + patternFactor * 0.2 + outcomeFactor * 0.2);
    }
    
    private double calculateOutcomeConsistency(List<SimilarDeviationResult> deviations) {
        Map<ResolutionEffectiveness, Long> effectivenessCount = deviations.stream()
            .collect(Collectors.groupingBy(
                SimilarDeviationResult::getResolutionEffectiveness,
                Collectors.counting()
            ));
        
        if (effectivenessCount.isEmpty()) {
            return 0.0;
        }
        
        // Calculate consistency as the proportion of the most common effectiveness
        long maxCount = effectivenessCount.values().stream().mapToLong(Long::longValue).max().orElse(0);
        return (double) maxCount / deviations.size();
    }
    
    private String generateAnalysisId() {
        return "ANALYSIS-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 8);
    }
    
    private String generateCacheKey(FeatureVector features) {
        return "similarity:" + featureExtractor.generateSimilarityHash(features);
    }
}
```

### 2.9 Validation Rules

```java
@Component
public class HistoricalLearningValidationRules {
    
    private static final double MIN_DATA_QUALITY_SCORE = 0.7;
    private static final int MIN_TRAINING_SAMPLES = 100;
    private static final double MIN_MODEL_ACCURACY = 0.75;
    
    public void validateHistoricalDeviation(HistoricalDeviation deviation) {
        if (deviation.getDescription() == null || deviation.getDescription().trim().isEmpty()) {
            throw new DataQualityException("Deviation description is required");
        }
        
        if (deviation.getOccurrenceDate() == null) {
            throw new DataQualityException("Occurrence date is required");
        }
        
        if (deviation.getOccurrenceDate().after(new Date())) {
            throw new DataQualityException("Occurrence date cannot be in the future");
        }
        
        validateResolutionData(deviation);
        validateOutcomeData(deviation);
        validateDataQualityScore(deviation);
    }
    
    private void validateResolutionData(HistoricalDeviation deviation) {
        if (deviation.getResolutionDate() != null) {
            if (deviation.getResolutionDate().before(deviation.getOccurrenceDate())) {
                throw new DataQualityException("Resolution date cannot be before occurrence date");
            }
            
            // Resolution should have effectiveness rating
            if (deviation.getResolutionEffectiveness() == null) {
                throw new DataQualityException("Resolution effectiveness is required when resolution date is provided");
            }
        }
    }
    
    private void validateOutcomeData(HistoricalDeviation deviation) {
        // If corrective actions are provided, they should be valid JSON
        if (deviation.getCorrectiveActions() != null) {
            try {
                ObjectMapper mapper = new ObjectMapper();
                JsonNode actionsNode = mapper.readTree(deviation.getCorrectiveActions());
                
                if (!actionsNode.isArray() || actionsNode.size() == 0) {
                    throw new DataQualityException("Corrective actions must be a non-empty array");
                }
                
            } catch (JsonProcessingException e) {
                throw new DataQualityException("Invalid corrective actions JSON format");
            }
        }
        
        // Cost impact should be reasonable
        if (deviation.getCostImpact() != null) {
            if (deviation.getCostImpact().compareTo(BigDecimal.ZERO) < 0) {
                throw new DataQualityException("Cost impact cannot be negative");
            }
            
            if (deviation.getCostImpact().compareTo(new BigDecimal("10000000")) > 0) {
                // Log warning for very high cost impact
            }
        }
    }
    
    private void validateDataQualityScore(HistoricalDeviation deviation) {
        if (deviation.getDataQualityScore() == null) {
            throw new DataQualityException("Data quality score is required");
        }
        
        if (deviation.getDataQualityScore() < 0.0 || deviation.getDataQualityScore() > 1.0) {
            throw new DataQualityException("Data quality score must be between 0.0 and 1.0");
        }
        
        if (deviation.getDataQualityScore() < MIN_DATA_QUALITY_SCORE && deviation.getIsTrainingData()) {
            throw new DataQualityException("Training data quality score too low: " + deviation.getDataQualityScore());
        }
    }
    
    public void validateTrainingDataset(List<HistoricalDeviation> trainingData) {
        if (trainingData.size() < MIN_TRAINING_SAMPLES) {
            throw new DataQualityException("Insufficient training samples: " + trainingData.size() + " (minimum: " + MIN_TRAINING_SAMPLES + ")");
        }
        
        // Check data distribution
        Map<EventType, Long> eventTypeDistribution = trainingData.stream()
            .collect(Collectors.groupingBy(HistoricalDeviation::getEventType, Collectors.counting()));
        
        // Ensure no event type has less than 10% of total data
        long minSamplesPerType = trainingData.size() / 10;
        for (Map.Entry<EventType, Long> entry : eventTypeDistribution.entrySet()) {
            if (entry.getValue() < minSamplesPerType) {
                throw new DataQualityException("Insufficient samples for event type " + entry.getKey() + ": " + entry.getValue());
            }
        }
        
        // Check outcome distribution
        long resolvedCount = trainingData.stream()
            .filter(d -> d.getResolutionDate() != null)
            .count();
        
        double resolvedPercentage = (double) resolvedCount / trainingData.size();
        if (resolvedPercentage < 0.5) {
            throw new DataQualityException("Too few resolved deviations in training data: " + resolvedPercentage);
        }
    }
    
    public void validateModelPerformance(ModelPerformanceMetrics performance) {
        if (performance.getAccuracyScore() == null || performance.getAccuracyScore() < MIN_MODEL_ACCURACY) {
            throw new ModelTrainingException("Model accuracy too low: " + performance.getAccuracyScore() + " (minimum: " + MIN_MODEL_ACCURACY + ")");
        }
        
        if (performance.getPrecisionScore() == null || performance.getPrecisionScore() < 0.7) {
            throw new ModelTrainingException("Model precision too low: " + performance.getPrecisionScore());
        }
        
        if (performance.getRecallScore() == null || performance.getRecallScore() < 0.7) {
            throw new ModelTrainingException("Model recall too low: " + performance.getRecallScore());
        }
        
        // Check for overfitting
        if (performance.getTrainingAccuracy() != null && performance.getValidationAccuracy() != null) {
            double accuracyGap = performance.getTrainingAccuracy() - performance.getValidationAccuracy();
            if (accuracyGap > 0.1) {
                throw new ModelTrainingException("Model may be overfitting - accuracy gap: " + accuracyGap);
            }
        }
    }
    
    public void validateSimilarityResults(List<SimilarDeviationResult> results, double threshold) {
        for (SimilarDeviationResult result : results) {
            if (result.getSimilarityScore() < threshold) {
                throw new InvalidLearningRequestException("Similarity result below threshold: " + result.getSimilarityScore());
            }
            
            if (result.getSimilarityScore() < 0.0 || result.getSimilarityScore() > 1.0) {
                throw new InvalidLearningRequestException("Invalid similarity score: " + result.getSimilarityScore());
            }
        }
        
        // Validate ordering (should be descending by similarity score)
        for (int i = 1; i < results.size(); i++) {
            if (results.get(i).getSimilarityScore() > results.get(i-1).getSimilarityScore()) {
                throw new InvalidLearningRequestException("Similarity results not properly ordered");
            }
        }
    }
}
```

### 2.10 Service Integrations

```java
@Service
public class MachineLearningEngineImpl implements MachineLearningEngine {
    
    @Value("${ml.python.service.url}")
    private String mlServiceUrl;
    
    @Value("${ml.model.storage.path}")
    private String modelStoragePath;
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Override
    public LearningModel trainSimilarityModel(List<HistoricalDeviation> trainingData) {
        try {
            // Prepare training data for ML service
            MLTrainingRequest request = new MLTrainingRequest();
            request.setModelType("similarity_matching");
            request.setTrainingData(convertToMLFormat(trainingData));
            request.setHyperparameters(getDefaultSimilarityParameters());
            
            // Call Python ML service
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<MLTrainingRequest> entity = new HttpEntity<>(request, headers);
            
            ResponseEntity<MLTrainingResponse> response = restTemplate.postForEntity(
                mlServiceUrl + "/train/similarity", entity, MLTrainingResponse.class
            );
            
            MLTrainingResponse mlResponse = response.getBody();
            if (mlResponse == null || !mlResponse.isSuccess()) {
                throw new ModelTrainingException("ML service training failed: " + mlResponse.getErrorMessage());
            }
            
            // Create learning model entity
            LearningModel model = new LearningModel();
            model.setModelId(generateModelId());
            model.setModelName("Similarity Matching Model");
            model.setModelType(ModelType.SIMILARITY_MATCHING);
            model.setModelParameters(objectMapper.writeValueAsString(request.getHyperparameters()));
            model.setTrainingDataSize(trainingData.size());
            model.setAccuracyScore(mlResponse.getMetrics().getAccuracy());
            model.setPrecisionScore(mlResponse.getMetrics().getPrecision());
            model.setRecallScore(mlResponse.getMetrics().getRecall());
            model.setF1Score(mlResponse.getMetrics().getF1Score());
            model.setTrainedAt(new Date());
            model.setVersion(generateModelVersion());
            model.setIsActive(false);
            model.setModelArtifactPath(mlResponse.getModelPath());
            
            return model;
            
        } catch (Exception e) {
            throw new ModelTrainingException("Failed to train similarity model: " + e.getMessage());
        }
    }
    
    @Override
    public List<LearningRecommendation> generateLearningRecommendations(
            FeatureVector currentFeatures, 
            List<SimilarDeviationResult> similarDeviations, 
            PatternInsights patterns) {
        
        try {
            // Prepare recommendation request
            RecommendationRequest request = new RecommendationRequest();
            request.setCurrentFeatures(currentFeatures);
            request.setSimilarDeviations(similarDeviations);
            request.setPatternInsights(patterns);
            
            // Call ML service for recommendations
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<RecommendationRequest> entity = new HttpEntity<>(request, headers);
            
            ResponseEntity<RecommendationResponse> response = restTemplate.postForEntity(
                mlServiceUrl + "/recommend", entity, RecommendationResponse.class
            );
            
            RecommendationResponse mlResponse = response.getBody();
            if (mlResponse == null || !mlResponse.isSuccess()) {
                throw new LearningEngineUnavailableException("ML recommendation service failed: " + mlResponse.getErrorMessage());
            }
            
            return mlResponse.getRecommendations();
            
        } catch (Exception e) {
            throw new LearningEngineUnavailableException("Failed to generate learning recommendations: " + e.getMessage());
        }
    }
    
    @Override
    public ModelPerformanceMetrics evaluateModel(LearningModel model, List<HistoricalDeviation> testData) {
        try {
            // Prepare evaluation request
            ModelEvaluationRequest request = new ModelEvaluationRequest();
            request.setModelPath(model.getModelArtifactPath());
            request.setModelType(model.getModelType().name());
            request.setTestData(convertToMLFormat(testData));
            
            // Call ML service for evaluation
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<ModelEvaluationRequest> entity = new HttpEntity<>(request, headers);
            
            ResponseEntity<ModelEvaluationResponse> response = restTemplate.postForEntity(
                mlServiceUrl + "/evaluate", entity, ModelEvaluationResponse.class
            );
            
            ModelEvaluationResponse mlResponse = response.getBody();
            if (mlResponse == null || !mlResponse.isSuccess()) {
                throw new ModelTrainingException("Model evaluation failed: " + mlResponse.getErrorMessage());
            }
            
            // Convert to internal metrics format
            ModelPerformanceMetrics metrics = new ModelPerformanceMetrics();
            metrics.setAccuracyScore(mlResponse.getMetrics().getAccuracy());
            metrics.setPrecisionScore(mlResponse.getMetrics().getPrecision());
            metrics.setRecallScore(mlResponse.getMetrics().getRecall());
            metrics.setF1Score(mlResponse.getMetrics().getF1Score());
            metrics.setConfusionMatrix(mlResponse.getMetrics().getConfusionMatrix());
            metrics.setEvaluationTimestamp(new Date());
            
            return metrics;
            
        } catch (Exception e) {
            throw new ModelTrainingException("Failed to evaluate model: " + e.getMessage());
        }
    }
    
    @Scheduled(cron = "0 0 2 * * SUN") // Weekly on Sunday at 2 AM
    public void performWeeklyModelRetraining() {
        try {
            // Get recent training data
            Date oneWeekAgo = Date.from(Instant.now().minus(7, ChronoUnit.DAYS));
            List<HistoricalDeviation> recentData = deviationRepository.findByOccurrenceDateAfterAndIsTrainingDataTrue(oneWeekAgo);
            
            if (recentData.size() >= MIN_TRAINING_SAMPLES) {
                // Retrain similarity model
                LearningModel newSimilarityModel = trainSimilarityModel(recentData);
                
                // Evaluate against existing model
                LearningModel currentModel = modelRepository.findByModelTypeAndIsActiveTrue(ModelType.SIMILARITY_MATCHING);
                if (currentModel != null) {
                    ModelPerformanceMetrics newPerformance = evaluateModel(newSimilarityModel, recentData);
                    ModelPerformanceMetrics currentPerformance = evaluateModel(currentModel, recentData);
                    
                    // Activate new model if it performs better
                    if (newPerformance.getF1Score() > currentPerformance.getF1Score()) {
                        currentModel.setIsActive(false);
                        newSimilarityModel.setIsActive(true);
                        
                        modelRepository.save(currentModel);
                        modelRepository.save(newSimilarityModel);
                        
                        // Log model update
                        logger.info("Activated new similarity model - Old F1: {}, New F1: {}", 
                            currentPerformance.getF1Score(), newPerformance.getF1Score());
                    }
                }
            }
            
        } catch (Exception e) {
            logger.error("Weekly model retraining failed", e);
        }
    }
    
    private List<MLTrainingData> convertToMLFormat(List<HistoricalDeviation> deviations) {
        return deviations.stream()
            .map(this::convertDeviationToMLData)
            .collect(Collectors.toList());
    }
    
    private MLTrainingData convertDeviationToMLData(HistoricalDeviation deviation) {
        MLTrainingData data = new MLTrainingData();
        data.setDeviationId(deviation.getDeviationId());
        data.setFeatures(featureExtractor.extractFeatures(deviation));
        data.setLabel(createLabel(deviation));
        return data;
    }
    
    private String createLabel(HistoricalDeviation deviation) {
        // Create label based on resolution effectiveness
        if (deviation.getResolutionEffectiveness() != null) {
            return deviation.getResolutionEffectiveness().name();
        }
        return "UNKNOWN";
    }
    
    private Map<String, Object> getDefaultSimilarityParameters() {
        Map<String, Object> params = new HashMap<>();
        params.put("algorithm", "cosine_similarity");
        params.put("dimensionality", 128);
        params.put("learning_rate", 0.001);
        params.put("batch_size", 32);
        params.put("epochs", 100);
        params.put("early_stopping", true);
        params.put("patience", 10);
        return params;
    }
    
    private String generateModelId() {
        return "MODEL-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 8);
    }
    
    private String generateModelVersion() {
        return "v" + new SimpleDateFormat("yyyyMMdd.HHmmss").format(new Date());
    }
}
```

---

## 3. Frontend React Details

### 3.1 UI Architecture

```jsx
// Historical Learning Dashboard Component
import React, { useState, useEffect } from 'react';
import { SimilarityAnalysis } from './SimilarityAnalysis';
import { PatternInsights } from './PatternInsights';
import { ModelPerformance } from './ModelPerformance';
import { LearningTrends } from './LearningTrends';
import { OutcomeFeedback } from './OutcomeFeedback';

const HistoricalLearningDashboard = () => {
    const [activeTab, setActiveTab] = useState('similarity');
    const [similarityResults, setSimilarityResults] = useState(null);
    const [patternInsights, setPatternInsights] = useState(null);
    const [modelPerformance, setModelPerformance] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadModelPerformance();
    }, []);

    const loadModelPerformance = async () => {
        try {
            const response = await fetch('/api/v1/historical-learning/models/current/performance');
            const performance = await response.json();
            setModelPerformance(performance);
        } catch (err) {
            console.error('Failed to load model performance:', err);
        }
    };

    return (
        <div className="historical-learning-dashboard">
            <header className="dashboard-header">
                <h1>Historical Deviation Learning System</h1>
                <div className="dashboard-metrics">
                    <div className="metric-card">
                        <span className="metric-value">
                            {modelPerformance ? (modelPerformance.accuracyScore * 100).toFixed(1) + '%' : 'N/A'}
                        </span>
                        <span className="metric-label">Model Accuracy</span>
                    </div>
                    <div className="metric-card">
                        <span className="metric-value">
                            {similarityResults ? similarityResults.similarDeviations.length : 0}
                        </span>
                        <span className="metric-label">Similar Cases Found</span>
                    </div>
                    <div className="metric-card">
                        <span className="metric-value">
                            {patternInsights ? patternInsights.patterns.length : 0}
                        </span>
                        <span className="metric-label">Patterns Identified</span>
                    </div>
                </div>
            </header>

            <nav className="dashboard-nav">
                <button 
                    className={activeTab === 'similarity' ? 'active' : ''}
                    onClick={() => setActiveTab('similarity')}
                >
                    Similarity Analysis
                </button>
                <button 
                    className={activeTab === 'patterns' ? 'active' : ''}
                    onClick={() => setActiveTab('patterns')}
                >
                    Pattern Insights
                </button>
                <button 
                    className={activeTab === 'performance' ? 'active' : ''}
                    onClick={() => setActiveTab('performance')}
                >
                    Model Performance
                </button>
                <button 
                    className={activeTab === 'trends' ? 'active' : ''}
                    onClick={() => setActiveTab('trends')}
                >
                    Learning Trends
                </button>
                <button 
                    className={activeTab === 'feedback' ? 'active' : ''}
                    onClick={() => setActiveTab('feedback')}
                >
                    Outcome Feedback
                </button>
            </nav>

            <div className="dashboard-content">
                {error && (
                    <div className="error-alert">
                        <strong>Error:</strong> {error}
                        <button onClick={() => setError(null)}>×</button>
                    </div>
                )}

                {activeTab === 'similarity' && (
                    <SimilarityAnalysis 
                        onAnalysisComplete={setSimilarityResults}
                        onPatternInsights={setPatternInsights}
                        loading={loading}
                        setLoading={setLoading}
                        setError={setError}
                    />
                )}

                {activeTab === 'patterns' && (
                    <PatternInsights 
                        insights={patternInsights}
                        onRefresh={() => {/* Refresh patterns */}}
                    />
                )}

                {activeTab === 'performance' && (
                    <ModelPerformance 
                        performance={modelPerformance}
                        onRefresh={loadModelPerformance}
                    />
                )}

                {activeTab === 'trends' && (
                    <LearningTrends />
                )}

                {activeTab === 'feedback' && (
                    <OutcomeFeedback 
                        onFeedbackSubmitted={() => {/* Handle feedback */}}
                    />
                )}
            </div>
        </div>
    );
};
```

### 3.2 UI Specifications

```jsx
// Similarity Analysis Component
import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const SimilarityAnalysis = ({ onAnalysisComplete, onPatternInsights, loading, setLoading, setError }) => {
    const validationSchema = Yup.object({
        currentEventId: Yup.string()
            .matches(/^[A-Z]{2,3}\d{6,10}$/, 'Invalid event ID format')
            .required('Current event ID is required'),
        eventDescription: Yup.string()
            .min(10, 'Description must be at least 10 characters')
            .max(5000, 'Description must be less than 5000 characters')
            .required('Event description is required'),
        eventType: Yup.string()
            .oneOf(['DEVIATION', 'CAPA', 'CHANGE_CONTROL', 'INCIDENT', 'COMPLAINT', 'OOS', 'OOT', 'INVESTIGATION'])
            .required('Event type is required'),
        maxSimilarEvents: Yup.number()
            .min(1, 'Must be at least 1')
            .max(50, 'Cannot exceed 50'),
        similarityThreshold: Yup.number()
            .min(0.1, 'Must be at least 0.1')
            .max(1.0, 'Cannot exceed 1.0')
    });

    const handleSubmit = async (values, { setSubmitting }) => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await fetch('/api/v1/historical-learning/analyze-similarity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                },
                body: JSON.stringify({
                    ...values,
                    maxSimilarEvents: values.maxSimilarEvents || 20,
                    similarityThreshold: values.similarityThreshold || 0.6,
                    includeOutcomes: true
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            onAnalysisComplete(result);
            onPatternInsights(result.patternInsights);
            
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
            setSubmitting(false);
        }
    };

    return (
        <div className="similarity-analysis">
            <h2>Historical Similarity Analysis</h2>
            <p className="analysis-description">
                Analyze current events against historical deviations to identify similar cases and learn from past outcomes.
            </p>
            
            <Formik
                initialValues={{
                    currentEventId: '',
                    eventDescription: '',
                    eventType: '',
                    productLine: '',
                    processArea: '',
                    severityLevel: '',
                    maxSimilarEvents: 20,
                    similarityThreshold: 0.6
                }}
                validationSchema={validationSchema}
                onSubmit={handleSubmit}
            >
                {({ isSubmitting, values }) => (
                    <Form className="analysis-form">
                        <div className="form-section">
                            <h3>Current Event Information</h3>
                            
                            <div className="form-row">
                                <div className="form-group col-md-6">
                                    <label htmlFor="currentEventId">Current Event ID *</label>
                                    <Field 
                                        type="text" 
                                        name="currentEventId" 
                                        placeholder="e.g., DEV123456"
                                        className="form-control"
                                    />
                                    <ErrorMessage name="currentEventId" component="div" className="error-message" />
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
                                        <option value="INVESTIGATION">Investigation</option>
                                    </Field>
                                    <ErrorMessage name="eventType" component="div" className="error-message" />
                                </div>
                            </div>

                            <div className="form-group">
                                <label htmlFor="eventDescription">Event Description *</label>
                                <Field 
                                    as="textarea" 
                                    name="eventDescription" 
                                    rows="4"
                                    placeholder="Provide detailed description of the current event..."
                                    className="form-control"
                                />
                                <div className="character-count">
                                    {values.eventDescription.length}/5000 characters
                                </div>
                                <ErrorMessage name="eventDescription" component="div" className="error-message" />
                            </div>
                        </div>

                        <div className="form-section">
                            <h3>Context Information</h3>
                            
                            <div className="form-row">
                                <div className="form-group col-md-4">
                                    <label htmlFor="productLine">Product Line</label>
                                    <Field 
                                        type="text" 
                                        name="productLine" 
                                        placeholder="e.g., Pharmaceuticals"
                                        className="form-control"
                                    />
                                </div>

                                <div className="form-group col-md-4">
                                    <label htmlFor="processArea">Process Area</label>
                                    <Field 
                                        type="text" 
                                        name="processArea" 
                                        placeholder="e.g., Manufacturing"
                                        className="form-control"
                                    />
                                </div>

                                <div className="form-group col-md-4">
                                    <label htmlFor="severityLevel">Severity Level</label>
                                    <Field as="select" name="severityLevel" className="form-control">
                                        <option value="">Select Severity</option>
                                        <option value="CRITICAL">Critical</option>
                                        <option value="MAJOR">Major</option>
                                        <option value="MINOR">Minor</option>
                                        <option value="NEGLIGIBLE">Negligible</option>
                                    </Field>
                                </div>
                            </div>
                        </div>

                        <div className="form-section">
                            <h3>Analysis Parameters</h3>
                            
                            <div className="form-row">
                                <div className="form-group col-md-6">
                                    <label htmlFor="maxSimilarEvents">Max Similar Events</label>
                                    <Field 
                                        type="number" 
                                        name="maxSimilarEvents" 
                                        min="1" 
                                        max="50"
                                        className="form-control"
                                    />
                                    <small className="form-text">Maximum number of similar events to return</small>
                                    <ErrorMessage name="maxSimilarEvents" component="div" className="error-message" />
                                </div>

                                <div className="form-group col-md-6">
                                    <label htmlFor="similarityThreshold">Similarity Threshold</label>
                                    <Field 
                                        type="number" 
                                        name="similarityThreshold" 
                                        min="0.1" 
                                        max="1.0" 
                                        step="0.1"
                                        className="form-control"
                                    />
                                    <small className="form-text">Minimum similarity score (0.1 - 1.0)</small>
                                    <ErrorMessage name="similarityThreshold" component="div" className="error-message" />
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
                                        Analyzing Similarity...
                                    </>
                                ) : (
                                    'Analyze Historical Similarity'
                                )}
                            </button>
                        </div>
                    </Form>
                )}
            </Formik>
        </div>
    );
};

// Similar Deviations Results Component
const SimilarDeviationsResults = ({ results }) => {
    if (!results || !results.similarDeviations || results.similarDeviations.length === 0) {
        return (
            <div className="no-results">
                <p>No similar deviations found. Try adjusting the similarity threshold or search parameters.</p>
            </div>
        );
    }

    return (
        <div className="similar-deviations-results">
            <h3>Similar Historical Deviations</h3>
            <div className="results-summary">
                <p>Found {results.similarDeviations.length} similar deviations with confidence score: 
                   <span className={`confidence-score ${getConfidenceClass(results.confidenceScore)}`}>
                       {(results.confidenceScore * 100).toFixed(1)}%
                   </span>
                </p>
            </div>

            <div className="deviations-list">
                {results.similarDeviations.map((deviation, index) => (
                    <div key={deviation.deviationId} className="deviation-card">
                        <div className="deviation-header">
                            <h4>#{index + 1} - {deviation.deviationId}</h4>
                            <div className="similarity-badge">
                                {(deviation.similarityScore * 100).toFixed(1)}% similar
                            </div>
                        </div>

                        <div className="deviation-content">
                            <div className="deviation-info">
                                <div className="info-row">
                                    <span className="label">Type:</span>
                                    <span className="value">{deviation.eventType}</span>
                                </div>
                                <div className="info-row">
                                    <span className="label">Severity:</span>
                                    <span className={`value severity-${deviation.severityLevel.toLowerCase()}`}>
                                        {deviation.severityLevel}
                                    </span>
                                </div>
                                <div className="info-row">
                                    <span className="label">Occurred:</span>
                                    <span className="value">{new Date(deviation.occurrenceDate).toLocaleDateString()}</span>
                                </div>
                                <div className="info-row">
                                    <span className="label">Resolution:</span>
                                    <span className={`value effectiveness-${deviation.resolutionEffectiveness?.toLowerCase()}`}>
                                        {deviation.resolutionEffectiveness || 'Unknown'}
                                    </span>
                                </div>
                            </div>

                            <div className="deviation-description">
                                <h5>Description:</h5>
                                <p>{deviation.description}</p>
                            </div>

                            {deviation.rootCause && (
                                <div className="root-cause">
                                    <h5>Root Cause:</h5>
                                    <p>{deviation.rootCause}</p>
                                </div>
                            )}

                            {deviation.correctiveActions && deviation.correctiveActions.length > 0 && (
                                <div className="corrective-actions">
                                    <h5>Corrective Actions:</h5>
                                    <ul>
                                        {deviation.correctiveActions.map((action, actionIndex) => (
                                            <li key={actionIndex}>{action}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {deviation.daysToresolve && (
                                <div className="resolution-time">
                                    <span className="label">Resolution Time:</span>
                                    <span className="value">{deviation.daysToresolve} days</span>
                                </div>
                            )}

                            {deviation.costImpact && (
                                <div className="cost-impact">
                                    <span className="label">Cost Impact:</span>
                                    <span className="value">${deviation.costImpact.toLocaleString()}</span>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {results.learningRecommendations && results.learningRecommendations.length > 0 && (
                <div className="learning-recommendations">
                    <h3>Learning-Based Recommendations</h3>
                    <div className="recommendations-list">
                        {results.learningRecommendations.map((recommendation, index) => (
                            <div key={index} className="recommendation-card">
                                <h4>{recommendation.title}</h4>
                                <p>{recommendation.description}</p>
                                <div className="recommendation-meta">
                                    <span className="confidence">Confidence: {(recommendation.confidence * 100).toFixed(1)}%</span>
                                    <span className="based-on">Based on {recommendation.basedOnCount} similar cases</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

const getConfidenceClass = (score) => {
    if (score >= 0.8) return 'high-confidence';
    if (score >= 0.6) return 'medium-confidence';
    return 'low-confidence';
};
```

### 3.3 API Integration

```jsx
// Historical Learning API Service
class HistoricalLearningAPI {
    constructor() {
        this.baseURL = process.env.REACT_APP_API_BASE_URL || '/api/v1';
        this.timeout = 30000; // 30 seconds for ML operations
    }

    async analyzeSimilarity(analysisRequest) {
        const response = await this.makeRequest('/historical-learning/analyze-similarity', {
            method: 'POST',
            body: JSON.stringify(analysisRequest)
        });
        return response;
    }

    async learnFromOutcome(outcomeRequest) {
        const response = await this.makeRequest('/historical-learning/learn-from-outcome', {
            method: 'POST',
            body: JSON.stringify(outcomeRequest)
        });
        return response;
    }

    async getPatterns(eventType, daysPeriod = 365, productLine = null) {
        const queryParams = new URLSearchParams({ daysPeriod: daysPeriod.toString() });
        if (productLine) queryParams.append('productLine', productLine);
        
        const response = await this.makeRequest(`/historical-learning/patterns/${eventType}?${queryParams}`, {
            method: 'GET'
        });
        return response;
    }

    async trainModel(trainingRequest) {
        const response = await this.makeRequest('/historical-learning/models/train', {
            method: 'POST',
            body: JSON.stringify(trainingRequest)
        });
        return response;
    }

    async getModelPerformance(modelId, evaluationDays = 30) {
        const queryParams = new URLSearchParams({ evaluationDays: evaluationDays.toString() });
        const response = await this.makeRequest(`/historical-learning/models/${modelId}/performance?${queryParams}`, {
            method: 'GET'
        });
        return response;
    }

    async submitRecommendationFeedback(feedback) {
        const response = await this.makeRequest('/historical-learning/recommendations/feedback', {
            method: 'POST',
            body: JSON.stringify(feedback)
        });
        return response;
    }

    async getTrendInsights(daysPeriod = 90, eventType = null, productLine = null) {
        const queryParams = new URLSearchParams({ daysPeriod: daysPeriod.toString() });
        if (eventType) queryParams.append('eventType', eventType);
        if (productLine) queryParams.append('productLine', productLine);
        
        const response = await this.makeRequest(`/historical-learning/insights/trends?${queryParams}`, {
            method: 'GET'
        });
        return response;
    }

    async validateDataQuality(validationRequest) {
        const response = await this.makeRequest('/historical-learning/data-quality/validate', {
            method: 'POST',
            body: JSON.stringify(validationRequest)
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
                throw new Error('Request timeout - ML analysis taking longer than expected');
            }
            throw error;
        }
    }

    getAuthToken() {
        return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
    }
}

export default new HistoricalLearningAPI();
```

---

## 4. Database Details

### 4.1 ER Diagram

```mermaid
erDiagram
    HISTORICAL_DEVIATIONS {
        BIGINT id PK
        VARCHAR deviation_id UK
        ENUM event_type
        TEXT description
        TEXT root_cause
        JSON corrective_actions
        JSON preventive_actions
        ENUM severity_level
        ENUM gxp_classification
        VARCHAR product_line
        VARCHAR process_area
        VARCHAR equipment_involved
        TIMESTAMP occurrence_date
        TIMESTAMP resolution_date
        ENUM resolution_effectiveness
        INTEGER recurrence_count
        DECIMAL cost_impact
        VARCHAR regulatory_impact
        JSON feature_vector
        VARCHAR similarity_hash
        DECIMAL data_quality_score
        BOOLEAN is_training_data
    }
    
    LEARNING_MODELS {
        BIGINT id PK
        VARCHAR model_id UK
        VARCHAR model_name
        ENUM model_type
        JSON model_parameters
        INTEGER training_data_size
        DECIMAL accuracy_score
        DECIMAL precision_score
        DECIMAL recall_score
        DECIMAL f1_score
        TIMESTAMP trained_at
        VARCHAR version
        BOOLEAN is_active
        VARCHAR model_artifact_path
    }
    
    SIMILARITY_ANALYSES {
        BIGINT id PK
        VARCHAR analysis_id UK
        VARCHAR current_event_id
        JSON current_features
        JSON similar_deviations
        JSON pattern_insights
        JSON learning_recommendations
        DECIMAL confidence_score
        TIMESTAMP analysis_timestamp
        BIGINT processing_time_ms
    }
    
    OUTCOME_LEARNING {
        BIGINT id PK
        VARCHAR learning_id UK
        VARCHAR deviation_id FK
        ENUM actual_outcome
        ENUM predicted_outcome
        DECIMAL prediction_confidence
        JSON feedback_data
        TIMESTAMP outcome_date
        VARCHAR feedback_source
        BOOLEAN model_updated
    }
    
    PATTERN_INSIGHTS {
        BIGINT id PK
        VARCHAR pattern_id UK
        VARCHAR pattern_name
        ENUM event_type
        VARCHAR product_line
        JSON pattern_characteristics
        INTEGER occurrence_frequency
        DECIMAL success_rate
        JSON recommended_actions
        TIMESTAMP identified_at
        TIMESTAMP last_updated
        BOOLEAN is_active
    }
    
    MODEL_PERFORMANCE_HISTORY {
        BIGINT id PK
        VARCHAR performance_id UK
        VARCHAR model_id FK
        DECIMAL accuracy_score
        DECIMAL precision_score
        DECIMAL recall_score
        DECIMAL f1_score
        JSON confusion_matrix
        INTEGER evaluation_samples
        TIMESTAMP evaluation_date
        VARCHAR evaluation_dataset
    }
    
    HISTORICAL_DEVIATIONS ||--o{ SIMILARITY_ANALYSES : "analyzed_in"
    HISTORICAL_DEVIATIONS ||--o{ OUTCOME_LEARNING : "learns_from"
    LEARNING_MODELS ||--o{ MODEL_PERFORMANCE_HISTORY : "has_performance"
    LEARNING_MODELS ||--o{ SIMILARITY_ANALYSES : "generates"
    PATTERN_INSIGHTS ||--o{ SIMILARITY_ANALYSES : "provides"
```

### 4.2 Database Validations

```sql
-- Historical Deviations Table
CREATE TABLE historical_deviations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    deviation_id VARCHAR(100) NOT NULL UNIQUE,
    event_type ENUM('DEVIATION', 'CAPA', 'CHANGE_CONTROL', 'INCIDENT', 'COMPLAINT', 'OOS', 'OOT', 'INVESTIGATION') NOT NULL,
    description TEXT NOT NULL,
    root_cause TEXT,
    corrective_actions JSON,
    preventive_actions JSON,
    severity_level ENUM('CRITICAL', 'MAJOR', 'MINOR', 'NEGLIGIBLE') NOT NULL,
    gxp_classification ENUM('GXP', 'NON_GXP') NOT NULL,
    product_line VARCHAR(100),
    process_area VARCHAR(100),
    equipment_involved VARCHAR(200),
    occurrence_date TIMESTAMP NOT NULL,
    resolution_date TIMESTAMP,
    resolution_effectiveness ENUM('HIGHLY_EFFECTIVE', 'EFFECTIVE', 'PARTIALLY_EFFECTIVE', 'INEFFECTIVE', 'UNKNOWN'),
    recurrence_count INTEGER DEFAULT 0 CHECK (recurrence_count >= 0),
    cost_impact DECIMAL(15,2) CHECK (cost_impact >= 0),
    regulatory_impact VARCHAR(500),
    feature_vector JSON,
    similarity_hash VARCHAR(32),
    data_quality_score DECIMAL(4,3) NOT NULL CHECK (data_quality_score >= 0.000 AND data_quality_score <= 1.000),
    is_training_data BOOLEAN NOT NULL DEFAULT TRUE,
    INDEX idx_deviation_id (deviation_id),
    INDEX idx_event_type (event_type),
    INDEX idx_severity_level (severity_level),
    INDEX idx_gxp_classification (gxp_classification),
    INDEX idx_product_line (product_line),
    INDEX idx_process_area (process_area),
    INDEX idx_occurrence_date (occurrence_date),
    INDEX idx_resolution_date (resolution_date),
    INDEX idx_similarity_hash (similarity_hash),
    INDEX idx_data_quality_score (data_quality_score),
    INDEX idx_is_training_data (is_training_data),
    FULLTEXT idx_description (description, root_cause),
    CONSTRAINT chk_resolution_date CHECK (resolution_date IS NULL OR resolution_date >= occurrence_date)
);

-- Learning Models Table
CREATE TABLE learning_models (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    model_id VARCHAR(100) NOT NULL UNIQUE,
    model_name VARCHAR(200) NOT NULL,
    model_type ENUM('SIMILARITY_MATCHING', 'CLASSIFICATION', 'RECOMMENDATION', 'PATTERN_RECOGNITION') NOT NULL,
    model_parameters JSON,
    training_data_size INTEGER CHECK (training_data_size > 0),
    accuracy_score DECIMAL(5,4) CHECK (accuracy_score >= 0.0000 AND accuracy_score <= 1.0000),
    precision_score DECIMAL(5,4) CHECK (precision_score >= 0.0000 AND precision_score <= 1.0000),
    recall_score DECIMAL(5,4) CHECK (recall_score >= 0.0000 AND recall_score <= 1.0000),
    f1_score DECIMAL(5,4) CHECK (f1_score >= 0.0000 AND f1_score <= 1.0000),
    trained_at TIMESTAMP NOT NULL,
    version VARCHAR(20) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    model_artifact_path VARCHAR(500),
    INDEX idx_model_id (model_id),
    INDEX idx_model_type (model_type),
    INDEX idx_is_active (is_active),
    INDEX idx_trained_at (trained_at),
    INDEX idx_accuracy_score (accuracy_score),
    UNIQUE KEY uk_active_model_type (model_type, is_active) -- Only one active model per type
);

-- Similarity Analyses Table
CREATE TABLE similarity_analyses (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    analysis_id VARCHAR(100) NOT NULL UNIQUE,
    current_event_id VARCHAR(100) NOT NULL,
    current_features JSON NOT NULL,
    similar_deviations JSON,
    pattern_insights JSON,
    learning_recommendations JSON,
    confidence_score DECIMAL(4,3) CHECK (confidence_score >= 0.000 AND confidence_score <= 1.000),
    analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_time_ms BIGINT CHECK (processing_time_ms >= 0),
    INDEX idx_analysis_id (analysis_id),
    INDEX idx_current_event_id (current_event_id),
    INDEX idx_analysis_timestamp (analysis_timestamp),
    INDEX idx_confidence_score (confidence_score)
);

-- Outcome Learning Table
CREATE TABLE outcome_learning (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    learning_id VARCHAR(100) NOT NULL UNIQUE,
    deviation_id VARCHAR(100) NOT NULL,
    actual_outcome ENUM('HIGHLY_EFFECTIVE', 'EFFECTIVE', 'PARTIALLY_EFFECTIVE', 'INEFFECTIVE') NOT NULL,
    predicted_outcome ENUM('HIGHLY_EFFECTIVE', 'EFFECTIVE', 'PARTIALLY_EFFECTIVE', 'INEFFECTIVE'),
    prediction_confidence DECIMAL(4,3) CHECK (prediction_confidence >= 0.000 AND prediction_confidence <= 1.000),
    feedback_data JSON,
    outcome_date TIMESTAMP NOT NULL,
    feedback_source VARCHAR(100),
    model_updated BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (deviation_id) REFERENCES historical_deviations(deviation_id) ON DELETE CASCADE,
    INDEX idx_learning_id (learning_id),
    INDEX idx_deviation_id (deviation_id),
    INDEX idx_actual_outcome (actual_outcome),
    INDEX idx_outcome_date (outcome_date),
    INDEX idx_model_updated (model_updated)
);

-- Pattern Insights Table
CREATE TABLE pattern_insights (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    pattern_id VARCHAR(100) NOT NULL UNIQUE,
    pattern_name VARCHAR(200) NOT NULL,
    event_type ENUM('DEVIATION', 'CAPA', 'CHANGE_CONTROL', 'INCIDENT', 'COMPLAINT', 'OOS', 'OOT', 'INVESTIGATION'),
    product_line VARCHAR(100),
    pattern_characteristics JSON NOT NULL,
    occurrence_frequency INTEGER NOT NULL CHECK (occurrence_frequency > 0),
    success_rate DECIMAL(4,3) NOT NULL CHECK (success_rate >= 0.000 AND success_rate <= 1.000),
    recommended_actions JSON,
    identified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    INDEX idx_pattern_id (pattern_id),
    INDEX idx_event_type (event_type),
    INDEX idx_product_line (product_line),
    INDEX idx_success_rate (success_rate),
    INDEX idx_identified_at (identified_at),
    INDEX idx_is_active (is_active)
);

-- Model Performance History Table
CREATE TABLE model_performance_history (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    performance_id VARCHAR(100) NOT NULL UNIQUE,
    model_id VARCHAR(100) NOT NULL,
    accuracy_score DECIMAL(5,4) NOT NULL CHECK (accuracy_score >= 0.0000 AND accuracy_score <= 1.0000),
    precision_score DECIMAL(5,4) NOT NULL CHECK (precision_score >= 0.0000 AND precision_score <= 1.0000),
    recall_score DECIMAL(5,4) NOT NULL CHECK (recall_score >= 0.0000 AND recall_score <= 1.0000),
    f1_score DECIMAL(5,4) NOT NULL CHECK (f1_score >= 0.0000 AND f1_score <= 1.0000),
    confusion_matrix JSON,
    evaluation_samples INTEGER NOT NULL CHECK (evaluation_samples > 0),
    evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    evaluation_dataset VARCHAR(100),
    FOREIGN KEY (model_id) REFERENCES learning_models(model_id) ON DELETE CASCADE,
    INDEX idx_performance_id (performance_id),
    INDEX idx_model_id (model_id),
    INDEX idx_evaluation_date (evaluation_date),
    INDEX idx_accuracy_score (accuracy_score)
);
```

---

## 5. Non Functional Requirements

### 5.1 Performance

```yaml
Performance Requirements:
  Similarity Analysis:
    - Standard Analysis: < 3 seconds (95th percentile)
    - Complex Multi-Feature Analysis: < 5 seconds (95th percentile)
    - Batch Analysis: < 30 seconds per 100 events
    
  Model Training:
    - Incremental Training: < 10 minutes
    - Full Model Retraining: < 2 hours
    - Model Evaluation: < 5 minutes
    
  Pattern Recognition:
    - Pattern Identification: < 2 seconds
    - Trend Analysis: < 10 seconds
    - Insight Generation: < 5 seconds
    
  Data Processing:
    - Feature Extraction: < 500ms per event
    - Similarity Calculation: < 100ms per comparison
    - Historical Data Retrieval: < 1 second for 10,000 records
    
  Resource Utilization:
    - CPU: < 80% during ML operations
    - Memory: < 85% heap utilization
    - GPU: < 90% utilization during training
    - Storage: Support 10+ years of historical data
```

### 5.2 Security

```yaml
Security Requirements:
  Data Protection:
    - Historical deviation data encryption at rest
    - ML model artifact protection
    - Feature vector anonymization
    
  Access Control:
    - Role-based access to historical data
    - Model training permission controls
    - Outcome feedback authorization
    
  Privacy:
    - Personal data anonymization in training datasets
    - Sensitive information masking in similarity results
    - GDPR compliance for historical data processing
    
  Model Security:
    - Model artifact integrity verification
    - Training data poisoning protection
    - Adversarial attack detection
```

### 5.3 Logging

```java
@Component
public class HistoricalLearningLogger {
    
    private static final Logger logger = LoggerFactory.getLogger(HistoricalLearningLogger.class);
    private static final Logger auditLogger = LoggerFactory.getLogger("HISTORICAL_LEARNING_AUDIT");
    private static final Logger performanceLogger = LoggerFactory.getLogger("HISTORICAL_LEARNING_PERFORMANCE");
    private static final Logger mlLogger = LoggerFactory.getLogger("ML_OPERATIONS");
    
    public void logSimilarityAnalysis(String analysisId, String currentEventId, int similarCount, 
                                    double confidenceScore, long processingTime) {
        auditLogger.info("Similarity analysis completed - AnalysisId: {}, CurrentEventId: {}, " +
            "SimilarCount: {}, Confidence: {}, ProcessingTime: {}ms", 
            analysisId, currentEventId, similarCount, confidenceScore, processingTime);
        
        if (processingTime > 3000) {
            performanceLogger.warn("Slow similarity analysis - AnalysisId: {}, ProcessingTime: {}ms", 
                analysisId, processingTime);
        }
    }
    
    public void logModelTraining(String modelId, ModelType modelType, int trainingDataSize, 
                               double accuracy, long trainingDuration) {
        mlLogger.info("Model training completed - ModelId: {}, Type: {}, DataSize: {}, " +
            "Accuracy: {}, Duration: {}ms", 
            modelId, modelType, trainingDataSize, accuracy, trainingDuration);
        
        if (accuracy < 0.75) {
            mlLogger.warn("Low model accuracy - ModelId: {}, Accuracy: {}", modelId, accuracy);
        }
    }
    
    public void logOutcomeLearning(String learningId, String deviationId, String actualOutcome, 
                                 String predictedOutcome, boolean modelUpdated) {
        auditLogger.info("Outcome learning processed - LearningId: {}, DeviationId: {}, " +
            "ActualOutcome: {}, PredictedOutcome: {}, ModelUpdated: {}", 
            learningId, deviationId, actualOutcome, predictedOutcome, modelUpdated);
    }
    
    public void logPatternIdentification(String patternId, String eventType, int occurrenceFrequency, 
                                       double successRate) {
        mlLogger.info("Pattern identified - PatternId: {}, EventType: {}, Frequency: {}, SuccessRate: {}", 
            patternId, eventType, occurrenceFrequency, successRate);
        
        if (successRate < 0.5) {
            mlLogger.warn("Low success rate pattern - PatternId: {}, SuccessRate: {}", patternId, successRate);
        }
    }
    
    public void logDataQualityIssue(String deviationId, String issueType, double qualityScore) {
        logger.warn("Data quality issue detected - DeviationId: {}, IssueType: {}, QualityScore: {}", 
            deviationId, issueType, qualityScore);
    }
    
    public void logModelPerformanceDegradation(String modelId, double currentAccuracy, double previousAccuracy) {
        mlLogger.warn("Model performance degradation detected - ModelId: {}, CurrentAccuracy: {}, " +
            "PreviousAccuracy: {}, Degradation: {}", 
            modelId, currentAccuracy, previousAccuracy, (previousAccuracy - currentAccuracy));
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
  Weka: 3.8.6
  DL4J: 1.0.0-M2.1

Frontend Dependencies:
  React: 18.2.0
  React Router: 6.11.0
  Formik: 2.4.0
  Yup: 1.2.0
  Axios: 1.4.0
  Material-UI: 5.13.0
  React Query: 4.29.0
  Chart.js: 4.3.0
  D3.js: 7.8.0
  React Virtualized: 9.22.0

Infrastructure Dependencies:
  MySQL: 8.0.33
  Redis: 7.0.11
  Python: 3.9.0
  TensorFlow: 2.13.0
  Scikit-learn: 1.3.0
  Pandas: 2.0.0
  NumPy: 1.24.0
  Docker: 24.0.0
  Kubernetes: 1.27.0

External Services:
  Python ML Service: v2.0
  Natural Language Processing API: v1.3
  Feature Store: v1.5
  Model Registry: v2.1
  Experiment Tracking: MLflow v2.5.0
```

---

## 7. Assumptions

```yaml
Technical Assumptions:
  - Historical deviation data is complete and accurate for training
  - Machine learning models can achieve 85%+ accuracy with available data
  - Feature extraction algorithms can identify meaningful patterns
  - Similarity calculations provide reliable matching results
  - Model retraining can be performed without significant downtime

Business Assumptions:
  - Historical outcomes are accurately recorded and available
  - Users provide timely feedback on recommendation effectiveness
  - Pattern recognition provides actionable insights for decision making
  - Learning from outcomes improves future recommendation accuracy
  - Data quality standards are maintained for training datasets

Operational Assumptions:
  - 24/7 availability for similarity analysis and pattern recognition
  - Automated model retraining processes work reliably
  - Performance monitoring and alerting systems are in place
  - Data backup and recovery procedures are established
  - Model versioning and rollback capabilities are available

Data Assumptions:
  - 10+ years of historical deviation data is available
  - Data quality scores accurately reflect record reliability
  - Feature vectors capture essential event characteristics
  - Outcome effectiveness ratings are consistent and meaningful
  - Training data distribution represents real-world scenarios

ML Assumptions:
  - Similarity algorithms generalize well across event types
  - Pattern recognition identifies actionable insights
  - Model performance degrades gracefully over time
  - Continuous learning improves recommendation accuracy
  - Feature importance remains stable across model versions
```