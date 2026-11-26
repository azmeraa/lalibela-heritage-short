# Cost and Performance Report

## Project: Lalibela — A Story Carved in Stone

## 1. Overview

This project produced an 89-second bilingual heritage film using cloud AI services, open-source software, a Kaggle GPU environment, and a local Windows computer.

This document records available performance measurements and identifies costs that could not be independently verified. It does not present unverified estimates as actual expenditure.

## 2. Tools and Services

| Tool or Service | Purpose | Cost Information |
|---|---|---|
| Python | Pipeline development and automation | Open-source |
| FFmpeg | Video assembly, camera movement, audio mixing, and encoding | Open-source |
| JSON Schema | Storyboard validation | Open-source |
| Cloudflare Workers AI — FLUX.2 Klein 4B | AI keyframe generation | Actual API charges not recorded |
| Google Gemini TTS — gemini-3.8-flash-tts | Amharic and English narration | Actual API charges not recorded |
| ACE-Step 1.5 | Original AI-generated music | Software is open-source |
| Kaggle GPU environment | GPU resources for music generation | GPU usage cost not measured |
| Local Windows computer | Development and final video assembly | Existing equipment; electricity cost not measured |

## 3. Recorded Generation Performance

The following measurements were calculated from successful generation records in `logs/runs.jsonl`.

| Stage | Successful Requests | Recorded Latency |
|---|---:|---:|
| Narration generation | 8 | 111.24 seconds total |
| Keyframe generation | 10 | 84.18 seconds total |

### Narration

- Model: `gemini-3.8-flash-tts`
- Voice: Kore
- Languages: Amharic and English
- Successful requests: 8
- Total recorded latency: 111.24 seconds
- Average latency per request: approximately 13.91 seconds
- Fastest request: 3.85 seconds
- Slowest request: 60.46 seconds

### Keyframe generation

- Model: `@cf/black-forest-labs/flux-2-klein-4b`
- Successful requests: 10, including initial generation and subsequent regeneration.
- Total recorded successful-request latency: 84.18 seconds.
- Three additional S01 attempts failed with HTTP 400 errors.
- The successful final S01 regeneration took 8.73 seconds.

These measurements represent recorded generation-request latency only. They do not represent the complete production time or the total time spent waiting, reviewing, editing, and assembling the film.

## 4. Resource and Cost Measurement Limitations

The production logs contain a `cost_usd` field, but its value is null for the recorded generation requests.

Consequently:

- Actual Cloudflare image-generation charges were not verified.
- Actual Gemini TTS charges were not verified.
- Kaggle GPU-minutes or GPU-hours were not recorded.
- Local CPU/GPU utilization and electricity consumption were not measured.
- Development and manual production hours were not comprehensively tracked.
- A reliable total monetary production cost cannot be calculated from the available evidence.
- A verified provider list-price equivalent is not available from the project records.

The project therefore reports measured latency separately from unverified financial costs.

## 5. Cost Optimization Decisions

Several decisions helped limit unnecessary generation and processing:

1. Used FFmpeg pan-and-zoom movements instead of generating separate AI video footage for every scene.
2. Reused existing keyframes and moving shots when rebuilding the final films.
3. Used selective regeneration to improve S01 without regenerating all eight scenes.
4. Used open-source tools for video processing and pipeline automation.
5. Selected one music candidate rather than repeatedly generating additional tracks.
6. Used storyboard validation and caching to reduce avoidable processing.

## 6. Future Cost Improvements

Future versions of the pipeline should:

- Capture actual provider billing information where available.
- Estimate list-price equivalents using documented provider pricing and recorded usage.
- Record GPU runtime and hardware allocation.
- Track processing time for video assembly and audio production.
- Track failed requests and retries alongside successful requests.
- Calculate estimated cost per scene and per completed film.
- Produce an automated cost and performance summary for each production run.

## 7. Conclusion

The project demonstrates that a heritage short can be produced through a combination of cloud-based AI generation, open-source software, and local processing.

The available logs provide measurable evidence of narration and image-generation latency. However, exact monetary costs and GPU resource consumption were not measured, so no unsupported total-cost claim is made.

More complete billing and resource instrumentation will be an important improvement in the next version of the pipeline.
