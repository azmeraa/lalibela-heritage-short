**# DESIGN.md — Production Design Notes**



**## 1. Creative intent**



**The film, \*\*“Lalibela: A Story Carved in Stone,”\*\* introduces international viewers to Lalibela, Ethiopia, through a respectful and emotionally engaging heritage story.**



**The film highlights Ethiopian history, the remarkable rock-hewn churches, living faith, cultural identity, and shared human heritage.**



**The intended audience is international viewers who may be unfamiliar with Lalibela and its cultural significance.**



**## 2. Story structure**



**The film uses eight shots with a total story duration of 85 seconds, followed by a 4-second end card.**



**The narrative moves through:**

**1. The Ethiopian highlands and landscape.**

**2. Visitors discovering Lalibela.**

**3. Details of the rock-hewn architecture.**

**4. An Ethiopian guide providing context.**

**5. Living religious traditions and pilgrims.**

**6. Biete Ghiorgis.**

**7. Visitors and the guide reflecting on shared heritage.**

**8. A closing aerial view and heritage message.**



**The closing message is:**



**“Different people. Different cultures. One shared heritage.”**



**## 3. Character strategy**



**The story uses four fictional AI-generated characters:**

**- A young Japanese woman visitor.**

**- A young Brazilian man visitor.**

**- A young European woman visitor.**

**- An Ethiopian male guide.**



**Consistent character descriptions are reused during image generation to maintain visual continuity.**



**No actual person was intentionally depicted or recorded.**



**## 4. Historical and cultural safeguards**



**The production follows these principles:**

**- Avoid fabricating historical facts, inscriptions, ceremonies, or architectural details.**

**- Treat Lalibela's churches and religious traditions respectfully.**

**- Avoid intrusive or disrespectful depictions of worshippers.**

**- Distinguish AI-generated artistic representations from verified historical documentation.**

**- Seek informed local review of Amharic wording and cultural details where possible.**



**## 5. Technical and production decisions**



**The production pipeline uses:**

**- `storyboard.json` as the central source of story and shot information.**

**- JSON Schema to validate the storyboard structure.**

**- Python scripts for validation and production tasks.**

**- Cloudflare Workers AI with FLUX.2 Klein for AI-generated keyframes.**

**- Gemini text-to-speech for English and Amharic narration.**

**- ACE-Step 1.5 for original background music.**

**- FFmpeg for moving shots, audio mixing, subtitles, and final assembly.**



**Because a practical Wan 2.2 image-to-video workflow was not completed within the production schedule, the project uses FFmpeg Ken Burns-style camera movement on generated keyframes. This provides motion while retaining the visual content of the original images.**



**The final film is exported in both horizontal 16:9 and vertical 9:16 formats.**



**The original music is mixed beneath the narration using audio ducking so that spoken content remains clear.**



**## 6. Audience testing**



**Audience testing is a required part of the project and must be completed with real participants.**



**### Radio-cut test**



**\*\*Status: Pending\*\***



**The radio cut consists of narration with placeholder/background music on a black screen.**



**At least three intended-audience participants should listen to it and provide feedback.**



**Questions:**

**1. What did you understand about Lalibela after listening?**

**2. Was the narration clear and comfortable to listen to?**

**3. Was the background music appropriate?**

**4. What would you improve?**



**Record actual participant feedback below.**



**| Participant | Main feedback | Planned or completed change |**

**|---|---|---|**

**| Participant 1 | Pending | Pending |**

**| Participant 2 | Pending | Pending |**

**| Participant 3 | Pending | Pending |**



**### Near-final film test**



**\*\*Status: Pending\*\***



**At least three intended-audience participants should watch the near-final film.**



**The same participants may take part in both tests.**



**Questions:**

**1. What did you learn about Lalibela?**

**2. Which scene or message was most memorable?**

**3. Were the subtitles and narration understandable?**

**4. Did the film represent Lalibela respectfully?**

**5. What would you improve?**



**Record actual feedback and resulting changes below.**



**| Participant | Main feedback | Planned or completed change |**

**|---|---|---|**

**| Participant 1 | Pending | Pending |**

**| Participant 2 | Pending | Pending |**

**| Participant 3 | Pending | Pending |**



**### Design changes resulting from audience feedback**



**To be completed after both audience tests. Document the feedback received, the changes made, and any suggestions that could not be implemented.**



**## 7. Current limitations**



**- Some AI-generated images may contain visual inaccuracies or artificial-looking details.**

**- The film has not yet been reviewed by a qualified local heritage expert.**

**- Audience testing and feedback documentation remain pending.**

**- A complete one-command regeneration workflow from a clean clone is not yet implemented.**

**- Music generation was performed separately using ACE-Step 1.5.**



**These limitations are documented rather than presented as completed work.**



**## 8. Future improvements**



**Future development could include:**

**- Review by Ethiopian heritage and language experts.**

**- Additional audience testing and revisions.**

**- Improved character and architectural consistency.**

**- A more automated and reproducible production pipeline.**

**- Better cost tracking and complete model-call records.**

**## Audience Feedback Collection System**



**To support audience evaluation, a Python-based feedback application was developed.**



**The application allows viewers to:**

**- Watch the radio cut or either final film version.**

**- Answer six questions about story understanding, narration, music, cultural learning, and overall experience.**

**- Submit suggestions for improvement.**

**- Have their responses saved automatically for later analysis.**



**The application also provides a summary of submitted feedback and distinguishes software-test records from non-test records.**



**### System verification**



**The application was launched and tested locally. A sample submission using participant code `TEST001` was saved successfully, and the summary correctly identified it as a test record.**



**### Actual audience testing status**



**The required radio-cut and near-final-film tests with at least three real viewers have not yet been completed. The sample response is not evidence of audience opinion. Genuine viewer responses must be collected before reporting audience findings or design changes.**



**### Planned use of feedback**



**Once genuine responses are collected, the project will document:**

**- What viewers understood about Lalibela.**

**- Whether the narration and music were effective.**

**- Which parts of the film viewers appreciated.**

**- Suggested improvements.**

**- Changes made to the film in response to feedback.**

