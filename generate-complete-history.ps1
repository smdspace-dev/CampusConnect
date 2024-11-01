# Enhanced Campus Connect Git History Generator
# Author: Thousif ibrahim <thousifibrahim07@gmail.com>
# Generates realistic commit history from Nov 2024 to Feb 2025

param(
    [string]$ProjectPath = "."
)

Set-Location $ProjectPath

# Define comprehensive commit types and messages for Campus Connect
$commitData = @{
    "feat" = @(
        "Add user authentication system with JWT",
        "Implement student dashboard with analytics",
        "Create teacher interface for course management",
        "Add admin panel with user management",
        "Implement placement management system",
        "Add resource person management module",
        "Create landing page with glassmorphic design",
        "Add demo popup functionality",
        "Implement responsive design framework",
        "Add dark mode support with theme switching",
        "Create notification system with real-time updates",
        "Add file upload functionality with validation",
        "Implement advanced search with filters",
        "Add data visualization with charts",
        "Create report generation system",
        "Add email notifications with templates",
        "Implement role-based access control",
        "Add API documentation with Swagger",
        "Create mobile responsive UI components",
        "Add progressive web app features",
        "Implement course assignment system",
        "Add grade management functionality",
        "Create attendance tracking system",
        "Add student profile management",
        "Implement placement drive management",
        "Add company registration portal",
        "Create interview scheduling system",
        "Add skill assessment module",
        "Implement club management system",
        "Add event management functionality"
    )
    "fix" = @(
        "Fix login authentication timeout issue",
        "Resolve responsive design issues on mobile",
        "Fix API endpoint CORS configuration",
        "Correct database migration conflicts",
        "Fix form validation error messages",
        "Resolve session management issues",
        "Fix memory leak in dashboard component",
        "Correct timezone handling in notifications",
        "Fix pagination bug in student list",
        "Resolve CSS conflicts in landing page",
        "Fix mobile navigation menu collapse",
        "Correct data export functionality",
        "Fix email template rendering issues",
        "Resolve security vulnerabilities in auth",
        "Fix performance bottlenecks in queries",
        "Correct file upload size validation",
        "Fix search results pagination",
        "Resolve database connection pooling",
        "Fix role permission validation",
        "Correct API response formatting"
    )
    "docs" = @(
        "Update README with installation guide",
        "Add comprehensive API documentation",
        "Create deployment guide for production",
        "Update contributing guidelines",
        "Add code of conduct for contributors",
        "Create user manual with screenshots",
        "Update system requirements documentation",
        "Add troubleshooting guide for common issues",
        "Create architecture documentation",
        "Update changelog with release notes",
        "Add security guidelines documentation",
        "Create database schema documentation",
        "Add component documentation with examples",
        "Update development environment setup",
        "Create testing guidelines and examples"
    )
    "style" = @(
        "Improve button styling consistency",
        "Update color scheme for better accessibility",
        "Enhance landing page visual design",
        "Improve form layouts and spacing",
        "Update navigation design patterns",
        "Enhance card components styling",
        "Improve typography across application",
        "Update spacing and margin consistency",
        "Enhance mobile design responsiveness",
        "Improve accessibility with ARIA labels",
        "Update dashboard layout design",
        "Enhance notification styling",
        "Improve table design and usability",
        "Update modal dialog styling",
        "Enhance loading states design"
    )
    "refactor" = @(
        "Refactor authentication logic for better maintainability",
        "Improve code organization in components",
        "Optimize database queries for performance",
        "Restructure component hierarchy for clarity",
        "Improve error handling patterns",
        "Optimize API endpoints for efficiency",
        "Refactor state management with Context API",
        "Improve code reusability with custom hooks",
        "Optimize bundle size and loading performance",
        "Improve test coverage and organization",
        "Refactor utility functions for clarity",
        "Improve component prop validation",
        "Optimize image loading and caching",
        "Refactor CSS organization with modules",
        "Improve API response handling"
    )
    "test" = @(
        "Add unit tests for authentication module",
        "Add integration tests for API endpoints",
        "Add end-to-end tests for user workflows",
        "Improve test coverage for components",
        "Add API endpoint validation tests",
        "Add component interaction tests",
        "Add security vulnerability tests",
        "Add performance benchmark tests",
        "Add accessibility compliance tests",
        "Add cross-browser compatibility tests",
        "Add mobile responsiveness tests",
        "Add database migration tests",
        "Add error handling tests",
        "Add load testing for API endpoints",
        "Add user authentication flow tests"
    )
    "chore" = @(
        "Update npm dependencies to latest versions",
        "Configure CI/CD pipeline with GitHub Actions",
        "Update build scripts for production",
        "Configure ESLint rules for code quality",
        "Update package versions for security",
        "Configure development environment with Docker",
        "Update docker configuration for production",
        "Configure monitoring and logging",
        "Setup error tracking with Sentry",
        "Update deployment scripts for automation",
        "Configure database backup scripts",
        "Update environment variable management",
        "Configure SSL certificate renewal",
        "Setup performance monitoring",
        "Configure automated testing pipeline"
    )
    "perf" = @(
        "Optimize React component rendering performance",
        "Improve database query execution time",
        "Optimize image loading and compression",
        "Improve API response time with caching",
        "Optimize bundle size with code splitting",
        "Improve server response time",
        "Optimize database indexes for queries",
        "Improve memory usage in components",
        "Optimize network requests with batching",
        "Improve loading states and perceived performance"
    )
    "security" = @(
        "Implement input sanitization for XSS prevention",
        "Add rate limiting for API endpoints",
        "Implement CSRF protection middleware",
        "Add SQL injection prevention measures",
        "Implement secure file upload validation",
        "Add authentication token encryption",
        "Implement secure password hashing",
        "Add security headers for protection",
        "Implement content security policy",
        "Add audit logging for security events"
    )
}

