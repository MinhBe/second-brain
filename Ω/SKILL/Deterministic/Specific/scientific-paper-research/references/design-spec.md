# SPEC-01-Scientific-Paper-Research-Strict-Skill

## Context tổng hợp

Tài liệu này ghi lại đầy đủ context và các quyết định thiết kế đã trao
đổi về việc xây dựng/custom harness skill cho nghiên cứu khoa học.

### 1. Context ban đầu: phân tích workflow kiểu SciSpace

Nội dung nguồn mô tả một nền tảng AI hỗ trợ nghiên cứu khoa học với các
nhóm khả năng chính:

-   Tìm kiếm bài báo và bằng chứng khoa học.
-   Literature review / tổng quan tài liệu.
-   Chat với PDF.
-   Giải thích abstract, methods, results, conclusion.
-   Trích xuất dữ liệu từ paper.
-   Hỗ trợ AI Writer.
-   Tìm research topic / research gap.
-   Paraphrase.
-   Citation generation.
-   AI detection.
-   Deep search.
-   Lựa chọn nguồn dữ liệu nghiên cứu.
-   Xuất kết quả thành report, manuscript, visualization, PowerPoint,
    Word hoặc PDF.
-   Chrome extension và ứng dụng di động để tương tác với tài liệu.
-   Library để lưu nội dung nghiên cứu.

Điểm phương pháp luận đáng chú ý không phải chỉ là số lượng tính năng,
mà là workflow:

``` text
Research Question
      ↓
Query Formulation
      ↓
Evidence Retrieval
      ↓
Paper Understanding
      ↓
Evidence Extraction
      ↓
Evidence Synthesis
      ↓
Artifact
```

Một nguyên tắc quan trọng trong workflow là chuẩn hóa câu hỏi nghiên cứu
trước khi tìm kiếm. Thay vì một câu hỏi quá rộng, cần xác định các
dimension như:

``` text
topic
population
geography
time range
study type
```

Ví dụ thay vì:

> Tổng quan về nghiên cứu triển khai và nghiên cứu can thiệp.

Cần tiến về một câu hỏi cụ thể hơn theo vấn đề, địa điểm/phạm vi và
khoảng thời gian.

Sau retrieval, workflow có thể chuyển sang phân tích từng paper theo các
trường:

``` text
abstract
study design
participants
sample size
inclusion criteria
exclusion criteria
intervention
comparator
outcomes
methods
statistical analysis
results
conclusion
limitations
```

### 2. Phân tích skill/repository hiện tại

Skill/repository `sci-papers-downloder` hiện tại về bản chất tập trung
vào một pipeline hẹp:

``` text
Natural-language intent
        ↓
quantity / freshness mapping
        ↓
Scopus Search
        ↓
metadata + DOI
        ↓
Unpaywall
        ↓
PDF
```

Điểm mạnh đáng giữ lại là **deterministic intent mapping**.

Ví dụ một yêu cầu kiểu:

``` text
latest 8 papers
```

có thể được ánh xạ rõ ràng thành tham số thực thi thay vì để model tự
quyết định tùy ý.

Đây là một pattern đặc biệt phù hợp cho bản strict.

### 3. Hai sản phẩm cần xây

Đã thống nhất rằng cần xây **hai dạng skill khác nhau**, không trộn lẫn.

#### Dạng A --- Strict Scientific Paper Research Skill

Mục tiêu:

> Dành cho AI/model có tư duy không cao hoặc độ thông minh thấp; hạn chế
> tối đa sự sáng tạo, suy diễn và linh hoạt.

Đặc điểm:

-   Workflow được định hướng gần như toàn bộ từ trước.
-   Model không đóng vai trò research strategist.
-   Model chủ yếu phân loại intent và điền slot.
-   Các quyết định quan trọng nằm trong rule, schema, enum, lookup table
    và script.
-   Input nào tương ứng với workflow nào phải được quy định rõ.
-   Không tự mở rộng yêu cầu của user.
-   Không tự đổi chiến lược khi tool thất bại nếu fallback chưa được
    khai báo.
-   Output có schema cố định.

Đây là ưu tiên thiết kế hiện tại.

