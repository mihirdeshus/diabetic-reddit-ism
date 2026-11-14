# Data Management Plan

## Social Networks and Content Dissemination: A Case Study of the Diabetic Reddit Community

Researchers: Mihir Deshpande and Sanya Gangwani

Supervisor: Prof. Lipika Dey

Course: CS-IS-3103

Institution: Ashoka University

Document version: 1.0 – November 2026

Status: Draft for supervisor review and institutional determination

---

## 1. Purpose and Scope

This document describes how research data will be collected, organised, processed, stored, protected, analysed, retained and shared for the ISM project, “Social Networks and Content Dissemination: A Case Study of the Diabetic Reddit Community”.

The plan covers the proposed Reddit post and comment corpus, derived analytical datasets, annotation data, interview-derived thematic material supplied to the research team, code, and research outputs.

All collection and processing activities are conditional on authorised access, applicable Reddit terms and policies, and any required Ashoka University ethics review or institutional determination.

## 2. Data Categories

The project may handle the following categories of data:

### 2.1 Reddit source data

Subject to authorised access and approval:

- Post identifiers and subreddit names.
- Post creation timestamps, titles, text and available metadata.
- Comment identifiers, parent identifiers, timestamps, text and available metadata.
- Engagement fields such as scores, comment counts and upvote ratios, where available.
- Listing observations, such as observed rank and collection timestamp, if the prospective component is approved and feasible.

### 2.2 Pseudonymised analytical data

Data prepared for analysis may include:

- Pseudonymised author identifiers.
- Cleaned post and comment records.
- Comment-tree relationships.
- User interaction network edge and node tables.
- Content labels, theme classifications and annotation records.
- Aggregated engagement and network measures.

### 2.3 Interview-derived thematic material

The project may use the six aggregate themes supplied to the research team as contextual input to the content-classification framework:

- T1 – The mental math never stops.
- T2 – Overnight is the frontier of fear.
- T3 – Cost creates stratified access.
- T4 – Hardware friction is constant.
- T5 – The emotional burden is invisible to the outside world.
- T6 – Self-taught by default; endo support is thin.

Interview transcripts, names, contact details or identifiable participant-level information will not be added to the repository. Any use beyond the aggregate themes will depend on the relevant consent and institutional requirements.

### 2.4 Research and software records

The repository may contain source code, documentation, codebooks, literature-search records, data dictionaries, analysis scripts, synthetic test data, aggregate tables and figures.

## 3. Data Collection

Data will be collected only through methods authorised under applicable Reddit terms and platform requirements.

Before collection begins, the researchers will confirm:

- Which subreddits are in scope.
- The historical sampling period and prospective observation schedule, if applicable.
- Which fields are necessary for the research questions.
- Whether the proposed access method is permitted.
- Whether institutional ethics review, exemption or another determination is required.

A collection log will record the date, collection method, subreddit, sampling window, fields collected, software version and any collection errors or exclusions.

The researchers will not attempt to bypass access controls, rate limits or platform restrictions.

## 4. Data Minimisation and Pseudonymisation

Only fields necessary to answer the research questions will be retained.

Author identifiers will be pseudonymised at ingestion using a consistent hashing procedure, if retaining a stable author-level identifier is approved and necessary for the analysis.

The original usernames and the secret used for hashing will be stored separately from analytical data, with access restricted to authorised research-team members. Neither the original identifiers nor the hashing secret will be committed to GitHub or included in public outputs.

Pseudonymised data will still be treated as potentially sensitive because it may permit linkage across records.

## 5. Data Storage and Access Control

The project repository will contain code, documentation, codebooks, synthetic test data and permitted aggregate or derived outputs.

Raw source data, credentials, API tokens, original usernames and hashing secrets will not be stored in the public repository.

Working data will be stored in access-controlled locations approved by the research team and institution. Access will be limited to the researchers and other individuals explicitly authorised for the project.

The researchers will use environment variables or an untracked local environment file for credentials where credentials are required. Such files will be excluded through `.gitignore`.

## 6. Data Processing and Quality Control

The processing pipeline will:

1. Validate unique identifiers and post/comment relationships.
2. Check that comment parents exist and belong to the appropriate discussion.
3. Convert timestamps to UTC.
4. identify duplicates and document their treatment.
5. Identify unavailable, deleted or removed records without reconstructing unavailable text.
6. Identify automated accounts only where there is a reliable basis for doing so.
7. Pseudonymise author identifiers where approved.
8. Construct comment trees and user interaction networks.
9. Record missing values, exclusions and transformations.

Validation scripts and processing decisions will be documented so that the analysis can be reproduced without publishing restricted raw data.

## 7. Data Sharing and Publication

The public repository may contain:

- Source code and installation instructions.
- Research protocol and this data management plan.
- Codebooks and annotation instructions.
- Synthetic datasets used for testing.
- Aggregate statistics, tables and figures.
- Documentation of data processing and analytical methods.

Raw Reddit posts, raw comments, usernames, credentials, hashing secrets and other restricted or identifiable data will not be published.

Derived data will be shared only where permitted by platform terms, institutional requirements and the ethical basis for the research. The researchers will not assume that publicly viewable content is automatically unrestricted for redistribution.

Reports and presentations will prioritise aggregate results and avoid verbatim or searchable quotations from individual posts and comments.

## 8. Data Retention and Deletion

The final retention period and deletion procedure will be confirmed with the supervisor and relevant institutional requirements before collection begins.

At the end of the project, the researchers will review:

- Which raw and derived data must be retained.
- Which data must be deleted.
- Whether any data can be retained for verification or reproducibility.
- Whether deletion is required by platform terms or institutional direction.

Deletion decisions and dates will be documented. No retention period is being claimed as approved in this draft.

## 9. Backup and Version Control

Code and documentation will be maintained using Git.

The repository will not be used as a backup location for raw Reddit data, personal information, credentials or hashing secrets.

The researchers will maintain versioned copies of approved documentation and record major changes to data-processing scripts. Fixed random seeds will be used where appropriate.

## 10. Responsibilities

The researchers, Mihir Deshpande and Sanya Gangwani, are responsible for following this plan, protecting project data, maintaining the collection and processing logs, and reporting any data-management concerns to the supervisor.

The supervisor and relevant institutional authority will provide direction on institutional requirements and any required changes to the plan.

## 11. Review and Updates

This plan is a working document. It will be updated when the data sources, collection methods, access permissions, ethics determination, storage arrangements or retention requirements are confirmed.

No data collection should begin until the required platform and institutional conditions have been satisfied.
