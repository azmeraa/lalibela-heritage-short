**# Final Project Report**

**## Lalibela: A Story Carved in Stone**



**\*\*Project:\*\* AI-Content Generation – The Heritage Short**  

**\*\*Creator:\*\* Independent AI content creator**  

**\*\*Location:\*\* Ethiopia**  

**\*\*Project date:\*\* November 2026**



**---**



**## 1. Project Overview**



**I created an AI-generated heritage short titled \*Lalibela: A Story Carved in Stone\*. The film introduces the historical, architectural, spiritual, and cultural importance of Lalibela, Ethiopia, to an international audience.**



**The intended audience includes international visitors and people interested in Ethiopian history and cultural heritage.**



**The film uses eight scenes, combining AI-generated images, camera movement, narration in Amharic and English, English subtitles, original background music, and an AI-generated end card.**



**The final film is approximately 89 seconds long and is available in vertical and horizontal formats.**



**## 2. What I Created**



**The project includes:**



**- Eight AI-generated visual keyframes.**

**- An eight-shot storyboard stored in JSON.**

**- A JSON Schema for storyboard validation.**

**- Amharic and English AI-generated narration.**

**- English subtitles.**

**- Original AI-generated background music.**

**- Audio mixing with background music ducked under narration.**

**- Eight moving shots created using FFmpeg pan-and-zoom effects.**

**- Horizontal and vertical MP4 films.**

**- An AI-generated end card.**

**- Project documentation and a Python audience feedback application.**



**## 3. Development Process and Learning**



**I learned how different AI and software tools can work together to produce a complete multimedia story.**



**The development process included story planning, storyboard validation, image generation, narration generation, music creation, audio mixing, video editing, subtitle integration, and final video production.**



**I also learned the importance of organizing project files, validating structured data, testing individual stages, and documenting technical decisions.**



**Developing the Python feedback application helped me understand how software can support the evaluation of AI-generated content.**



**## 4. Hardest Technical Challenge**



**One of the hardest challenges was integrating different AI-generated assets and production tools into a working video pipeline.**



**I encountered technical problems with AI model configuration, audio file formats, FFmpeg filter paths on Windows, and video rendering.**



**For example, FFmpeg initially encountered problems with the Windows drive-letter colon in the subtitle filter path. I resolved this by using a project-relative subtitle path.**



**I also used FFmpeg to create camera movement from still images when full AI video generation was not practical within the available time.**



**These experiences taught me to solve problems systematically and validate each production stage.**



**## 5. Practices That Helped and Did Not Help**



**### Practices that helped**



**- Breaking the production process into smaller stages.**

**- Validating the storyboard before generating assets.**

**- Testing individual images and audio clips before assembling the film.**

**- Keeping generated assets organized.**

**- Using FFmpeg for reliable audio and video processing.**



**### Practices that were less effective**



**Attempting to use more complex AI video generation was not practical within the available development time and computing resources.**



**The project therefore used FFmpeg pan-and-zoom animation as a fallback. This allowed the film to meet its moving-shot requirement without relying on expensive or difficult video-generation infrastructure.**



**## 6. Audience Evaluation**



**A Python-based audience feedback application was developed using Tkinter.**



**The application allows viewers to play the radio cut and final film versions, answer six questions, and save responses in a CSV file. It also provides a feedback summary.**



**The application was tested locally using a sample response with participant code `TEST001`. The software successfully saved the response and identified it as a test record.**



**\*\*Actual audience testing with at least three real viewers remains pending.\*\* Therefore, no real audience findings or resulting design changes are claimed in this report.**



**## 7. What I Would Do With More Time**



**With additional time and resources, I would:**



**- Improve the realism and consistency of AI-generated visual scenes.**

**- Explore more advanced image-to-video generation.**

**- Obtain feedback from Ethiopian heritage experts.**

**- Complete audience testing and document resulting improvements.**

**- Improve the automated production pipeline.**

**- Conduct additional subtitle and audio quality checks.**

**- Improve the feedback application with more detailed analysis.**



**## 8. Next Steps**



**The next steps are to complete audience testing, incorporate genuine feedback, finalize project documentation, publish the source code in a public GitHub repository, and prepare the required project walkthrough and public film links.**



**## 9. Conclusion**



**This project demonstrates how AI tools can support the creation of a short cultural heritage film using accessible technologies and a structured production workflow.**



**Through this work, I gained practical experience in AI-assisted storytelling, multimedia production, software integration, and technical problem-solving.**



**The project also demonstrates the potential of AI-generated content to introduce Ethiopia's cultural heritage to international audiences.**



**---**



**\*\*Project title:\*\* Lalibela: A Story Carved in Stone**  

**\*\*Status:\*\* Film production completed; audience evaluation and final submission activities pending.**

