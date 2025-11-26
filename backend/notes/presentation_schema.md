Here’s how I’d structure this for an AI-presentation SaaS product.

---

## 1. Inputs to ask from the user when creating a presentation

Think of it in layers: **must-have**, **nice-to-have (optional)**, and **image-related**.

### A. Must-have inputs

These are the minimum you should collect to generate something meaningful:

1. **Prompt / Topic**

   * `topic` (string): e.g. “AI in healthcare for non-technical executives”
   * Can also ask for: “What should this presentation be about?”

2. **Presentation type**

   * `presentation_type` (enum):

     * `pitch_deck`, `sales_deck`, `report`, `training`, `lecture`, `marketing`, `internal_update`, `investor_deck`, `others`
   * This strongly shapes structure & tone.

3. **Target audience**

   * `audience_type` (string/enum): e.g. `executives`, `students`, `investors`, `customers`, `internal_team`
   * `audience_background` (optional string): tech vs non-tech, industry, region, etc.

4. **Goal / Intent**

   * `goal` (enum/string):

     * `inform`, `persuade`, `sell`, `update`, `train`, `raise_funds`, `onboard`, etc.

5. **Length of presentation**

   * `num_slides` (int): e.g. 10, 15, 20
   * Optionally: `length_mode`:

     * `auto`, `short`, `medium`, `detailed`

6. **Language**

   * `language` (enum/string): `en`, `es`, `fr`, etc.

7. **Tone / Writing style**

   * `tone` (enum/string):

     * `formal`, `informal`, `storytelling`, `data_driven`, `inspirational`, `playful`, `technical`, etc.

8. **Aspect ratio & format**

   * `aspect_ratio` (enum): `16:9`, `4:3`, `9:16` (for vertical), etc.
   * `export_format` (enum):

     * `pptx`, `pdf`, `google_slides`, `images_zip`.

---

### B. Image-related inputs (with optional flag)

You want image support to be fully configurable:

1. **Whether to include images**

   * `use_images` (boolean): `true` / `false`

2. **Preferred image source**

   * Only relevant if `use_images = true`
   * `image_source` (enum):

     * `ai_generated`, `stock`, `user_uploaded`, `mixed`

3. **Image density**

   * Again, only if `use_images = true`
   * `image_density` (enum/int):

     * `low`, `medium`, `high` or numeric: images per slide or total images

4. **Image style / vibe**

   * `image_style` (enum/string):

     * `realistic`, `illustration`, `flat`, `3d`, `minimal`, `cartoon`, `corporate`, etc.

5. **Content restrictions**

   * `allow_people` (boolean)
   * `allow_logos` (boolean)
   * `nsfw_filter_level` (enum): `strict`, `standard`
   * `copyright_restrictions` (enum): `no_third_party_logos`, etc.

6. **User image uploads (optional)**

   * `uploaded_image_ids` (array of asset IDs)
   * Optionally: map each upload to:

     * `intended_use` (background, product image, logo, etc.)

---

### C. Extra / advanced inputs to collect along with the prompt

These make generations more aligned and “pro-grade”:

1. **Structure control**

   * `has_custom_outline` (boolean)
   * If true:

     * `outline` (array of sections/slides user wants)
   * If false:

     * `auto_outline` (boolean) – usually true

2. **Branding / design preferences**

   * `brand_kit_id` (fk to brand kit table)
   * If no saved kit, ask:

     * `primary_color` (string, hex)
     * `secondary_color` (string, hex)
     * `accent_color` (string, hex)
     * `font_heading` (string)
     * `font_body` (string)
     * `logo_image_id` (fk to assets)
   * `visual_style` (enum):

     * `minimal`, `corporate`, `playful`, `creative`, `dark_theme`, `light_theme`

3. **Content inputs beyond the prompt**

   * `key_points` (array of short strings)
   * `data_sources`:

     * `urls` (array)
     * `uploaded_docs_ids` (array)
   * `must_include_phrases` (array of strings)
   * `must_avoid_topics` (array/string)

