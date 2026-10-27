# CSET-455 Agile Software Development — Lab Assignment 09

## JQL Custom Filters and Board Quick Filters

**Scenario:** ShopEase e-commerce application  
**Date checked:** 27 October 2026

> **Environment note:** The connected Jira site currently has no ShopEase project and no project key `SHOP`. Replace `SHOP` below with the actual ShopEase project key before running the queries. Do not use an unrelated Jira project as a substitute.

## Objectives

- Save useful JQL searches as custom filters.
- Share saved filters using least-privilege viewer/editor permissions.
- Use saved filters or board Quick Filters to narrow the issues shown on a board.

## Task 1 — Three custom filters

### 1. ShopEase — In Progress Issues

```jql
project = SHOP AND status = "In Progress"
```

Shows issues in ShopEase currently being worked on.

### 2. ShopEase — All Bugs

```jql
project = SHOP AND issuetype = Bug
```

Shows all Bug-type issues in ShopEase, regardless of status.

### 3. ShopEase — Pending Issues

```jql
project = SHOP AND status NOT IN (Done, Cancelled)
```

Excludes issues whose status is Done or Cancelled; other statuses such as To Do and In Progress may remain. Confirm exact status names in the project workflow.

## Task 2 — Sharing permissions

| Filter | Viewers | Editors | Reason |
|---|---|---|---|
| ShopEase — In Progress Issues | ShopEase project/team or appropriate project role/group | Scrum Master or trusted co-owner only | Team can run the filter without broad edit rights |
| ShopEase — All Bugs | ShopEase project/team or appropriate project role/group | Scrum Master or trusted co-owner only | Team can track defects without changing the query |
| ShopEase — Pending Issues | ShopEase project/team or appropriate project role/group | Scrum Master or trusted co-owner only | Team can review unfinished work while protecting the query |

Filter sharing does not grant permission to browse the underlying Jira issues. Verify access by asking an authorized teammate to open and run the shared filter. Keep experimental filters private.

## Task 3 — Board quick filters / JQL search

If the board exposes Quick Filters configuration, create these shortcuts:

- **In Progress:** `project = SHOP AND status = "In Progress"`
- **Bugs:** `project = SHOP AND issuetype = Bug`
- **Pending:** `project = SHOP AND status NOT IN (Done, Cancelled)`

If the Jira version exposes a Custom Filter selector instead, choose one of the saved filters. Confirm the displayed issues match the JQL.

## JQL operator reference

| Operator | Meaning | Example |
|---|---|---|
| `=` | Matches | `issuetype = Bug` |
| `!=` | Does not match | `status != Done` |
| `IN` | Matches any listed value | `status IN (Done, "In Progress")` |
| `NOT IN` | Excludes listed values | `status NOT IN (Done, Cancelled)` |
| `AND` | Both conditions must match | `project = SHOP AND issuetype = Bug` |
| `OR` | Either condition may match | `status = Done OR status = Cancelled` |
| `ORDER BY` | Sorts results | `ORDER BY created DESC` |

## Submission checklist — seven screenshots

- [ ] Screenshot 1 — First filter creation, name and JQL visible.
- [ ] Screenshot 2 — At least three saved custom filters visible.
- [ ] Screenshot 3 — Filter sharing permissions, including Viewers and Editors if configured.
- [ ] Screenshot 4 — Shared filter opened by an authorized teammate.
- [ ] Screenshot 5 — ShopEase board with a saved filter applied.
- [ ] Screenshot 6 — JQL entered in the JQL option and the resulting issue list.
- [ ] Screenshot 7 — Final results for a query such as all ShopEase bugs.

## Completion steps

1. Open Jira issue search and choose Advanced/JQL.
2. Replace `SHOP` with the true ShopEase key; run Query 1 and save it as **ShopEase — In Progress Issues**.
3. Repeat for **ShopEase — All Bugs** and **ShopEase — Pending Issues**.
4. Open **Filters → View all filters** and configure sharing.
5. Test the shared filter as an authorized teammate.
6. Return to the ShopEase board and apply the filter or quick filter.
7. Capture all seven screenshots.

## Environment status

The connected Jira site was checked on 27 October 2026. Its visible projects are Customer Churn Project (`CCP`), HealthTracker App (`HT`), MediAlert (`MED`), and medilab (`PRIOR`). No project named ShopEase or project key `SHOP` was found. This guide provides the handout-derived configuration but does not claim the Jira filters/quick filters have already been deployed. The requested screenshots also must come from the real Jira UI.