#### Dạng B --- Research Harness Skill

Dạng thứ hai sẽ linh hoạt và có khả năng compose workflow nghiên cứu:

``` text
research.search
research.acquire
research.read
research.extract
research.synthesize
research.export
```

Có thể dùng router để tạo các pipeline khác nhau như search paper,
download, understand paper, literature review và research-gap analysis.

Dạng B chưa phải phần cần triển khai trước. Trước mắt tập trung hoàn
thiện Dạng A.

------------------------------------------------------------------------

# Scientific Paper Research --- Strict Skill

## 4. Design philosophy

Triết lý trung tâm:

``` text
LLM = parser
LLM ≠ research strategist
```

Model chỉ nên làm những nhiệm vụ mà model buộc phải làm, ví dụ:

``` text
classification
slot extraction
formatting
```

Các hành vi có thể deterministic phải chuyển khỏi reasoning của LLM
sang:

``` text
rules
lookup tables
schemas
enums
validators
scripts
```

Pipeline tổng quát:

``` text
USER INPUT
    ↓
CLASSIFY INTO FIXED MODE
    ↓
VALIDATE REQUIRED INPUTS
    ↓
NORMALIZE USING FIXED RULES
    ↓
EXECUTE ONLY ALLOWED ACTIONS
    ↓
RETURN FIXED OUTPUT
```

Model không được tự chọn chiến lược nghiên cứu.

------------------------------------------------------------------------

## 5. Fixed execution modes

Phiên bản đầu đề xuất sáu mode.

  -----------------------------------------------------------------------
  Mode                    Trigger                 Allowed behavior
  ----------------------- ----------------------- -----------------------
  `TOPIC_SEARCH`          User cung cấp tên đề    Parse topic → tạo
                          tài/chủ đề              keyword theo rule →
                                                  search

  `KEYWORD_SEARCH`        User cung cấp keyword   Search đúng
                          cụ thể                  keyword/query

  `DOI_DOWNLOAD`          User cung cấp DOI hoặc  Chỉ resolve/download
                          danh sách DOI           đúng DOI

  `TITLE_DOWNLOAD`        User cung cấp           Resolve title → DOI →
                          title/list title        download

  `PAPER_ANALYSIS`        User cung cấp một       Phân tích paper theo
                          PDF/paper               schema cố định

  `BATCH_ANALYSIS`        User cung cấp nhiều     Extract cùng một schema
                          PDF/paper               cho tất cả
  -----------------------------------------------------------------------

### DOI_DOWNLOAD

Ví dụ input:

``` text
10.1016/j.xxx
10.1001/xxx
10.1038/xxx
```

Phải deterministic route:

``` text
DOI_DOWNLOAD
```

Allowed pipeline:

``` text
validate DOI
→ resolve allowed source
→ download
→ verify
→ report success/failure
```

Không được:

``` text
search related papers
add alternative papers
replace DOI
expand topic
perform literature review
generate additional recommendations
```

Nguyên tắc:

> Nếu user đưa DOI thì DOI là tập paper đóng. Skill chỉ xử lý đúng tập
> DOI user cung cấp.

------------------------------------------------------------------------

## 6. Topic handling

Nếu user chỉ cung cấp tên đề tài, model không được tự do brainstorm một
search strategy.

Ví dụ:

> Ứng dụng trí tuệ nhân tạo trong phát hiện ung thư phổi trên CT.

Pipeline:

``` text
TITLE/TOPIC
     ↓
Extract concepts
     ↓
Map concepts → fixed search blocks
     ↓
Map concepts → canonical terms
     ↓
Apply approved synonym policy
     ↓
Compile exact query
     ↓
Search
```

Intermediate representation có thể là:

``` yaml
topic:
  original: "Ứng dụng trí tuệ nhân tạo trong phát hiện ung thư phổi trên CT"

concepts:
  technology:
    required: true
    canonical_term: "artificial intelligence"

  disease:
    required: true
    canonical_term: "lung cancer"

  modality:
    required: true
    canonical_term: "computed tomography"
```

Query tối thiểu:

``` text
("artificial intelligence")
AND
("lung cancer")
AND
("computed tomography")
```