4. **Slide-level preferences**

   * `sections` (array): e.g. Intro, Problem, Solution, Market, etc.
   * `cta_type` (string): e.g. “Schedule a demo”, “Contact us”, etc.

5. **Speaker notes**

   * `generate_speaker_notes` (boolean)
   * `speaker_notes_style` (enum): `bullet_points`, `script_like`
   * `speaker_notes_length` (enum): `short`, `detailed`

6. **Collaboration / sharing settings**

   * `is_shared` (boolean)
   * `shared_with_user_ids` (array)

7. **Regulatory/safety preferences (enterprise)**

   * `compliance_mode` (enum): `none`, `finance`, `healthcare`
   * `show_disclaimers` (boolean)

---

## 2. Suggested DB structure

Assuming a relational DB (e.g. Postgres). I’ll keep it reasonably normalized and SaaS-friendly.

### 2.1. `users`

```sql
CREATE TABLE users (
  id                UUID PRIMARY KEY,
  email             VARCHAR(255) UNIQUE NOT NULL,
  name              VARCHAR(255),
  password_hash     VARCHAR(255),
  created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at        TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### 2.2. `organizations` (optional, for teams)

```sql
CREATE TABLE organizations (
  id                UUID PRIMARY KEY,
  name              VARCHAR(255) NOT NULL,
  plan              VARCHAR(50), -- free, pro, enterprise
  created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at        TIMESTAMP NOT NULL DEFAULT NOW()
);
```

Link users ↔ orgs (many-to-many or role-based):

```sql
CREATE TABLE organization_members (
  id                UUID PRIMARY KEY,
  organization_id   UUID NOT NULL REFERENCES organizations(id),
  user_id           UUID NOT NULL REFERENCES users(id),
  role              VARCHAR(50), -- owner, admin, member
  created_at        TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### 2.3. `brand_kits`

```sql
CREATE TABLE brand_kits (
  id                UUID PRIMARY KEY,
  organization_id   UUID REFERENCES organizations(id),
  user_id           UUID REFERENCES users(id), -- personal brand kit
  name              VARCHAR(255),

  primary_color     VARCHAR(20),
  secondary_color   VARCHAR(20),
  accent_color      VARCHAR(20),
  font_heading      VARCHAR(255),
  font_body         VARCHAR(255),
  logo_asset_id     UUID REFERENCES assets(id),

  created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at        TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### 2.4. `presentations`

This is the core entity.

```sql
CREATE TABLE presentations (
  id                       UUID PRIMARY KEY,
  user_id                  UUID NOT NULL REFERENCES users(id),
  organization_id          UUID REFERENCES organizations(id),
  brand_kit_id             UUID REFERENCES brand_kits(id),

  title                    VARCHAR(255),
  topic                    TEXT,     -- original prompt/topic
  description              TEXT,     -- optional longer description

  presentation_type        VARCHAR(50),  -- pitch_deck, report, etc.
  audience_type            VARCHAR(100),
  audience_background      TEXT,
  goal                     VARCHAR(100),

  num_slides               INT,
  aspect_ratio             VARCHAR(10),  -- "16:9", "4:3"
  export_format            VARCHAR(50),  -- pptx, pdf, etc.
  language                 VARCHAR(10),
  tone                     VARCHAR(50),
  visual_style             VARCHAR(50),  -- minimal, corporate...

  use_images               BOOLEAN DEFAULT TRUE,
  image_source             VARCHAR(50),  -- ai_generated, stock, etc.
  image_density            VARCHAR(20),  -- low, medium, high
  image_style              VARCHAR(50),  -- realistic, illustration...
  allow_people             BOOLEAN DEFAULT TRUE,
  allow_logos              BOOLEAN DEFAULT TRUE,

  generate_speaker_notes   BOOLEAN DEFAULT FALSE,
  speaker_notes_style      VARCHAR(50),
  speaker_notes_length     VARCHAR(20),

  status                   VARCHAR(50),  -- draft, generating, ready, failed
  error_message            TEXT,

  created_at               TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at               TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### 2.5. `slides`

Each slide belongs to a presentation.

```sql
CREATE TABLE slides (
  id                UUID PRIMARY KEY,
  presentation_id   UUID NOT NULL REFERENCES presentations(id) ON DELETE CASCADE,
  slide_index       INT NOT NULL, -- 0-based or 1-based ordering

  layout_type       VARCHAR(50), -- title_only, title_body, two_column, etc.
  title             TEXT,
  body              TEXT,        -- could be markdown or HTML
  speaker_notes     TEXT,

  created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at        TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### 2.6. `assets` (images, logos, etc.)

```sql
CREATE TABLE assets (
  id                UUID PRIMARY KEY,
  user_id           UUID REFERENCES users(id),
  organization_id   UUID REFERENCES organizations(id),

  type              VARCHAR(50),     -- image, logo, icon, background
  source            VARCHAR(50),     -- uploaded, ai_generated, stock
  file_path         TEXT NOT NULL,   -- URL / storage key
  mime_type         VARCHAR(100),
  width             INT,
  height            INT,

  metadata          JSONB,           -- style, prompt used, etc.
  created_at        TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### 2.7. `slide_assets` (link images to slides + position)

```sql
CREATE TABLE slide_assets (
  id                UUID PRIMARY KEY,
  slide_id          UUID NOT NULL REFERENCES slides(id) ON DELETE CASCADE,
  asset_id          UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,

  position_x        NUMERIC,  -- relative or absolute
  position_y        NUMERIC,
  width             NUMERIC,
  height            NUMERIC,
  z_index           INT DEFAULT 0,
  role              VARCHAR(50), -- background, main_image, icon, logo

  created_at        TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### 2.8. `generation_jobs` (tracking AI calls)

Useful for debugging & async processing.

```sql
CREATE TABLE generation_jobs (
  id                UUID PRIMARY KEY,
  presentation_id   UUID REFERENCES presentations(id),
  user_id           UUID REFERENCES users(id),

  provider          VARCHAR(50),   -- openai, internal, etc.
  model             VARCHAR(100),
  input_prompt      TEXT,
  settings          JSONB,         -- temperature, etc.

  status            VARCHAR(50),   -- pending, running, completed, failed
  error_message     TEXT,
  raw_response      JSONB,

  started_at        TIMESTAMP,
  completed_at      TIMESTAMP
);
```

---

### 2.9. `creation_sessions` (optional but nice)

To store everything user entered during “wizard” flow, including extra fields like `key_points`.

```sql
CREATE TABLE creation_sessions (
  id                UUID PRIMARY KEY,
  user_id           UUID REFERENCES users(id),
  presentation_id   UUID REFERENCES presentations(id),

  topic             TEXT,
  key_points        JSONB,    -- array of strings
  data_sources      JSONB,    -- urls, doc_ids
  must_include      JSONB,    -- phrases
  must_avoid        JSONB,

  raw_user_input    JSONB,    -- full request payload
  created_at        TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## 3. Summary of “extra inputs” to take along with prompt

Here’s a concise checklist you can implement in your UI:

* **Prompt / Topic**
* **Presentation type**
* **Target audience & background**
* **Goal (inform/sell/train/etc.)**
* **Language**
* **Tone / style**
* **Number of slides**
* **Aspect ratio & export format**
* **Use images?** (boolean)

  * If yes:

    * Image source (AI/stock/upload/mix)
    * Image density (few/medium/many)
    * Image style (realistic/illustration/etc.)
    * Content restrictions (people/logos/NSFW)
* **Branding**

  * Brand kit or custom colors, fonts, logo
* **Content helpers**

  * Key points
  * Data sources (links, uploads)
  * Must-include phrases
  * Topics to avoid
* **Structure**

  * Auto outline vs custom outline
  * Sections
  * Desired CTA
* **Speaker notes**

  * Generate notes? style & length

If you tell me your tech stack (e.g. Node/Postgres, Django, etc.), I can also sketch model classes or a concrete schema tailored to that.
