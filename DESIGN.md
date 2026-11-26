# DESIGN.md — Production Design Notes

## 1. Creative intent

The film, **“Lalibela: A Story Carved in Stone,”** introduces international viewers to Lalibela, Ethiopia, through a respectful and emotionally engaging heritage story.

The film highlights Ethiopian history, the remarkable rock-hewn churches, living faith, cultural identity, and shared human heritage.

The intended audience is international viewers who may be unfamiliar with Lalibela and its cultural significance.

## 2. Story structure

The film uses eight shots with a total story duration of 85 seconds, followed by a 4-second end card.

The narrative moves through:

1. The Ethiopian highlands and landscape.
2. Visitors discovering Lalibela.
3. Details of the rock-hewn architecture.
4. An Ethiopian guide providing context.
5. Living religious traditions and pilgrims.
6. Biete Ghiorgis.
7. Visitors and the guide reflecting on shared heritage.
8. A closing aerial view and heritage message.

### 2.1 Shot-by-shot creative purpose

| Shot | Creative purpose |
|---|---|
| S01 – Discovering Ethiopia | Establish Ethiopia's highland landscape and introduce the journey toward Lalibela. |
| S02 – First sight of Lalibela | Create an emotional connection by showing international visitors discovering Lalibela. |
| S03 – Carved from living rock | Reveal the craftsmanship and distinctive character of the rock-hewn architecture. |
| S04 – History and human vision | Introduce local interpretation and provide historical context for the churches. |
| S05 – A living place of faith | Show that Lalibela remains a living place of worship and pilgrimage. |
| S06 – Church of Saint George | Highlight Biete Ghiorgis and its distinctive cross-shaped rock-hewn design. |
| S07 – Different cultures, shared heritage | Express the central theme of cultural exchange and shared human heritage. |
| S08 – A heritage for generations | Conclude with a memorable view of Lalibela and reinforce the heritage message. |

Each shot has a defined narrative function rather than serving only as a visual illustration. These purposes are also stored in the corresponding `story_purpose` fields in `storyboard.json`, making the creative rationale part of the production source data.

The closing message is:

**“Different people. Different cultures. One shared heritage.”**

## 3. Character strategy

The story uses four fictional AI-generated characters:

- A young Japanese woman visitor.
- A young Brazilian man visitor.
- A young European woman visitor.
- An Ethiopian male guide.

Consistent character descriptions are reused during image generation to maintain visual continuity.

No actual person was intentionally depicted or recorded.

## 4. Historical and cultural safeguards

The production follows these principles:

- Avoid fabricating historical facts, inscriptions, ceremonies, or architectural details.
- Treat Lalibela's churches and religious traditions respectfully.
- Avoid intrusive or disrespectful depictions of worshippers.
- Distinguish AI-generated artistic representations from verified historical documentation.
- Seek informed local review of Amharic wording and cultural details where possible.

## 5. Technical and production decisions

The production pipeline uses:

- `storyboard.json` as the central source of story and shot information.
- JSON Schema to validate the storyboard structure.
- Python scripts for validation and production tasks.
- Cloudflare Workers AI with FLUX.2 Klein for AI-generated keyframes.
- Gemini text-to-speech for English and Amharic narration.
- ACE-Step 1.5 for original background music.
- FFmpeg for moving shots, audio mixing, subtitles, and final assembly.

Because a practical Wan 2.2 image-to-video workflow was not completed within the production schedule, the project uses FFmpeg Ken Burns-style camera movement on generated keyframes. This provides motion while retaining the visual content of the original images.

The final film is exported in both horizontal 16:9 and vertical 9:16 formats.

The original music is mixed beneath the narration using audio ducking so that spoken content remains clear.

## 6. Audience testing

Four audience reviews are documented below: P01, P02, and P04 reviewed the near-final film, while P03 listened to the radio cut. P01–P03 are retained as written summaries in the project report; P04 is the only review whose raw response is preserved in the current feedback CSV.

### Radio-cut test

**Status: Completed with one documented participant response.**

**Participant P03**

P03 listened to the radio cut and provided the following feedback:

- Understanding: Understood that the audio presented a general overview of the churches of Lalibela.
- New learning: Reported that the audio did not provide new information.
- Narration: Reported that the narration was not sufficiently clear.
- Music: Found the background music comfortable.
- Suggestions: Improve the language and translation, make the narration flow more smoothly, and consider additional language options such as French or Arabic.

### Near-final film test

**Status: Three documented participant responses.**

**Participant P01**

- Appreciated the bilingual Amharic and English presentation and the script.
- Suggested improving images that did not clearly match the main story of Lalibela.
- Recommended smaller subtitles positioned near the bottom of the video.
- Suggested adding Amharic text when English narration is used.
- Recommended exploring Addis AI Amharic voices for improved audio quality.

**Participant P02**

