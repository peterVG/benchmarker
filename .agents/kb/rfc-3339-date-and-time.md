# RFC 3339 - Date and Time on the Internet

## 1. Overview
RFC 3339 defines a date and time format for use in Internet protocols. It is a specific profile of the ISO 8601 standard, designed to improve consistency and interoperability by reducing the ambiguity found in the broader ISO standard.

Status: Proposed Standard

Relationship to ISO 8601: RFC 3339 is a "strict" subset/profile of ISO 8601.

Primary Use Case: Timestamps for Internet protocol events.

## 2. Core Concepts
### 2.1 The Timeline
RFC 3339 assumes all dates and times are based on the Gregorian Calendar. It uses UTC (Coordinated Universal Time) as the reference point for all timestamps.

### 2.2 Time Zones and Offsets
Z (Zulu): Represents UTC (Zero offset).

Numeric Offsets: Expressed as +HH:MM or -HH:MM.

Local Time: If the offset is unknown, -00:00 may be used to indicate that the time is in UTC but the local offset was not provided (distinct from +00:00 which implies UTC is the preferred reference).

## 3. Grammar (ABNF)
AI agents should use these rules to validate or generate RFC 3339 strings.

date-fullyear   = 4DIGIT

date-month      = 2DIGIT  ; 01-12

date-mday       = 2DIGIT  ; 01-28, 01-29, 01-30, 01-31 based on month/year

time-hour       = 2DIGIT  ; 00-23

time-minute     = 2DIGIT  ; 00-59

time-second     = 2DIGIT  ; 00-58, 00-59, 00-60 based on leap second

time-secfrac    = "." 1*DIGIT

time-numoffset  = ("+" / "-") time-hour ":" time-minute

time-offset     = "Z" / time-numoffset

partial-time    = time-hour ":" time-minute ":" time-second [time-secfrac]

full-date       = date-fullyear "-" date-month "-" date-mday

full-time       = partial-time time-offset

date-time       = full-date "T" full-time

## 4. Examples
UTC (Z): 1985-04-12T23:20:50Z (April 12, 1985, 11:20 PM UTC)

With Offset: 1996-12-19T16:39:57-08:00 (Dec 19, 1996, 4:39 PM, 8 hours behind UTC)

Fractional Seconds: 1937-01-01T12:00:27.87Z (Noon on Jan 1, 1937, with 870ms precision)

## 5. Implementation Rules & Restrictions
The "T" Separator: The date and time must be separated by the character T. (Note: While the spec allows a space instead of T for readability in some contexts, strict parsers often require T).

Upper Case: The T and Z characters should be upper case (though parsers SHOULD accept lower case).

Leading Zeros: Leading zeros are mandatory for all fields (e.g., 05 instead of 5).

Leap Seconds: The format explicitly supports leap seconds (e.g., 23:59:60).

No Year 0: The year 0000 is allowed and represents 1 BCE in the proleptic Gregorian calendar.

## 6. Key Differences: RFC 3339 vs. ISO 8601
Punctuation: RFC 3339 requires "-" and ":" whereas ISO 8601 allows "Basic" format with no punctuation.

Complexity: RFC 3339 is simple and focused on timestamps; ISO 8601 includes durations, intervals, and week dates.

Seconds: Mandatory in RFC 3339; optional in ISO 8601.

Decimal Point: RFC 3339 must use a period "."; ISO 8601 allows period or comma.

## 7. Troubleshooting & FAQ for Agents
Query: "Is 2023-10-27 a valid RFC 3339 timestamp?"

Answer: No. RFC 3339 requires the full date-time structure including time and offset. It is a valid full-date, but usually, APIs expect date-time.

Common Error: Using a space instead of T. Correction: Change 2023-01-01 12:00:00Z to 2023-01-01T12:00:00Z.

Common Error: Missing time zone. Correction: Always append Z or a numerical offset like +00:00.

Reference: RFC 3339 (https://www.rfc-editor.org/rfc/rfc3339)