Model không tự nghĩ thêm synonym.

Nếu sử dụng synonym, synonym phải đến từ nguồn đã được phê duyệt trước.

Ví dụ:

``` yaml
artificial_intelligence:
  allowed_synonyms:
    - "artificial intelligence"
    - "machine learning"
    - "deep learning"

computed_tomography:
  allowed_synonyms:
    - "computed tomography"
    - "CT"
```

Compiler mới được tạo:

``` text
(
  "artificial intelligence"
  OR "machine learning"
  OR "deep learning"
)
AND
(
  "lung cancer"
)
AND
(
  "computed tomography"
  OR "CT"
)
```

Điểm quan trọng:

> LLM chỉ extract concept. Search query được compile bằng policy.

------------------------------------------------------------------------

## 7. Exact keyword handling

Nếu user cung cấp exact keywords hoặc exact query:

``` text
KEYWORD_SEARCH
```

Nguyên tắc mặc định:

``` text
preserve user keywords
```

Skill không được tự:

-   thay keyword;
-   dịch keyword;
-   thêm synonym;
-   bỏ keyword;
-   đổi Boolean operator;
-   mở rộng concept;
-   thu hẹp concept;

trừ khi rule của mode đó cho phép rõ ràng.

Nếu hệ thống cần normalization kỹ thuật như trim whitespace hoặc
canonicalize dấu ngoặc, normalization không được làm thay đổi semantic
query.

------------------------------------------------------------------------

## 8. Strict non-negotiable rules

``` markdown
## NON-NEGOTIABLE RULES

1. NEVER expand the user's research scope unless an explicit rule permits it.

2. NEVER invent search keywords.

3. NEVER add synonyms unless they exist in an approved synonym table
   or an explicitly permitted terminology source.

4. If the user provides DOI values:
   - enter DOI_DOWNLOAD mode;
   - process only those DOI values;
   - never search for related papers.

5. If the user provides exact keywords:
   - preserve them;
   - do not replace them with inferred alternatives.

6. If the user provides only a topic/title:
   - extract concepts using the fixed topic schema;
   - generate queries only through approved query templates.

7. NEVER silently change:
   - year range;
   - geography;
   - population;
   - intervention/exposure;
   - comparator;
   - outcome;
   - study type;
   - language;
   - document type;
   - result count.

8. Missing required information must trigger either:
   - a predefined default; or
   - a predefined clarification rule.

9. Tool failure MUST NOT cause strategy switching unless a fallback
   is explicitly defined for that operation.

10. Output MUST follow the mode-specific schema.

11. NEVER claim that a paper was read in full if only metadata or
    abstract was available.

12. NEVER substitute a failed requested paper with a different paper.

13. NEVER add papers to a closed DOI/title set unless the user
    explicitly requests expansion.

14. NEVER perform an additional research task merely because it
    appears useful.

15. Every mode MUST execute only its declared allowed pipeline.
```

------------------------------------------------------------------------

## 9. Deterministic defaults

Các từ tự nhiên có tính mơ hồ nên được map thành policy thay vì để model
suy luận.

Ví dụ:

``` yaml
freshness:
  latest:
    sort: publication_date_desc
    default_year_window: 3

  recent:
    sort: publication_date_desc
    default_year_window: 5
```

Các con số trên mới là đề xuất ban đầu; cần chốt thành product policy
trước khi triển khai.

Tương tự cần định nghĩa:

``` yaml
defaults:
  result_count: TBD
  language: TBD
  document_type: TBD
  year_window: TBD
  sort: TBD
```

Không để model tự đặt default khác nhau giữa các lần chạy.

------------------------------------------------------------------------

## 10. Paper acquisition

Phần download nên được tách thành deterministic acquisition resolver.

Concept:

``` text
DOI
 │
 ├─► Open-access resolver
 ├─► Publisher OA
 ├─► PubMed Central
 ├─► Europe PMC
 ├─► Preprint repository
 ├─► Institutional repository
 │
 └─► metadata/abstract only
```

Một nguồn không thành công không đồng nghĩa model được quyền tự nghĩ ra
chiến lược mới.

