"""Deterministic Scopus query compiler. The model supplies concepts; this file builds the query."""

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from lib.config import load_yaml
from lib.scopus import escape_quotes


@dataclass
class ConceptBlock:
    slot: str
    input_term: str
    matched_key: Optional[str]
    terms: List[str]
    expansion: str  # "synonyms" | "none"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "slot": self.slot,
            "input_term": self.input_term,
            "matched_key": self.matched_key,
            "terms": list(self.terms),
            "expansion": self.expansion,
        }


@dataclass
class QueryPlan:
    query: str
    sort: str
    from_year: Optional[int]
    filters: Dict[str, Any] = field(default_factory=dict)


def normalize_term(value: str) -> str:
    text = re.sub(r"\s+", " ", (value or "").strip().lower())
    return text.rstrip(".").strip()


def build_synonym_index(table: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """Map every normalized canonical/synonym/key to its concept key. Collisions are an error."""
    table = table if table is not None else load_yaml("synonyms")
    index: Dict[str, str] = {}
    for key, entry in (table.get("concepts") or {}).items():
        aliases = [key.replace("_", " "), entry.get("canonical", "")] + list(entry.get("synonyms") or [])
        for alias in aliases:
            norm = normalize_term(alias)
            if not norm:
                continue
            if norm in index and index[norm] != key:
                raise ValueError(f"synonyms.yaml alias collision: '{alias}' in {index[norm]} and {key}")
            index[norm] = key
    return index


def resolve_concept(slot: str, term: str, table: Optional[Dict[str, Any]] = None) -> ConceptBlock:
    table = table if table is not None else load_yaml("synonyms")
    index = build_synonym_index(table)
    key = index.get(normalize_term(term))
    if key is None:
        return ConceptBlock(slot=slot, input_term=term, matched_key=None, terms=[term.strip()], expansion="none")
    entry = table["concepts"][key]
    terms = [entry["canonical"]] + list(entry.get("synonyms") or [])
    return ConceptBlock(slot=slot, input_term=term, matched_key=key, terms=terms, expansion="synonyms")


def block_to_scopus(block: ConceptBlock) -> str:
    quoted = " OR ".join(f'"{escape_quotes(t)}"' for t in block.terms)
    return f"TITLE-ABS-KEY({quoted})"


def compile_topic_query(blocks: List[ConceptBlock]) -> str:
    return " AND ".join(block_to_scopus(b) for b in blocks)


def compile_keyword_query(query: str, is_scopus_syntax: bool = False) -> str:
    text = (query or "").strip()
    if is_scopus_syntax:
        return text
    return f'TITLE-ABS-KEY("{escape_quotes(text)}")'


def compile_title_query(title: str) -> str:
    return f'TITLE("{escape_quotes((title or "").strip())}")'


def resolve_from_year(
    year_from: Optional[int],
    years_back: Optional[int],
    freshness: Optional[str],
    defaults: Optional[Dict[str, Any]] = None,
    today: Optional[date] = None,
) -> Optional[int]:
    """Precedence: year_from > years_back > freshness > none."""
    defaults = defaults if defaults is not None else load_yaml("defaults")
    today = today or date.today()
    if year_from:
        return int(year_from)
    if years_back:
        return today.year - max(1, int(years_back)) + 1
    if freshness:
        window = int(defaults["freshness"][freshness]["years_back"])
        return today.year - window + 1
    return None


def attach_filters(
    base_query: str,
    from_year: Optional[int],
    language: str,
    document_type: str,
    defaults: Optional[Dict[str, Any]] = None,
) -> QueryPlan:
    """Append PUBYEAR, LANGUAGE, DOCTYPE clauses in a fixed order. Sort is date-first when a year filter exists."""
    defaults = defaults if defaults is not None else load_yaml("defaults")
    query = base_query
    clauses: List[str] = []
    if from_year is not None:
        clauses.append(f"PUBYEAR > {int(from_year) - 1}")
    lang_clause = defaults["scopus"]["language_clause"].get(language)
    if lang_clause:
        clauses.append(lang_clause)
    doc_clause = defaults["scopus"]["document_type_clause"].get(document_type)
    if doc_clause:
        clauses.append(doc_clause)
    if clauses:
        query = f"({base_query}) AND " + " AND ".join(clauses)
    sort = defaults["sort"]["when_freshness"] if from_year is not None else defaults["sort"]["default"]
    return QueryPlan(
        query=query,
        sort=sort,
        from_year=from_year,
        filters={"from_year": from_year, "language": language, "document_type": document_type},
    )


# ---- OpenAlex (no-key provider) ---------------------------------------------

@dataclass
class OpenAlexPlan:
    search: str
    filters: List[str]
    sort: str
    from_year: Optional[int]
    filters_dict: Dict[str, Any] = field(default_factory=dict)


def _oa_term(term: str) -> str:
    return '"' + term.replace('"', "").strip() + '"'


def block_to_openalex(block: ConceptBlock) -> str:
    return "(" + " OR ".join(_oa_term(t) for t in block.terms) + ")"


def compile_topic_query_openalex(blocks: List[ConceptBlock]) -> str:
    return " AND ".join(block_to_openalex(b) for b in blocks)


def compile_keyword_query_openalex(query: str) -> str:
    """Verbatim (trimmed). OpenAlex boolean operators must be uppercase AND/OR/NOT; phrases in double quotes."""
    return (query or "").strip()


def attach_filters_openalex(
    search: str,
    from_year: Optional[int],
    language: str,
    document_type: str,
    providers_cfg: Optional[Dict[str, Any]] = None,
) -> OpenAlexPlan:
    providers_cfg = providers_cfg if providers_cfg is not None else load_yaml("providers")
    oa = providers_cfg["openalex"]
    filters: List[str] = []
    if from_year is not None:
        filters.append(f"publication_year:>{int(from_year) - 1}")
    lang = oa["language_filter"].get(language)
    if lang:
        filters.append(lang)
    typ = oa["type_filter"].get(document_type)
    if typ:
        filters.append(typ)
    sort = oa["sort"]["when_freshness"] if from_year is not None else oa["sort"]["default"]
    return OpenAlexPlan(
        search=search,
        filters=filters,
        sort=sort,
        from_year=from_year,
        filters_dict={"from_year": from_year, "language": language, "document_type": document_type},
    )


def openalex_compiled_string(plan: OpenAlexPlan) -> str:
    parts = [f"search={plan.search}"]
    if plan.filters:
        parts.append("filter=" + ",".join(plan.filters))
    parts.append(f"sort={plan.sort}")
    return " | ".join(parts)
