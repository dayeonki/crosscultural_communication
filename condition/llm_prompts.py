NEO_INST = """You are a multilingual language expert, who can understand neologisms very well. Neologism is any newly formed word, term, or phrase that has achieved popular or institutional recognition and is becoming accepted into mainstream language. We are particularly interested in internet slangs, which are non-standard or unofficial forms of language used by people on the Internet (such as social media, forums, or messaging apps) to communicate with one another."""

AI_REWRITE = """Given the social media post with the word "{term}", translate it into plain English, which is suitable for a general audience. You must translate the “{term}” into {target_language}. Return only the translation, no other text.
Post: {text}
Translation: """

AI_EXPLANATION = """Given the word {text}, explain in {target_language} how it is used, including typical situations, tone, intended audience, and connotations. Return only the explanation in 3–5 sentences, no other text.
Word: {text}
Explanation: """

prompt_map = {
    # instructions
    "inst-neo": NEO_INST,
    # task specific
    "ai-rewrite": AI_REWRITE,
    "ai-explain": AI_EXPLANATION,
}