Fallback chain phải được khai báo trong configuration.

Ví dụ:

``` yaml
acquisition:
  fallback_order:
    - unpaywall
    - publisher_open_access
    - pubmed_central
    - europe_pmc
    - approved_preprint_repository
    - metadata_only
```

Nếu không có full text:

``` json
{
  "full_text_available": false,
  "evidence_level": "abstract_only"
}
```

Điều này ngăn downstream model nói như thể đã đọc toàn văn.

------------------------------------------------------------------------

## 11. Paper analysis schema

`PAPER_ANALYSIS` không nên trả một bài văn tự do trước tiên.

Nó nên extract structured evidence.

Ví dụ:

``` json
{
  "paper_id": "...",
  "doi": "...",
  "title": "...",
  "study_design": "...",
  "population": "...",
  "sample_size": null,
  "intervention": "...",
  "comparator": "...",
  "outcomes": [],
  "inclusion_criteria": [],
  "exclusion_criteria": [],
  "methods": [],
  "statistical_methods": [],
  "key_results": [],
  "conclusions": [],
  "limitations": [],
  "full_text_available": true,
  "evidence_locations": []
}
```

Nếu thông tin không có:

``` json
"sample_size": null
```

thay vì đoán.

Rule:

``` text
NOT FOUND ≠ INFER
```

------------------------------------------------------------------------

## 12. Provenance

Một harness nghiên cứu khoa học cần phân biệt rõ:

``` text
metadata-derived
abstract-derived
full-text-derived
model-inferred
```

Bản strict lý tưởng nên hạn chế hoặc vô hiệu hóa `model-inferred` đối
với evidence extraction.

Ví dụ:

``` json
{
  "study_design": {
    "value": "randomized controlled trial",
    "source": "full_text",
    "location": "Methods"
  }
}
```

Nếu không xác định được:

``` json
{
  "study_design": {
    "value": null,
    "source": null,
    "status": "not_found"
  }
}
```

Không tự suy luận chỉ vì paper "có vẻ là RCT".

------------------------------------------------------------------------

## 13. Separation between strict skill and intelligent harness

Không nên cố làm một `SKILL.md` phục vụ cả hai mục tiêu.

### Strict skill

``` text
User
 ↓
Intent classifier
 ↓
Fixed mode
 ↓
Validator
 ↓
Deterministic pipeline
 ↓
Structured output
```

### Intelligent harness sau này

``` text
User
 ↓
Research Router
 ↓
Planner
 ├── search
 ├── acquire
 ├── read
 ├── extract
 ├── compare
 ├── synthesize
 └── export
```

Harness linh hoạt sau này có thể có primitives:

``` text
research.search
research.acquire
research.read
research.extract
research.synthesize
research.export
```

và compose thành workflow như:

``` yaml
search_papers:
  pipeline:
    - formulate_query
    - search
    - rank

download_papers:
  pipeline:
    - formulate_query
    - search
    - acquire

understand_paper:
  pipeline:
    - parse
    - extract
    - answer

literature_review:
  pipeline:
    - formulate_query
    - search
    - rank
    - acquire
    - parse
    - extract
    - synthesize

research_gap:
  pipeline:
    - formulate_query
    - search
    - acquire
    - extract
    - compare
    - identify_gaps
```

Nhưng **đây không phải behavior của strict skill**.

------------------------------------------------------------------------

## 14. Architecture direction

Strict skill nên tiến tới cấu trúc kiểu:

``` text
scientific-paper-research/
│
├── SKILL.md
│
├── config/
│   ├── defaults.yaml
│   ├── modes.yaml
│   ├── synonyms.yaml
│   ├── acquisition.yaml
│   └── output-contracts.yaml
│
├── schemas/
│   ├── request.schema.json
│   ├── topic.schema.json
│   ├── paper.schema.json
│   └── evidence.schema.json
│
├── scripts/
│   ├── classify_input.py
│   ├── validate_request.py
│   ├── compile_query.py
│   ├── search.py
│   ├── acquire.py
│   ├── parse_paper.py
│   └── extract_evidence.py
│
└── tests/
    ├── routing/
    ├── queries/
    ├── acquisition/
    └── outputs/
```

