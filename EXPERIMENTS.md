**# EXPERIMENTS.md**



**## Project: Lalibela — A Story Carved in Stone**



**This document records experiments, technical tests, and production decisions made while developing the AI-assisted heritage short.**



**The experiments focused on image generation, narration, music, motion, subtitles, and final video assembly.**



**## Experiment 1: Storyboard Structure**



**\*\*Objective:\*\* Establish a structured production plan for the film.**



**\*\*Approach:\*\* Created an eight-shot storyboard in JSON, including shot timing, characters, locations, visual prompts, and motion prompts.**



**\*\*Observation:\*\* A structured storyboard made it easier to organize the film and connect production stages.**



**\*\*Decision:\*\* Retained JSON as the central production contract and added JSON Schema validation.**



**## Experiment 2: Storyboard Validation**



**\*\*Objective:\*\* Detect missing or inconsistent production information before generating media.**



**\*\*Approach:\*\* Tested `scripts/01\_validate\_storyboard.py` against `storyboard.json` and `storyboard.schema.json`.**



**\*\*Result:\*\* All validation checks passed, including shot references, timing continuity, prompts, narration, and subtitles.**



**\*\*Decision:\*\* Keep storyboard validation as an essential production step.**



**## Experiment 3: AI Image Generation**



**\*\*Objective:\*\* Generate visual keyframes representing Lalibela and its cultural heritage.**



**\*\*Approach:\*\* Used FLUX.2 Klein 4B through Cloudflare Workers AI with documentary-style prompts.**



**\*\*Observation:\*\* The model generated usable images, but some results did not fully achieve the intended natural photographic appearance.**



**\*\*Decision:\*\* Selected images that supported the story and continued production rather than repeatedly regenerating every image.**



**## Experiment 4: Character Consistency**



**\*\*Objective:\*\* Maintain continuity among the fictional international visitors and Ethiopian guide.**



**\*\*Approach:\*\* Repeated character descriptions, clothing details, and visual characteristics across relevant image prompts.**



**\*\*Observation:\*\* Reusing descriptions helped communicate character continuity, although generated appearances were not perfectly consistent.**



**\*\*Decision:\*\* Retained the established fictional characters and visual direction.**



**## Experiment 5: Amharic and English Narration**



**\*\*Objective:\*\* Produce bilingual narration for an international heritage audience.**



**\*\*Approach:\*\* Used Gemini 3.8 Flash TTS with the Kore voice to generate Amharic and English narration clips.**



**\*\*Observation:\*\* Both languages were generated successfully. The completed narration was listened to and considered satisfactory.**



**\*\*Decision:\*\* Retained the generated narration and assembled the clips into one narration track.**



**## Experiment 6: Music Generation**



**\*\*Objective:\*\* Create an original instrumental soundtrack appropriate for a heritage documentary.**



**\*\*Approach:\*\* Used ACE-Step 1.5 to generate music candidates. Three candidates were produced and considered.**



**\*\*Observation:\*\* Candidate 1 was selected for its classical musical character.**



**\*\*Decision:\*\* Used candidate 1 as the film's soundtrack.**



**## Experiment 7: Audio Mixing**



**\*\*Objective:\*\* Balance narration and background music.**



**\*\*Approach:\*\* Used FFmpeg audio processing, including sidechain compression, mixing, and limiting.**



**\*\*Observation:\*\* The resulting 85-second audio mix was listened to and judged satisfactory.**



**\*\*Decision:\*\* Retained the final narration and music mix for video assembly.**



**## Experiment 8: Image-to-Video Alternatives**



**\*\*Objective:\*\* Give the still images a sense of camera movement.**



**\*\*Approach:\*\* Considered AI video generation and used FFmpeg to apply slow pan and zoom movements to the generated keyframes.**



**\*\*Observation:\*\* The FFmpeg approach produced smooth moving shots without requiring a separate video-generation model.**



**\*\*Decision:\*\* Used the Ken Burns-style approach as a practical alternative to AI image-to-video generation.**



**## Experiment 9: Subtitle Readability**



**\*\*Objective:\*\* Improve English subtitle readability.**



**\*\*Approach:\*\* Reviewed the initial film and found that the subtitle text was too small. Updated the horizontal assembly script to use larger, bold Arial subtitles with an outline and shadow.**



**\*\*Observation:\*\* The revised horizontal film and regenerated vertical version completed successfully. The final vertical film was reviewed and considered good overall.**



**\*\*Decision:\*\* Retained the larger subtitle styling.**



**## Experiment 10: Horizontal and Vertical Outputs**



**\*\*Objective:\*\* Produce both required aspect ratios.**



**\*\*Approach:\*\* Assembled the horizontal film at 1920 × 1080 and converted it into a vertical 1080 × 1920 version using FFmpeg.**



**\*\*Observation:\*\* Both versions were successfully generated with approximately 89 seconds of total duration.**



**\*\*Decision:\*\* Retained both versions as the final film outputs.**



**## Overall Learning**



**The experiments demonstrated that a practical AI-assisted film pipeline can combine structured data, AI-generated media, conventional video-processing tools, and human review.**



**The most important lesson was that successful production depends not only on AI generation but also on validation, careful selection, audio processing, subtitle readability, and final quality checks.**