- Understood the film as a documentary-style introduction to Lalibela, its rock-hewn churches, living religious traditions, and shared heritage.
- Appreciated the bilingual storytelling, clear narration, background music, and closing message.
- Noted that some AI-generated architectural details, particularly Biete Giyorgis, looked stylized or inaccurate.
- Recommended using an Ethiopic-compatible font for the Amharic end-card text.
- Suggested smaller subtitles with a semi-transparent dark background near the bottom.
- Recommended improving one Amharic narration phrase to make it sound more natural.
- Suggested using more authentic visual references for Biete Giyorgis and religious clothing.

**Participant P04**

- Understood Lalibela as a historic destination with rock-hewn churches, living faith, Biete Giorgis, and shared heritage.
- Found the Amharic and English narration clear, calm, and well-paced, while suggesting greater consistency between the languages.
- Described the music as soft, reflective, and emotional, and appreciated the progression from visitors and architecture to living faith and shared humanity.
- Identified the New Jerusalem concept and Biete Giorgis' shape as memorable points for audiences new to Lalibela.
- Reported that the visuals appeared black during viewing and recommended checking the export, improving bilingual consistency and captions, refining abstract visual wording, and balancing music transitions.
- Following this report, local FFmpeg decoding checks passed for both final exports, and sampled frames from both showed Lalibela. These checks confirm the local files and sampled frames, but do not establish what happened on the participant's playback device.

### Design changes and lessons resulting from audience feedback

The feedback identified several strengths and areas for improvement.

**Positive feedback:**

- The bilingual Amharic and English storytelling was appreciated, with P04 describing both narrations as clear, calm, and well-paced.
- The script, shared-heritage message, and progression from architecture to living faith were well received.
- The background music was considered comfortable, soft, and suitable by participants who commented on it.
- P04 identified the New Jerusalem concept and Biete Giorgis' distinctive shape as memorable learning points for audiences unfamiliar with Lalibela.

**Areas identified for improvement:**

1. Improve the relevance and historical accuracy of AI-generated images.
2. Reduce subtitle size and position subtitles closer to the bottom of the video.
3. Improve Amharic text rendering using an Ethiopic-compatible font.
4. Review Amharic narration and translation for natural language flow.
5. Explore alternative Amharic TTS voices and additional language options.

The feedback was reviewed against the assignment requirements. English subtitles were retained because English subtitles are a required deliverable. Suggestions for additional Amharic subtitles, French or Arabic translations, alternative TTS voices, and more authentic architectural imagery are recorded as future improvements rather than claimed as completed changes.

The feedback also highlighted the importance of checking AI-generated heritage visuals against reliable historical references.

## 7. Current limitations

- Some AI-generated images may contain visual inaccuracies or artificial-looking architectural details.
- The film has not yet been reviewed by a qualified local heritage expert.
- Four reviews are documented: three near-final-film reviews and one radio-cut review. Only P04's raw response is preserved in the current CSV; P01–P03 remain written summaries in the report. The radio-cut review target of three participants has not been met.
- Some audience suggestions have not yet been implemented.
- A complete one-command regeneration workflow from a clean clone is not yet implemented.
- Music generation was performed separately using ACE-Step 1.5.

These limitations are documented rather than presented as completed work.

## 8. Future improvements

Future development could include:

- Review by Ethiopian heritage and language experts.
- Further audience testing and revisions.
- Improved character and architectural consistency.
- Smaller subtitles and improved subtitle placement.
- Better Amharic text rendering and narration quality.
- Additional language support for international audiences.
- A more automated and reproducible production pipeline.
- Better cost tracking and complete model-call records.

## 9. Audience Feedback Collection System

To support audience evaluation, a Python-based feedback application was developed.

The application allows viewers to:

- Watch the radio cut or either final film version.
- Answer six questions about story understanding, narration, music, cultural learning, and overall experience.
- Submit suggestions for improvement.
- Have their responses saved automatically for later analysis.

The application also provides a summary of submitted feedback and distinguishes software-test records from non-test records.

### System verification

The application was launched and tested locally. A sample submission using participant code `TEST001` was saved successfully, and the summary correctly identified it as a test record.

The TEST001 record is a software-test entry and is not included as genuine audience feedback.

### Actual audience feedback status

Four genuine audience reviews are documented:

- P01 reviewed the near-final film (summary retained in the report).
- P02 reviewed the near-final film (summary retained in the report).
- P03 listened to the radio cut (summary retained in the report).
- P04 reviewed the near-final film (raw response retained in `outputs/audience_feedback.csv`).

The P01–P03 raw survey responses were not found in the project files. The separate `TEST001` entry is a software-test record and is excluded from genuine participant counts. The documented near-final reviews reach the target of three, but the radio-cut review count remains one against a target of three.

### Use of feedback

The feedback informed the evaluation of the completed film and the identification of future improvements. Suggestions that were not implemented during this production period are documented rather than presented as completed changes.