# Project Guidelines

## Code Style and Standards

### General Principles
- Write clear, self-documenting code with meaningful variable and function names
- Follow the single responsibility principle - each function/class should do one thing well
- Keep functions small and focused (generally under 50 lines)
- Prefer composition over inheritance
- Write code that is easy to test and maintain

### Code Organization
- Group related functionality together
- Use consistent file and folder naming conventions
- Keep configuration separate from code
- Organize imports/requires in a consistent order

### Documentation
- Add comments for complex logic or non-obvious decisions
- Keep comments up-to-date with code changes
- Document public APIs and interfaces
- Include examples in documentation where helpful

## Testing

### Testing Requirements
- Write tests for new features and bug fixes
- Aim for high test coverage of critical paths
- Use descriptive test names that explain what is being tested
- Follow the Arrange-Act-Assert pattern
- Keep tests independent and repeatable

### Test Organization
- Place tests close to the code they test
- Use consistent naming (e.g., `*.test.js`, `*.spec.js`)
- Group related tests using describe blocks
- Mock external dependencies appropriately

## Git Workflow

### Commits
- Write clear, descriptive commit messages
- Use conventional commit format when applicable
- Make atomic commits (one logical change per commit)
- Avoid committing commented-out code or debug statements

### Branches
- Use descriptive branch names (e.g., `feature/add-user-auth`, `fix/login-error`)
- Keep branches focused on a single feature or fix
- Regularly sync with main branch to avoid large merge conflicts
- Delete branches after they are merged

## Security

### Best Practices
- Never commit secrets, API keys, or credentials
- Use environment variables for configuration
- Validate and sanitize all user inputs
- Follow OWASP guidelines for common vulnerabilities:
  - Prevent SQL injection
  - Prevent XSS attacks
  - Prevent CSRF attacks
  - Use secure authentication and session management
- Keep dependencies up-to-date
- Use security linting tools

## Performance

### Optimization Guidelines
- Profile before optimizing
- Avoid premature optimization
- Cache expensive operations when appropriate
- Use efficient data structures
- Minimize network requests and payload sizes
- Implement proper error handling and logging

## Code Review

### Review Checklist
- Does the code meet the requirements?
- Is the code well-tested?
- Are there any security concerns?
- Is the code maintainable and readable?
- Are there any performance issues?
- Is the documentation adequate?
- Does it follow project conventions?

## Project-Specific Guidelines

### Technology Stack
- Document your main technologies, frameworks, and libraries here
- Include version requirements if applicable

### Architecture Patterns
- Document architectural decisions and patterns used in the project
- Explain the project structure and organization

### Dependencies
- Justify new dependencies before adding them
- Prefer well-maintained, popular libraries
- Keep the dependency tree as small as possible
- Regularly update dependencies to get security patches

## Additional Notes

- Customize these guidelines based on your project's specific needs
- Keep this document up-to-date as the project evolves
- Share this with all contributors to ensure consistency
