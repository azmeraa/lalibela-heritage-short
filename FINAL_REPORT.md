# Final Project Report

## Lalibela: A Story Carved in Stone

**Project:** AI-Content Generation – The Heritage Short  
**Creator:** Independent AI content creator  
**Location:** Ethiopia  
**Project date:** November 2026

---

## 1. Project Overview

I created an AI-generated heritage short titled *Lalibela: A Story Carved in Stone*. The film introduces the historical, architectural, spiritual, and cultural importance of Lalibela, Ethiopia, to an international audience.

The intended audience includes international visitors and people interested in Ethiopian history and cultural heritage.

The film uses eight scenes, combining AI-generated images, camera movement, narration in Amharic and English, English subtitles, original background music, and an AI-generated end card.

The final film is approximately 89 seconds long and is available in vertical and horizontal formats.

## 2. What I Created

The project includes:

- Eight-scene storyboard stored in JSON.
- JSON Schema for storyboard validation.
- Eight AI-generated visual keyframes.
- Amharic and English AI-generated narration.
- English subtitles.
- Original AI-generated background music.
- Audio mixing with background music ducked under narration.
- Eight moving shots created using FFmpeg pan-and-zoom effects.
- Horizontal and vertical MP4 films.
- A radio cut containing narration and background music over a black screen.
- An AI-generated end card.
- A Python audience feedback application.
- Technical documentation, experiment records, cost and performance report, and ethics documentation.
- A public GitHub repository containing the source code, assets, documentation, and video outputs.

## 3. Development Process and Learning

I learned how different AI and software tools can work together to produce a complete multimedia story.

The development process included story planning, storyboard validation, image generation, narration generation, music creation, audio mixing, video editing, subtitle integration, and final video production.

I documented 11 technical experiments covering storyboard structure, validation, image generation, character consistency, narration, music, audio mixing, image-to-video alternatives, subtitle readability, video formats, and selective keyframe regeneration.

The experiments helped me compare approaches, document observations, and make production decisions. For example, I used FFmpeg pan-and-zoom effects instead of generating a separate AI video for every scene. This provided camera movement while keeping the workflow practical with the available time and resources.

I also learned the importance of organizing project files, validating structured data, testing individual stages, reusing generated assets, and documenting technical decisions.

Developing the Python feedback application helped me understand how software can support the evaluation of AI-generated content.

The project demonstrated that AI-generated heritage storytelling requires attention to cultural accuracy, language quality, visual consistency, and audience understanding—not just technical production.

## 4. Hardest Technical Challenge

One of the hardest challenges was integrating different AI-generated assets and production tools into a working video pipeline.

I encountered technical problems with AI model configuration, audio file formats, FFmpeg filter paths on Windows, and video rendering.

For example, FFmpeg initially encountered problems with the Windows drive-letter colon in the subtitle filter path. I resolved this by using a project-relative subtitle path.

Another challenge occurred when I revised the opening scene, S01, and attempted to regenerate its keyframe. The first three logged attempts failed with HTTP 400 errors. A subsequent attempt succeeded, generating the new keyframe in 8.73 seconds.

I configured the generation process to target S01 rather than regenerate all eight keyframes. I then regenerated its moving shot while reusing the other seven moving shots. Both final film formats were reassembled and passed FFmpeg decoding checks.

This selective-regeneration process demonstrated the value of caching and targeted updates. It also showed why failed requests and retries should be recorded rather than hidden.

These experiences taught me to solve problems systematically, inspect logs, and validate each production stage.

## 5. Performance Measurement and Cost Considerations

The project recorded generation-request latency in `logs/runs.jsonl`.

The available successful-request measurements were:

| Production stage | Successful requests | Recorded total latency |
|---|---:|---:|
| Narration generation | 8 | 111.24 seconds |
| Keyframe generation | 10 | 84.18 seconds |

The narration requests used `gemini-3.8-flash-tts` with the Kore voice. Their average recorded latency was approximately 13.91 seconds per request.

The keyframe requests used Cloudflare Workers AI with `@cf/black-forest-labs/flux-2-klein-4b`. The final S01 regeneration succeeded in 8.73 seconds after three failed HTTP 400 attempts.

These figures represent recorded model-request latency, not total production time. The logs do not provide verified monetary API charges, GPU-minutes, electricity consumption, or total development hours. Therefore, I do not claim an exact total production cost or an unsupported list-price equivalent.

Open-source tools such as Python and FFmpeg helped limit software costs. Reusing generated assets and selectively regenerating S01 also reduced unnecessary processing.

More detailed performance and cost limitations are documented in `COSTS.md`.

