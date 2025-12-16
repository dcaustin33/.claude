# Common Bug Patterns and Critical Issues

This document outlines critical issues and common bug patterns to check for when analyzing repository dependencies.

## Table of Contents

1. [Critical Import/Dependency Issues](#critical-importdependency-issues)
2. [Data Flow and Type Mismatches](#data-flow-and-type-mismatches)
3. [Configuration and Environment Issues](#configuration-and-environment-issues)
4. [Resource Management](#resource-management)
5. [Concurrency and Threading](#concurrency-and-threading)
6. [API and Interface Misuse](#api-and-interface-misuse)
7. [Training-Specific Issues](#training-specific-issues)

## Critical Import/Dependency Issues

### Missing Dependencies
- **Pattern**: Function/class imported but not defined in source file
- **Impact**: ImportError or ModuleNotFoundError at runtime
- **Check**: Verify all imported symbols exist in their source modules

### Circular Dependencies
- **Pattern**: Module A imports B, B imports A (directly or indirectly)
- **Impact**: ImportError, initialization issues, or unexpected behavior
- **Check**: Trace import chains for cycles

### Version Incompatibilities
- **Pattern**: Code uses features not available in specified dependency versions
- **Impact**: AttributeError, API mismatches at runtime
- **Check**: Verify API usage matches available versions

### Incorrect Relative Imports
- **Pattern**: Relative imports that don't match actual directory structure
- **Impact**: ImportError when running from different locations
- **Check**: Validate relative import paths against actual file locations

## Data Flow and Type Mismatches

### Shape Mismatches (ML/Tensor Operations)
- **Pattern**: Tensor/array operations with incompatible dimensions
- **Impact**: Runtime shape errors, dimension mismatches
- **Check**: Trace tensor shapes through transformations; verify input/output dimensions match expectations

### Type Mismatches
- **Pattern**: Function expects type A but receives type B
- **Impact**: TypeError or unexpected coercion behavior
- **Check**: Verify argument types match function signatures; check dict access patterns

### Missing Required Arguments
- **Pattern**: Function calls missing required parameters
- **Impact**: TypeError at runtime
- **Check**: Verify all non-default parameters are provided in function calls

### Incorrect Return Value Usage
- **Pattern**: Using function return value incorrectly (e.g., unpacking wrong number of values)
- **Impact**: ValueError or unexpected behavior
- **Check**: Verify return value expectations match actual returns

## Configuration and Environment Issues

### Missing Configuration Files
- **Pattern**: Code loads config files that don't exist in repo
- **Impact**: FileNotFoundError or incorrect defaults
- **Check**: Verify all referenced config files exist or have proper defaults

### Environment Variable Dependencies
- **Pattern**: Code relies on environment variables not documented or set
- **Impact**: KeyError or incorrect defaults
- **Check**: Identify all env var usage; verify they're documented and have fallbacks

### Path Dependencies
- **Pattern**: Hardcoded or relative paths that may not exist at runtime
- **Impact**: FileNotFoundError or incorrect file access
- **Check**: Verify paths are portable or properly constructed

### Missing Data Files
- **Pattern**: Code loads data files (models, weights, datasets) that aren't provided
- **Impact**: FileNotFoundError at runtime
- **Check**: Verify all data file references exist or are properly handled

## Resource Management

### Memory Leaks
- **Pattern**: Resources allocated but never freed (especially in loops)
- **Impact**: Out-of-memory errors
- **Check**: Verify large objects are deleted; context managers are used properly

### File Handle Leaks
- **Pattern**: Files opened but not closed
- **Impact**: "Too many open files" errors
- **Check**: Verify files are opened with context managers or explicitly closed

### GPU Memory Management
- **Pattern**: Tensors not moved off GPU; no torch.no_grad() in inference; cached computations
- **Impact**: CUDA out-of-memory errors
- **Check**: Verify proper GPU memory cleanup; check for gradient accumulation issues

## Concurrency and Threading

### Race Conditions
- **Pattern**: Shared state modified by multiple threads without synchronization
- **Impact**: Inconsistent state, data corruption
- **Check**: Verify shared resources use proper locking mechanisms

### Deadlocks
- **Pattern**: Circular wait conditions with locks
- **Impact**: Program hangs indefinitely
- **Check**: Analyze lock acquisition order across threads

### Thread-Unsafe Data Structures
- **Pattern**: Using non-thread-safe structures in multi-threaded context
- **Impact**: Data corruption, crashes
- **Check**: Verify thread-safe alternatives are used when needed

## API and Interface Misuse

### Deprecated API Usage
- **Pattern**: Using deprecated functions or methods
- **Impact**: Warnings or errors in newer versions
- **Check**: Verify no deprecated APIs are used; check for version-specific changes

### Incorrect API Contract
- **Pattern**: Violating expected behavior (e.g., mutating inputs that shouldn't be mutated)
- **Impact**: Unexpected side effects, data corruption
- **Check**: Verify API contracts are respected; check for unexpected mutations

### Missing Error Handling
- **Pattern**: No try-except around operations that can fail
- **Impact**: Uncaught exceptions crash the program
- **Check**: Verify critical operations have proper error handling

## Training-Specific Issues

### Data Loading Issues
- **Pattern**: Incorrect batch size, shuffle settings, or data augmentation
- **Impact**: Poor training convergence, incorrect results
- **Check**: Verify DataLoader configurations; check for data preprocessing bugs

### Gradient Issues
- **Pattern**: Gradients not computed (.requires_grad=False); gradients not zeroed; gradient clipping issues
- **Impact**: Model doesn't train or trains incorrectly
- **Check**: Verify gradient flow through model; check optimizer.zero_grad() placement

### Loss Function Mismatches
- **Pattern**: Loss function doesn't match task (e.g., wrong reduction, incorrect target format)
- **Impact**: Model optimizes wrong objective
- **Check**: Verify loss function matches model outputs and targets

### Learning Rate Issues
- **Pattern**: LR too high/low; scheduler misconfigured; LR not adjusted properly
- **Impact**: Training divergence or slow convergence
- **Check**: Verify LR scheduler configuration and update frequency

### Checkpoint/Model Saving Issues
- **Pattern**: Saving incorrect state_dict; missing optimizer state; incorrect loading
- **Impact**: Can't resume training properly or load model for inference
- **Check**: Verify save/load logic handles all necessary components

### Device Mismatches
- **Pattern**: Model on GPU but data on CPU (or vice versa)
- **Impact**: Runtime errors about tensor device mismatches
- **Check**: Verify consistent device placement for model, data, and operations

### Distributed Training Issues
- **Pattern**: Incorrect world_size/rank usage; missing synchronization barriers
- **Impact**: Deadlocks, incorrect gradient accumulation
- **Check**: Verify distributed setup is correct; check for proper synchronization

## Analysis Priority

When analyzing dependencies, prioritize issues by severity:

1. **Critical**: Will cause immediate runtime failures (ImportError, missing files, type errors)
2. **High**: Will cause incorrect behavior or failures under certain conditions (shape mismatches, device mismatches)
3. **Medium**: Will cause degraded performance or eventual failures (memory leaks, missing error handling)
4. **Low**: Code quality or maintainability issues that may lead to bugs later (deprecated APIs, poor patterns)

## Language-Specific Patterns

### Python
- Check for: Missing imports, incorrect unpacking, mutable default arguments, scope issues with closures
- ML-specific: Tensor shape issues, gradient computation problems, device placement

### JavaScript/TypeScript
- Check for: Undefined variables, incorrect async/await usage, missing null checks, incorrect this binding
- Common: Promise handling errors, missing error callbacks

### Go
- Check for: Unhandled errors (missing error checks), goroutine leaks, channel deadlocks
- Common: Incorrect error wrapping, missing context cancellation

### Java
- Check for: Null pointer issues, resource leaks (missing try-with-resources), incorrect exception handling
- Common: Thread safety issues in concurrent code

### C/C++
- Check for: Memory leaks, buffer overflows, use-after-free, null pointer dereferences
- Common: Missing delete/free, incorrect pointer arithmetic, undefined behavior
