from chatgpt_automation import ChatGPT_Client
import random
import jsonlines

# Initialize the client
chatgpt = ChatGPT_Client("user", "password")

# Define prompts for various topics
prompts = [
    "Define and provide examples of declarative and interrogative sentences.",
    "Explain the structure of simple, compound, and complex sentences.",
    "Discuss the basic sentence structure in English.",
    "What are subject and predicate? Provide examples.",
    "Illustrate the difference between a phrase and a clause.",
    "Define a sentence fragment and provide examples.",
    "Describe the difference between a statement, a question, a command, and an exclamation.",
    "Discuss how to form negative sentences in English.",
    "Discuss how to form interrogative sentences in English.",
    "Discuss the difference between direct and indirect questions.",
    "Discuss the use and types of pronouns in English.",
    "Explain the use of different verb tenses in English.",
    "Explain the concept of active and passive voice.",
    "What are modal verbs? Provide examples and use cases.",
    "Discuss the use of conjunctions in English.",
    "Explain the concept of adjectives andataset.pyd adverbs and their placement in sentences.",
    "Discuss the rules and uses of punctuation marks in English.",
    "Describe the types and uses of prepositions.",
    "Discuss the concept of gerunds and infinitives in English.",
    "Discuss the concept of conditional sentences in English."
]

# Define target audiences
audiences = ["primary school students", "middle school students", "high school students", 
             "undergraduate students", "graduate students", "adult learners"]

# Define vocabulary
diversity_vocab = [
    "statement", "question", "command", "exclamation",
    "subject", "predicate", "phrase", "clause",
    "fragment", "negative", "interrogative", "direct", "indirect",
    "pronoun", "verb", "tense", "active", "passive", 
    "modal", "conjunction", "adjective", "adverb", 
    "punctuation", "preposition", "gerund", "infinitive", "conditional"
]

# Run the script to generate the dataset
with jsonlines.open('generated_text.jsonl', mode='w') as writer:
    for i in range(int(1e9 // 20)):  # number of iterations to generate 1B+ tokens
        prompt = random.choice(prompts)
        audience = random.choice(audiences)
        vocab = random.sample(diversity_vocab, 3)  # choose three random vocabulary terms to inject diversity
        complete_prompt = f"Explain to {audience} about '{prompt}', and try to use these words in your explanation: {', '.join(vocab)}."
        answer = chatgpt.interact(complete_prompt)
        # Write the prompt and the answer directly to the file
        writer.write({
            "prompt": complete_prompt,
            "answer": answer
        })