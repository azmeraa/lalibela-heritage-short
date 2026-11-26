**# COSTS.md**



**## Project: Lalibela — A Story Carved in Stone**



**## 1. Overview**



**This project used a combination of AI services, open-source software, local computing resources, and manual review to produce an 89-second heritage short.**



**The purpose of this document is to identify the resources used and explain the project's cost considerations.**



**## 2. Tools and Services**



**| Tool or Service | Purpose | Cost Information |**

**|---|---|---|**

**| Python | Pipeline development and automation | Open-source |**

**| FFmpeg | Video editing, audio mixing, and encoding | Open-source |**

**| JSON Schema | Storyboard validation | Open-source |**

**| Cloudflare Workers AI | AI image generation using FLUX.2 Klein 4B | Actual usage cost not verified |**

**| Google Gemini TTS | Amharic and English narration | Actual usage cost not verified |**

**| ACE-Step 1.5 | Original music generation | Software is open-source; computing cost not separately measured |**

**| Kaggle GPU environment | Music generation using GPU resources | Actual resource cost not measured |**

**| Local Windows computer | Development, processing, and final assembly | Existing equipment; electricity cost not measured |**



**## 3. Media Production Resources**



**The project generated:**



**- Eight AI keyframe images.**

**- Eight moving-shot video clips.**

**- Amharic and English narration clips.**

**- One original AI-generated music track.**

**- One English subtitle file.**

**- One AI-generated end card.**

**- One horizontal final film.**

**- One vertical final film.**



**## 4. Cost Tracking Limitations**



**The production log records model names, generation parameters, timestamps, latency, and output files for many generation operations.**



**However, exact monetary costs were not consistently available in the generation logs.**



**In particular:**



**- Image-generation cost values were not returned in the recorded results.**

**- Exact narration API charges were not separately verified.**

**- GPU computing costs were not measured.**

**- Local electricity and development time were not monetized.**



**Therefore, this document does not claim an exact total production cost.**



**## 5. Cost Optimization Decisions**



**Several decisions helped keep the project practical:**



**1. Used FFmpeg for camera movement instead of generating a separate AI video for every shot.**

**2. Reused generated assets during final assembly.**

**3. Used a structured storyboard to organize production inputs.**

**4. Selected one music candidate rather than continuing to generate additional tracks.**

**5. Used open-source tools for video processing and pipeline development.**



**## 6. Future Cost Improvements**



**For a future production version, the pipeline should:**



**- Record actual API charges whenever providers expose them.**

**- Estimate costs for services that do not return direct billing information.**

**- Record GPU usage and processing time.**

**- Track the cost of failed and repeated generation attempts.**

**- Compare image-generation and video-generation costs.**

**- Provide a cost summary for each completed production run.**



**## 7. Conclusion**



**The project demonstrates a practical approach to AI-assisted heritage filmmaking using a mixture of cloud AI services and open-source tools.**



**Accurate cost measurement remains an area for improvement. Future versions should integrate provider billing information and more complete resource tracking.**

