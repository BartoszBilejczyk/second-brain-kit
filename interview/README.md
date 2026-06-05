# The Interview

This is how you give your AI a real sense of who you are.

You talk. Freely. About your life, your beliefs, your stories, your opinions. The tangents are often the best material — they're where the real you shows up rather than the polished version.

The AI transcribes your recordings and synthesizes them into linked wiki pages. After 3-5 sessions, it starts to know you well enough to answer questions in your actual voice — not generic AI voice.

---

## How to generate your interview questions

Don't use a generic question list. The best questions are ones that feel written specifically for you — your life, your field, your context.

**Paste this prompt into any LLM (Claude, ChatGPT, Gemini, etc.):**

```
I'm building a personal second brain — a vault of cross-linked markdown pages that captures who I am, what I believe, and how I think. An AI assistant will read these pages and use them to answer questions and write content in my voice.

I need a personalized set of interview questions to populate this brain. Please generate 30-40 questions organized into themes.

About me:
[WHO YOU ARE — 3-5 sentences. Your role, what you do, what you care about.]

[YOUR CONTEXT — what domains matter most to you. E.g.: "I'm an Instagram content creator focused on personal brand. I also care about relationships, mental health, and long-term financial independence."]

[WHAT YOU WANT FROM THE BRAIN — e.g.: "I mainly want it to help me write content in my voice, generate ideas for posts, and think through career decisions."]

[OPTIONAL: any specific topics you want covered that a generic list would miss.]

Please make the questions open-ended and specific to my context. Avoid generic self-help questions. Focus on questions that would surface genuine opinions, defining stories, contradictions, and strong views. I want to record myself answering these — conversationally, not as essays.
```

---

## Example — filled in for a content creator / Instagram influencer

Here's what the prompt looks like when filled in. Use this as a model:

```
About me:
I'm a content creator and Instagram influencer. I post about lifestyle, relationships, personal growth, and aesthetics. I've been building my personal brand for about 3 years. My audience is mostly people my age who are figuring out life — career, relationships, identity.

My context:
Content creation is my main focus. I also care deeply about relationships (I think how you connect with people is a reflection of who you are), money (I'm still working out my relationship with it — earning from content feels different to earning from a "real job"), and personal growth (the honest kind, not the toxic positivity kind).

What I want from the brain:
Mainly to write captions, scripts, and post ideas that sound genuinely like me — not like AI content. I also want to find my unique angles on topics and remember the specific stories and opinions that make me different from other creators.

Specific topics I want covered:
- Why I create content (not the "I want to inspire people" answer — the real one)
- My relationship with my audience and how much of myself I actually share
- How my content has changed me (and not always in good ways)
- My aesthetics philosophy — what I find beautiful and why
- How I handle comparison with other creators
- My relationship with money and how it affects what I post about
- What I would never post about and why
```

This generates questions like:
- "What was the first piece of content you created that felt genuinely like you? What made it different?"
- "When did you last feel uncomfortable with how much you'd shared? What happened?"
- "Describe your relationship with comparison in one honest sentence."
- "What's a view you have about content creation that most creators would disagree with?"

---

## Categories to consider

Use these as inspiration — your question generator will likely cover most of them:

- **Origin story** — where you came from, what shaped you
- **Core beliefs** — things you'd actually defend in an argument
- **Work and craft** — how you work, what you care about in your field
- **Money** — your real relationship with it, not the aspirational version
- **Relationships** — how you love, what you need, what you give
- **Identity** — who you are when no one's watching
- **Voice and communication** — how you sound, what you never say
- **Aesthetics and taste** — what you find beautiful or meaningful
- **Fears and contradictions** — the stuff you'd rather not admit but know is true
- **Domain-specific** — whatever is most relevant to *you* (your industry, your platform, your specific life situation)

---

## Tips for recording

- **Talk, don't write.** The transcription captures how you actually speak. That's the point.
- **Don't edit yourself.** The first answer is usually more honest than the polished one.
- **One theme per recording** works well — it gives brain-ingest a clear focus.
- **Tangents are welcome.** If you start answering "why I create" and end up talking about your childhood, that's gold.
- Save recordings as `.m4a`, `.mp3`, or `.wav` in the `recordings/` folder next to this file.
- Then run `/brain-transcribe` → `/brain-ingest`.

---

## Saving your generated questions

Save your LLM-generated questions as markdown files here:

```
interview/
├── 01-identity-and-origins.md
├── 02-work-and-craft.md
├── 03-relationships.md
└── recordings/
    ├── session-01-identity.m4a
    └── session-02-work.m4a
```

You don't have to answer them all at once. One theme per session is a good pace.
