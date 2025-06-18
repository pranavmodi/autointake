# AI-Driven Patient Intake & Appointment Reminder System

## Product Discovery Ticket: AI-Driven Patient Intake & Appointment Reminders

### Description
We are implementing an AI-driven patient intake system to optimize scheduling, reduce no-shows, and ensure all necessary documents are completed before a patient's visit. The system will integrate with RadFlow 360 to track intake status, automate reminders via SMS and voice calls, and provide real-time AI assistance. A human call will be used as the last step to try and get the intake completed.

This will introduce a new position in the company called **Intake Coordinator** for a human as well as AI.

**Diagram Artifact:** [View Diagram](https://claude.ai/public/artifacts/b5c6178c-9540-4807-bfff-cb321bbeaec7)

---

## Trigger & Conditions

:gun: **Trigger**: Check every time a new order is entered if all intake tasks are completed.

:thermometer: **Conditions**:
- If NOT PI financial type, skip step 1 for liens and change everything to 2 steps.
- We require the following items to be completed prior to scheduling a patient for an exam. If 1 or more of the 3 items are missing, AI will initiate a sequence of events to attempt to get all 3 tasks completed via SMS then voice:
    - Liens
    - Photo ID
    - Pre-screen form
- If all 3 steps are already completed, just send a text informing them we have a new order from their doctor and to schedule online or give us a call.
    - **Text Template**: `Hi [Patient First Name], we received a new imaging order from your doctor. Since your intake is already complete (thanks for that!), you can schedule your appointment online here: :arrow_right: [Scheduling Link] or call us at 818-629-1169 (Mon-Fri, 8 AM – 5 PM). We're happy to assist you!"`
- :phone: Send from a different phone # instead of using our current numbers, so all of the intake texts are in its own thread on their phone. A phone number will be created just for the intake process but if they need human help the message will still go to Front for a human to chat with them as needed.
- :lemon: Use emojis in the replies.
- :x: **Remove**: The current "ordered status" static text message we send in RadFlow automations. See new AI logic here: `AI Scheduling - Outbound Workflow`.
- :rotating_light: **Feature**: In RadFlow automations, we need to be able to turn this entire feature off/on.

---

## Key Features & High-Level Workflow

1.  **Single SMS for Self-Service:**
    - Send a single SMS with a patient portal link for them to do it all themselves.
    - **SMS Template**: `:wave: Hi [Patient First Name], before we can schedule your appointment with Precise Imaging for your {type} exam, we need you to complete a few quick important steps. Go here to sign your lien, upload your photo ID, and fill out a short screening form: :arrow_right: [Patient Portal link].`

2.  **Guided Step-by-Step SMS Workflow:**
    - If they don't complete via the single SMS patient portal link 24 hours after the SMS was sent, the next SMS will guide them through step-by-step.
    - **Step 1: Send Lien E-Sign Link**
        - AI sends an SMS with a secure lien signing link.
        - AI tracks completion in RadFlow 360. Once done, sends SMS for step 2.
    - **Step 2: ID Upload via MMS**
        - AI requests a front & back ID photo via text.
        - Local OCR API verifies the ID, combines the front and back of the ID into one PDF, and sends front ID metadata to RadFlow.
        - AI tracks completion in RadFlow 360. Once done, sends SMS for step 3.
    - **Step 3: Send Pre-Screening Form**
        - AI sends a pre-screening form link.
        - AI verifies submission status in RadFlow 360.
        - If any patient demo information is missing (first name, last name, DOB, accident type, DOI, address, home #), capture it during pre-screen questions, insert it into Radflow, and send it to Ramsoft via HL7.
        - AI tracks completion in RadFlow 360. Once done, sends SMS for step 4.
    - **Step 4: Final Check**
        - If all documents are completed, AI sends a link so they can schedule themselves.
        - If incomplete, AI sends follow-ups.

3.  **Escalation Protocol:**
    - **Voice AI:** If incomplete after 48 hours, follow up with AI voice telling them to check their text messages to complete the intake process before we can schedule them.
    - **Human Call:** If incomplete after 72 hours, a human calls to finish the intake process then transfers them to the scheduler priority queue.

---

## Inbound Call Handling (Phase 2)

This will be its own task but is summarized here. For now, it will route to an Intake queue if the patient has not completed the 3 steps, and the human will guide them through completing any of the missing 3 steps.

### AI-Driven Phone System with Intent Detection
- AI answers all inbound calls immediately.
- Performs a RadFlow 360 database lookup based on the caller's phone number.
    - If it's a known patient phone #, check intake status. If complete, proceed as normal.
    - If not complete, route to a human intake coordinator.
- Routes to the correct AI agent or transfers to a live agent when needed.

---

## Detailed AI-Driven 4-Step Intake Workflow

This streamlined workflow ensures efficient patient intake using automated text messaging and local OCR processing if they don't do it themselves via the portal.

### Step 1: Send Lien E-Sign Link
- **Trigger**: New order comes in and we are missing 1 or more pre-req items.
- **Automated SMS**: `:wave: Hi [Patient First Name], before we can schedule your appointment, we need you to complete a few quick steps. I will personally guide you through each step to make it as easy as possible for you. Should take less than 5 minutes to complete all the steps :clock1:\n\n:one: Step 1 of 3: Click here to sign your medical records release & liens. :arrow_right: [link].`
- **System Check**:
    - If patient completes the lien → Trigger Step 2 automatically.
    - If no response → Follow-up reminder after 24 hours.
    - **Reminder SMS**: `:reminder_ribbon: Just a quick reminder we are still waiting on Step 1 to be completed before we can see you for your exam. \n\nStep 1: Click here to sign your medical records release & liens: :arrow_right: [link].`

### Step 2: Request ID Photos (MMS)

#### Front of ID
- **Automated SMS**: `:slightly_smiling_face: Thank you for signing the medical lien.\n\n:two: Step 2 of 3: :camera_with_flash: Next, please take a clear photo of the FRONT of your driver's license and send it as a reply to this message.`
- **OCR Processing**:
    - Local OCR API analyzes image quality and extracts name, DOB, and address. All items may not be on there depending on the ID type, which is fine. It could be a driver's license, passport, green card, or other government ID. Need to verify it has a photo and its close to their name. Doesn't have to be exact.
    - If unreadable → AI requests a clearer image.
    - Once validated → Trigger request for back of ID.

#### Back of ID
- **Automated SMS**: `:slightly_smiling_face: Thank you for sending the front of the ID.\n\n:camera_with_flash: Now, please take a clear photo of the BACK of your driver's license and send it as a reply to this message.`
- **OCR & Barcode Processing**:
    - Local OCR API decodes barcode and verifies ID authenticity.
    - If barcode → decode and send data to RadFlow. Take front and back image and make into 1 PDF and save to doc manager.
    - If no barcode → take front and back image and make into 1 PDF and save to doc manager.
- **System Check**:
    - Once validated → Trigger Step 3.
    - If no response → Follow-up reminder after 24 hours.

### Step 3: Send Pre-Screening Form Link
- **Automated SMS**: `:checkered_flag: Final step! Please complete this quick pre-screening form: :arrow_right: [pre-screen_link]. \nLet us know when you're done! This should take you about 2-3 minutes :timer_clock:`
- **System Check**:
    - If no response → Follow-up reminder after 24 hours.
    - If form is completed → send SMS:
    - **Completion SMS**: `:slightly_smiling_face: Thank you very much for completing the required items.\n\nPlease visit the link to self-schedule: :arrow_right: [Patient portal self schedule link] or you can call us at 818-629-1169 M-F 8am to 5pm`

### Final Attempt (Escalation)
- **Condition**: If no response in 48 hours or all 3 steps are not completed.
- **Automated Text Example**: `:warning: Last reminder! We can't schedule your appointment until all 3 steps are completed. Click here now: [link]. If you need assistance, reply 'CALL' and we'll walk you through it. :warning:`
- If patient replies "CALL" → Intake Coordinator calls them directly. Send to Front scheduling channel and apply tag `{Intake Coordinator Help}`.

---

## Optimized Features
- ✔ Local OCR API for ID processing – Faster verification without cloud dependency.
- ✔ MMS-based ID submission – Simplifies patient experience.
- ✔ Automated reminders & AI follow-ups – Reduces manual workload.
- ✔ If patient replies "HELP" or wants to talk to a human → Route to Front SMS human, add tag `{Intake coordinator Help}`.
- ✔ Use a Shortened, Personalized Link → Higher engagement. We have `links.radflow360.com/*` for URL shortener.

---

## Tech Stack

| Component | Technology | Purpose |
| --- | --- | --- |
| **SMS Automation** | Twilio | Sends automated texts for lien signing, ID upload, pre-screening forms, and reminders. |
| **AI Voice Calls**| OpenAI Real-Time Voice API | AI-powered inbound & outbound calls for intake assistance and reminders. |
| **Call Routing** | Twilio Voice / FreePBX SIP | Routes patient calls based on intent and transfers to live agents if needed. |
| **Intent Detection** | OpenAI (gpt-4o) | Understands patient inquiries and provides AI-driven responses and actions. |
| **AI Chatbot** | OpenAI (gpt-4o-mini) | Generates text replies for SMS conversations. |
| **Database Lookup**| RadFlow 360 API | Pulls patient intake status and appointment history based on phone number. |
| **OCR & ID Verify**| Local OCR API (Linux VM) | Extracts text & verifies driver's license images. |
| **Lien Signing** | Local RadFlow API | Handles digital lien signing and tracks completion. |
| **Pre-Screening** | Local RadFlow API | Collects patient responses and updates status in RadFlow 360. |
| **Live Agent Voice**| FreePBX | Transfers calls to a human for voice support. |
| **Live Agent Text** | Front | Transfers texts to an intake coordinator if AI detects confusion. |
| **Logging** | RadFlow 360 + Internal Analytics | Tracks intake completion, call logs, and patient interactions. |
| **QA & Testing** | Sandbox Environment | Create sandbox numbers for QA; send staged orders nightly for regression tests. |
