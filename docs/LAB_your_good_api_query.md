# LAB: API Queries - MyHealthfinder API

## API Overview

| | |
|---|---|
| **Source** | U.S. Department of Health and Human Services (HHS) |
| **Base URL** | `https://odphp.health.gov/myhealthfinder/api/v4/` |
| **Authentication** | None required (public API) |
| **Rate Limits** | None documented |

## Primary Endpoint: Personalized Recommendations

**`GET /myhealthfinder.json`** — Returns age- and sex-appropriate preventive care
recommendations based on user demographics and health behaviors.

### Parameters

| Parameter        | Type   | Required | Description                    |
|------------------|--------|----------|--------------------------------|
| `age`            | int    | Yes      | User age (e.g., 25)           |
| `sex`            | string | Yes      | `"male"` or `"female"`        |
| `pregnant`       | string | No       | `"yes"` or `"no"`             |
| `sexuallyActive` | string | No       | `"yes"` or `"no"`             |
| `tobaccoUse`     | string | No       | `"yes"` or `"no"`             |
| `Lang`           | string | No       | `"en"` or `"es"`              |

### Example Query

```text
https://odphp.health.gov/myhealthfinder/api/v4/myhealthfinder.json?age=25&sex=female&pregnant=no&sexuallyActive=yes&tobaccoUse=no
```

### How Zena Uses This

1. User enters their age and vaccination status in the sidebar
2. `fetch_myhealthfinder(age=25, sex="female", ...)` calls the API
3. The API returns **only age-appropriate recommendations** (e.g., a 25-year-old
   gets cervical cancer screening but not mammograms; a 50-year-old gets both)
4. `process_recommendations()` categorizes, assigns priority, and filters out
   vaccines the user has already completed
5. Results populate the interactive checklist table

### Response Structure

```json
{
  "Result": {
    "Resources": {
      "All": {
        "Resource": [
          {
            "Title": "Get Screened for Cervical Cancer",
            "MyHFTitle": "...",
            "MyHFCategory": "Screenings",
            "Categories": "...",
            "Sections": {
              "section": [
                { "Content": "<p>HTML content with details...</p>" }
              ]
            }
          }
        ]
      }
    }
  }
}
```

## Secondary Endpoints

### Topic List (`GET /itemlist.json`)

Returns all available health topics or categories.

```text
https://odphp.health.gov/myhealthfinder/api/v4/itemlist.json?Type=topic&Lang=en
```

### Topic Details (`GET /topicsearch.json`)

Returns detailed information for a specific topic by ID.

```text
https://odphp.health.gov/myhealthfinder/api/v4/topicsearch.json?TopicId=30544&Lang=en
```

## Python Implementation (`src/api_client.py`)

| Function                  | Endpoint               | Returns              |
|---------------------------|------------------------|----------------------|
| `fetch_myhealthfinder()`  | `myhealthfinder.json`  | `dict` or `None`     |
| `fetch_itemlist()`        | `itemlist.json`        | `dict` or `None`     |
| `fetch_topic()`           | `topicsearch.json`     | `dict` or `None`     |

All functions return `None` on error (timeout, HTTP error, network failure) with
a printed error message. The app's `processed_df()` handles `None` gracefully by
showing a "Could not load recommendations" message.

## Data Processing Pipeline (`src/data_processing.py`)

After the API response is received, `process_recommendations()` applies:

1. **Vaccine filtering** — Removes recommendations for vaccines the user marked as completed
2. **Categorization** — Assigns each recommendation to one of: Vaccinations, Screenings,
   Preventive Visits, Lifestyle & Mental Health, or Sexual Health
3. **Priority assignment** — High (vaccines, cervical/HPV), Routine (visits/checkups),
   or Informational (everything else)
4. **Unsure flagging** — Marks items as "verify" if the user checked "Unsure about some vaccines"