## 6. Practices That Helped and Did Not Help

### Practices that helped

- Breaking the production process into smaller stages.
- Validating the storyboard before generating assets.
- Testing individual images and audio clips before assembling the film.
- Keeping generated assets organized.
- Using FFmpeg for reliable audio and video processing.
- Reusing cached assets instead of regenerating everything.
- Using selective regeneration when a single scene needed improvement.
- Recording technical problems, experiments, and decisions.

### Practices that were less effective

Attempting to use more complex AI video generation was not practical within the available development time and computing resources.

The project therefore used FFmpeg pan-and-zoom animation as a fallback. This allowed the film to include moving shots without relying on expensive or difficult video-generation infrastructure.

Some image-generation attempts also failed and required retries. These experiences reinforced the importance of validating model parameters, inspecting error responses, and keeping generation logs.

## 7. Audience Evaluation

A Python-based audience feedback application was developed using Tkinter.

The application allows viewers to play the radio cut and final film versions, answer six questions, and save responses in a CSV file. It also provides a feedback summary.

The application was tested locally using a sample response with participant code `TEST001`. The software successfully saved the response and identified it as a test record. This software-test entry is separate from genuine audience feedback.

### Actual audience feedback

Three participants provided genuine feedback:

**P01 — Near-final film**

P01 appreciated the bilingual Amharic and English presentation and the script. The participant recommended improving images that did not clearly match Lalibela, reducing subtitle size and moving subtitles to the bottom, adding Amharic text alongside English narration, and exploring Addis AI Amharic voices.

**P02 — Near-final film**

P02 understood the film as an introduction to Lalibela's rock-hewn churches, living religious traditions, and shared heritage. The participant appreciated the bilingual storytelling, narration, music, and closing message.

P02 also identified stylized or inaccurate AI-generated architectural details, especially around Biete Giyorgis. Further suggestions included using an Ethiopic-compatible font for the Amharic end card, improving subtitle placement, refining an Amharic narration phrase, and using more authentic architectural and cultural references.

**P03 — Radio cut**

P03 understood that the audio presented a general overview of Lalibela's churches. The participant reported no new learning, found the narration insufficiently clear, and considered the background music comfortable. Suggestions included improving translation and narration flow and considering additional languages such as French or Arabic.

### What I learned from the feedback

The feedback highlighted strengths in bilingual storytelling, the script, background music, and the shared-heritage message.

It also identified opportunities to improve visual accuracy, subtitle presentation, Amharic text rendering, narration clarity, and translation quality.

English subtitles were retained because they are a required project deliverable. Suggestions that were not implemented during the production period are documented as future improvements rather than claimed as completed changes.

At the time of this report, two participants had reviewed the near-final film and one had reviewed the radio cut. The assignment target is at least three audience participants for each version, so the audience-testing requirement is not yet fully met. Two additional reviewers have been contacted, and their feedback is pending. Their responses will be added when received.

## 8. What I Would Do With More Time

With additional time and resources, I would:

- Improve the realism and consistency of AI-generated visual scenes.
- Use more reliable historical references for Lalibela's architecture.
- Explore more advanced image-to-video generation.
- Obtain feedback from Ethiopian heritage and language experts.
- Improve subtitle size, placement, and Amharic text rendering.
- Explore alternative Amharic TTS voices and improve narration flow.
- Test additional language options for international audiences.
- Improve automated performance and cost tracking.
- Improve the feedback application with more detailed analysis.
- Complete the outstanding audience reviews for both film versions.

## 9. Next Steps

The remaining submission activities are to:

- Complete the outstanding audience reviews and update the feedback records.
- Regenerate and verify the final report PDF after report updates.
- Record the required project walkthrough within the five-minute limit.
- Confirm that the vertical film, horizontal film, walkthrough, and public post are accessible to the graders.
- Publish the required public post with the appropriate AI disclosure.
- Perform a final review of the public GitHub repository and submission links.

## 10. Conclusion

This project demonstrates how AI tools can support the creation of a short cultural heritage film using accessible technologies and a structured production workflow.

Through this work, I gained practical experience in AI-assisted storytelling, multimedia production, software integration, technical problem-solving, experimentation, performance measurement, and audience evaluation.

The project also demonstrates the potential of AI-generated content to introduce Ethiopia's cultural heritage to international audiences while highlighting the importance of cultural respect, accuracy, transparency, and audience feedback.

---

**Project title:** Lalibela: A Story Carved in Stone  
**Status:** Film production completed; three genuine audience reviews collected (two near-final film reviews and one radio-cut review); additional audience feedback pending; public GitHub repository created; final submission activities in progress.
