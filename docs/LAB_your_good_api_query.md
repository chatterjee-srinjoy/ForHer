# LAB: API Queries - MyHealthfinder API

## API Overview

**Source**: U.S. Department of Health and Human Services (HHS)  
**Base URL**: `https://odphp.health.gov/myhealthfinder/api/v4/`  
**Authentication**: None required (public API)

## Endpoints Used

### 1. Personalized Recommendations (`myhealthfinder.json`)

Returns preventive care recommendations based on user demographics.

**URL**: `https://odphp.health.gov/myhealthfinder/api/v4/myhealthfinder.json`

**Parameters**:
| Parameter      | Type   | Description                    |
|----------------|--------|--------------------------------|
| age            | int    | User age (e.g., 25)           |
| sex            | string | "male" or "female"            |
| pregnant       | string | "yes" or "no"                 |
| sexuallyActive | string | "yes" or "no"                 |
| tobaccoUse     | string | "yes" or "no"                 |
| Lang           | string | "en" or "es" (optional)       |

**Example Query**:

```text
https://odphp.health.gov/myhealthfinder/api/v4/myhealthfinder.json?age=25&sex=female&pregnant=no&sexuallyActive=yes&tobaccoUse=no
```

### 2. Topic List (`itemlist.json`)

Returns all available health topics.

```text
https://odphp.health.gov/myhealthfinder/api/v4/itemlist.json?Type=topic&Lang=en
```

### 3. Category List (`itemlist.json`)

Returns all health categories.

```text
https://odphp.health.gov/myhealthfinder/api/v4/itemlist.json?Type=category&Lang=en
```

## Python Implementation

See `src/api_client.py` for the API client functions:
- `fetch_myhealthfinder()` – personalized recommendations
- `fetch_itemlist()` – topics or categories
- `fetch_topic()` – details for a specific topic
