# Research Protocol

## Social Networks and Content Dissemination: A Case Study of the Diabetic Reddit Community

Researchers: Mihir Deshpande and Sanya Gangwani

Supervisor: Prof. Lipika Dey

Course: CS-IS-3103

Institution: Ashoka University

Protocol version: 1.0 – November 2026

Status: Draft for supervisor review and institutional ethics/access determination

---

## 1. Study Overview

This study investigates how health-related content circulates within online Type 1 Diabetes (T1D) communities on Reddit. It examines the relationship between content characteristics, visible engagement, interaction networks and discussion structures.

The research combines three areas:

1. Social-media recommendation and ranking mechanisms.

2. Social-network structure and content-diffusion theory.

3. The informational, emotional and behavioural role of online chronic-illness communities.

The study will use publicly accessible Reddit material, subject to platform-authorised access and institutional ethics requirements. Interview-derived themes supplied by the research team will provide contextual grounding for the content-classification framework. They will not be treated as a substitute for the Reddit dataset.

## 2. Research Questions

### Primary research question

How do the network structure of the diabetic Reddit community and engagement-driven ranking relate to which health content spreads widely and which stays contained, and what does that mean for patients who learn from it?

### Secondary research questions

- RQ1 – Content: What recurring themes, content types and evidence characteristics appear in the selected Reddit communities?

- RQ2 – Dissemination: Which types of content receive greater visible engagement and which remain relatively contained?

- RQ3 – Network: What interaction patterns and network structures characterise the community?

- RQ4 – Explanation: How much of the observed variation in dissemination is associated with content characteristics versus process and network characteristics?

- RQ5 – Patients: What might the composition of highly visible content imply for people who rely on online communities for informal diabetes-related learning?

## 3. Study Design

The project will use an observational computational case-study design.

Two complementary datasets are proposed:

A. Historical corpus

A collection of Reddit posts and their associated comment trees over a fixed historical period. This corpus will support content classification, engagement analysis, thread-tree analysis and network construction.

B. Prospective corpus (conditional)

Repeated observations of subreddit listings and post trajectories over time. This component will be undertaken only if authorised access, technical feasibility and institutional approval permit it.

The prospective corpus is intended to provide a proxy for ranking visibility. It will not measure actual individual impressions or exposure.

No experimental manipulation, direct intervention or recruitment of Reddit users is proposed in the current design.

## 4. Proposed Data Sources and Sampling

### 4.1 Subreddits

The proposed collection scope is:

- r/diabetes_t1 – primary community, subject to verification of its existence, activity and suitability.

- r/diabetes – broader diabetes community.

- r/diabetes_t2 – optional contrast dataset for network structure only; not included in the primary content-classification analysis.

The final subreddit list will be confirmed with the supervisor before collection.

### 4.2 Historical sampling period

The proposed sampling window is a fixed 12-month period.

The initial target is at least 3,000 posts, subject to data availability and authorised access.

Posts less than 14 days old at the point of collection will be excluded from the historical engagement analysis to allow time for visible engagement to accumulate.

Where API listing limits constrain collection, the sampling strategy will document the discovery method for each post, including New, Hot, Top listings and permitted keyword searches.

The researchers will report the resulting sampling limitations and will not describe a convenience or supplemented sample as a complete census.

### 4.3 Prospective sampling

If feasible and authorised, the prospective collection will record selected Hot and New listings at regular intervals.

Proposed fields include post ID, observed rank, score, comment count, upvote ratio and observation timestamp.

Post trajectories will be observed at approximately 1 hour, 6 hours, 24 hours, 72 hours and 7 days after creation.

This module will be omitted if access or operational requirements cannot be satisfied.

## 5. Data to Be Collected

Subject to platform permissions and ethics approval, the proposed post-level fields are:

- Post identifier

- Subreddit

- Creation timestamp

- Title and text body

- Flair

- Score and upvote ratio, where available

- Number of comments

- Crosspost information, where available

- Self-post and media indicators

- Collection timestamp

- Discovery method

Proposed comment-level fields include:

- Comment identifier

- Parent post identifier

- Parent comment identifier

- Creation timestamp

- Score, where available

- Comment depth

- Text body

Author identifiers will be pseudonymised at ingestion using a consistent hashing procedure. The original identifiers and any hashing secret will not be placed in the public research repository.

Only fields necessary to answer the research questions will be retained.

## 6. Data Processing and Exclusion

The processing pipeline will include:

1. Validation of unique identifiers and parent-child relationships.

2. Removal of duplicate records.

3. Conversion of timestamps to UTC.

4. Identification of deleted, removed and unavailable content.

5. Identification and exclusion of automated accounts where reliably detectable.

6. Construction of comment trees and user interaction networks.

7. Pseudonymisation of author identifiers.

8. Documentation of missing records and exclusion decisions.

Deleted or removed records will be handled transparently. Their presence and frequency may be reported in aggregate where feasible, but unavailable text will not be reconstructed.

Raw data will remain separate from processed analytical datasets.

## 7. Content Classification Framework

The initial thematic framework is derived from the supplied interview synthesis. These categories will be treated as sensitising concepts rather than an exhaustive taxonomy.

### Theme classification

- T1 – The mental math never stops.

- T2 – Overnight is the frontier of fear.

- T3 – Cost creates stratified access.

- T4 – Hardware friction is constant.

- T5 – The emotional burden is invisible to the outside world.

