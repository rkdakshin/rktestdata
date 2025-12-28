# Claude Integration Guide

This invoice generator is optimized for development with Claude Code.

## Claude Configuration

The `.claude/` directory contains configuration for Claude-assisted development.

## Skills

Located in `/skills/`, these are reusable utilities:
- `pdf_generator.py` - PDF generation logic
- `invoice_validator.py` - Invoice data validation

## Agents

Located in `/agents/`, these automate specific tasks:
- `invoice_agent.py` - Invoice processing automation

## Prompts and Patterns (PRPs)

Located in `/PRPs/`, documentation for common development patterns:
- API endpoint examples
- Invoice template customization
- Database query patterns

## Development Workflow with Claude

1. Use Claude to generate boilerplate code
2. Leverage skills for common operations
3. Run agents for automated tasks
4. Reference PRPs for best practices

## Example Commands

Ask Claude:
- "Add a new field to the invoice model"
- "Create a discount calculation feature"
- "Generate a tax calculation utility"
- "Add email sending capability"
