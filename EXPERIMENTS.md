# Experiments and Technical Decisions

## Project: Lalibela — A Story Carved in Stone

This document records experiments, technical tests, observations, failures, and production decisions made while developing the AI-assisted heritage short.

The experiments covered storyboard design, validation, image generation, narration, music, audio mixing, motion, subtitles, video assembly, and selective regeneration.

## Experiment 1: Storyboard Structure

**Hypothesis:** A structured JSON storyboard would make the eight-scene production easier to organize and maintain.

**Objective:** Establish a structured production plan for the film.

**Approach:** Created an eight-shot storyboard in JSON, including shot timing, characters, locations, visual prompts, and motion prompts.

**Observation:** A structured storyboard made it easier to organize the film and connect production stages.

**Decision:** Retained JSON as the central production contract and added JSON Schema validation.

## Experiment 2: Storyboard Validation

**Hypothesis:** Automated checks would identify missing or inconsistent production information before media generation.

**Objective:** Detect missing or inconsistent production information before generating media.

**Approach:** Tested `scripts/01_validate_storyboard.py` against `storyboard.json` and `storyboard.schema.json`.

**Result:** The validation checks passed, including shot references, timing continuity, prompts, narration, and subtitles.

**Decision:** Kept storyboard validation as an essential production step before media generation.

## Experiment 3: AI Image Generation

**Hypothesis:** FLUX.2 Klein 4B could generate usable documentary-style keyframes about Lalibela.

**Objective:** Generate visual keyframes representing Lalibela and its cultural heritage.

**Approach:** Used FLUX.2 Klein 4B through Cloudflare Workers AI with documentary-style prompts.

**Observation:** The model generated usable images, but some results did not fully achieve the intended natural photographic appearance or architectural accuracy.

**Decision:** Selected images that supported the story and prioritized improvements to the most important scenes rather than repeatedly regenerating every image.

## Experiment 4: Character Consistency

**Hypothesis:** Repeating character descriptions and clothing details would improve visual continuity.

**Objective:** Maintain continuity among the fictional international visitors and Ethiopian guide.

**Approach:** Repeated character descriptions, clothing details, and visual characteristics across relevant image prompts.

**Observation:** Reusing descriptions helped communicate character continuity, although generated appearances were not perfectly consistent.

**Decision:** Retained the established fictional characters and visual direction, while recognizing character consistency as an area for future improvement.

## Experiment 5: Amharic and English Narration

**Hypothesis:** Gemini Flash TTS could generate usable narration in both Amharic and English.

**Objective:** Produce bilingual narration for an international heritage audience.

**Approach:** Used Gemini 3.8 Flash TTS with the Kore voice to generate Amharic and English narration clips.

**Observation:** Both languages were generated successfully. The completed narration was listened to and considered satisfactory. Audience feedback later identified opportunities to improve narration clarity and translation flow.

**Decision:** Retained the generated narration and assembled the clips into one narration track. Further language review remains a possible improvement.

## Experiment 6: Music Generation

**Hypothesis:** Generating multiple instrumental candidates would help identify a soundtrack suitable for the heritage story.

**Objective:** Create an original instrumental soundtrack appropriate for a heritage documentary.

**Approach:** Used ACE-Step 1.5 to generate three music candidates.

**Observation:** Candidate 1 was selected for its classical musical character and suitability for the film.

**Decision:** Used candidate 1 as the soundtrack.

## Experiment 7: Audio Mixing

**Hypothesis:** FFmpeg mixing and sidechain compression could keep music audible without overpowering narration.

**Objective:** Balance narration and background music.

**Approach:** Used FFmpeg audio processing, including sidechain compression, mixing, and limiting.

**Observation:** The resulting approximately 85-second audio mix was listened to and judged satisfactory. The music was kept below the narration to preserve speech clarity.

**Decision:** Retained the final narration and music mix for video assembly.

## Experiment 8: Image-to-Video Alternatives

**Hypothesis:** FFmpeg pan-and-zoom effects could create camera movement without a separate AI video model.

**Objective:** Give still images a sense of camera movement.

**Approach:** Considered AI video generation and used FFmpeg to apply slow pan-and-zoom movements to generated keyframes.

**Observation:** The FFmpeg approach produced smooth moving shots without requiring a separate video-generation model.

**Decision:** Used the Ken Burns-style approach as a practical alternative that reduced additional model dependencies and production complexity.

## Experiment 9: Subtitle Readability

**Hypothesis:** Larger, bold subtitles with outline and shadow would improve subtitle visibility.

**Objective:** Improve English subtitle readability.

**Approach:** Reviewed the initial film and identified subtitle size and visibility as areas for improvement. Updated the horizontal assembly script to use larger, bold Arial subtitles with an outline and shadow.

**Observation:** The revised horizontal film and regenerated vertical version completed successfully. Subsequent audience feedback still identified subtitle size and placement as areas for further improvement.

**Decision:** Retained the revised subtitle styling while documenting further refinements as future work.

## Experiment 10: Horizontal and Vertical Outputs

**Hypothesis:** The same story and source assets could be assembled into valid horizontal and vertical formats.

**Objective:** Produce both required aspect ratios.

**Approach:** Assembled the horizontal film at 1920 × 1080 and the vertical film at 1080 × 1920 using FFmpeg.

**Observation:** Both versions were successfully generated with approximately 89 seconds of total duration. Both final files were checked using FFmpeg decoding and passed the verification command.

**Decision:** Retained both versions as the final film outputs.

## Experiment 11: Selective Keyframe Regeneration

**Hypothesis:** Targeting one changed scene would allow its keyframe to be regenerated without selecting the other seven scenes.

**Objective:** Improve the opening scene without unnecessarily regenerating all eight keyframes.

**Approach:** Added "with a traditional Ethiopian highland footpath visible in the foreground" to the S01 prompt. Set `REGENERATE_ONLY = {"S01"}` so only S01 was selected.

**Observation:** The first three logged generation attempts failed with HTTP 400 errors. A subsequent attempt succeeded and generated `assets/images/S01.jpg` in 14.1 seconds. S02–S08 were not selected and remained untouched. Both final film versions were reassembled and passed FFmpeg decoding checks.

**Decision:** Retained the new S01 keyframe and selective-regeneration workflow. This demonstrated how a targeted change could be made without repeating the entire image-generation process.

## Overall Learning

The experiments demonstrated that a practical AI-assisted film pipeline can combine structured data, AI-generated media, conventional video-processing tools, and human review.

The most important lessons were:

- A validated storyboard provides a reliable structure for a multi-stage production pipeline.
- AI-generated images require human review, particularly when representing historically significant architecture.
- Reusing existing assets and selectively regenerating one shot can save time and avoid unnecessary model calls.
- Conventional tools such as FFmpeg remain valuable for motion, audio processing, subtitles, and final assembly.
- Technical success does not guarantee audience satisfaction; feedback can reveal issues that production checks do not identify.
- Failures and limitations should be recorded honestly rather than hidden.

The experiment log records hypotheses, technical observations, and decisions. Audience findings are summarized in `FINAL_REPORT.md`; the current CSV contains P04's raw response and the separate TEST001 software-test record.