- T6 – Self-taught by default; endo support is thin.

- X – Emergent themes identified during pilot coding.

- OTH – Other or off-topic content.

Each post will receive a primary theme. A secondary theme may be assigned when a distinct additional topic is clearly present.

### Additional classification fields

Content type: Personal experience, question or request for help, advice or recommendation, sourced information, emotional expression or support, or other.

Evidence status: Supported, unsupported, contradicts guidance, unclear, or not applicable to non-claim-bearing content.

Emotional intensity and tone: Intensity on a three-level scale and a dominant tone category.

Evidence status will be distinguished from emotional tone. The researchers are not acting as clinicians. Uncertain cases will be labelled unclear, and any contradiction-of-guidance classification will require additional review.

## 8. Annotation and Reliability

A proposed gold-standard sample of 500 posts will be drawn from the historical primary subreddit corpus, stratified by month.

The plan is to independently double-code 120 posts and divide the remaining 380 between the two researchers.

A pilot of 40 jointly coded posts will be used to refine the codebook before full annotation.

Inter-coder reliability will be assessed using:

- Cohen's kappa for categorical fields.

- Weighted kappa for ordinal emotional intensity.

A target of 0.60 or higher is proposed. If reliability is inadequate, categories and definitions will be revised and the relevant overlapping sample will be re-coded.

Any automated labelling approach will be validated against held-out human annotations. Corpus-wide use will depend on pre-specified performance criteria, including macro-F1 and agreement with human labels.

## 9. Analytical Methods

### Content and engagement

The study will describe theme, content-type, evidence-status and emotional-tone distributions.

Visible engagement measures will include scores, comment counts and unique participants where available.

### Discussion and diffusion

Thread-level analysis will include:

- Number of comments and participants.

- Maximum depth and breadth.

- Mean depth.

- Wiener index / structural virality.

- Reply structure and discussion-tree characteristics.

Structural virality will be treated as a property of observed discussion structure, not as a direct measure of impressions or actual exposure.

### Network analysis

A directed, weighted user-reply network will be constructed, with edges from the replier to the author of the post or comment being answered.

Proposed measures include degree, weighted degree, density, reciprocity, connected components, PageRank, Louvain communities, modularity, k-core and degree assortativity.

Where appropriate, observed network structure will be compared against degree-preserving rewired null networks.

### Statistical modelling

Engagement outcomes will be analysed using models appropriate to their distributions, including negative-binomial and hurdle models where justified.

Potential predictors include theme, content type, evidence status, emotional intensity, text length, post age, time of posting, media, flair, subreddit and author activity.

Robustness checks will include outlier sensitivity, text-only analyses and comparisons between human-labelled and model-labelled data.

### Ranking and visibility

If prospective observations are available, the analysis will examine early engagement trajectories, observed Hot-list rank and visibility composition.

A visibility-skew measure will compare the share of a category in observed Hot listings with its share in the overall corpus.

These observations will be interpreted as ranking-exposure proxies, not true individual exposure.

## 10. Ethical Considerations

The material concerns health-related discussions and may contain sensitive personal experiences.

Before collection begins, the researchers will seek guidance from the supervisor and the appropriate Ashoka University ethics-review authority regarding the need for formal review, exemption or another institutional determination.

The research will:

- Use only an access method authorised under applicable Reddit terms.

- Avoid direct contact with Reddit users unless separately approved.

- Avoid publishing usernames, account identifiers or identifiable personal details.

- Report aggregate findings.

- Avoid reproducing verbatim posts or comments in the report.

- Use paraphrased or constructed examples where illustration is necessary.

- Restrict access to raw data to authorised research-team members.

- Document deletion, retention and access-control procedures.

- Avoid making clinical judgments or recommendations about individual users.

Interview-derived material will be used only to the extent permitted by the relevant consent and institutional requirements. If consent for academic use is unclear, the team will restrict use to the six aggregate thematic labels without quotes or personal details.

## 11. Data Management

Raw, processed and analytical datasets will be maintained separately.

The research repository will contain code, documentation, codebooks, aggregate outputs and permitted derived data. Raw Reddit data and credentials will not be published.

The researchers will maintain a data collection log, record dataset versions, document transformations and use fixed random seeds where applicable.

The final retention and deletion schedule will be confirmed with the supervisor and institutional requirements before collection.

## 12. Limitations

The study is limited by:

- The use of a single platform and selected communities.

- Incomplete access to historical Reddit material.

- Deleted, removed or unavailable content.

- The absence of individual-level impression data.

- Potential self-selection into online communities.

- The limits of non-clinician evidence-status coding.

- The transferability of interview-derived themes to Reddit.

- The observational nature of the analysis.

The researchers will not claim that Reddit's ranking algorithm caused observed engagement patterns. Results will be described as associations, observations or patterns consistent with proposed mechanisms.

## 13. Research Outputs

The expected outputs are:

1. A reproducible research dataset and documented processing pipeline, subject to data-sharing permissions.

2. A transparent content codebook and annotation reliability report.

3. Content and engagement analysis.

4. User interaction networks and discussion-tree analysis.

5. Statistical models and robustness checks.

6. A mechanism-evidence table distinguishing documented platform mechanisms from observed associations.

7. A final ISM research report and joint presentation.

---

Approval status: This protocol is a working research document. Subreddit scope, access method, collection period, ethics requirements, data-retention rules and final analytical decisions remain subject to supervisor and institutional review.
