# Module: tools/data/

## Purpose

Data processing workflows for common data manipulation tasks. These tools are general-purpose utilities that can be used across many agent types.

## Available Workflows

| File | Description |
|------|-------------|
| `web-scraping.workflow.json` | Fetch and extract structured content from a web page |
| `date-parser.workflow.json` | Parse natural language or ambiguous date strings into ISO 8601 |

## web-scraping

Fetches a web page and extracts specified fields from its content. Useful for product information lookup, news fetching, or any scenario where the agent needs to retrieve external web content.

**Canvas alias suggestion**: `scrape_web`

**Key outputs**:
- `content` (object): Extracted fields (or full page text if no fields specified)
- `success` (boolean): Whether the fetch succeeded
- `error_code` (string | null): Failure reason if `success` is `false`

## date-parser

Converts natural language date expressions ("next Monday", "3 days ago", "2024年春节") into a consistent ISO 8601 date string. Supports locale-aware parsing.

**Canvas alias suggestion**: `parse_date`

**Key outputs**:
- `parsed_date` (string | null): ISO 8601 formatted date if parsing succeeded
- `success` (boolean): Whether parsing succeeded
- `error_code` (string | null): Failure reason if `success` is `false`

## Used By

- *(Add agent references here as they are created)*