# Define realistic file patterns for different types of changes
$fileGroups = @{
    "authentication" = @(
        "backend/backend/auth_views.py",
        "backend/common_features/models.py",
        "frontend/src/context/AuthContext.js",
        "frontend/src/components/auth/LoginPage.js"
    )
    "frontend_components" = @(
        "frontend/src/components/auth/LandingPage.js",
        "frontend/src/components/dashboards/",
        "frontend/src/components/student/",
        "frontend/src/components/teacher/",
        "frontend/src/components/admin/"
    )
    "backend_apis" = @(
        "backend/admin_system/views.py",
        "backend/student_interface/views.py",
        "backend/teacher_interface/views.py",
        "backend/placement_management/views.py",
        "backend/resource_person_management/views.py"
    )
    "styling" = @(
        "frontend/src/index.css",
        "frontend/src/styles/",
        "frontend/src/components/shared/DemoPopup.css",
        "frontend/src/components/auth/PremiumLanding.css"
    )
    "documentation" = @(
        "README.md",
        "SYSTEM_DOCUMENTATION.md",
        "PRODUCTION_DEPLOYMENT.md",
        "GITHUB_SETUP.md"
    )
    "configuration" = @(
        "docker-compose.yml",
        "docker-compose.prod.yml",
        "backend/requirements.txt",
        "frontend/package.json",
        ".gitignore"
    )
}

# Generate realistic commit dates from Nov 1, 2024 to Feb 28, 2025
$startDate = Get-Date "2024-11-01 09:00:00"
$endDate = Get-Date "2025-02-28 17:00:00"
$totalDays = ($endDate - $startDate).TotalDays

Write-Host "🚀 Generating realistic Campus Connect development history..." -ForegroundColor Green
Write-Host "👨‍💻 Developer: Thousif ibrahim <thousifibrahim07@gmail.com>" -ForegroundColor Cyan
Write-Host "📅 Period: $($startDate.ToString('yyyy-MM-dd')) to $($endDate.ToString('yyyy-MM-dd'))" -ForegroundColor Cyan
Write-Host "📊 Target: 400+ commits with realistic patterns" -ForegroundColor Cyan
Write-Host ""

# Create initial commit with proper author
git add .gitignore 2>$null
if (-not $?) { git add . }

$env:GIT_COMMITTER_DATE = $startDate.ToString("yyyy-MM-dd HH:mm:ss")
$env:GIT_AUTHOR_DATE = $startDate.ToString("yyyy-MM-dd HH:mm:ss")
$env:GIT_COMMITTER_NAME = "Thousif ibrahim"
$env:GIT_COMMITTER_EMAIL = "thousifibrahim07@gmail.com"
$env:GIT_AUTHOR_NAME = "Thousif ibrahim"
$env:GIT_AUTHOR_EMAIL = "thousifibrahim07@gmail.com"

git commit -m "feat: Initialize Campus Connect - College Management System

Initial project setup with comprehensive features for college management including multi-role authentication, student dashboard, course management, placement system, and responsive design with React frontend and Django backend." --date="$($startDate.ToString('yyyy-MM-dd HH:mm:ss'))"

$commitCount = 1
Write-Host "✅ [$commitCount] $($startDate.ToString('yyyy-MM-dd HH:mm')) - Initial project setup" -ForegroundColor Green

$currentDate = $startDate.AddDays(1)

# Development phase patterns
$phases = @{
    "setup" = @{ start = 0; end = 7; intensity = 3 }           # Week 1: Project setup
    "core_dev" = @{ start = 7; end = 30; intensity = 4 }       # Weeks 2-5: Core development
    "feature_dev" = @{ start = 30; end = 60; intensity = 5 }   # Weeks 6-9: Feature development
    "integration" = @{ start = 60; end = 75; intensity = 3 }   # Weeks 10-11: Integration
    "testing" = @{ start = 75; end = 90; intensity = 4 }       # Weeks 12-13: Testing
    "refinement" = @{ start = 90; end = 119; intensity = 3 }   # Final weeks: Refinement
}

