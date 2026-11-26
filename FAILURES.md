**# FAILURES.md**



**## Project: Lalibela — A Story Carved in Stone**



**This document records technical difficulties encountered during development and the approaches used to resolve them.**



**## 1. AI Image Quality**



**\*\*Problem:\*\* Some generated images did not look as natural or realistic as intended. Certain visual details and human appearances were imperfect.**



**\*\*Resolution:\*\* Reviewed the generated images, adjusted prompts for selected shots, and retained images that were suitable for communicating the story.**



**\*\*Lesson:\*\* AI-generated images require human review and selection. More detailed prompts do not guarantee perfect results.**



**## 2. Image Generation and File Formats**



**\*\*Problem:\*\* Some generated image files had file extensions that did not accurately represent their actual image format.**



**\*\*Resolution:\*\* Used image-checking and extension-correction scripts to inspect and organize the generated images.**



**\*\*Lesson:\*\* Generated assets should be checked before they are passed to later pipeline stages.**



**## 3. Music File Format**



**\*\*Problem:\*\* The selected music file was saved with a WAV extension even though its actual encoding was MP3.**



**\*\*Resolution:\*\* Used FFmpeg to identify and decode the audio correctly during subsequent processing.**



**\*\*Lesson:\*\* File extensions should not be treated as proof of the actual media encoding.**



**## 4. AI Music Generation Environment**



**\*\*Problem:\*\* Running ACE-Step 1.5 required additional environment configuration and GPU compatibility adjustments.**



**\*\*Resolution:\*\* Set up the required Python environment and adjusted the generation configuration to use float32 on CUDA with CPU offloading.**



**\*\*Lesson:\*\* AI media-generation systems can require hardware-specific configuration before they work reliably.**



**## 5. Video Subtitle Path on Windows**



**\*\*Problem:\*\* FFmpeg initially failed to process the subtitle filter because the Windows absolute path contained a drive-letter colon.**



**\*\*Resolution:\*\* Changed the subtitle filter to use a project-relative path:**



**`subtitles=assets/subtitles/en.srt`**



**\*\*Lesson:\*\* Relative paths can make media-processing scripts more portable across environments.**



**## 6. Subtitle Readability**



**\*\*Problem:\*\* The initial English subtitles appeared too small in the finished film.**



**\*\*Resolution:\*\* Increased the subtitle font size, used bold Arial, and added an outline and shadow. Regenerated the horizontal and vertical outputs.**



**\*\*Lesson:\*\* Subtitle readability must be checked in the actual viewing format, especially on mobile screens.**



**## 7. Long Video Rendering Time**



**\*\*Problem:\*\* Final video rendering took longer than expected. FFmpeg also paused while waiting for terminal input during one rendering attempt.**



**\*\*Resolution:\*\* Resumed the rendering process and waited for FFmpeg to complete the output file.**



**\*\*Lesson:\*\* Rendering time and terminal interaction should be considered when planning a production schedule.**



**## 8. AI Video Generation Constraints**



**\*\*Problem:\*\* Generating fully animated AI video for every shot was not practical within the available time and technical resources.**



**\*\*Resolution:\*\* Used FFmpeg pan and zoom effects on the generated still images to create smooth moving shots.**



**\*\*Lesson:\*\* A simpler and more controllable technical approach can be effective when it meets the creative and delivery requirements.**



**## 9. General Production Learning**



**The project showed that AI-generated media does not remove the need for human judgment. Prompt adjustment, asset inspection, file validation, audio review, and final video checks were important parts of the workflow.**



**The main improvement for a future version would be to strengthen automation, caching, error handling, and repeatable production from a clean environment.**

