# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Proper table cell merging to maintain template structure
- Permission error handling with Windows toast notifications
- Comprehensive error handling for locked documents
- README.md with full documentation

### Changed
- Optimized document generation using only python-docx methods
- Fixed table, text, and image ordering (Table → Text → Image sequence)
- Removed all debug logs for better performance
- Reduced memory usage and CPU overhead

### Fixed
- Table formatting now preserves merged cells from template
- Correct sequential ordering of tables, text, and images
- Document locking detection with proper user notifications

## [1.0.0] - Initial Release

### Added
- Basic document generation functionality
- FastAPI web interface
- Template-based document creation
- Image upload and insertion
- Context management for test cases