Mục tiêu kiến trúc:

> Những gì có thể biểu diễn bằng code/config thì không giao cho LLM
> quyết định.

------------------------------------------------------------------------

## 15. Ví dụ end-to-end

### Case A --- DOI list

Input:

``` text
Tải giúp tôi:
10.xxxx/aaa
10.xxxx/bbb
10.xxxx/ccc
```

Route:

``` text
DOI_DOWNLOAD
```

Execution:

``` text
parse DOI
→ validate DOI
→ acquire DOI #1
→ acquire DOI #2
→ acquire DOI #3
→ verify downloaded files
→ return download report
```

Không search.

Không tìm alternative papers.

Không literature review.

------------------------------------------------------------------------

### Case B --- Exact keywords

Input:

``` text
Search:
("lung cancer") AND ("computed tomography")
```

Route:

``` text
KEYWORD_SEARCH
```

Execution:

``` text
preserve query
→ apply explicit filters only
→ search
→ deterministic sort
→ return results
```

Không tự thêm:

``` text
AI
deep learning
pulmonary neoplasm
CT screening
```

------------------------------------------------------------------------

### Case C --- Research topic

Input:

``` text
Ứng dụng trí tuệ nhân tạo trong phát hiện ung thư phổi trên CT
```

Route:

``` text
TOPIC_SEARCH
```

Execution:

``` text
extract fixed concept slots
→ canonical terminology lookup
→ approved synonym lookup
→ query compiler
→ search
```

LLM không viết search strategy tự do.

------------------------------------------------------------------------

### Case D --- PDF analysis

Input:

``` text
Phân tích phương pháp nghiên cứu của paper này.
```

Route:

``` text
PAPER_ANALYSIS
```

Execution:

``` text
parse paper
→ locate methods
→ extract fixed fields
→ attach evidence locations
→ return schema
```

Không tự chuyển sang:

``` text
literature review
related paper search
research gap
proposal generation
```

------------------------------------------------------------------------

## 16. Các quyết định còn chưa chốt

Hai quyết định đầu tiên cần khóa trước khi viết production `SKILL.md`:

### Decision 1 --- Synonym policy

Hai lựa chọn:

**A. Ultra-strict**

``` text
one concept
→ one canonical term
```

Không synonym nếu user không cung cấp.

**B. Strict controlled expansion**

``` text
one concept
→ canonical term
→ approved synonym whitelist
```

Model không tự tạo synonym.

Đề xuất hiện tại:

> **B --- Strict controlled expansion**, vì vẫn deterministic nhưng
> recall tốt hơn đáng kể.

### Decision 2 --- Missing parameters

Ví dụ user không nói:

``` text
year range
number of papers
language
study type
```

Hai lựa chọn:

**A. Clarification-first**

Thiếu parameter bắt buộc → hỏi user.

**B. Fixed-default**

Thiếu parameter → lấy từ `defaults.yaml`.

Đề xuất hiện tại:

> Dùng **fixed defaults cho các parameter an toàn và phổ thông**, còn
> các parameter có khả năng thay đổi bản chất research question thì hỏi
> lại.

Ví dụ:

``` yaml
can_default:
  result_count: true
  sort: true

must_not_silently_default:
  population: true
  geography: true
  intervention: true
  comparator: true
  study_type: true
```

------------------------------------------------------------------------

# Kết luận hiện tại

Mục tiêu trước mắt không phải tạo một AI researcher thông minh.

Mục tiêu là tạo:

> **`scientific-paper-research` --- một deterministic scientific
> research skill có behavior bị giới hạn chặt, phù hợp với model
> reasoning thấp và cho kết quả có thể dự đoán, kiểm thử và tái lập.**

Nguyên tắc thiết kế trung tâm:

``` text
MODEL DECIDES LESS
CODE DECIDES MORE
```

và:

``` text
User intent
→ fixed mode
→ fixed contract
→ fixed pipeline
→ fixed output
```

Sau khi strict skill ổn định mới phát triển sản phẩm thứ hai:

> **Scientific Research Harness**

với khả năng planning, composition, evidence synthesis và research
workflow linh hoạt hơn.