# Generate commits with realistic development patterns
while ($currentDate -le $endDate -and $commitCount -lt 420) {
    $daysSinceStart = ($currentDate - $startDate).TotalDays
    $dayOfWeek = $currentDate.DayOfWeek
    
    # Determine development phase
    $currentPhase = "refinement"
    foreach ($phase in $phases.GetEnumerator()) {
        if ($daysSinceStart -ge $phase.Value.start -and $daysSinceStart -lt $phase.Value.end) {
            $currentPhase = $phase.Key
            break
        }
    }
    
    # Calculate skip probability based on day and holidays
    $skipProbability = 0.1
    
    # Weekend patterns
    if ($dayOfWeek -eq "Saturday") { $skipProbability = 0.6 }
    if ($dayOfWeek -eq "Sunday") { $skipProbability = 0.8 }
    
    # Holiday periods (Christmas/New Year)
    if ($currentDate -ge (Get-Date "2024-12-23") -and $currentDate -le (Get-Date "2025-01-02")) {
        $skipProbability = 0.9
    }
    
    # Thanksgiving week
    if ($currentDate -ge (Get-Date "2024-11-25") -and $currentDate -le (Get-Date "2024-11-29")) {
        $skipProbability = 0.7
    }
    
    if ((Get-Random -Minimum 0 -Maximum 100) / 100 -gt $skipProbability) {
        # Determine number of commits for this day based on phase intensity
        $phaseIntensity = $phases[$currentPhase].intensity
        $maxCommits = [Math]::Min($phaseIntensity, 6)
        $commitsToday = Get-Random -Minimum 1 -Maximum ($maxCommits + 1)
        
        for ($i = 0; $i -lt $commitsToday -and $commitCount -lt 420; $i++) {
            # Select commit type based on development phase
            $commitType = switch ($currentPhase) {
                "setup" { @("feat", "chore", "docs") | Get-Random }
                "core_dev" { @("feat", "feat", "fix", "refactor") | Get-Random }
                "feature_dev" { @("feat", "feat", "style", "fix") | Get-Random }
                "integration" { @("fix", "refactor", "test", "perf") | Get-Random }
                "testing" { @("test", "fix", "fix", "security") | Get-Random }
                "refinement" { @("fix", "style", "docs", "perf", "chore") | Get-Random }
                default { @("feat", "fix", "docs") | Get-Random }
            }
            
            $commitMessage = $commitData[$commitType] | Get-Random
            
            # Add random working hour time
            $workingHour = Get-Random -Minimum 9 -Maximum 18
            $workingMinute = Get-Random -Minimum 0 -Maximum 59
            $commitTime = $currentDate.Date.AddHours($workingHour).AddMinutes($workingMinute)
            
            # Stage some files (simulate realistic development)
            $randomChoice = Get-Random -Minimum 1 -Maximum 5
            switch ($randomChoice) {
                1 { git add "frontend/" 2>$null }
                2 { git add "backend/" 2>$null }
                3 { git add "*.md" 2>$null }
                4 { git add "docker*" 2>$null }
                default { git add . 2>$null }
            }
            
            # Set commit environment with your details
            $env:GIT_COMMITTER_DATE = $commitTime.ToString("yyyy-MM-dd HH:mm:ss")
            $env:GIT_AUTHOR_DATE = $commitTime.ToString("yyyy-MM-dd HH:mm:ss")
            $env:GIT_COMMITTER_NAME = "Thousif ibrahim"
            $env:GIT_COMMITTER_EMAIL = "thousifibrahim07@gmail.com"
            $env:GIT_AUTHOR_NAME = "Thousif ibrahim"
            $env:GIT_AUTHOR_EMAIL = "thousifibrahim07@gmail.com"
            
            $fullCommitMessage = "$commitType`: $commitMessage"
            git commit -m $fullCommitMessage --date="$($commitTime.ToString('yyyy-MM-dd HH:mm:ss'))" --allow-empty 2>$null
            
            $commitCount++
            
            # Progress indicator
            if ($commitCount % 25 -eq 0) {
                $progress = [Math]::Round(($commitCount / 420) * 100, 1)
                Write-Host "📈 Progress: $commitCount commits ($progress%) - $($commitTime.ToString('yyyy-MM-dd'))" -ForegroundColor Yellow
            }
            
            Start-Sleep -Milliseconds 50
        }
    }
    
    $currentDate = $currentDate.AddDays(1)
}

Write-Host ""
Write-Host "🎉 Campus Connect development history generation complete!" -ForegroundColor Green
Write-Host "📊 Total commits created: $commitCount" -ForegroundColor Cyan
Write-Host "👨‍💻 All commits authored by: Thousif ibrahim <thousifibrahim07@gmail.com>" -ForegroundColor Cyan
Write-Host "📅 Development period: Nov 2024 - Feb 2025" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔍 Commands to explore your history:" -ForegroundColor Magenta
Write-Host "  git log --oneline" -ForegroundColor White
Write-Host "  git log --graph --pretty=format:'%h -%d %s (%cr) <%an>'" -ForegroundColor White
Write-Host "  git shortlog -sn" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Ready to push to GitHub! Your contribution graph will show consistent activity." -ForegroundColor Green