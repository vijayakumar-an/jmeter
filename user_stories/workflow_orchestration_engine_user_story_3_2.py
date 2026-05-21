"""
# User Story

## EPIC Id
EP003

## User Story Id
US008

## Title
Inter-Step Output Passing and Data Flow

## Description
As a system,
I want to pass outputs from step N to step N+1 seamlessly,
So that workflow data flows correctly through the entire pipeline without data loss or corruption.

## Acceptance Criteria

### Given: Step N completes with output data
- When: System prepares for step N+1 execution
- Then: System should capture step N output in standardized format
- And: System should validate output schema compliance
- And: System should transform data if required for next step
- And: System should pass data to step N+1 input

### Given: Data transformation requirements between steps
- When: Output format differs from next step input format
- Then: System should apply configured transformation rules
- And: System should validate transformed data integrity
- And: System should log transformation details
- And: System should handle transformation errors gracefully

### Given: Large data volumes between steps
- When: Step outputs contain substantial data
- Then: System should use efficient data transfer mechanisms
- And: System should implement data streaming where appropriate
- And: System should monitor memory usage during transfers
- And: System should provide progress indicators for long transfers

## Functional Requirements
- Standardized data format definitions
- Data transformation engine
- Schema validation framework
- Efficient data transfer mechanisms
- Memory management for large datasets
- Progress tracking for data operations
- Error handling and recovery

## Validations
- Output schema compliance validation
- Data transformation accuracy validation
- Data integrity validation during transfer
- Memory usage validation
- Transfer completion validation

## Non Functional Requirements
- Data transfer speed: > 1GB/minute for large datasets
- Memory efficiency: < 2x data size memory usage
- Data integrity: 100% accuracy in transfers
- Transformation performance: < 10 seconds for standard datasets
- Error recovery: Automatic retry with exponential backoff
- Monitoring: Real-time transfer progress visibility

## Assumptions
- Data schemas are well-defined and documented
- Transformation rules are tested and validated
- System has sufficient memory and storage capacity
- Network bandwidth supports required transfer speeds
"""