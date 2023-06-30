from chatgpt_automation import ChatGPT_Client
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
import sys
import random
import json
import jsonlines

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
    "Explain the concept of adjectives and adverbs and their placement in sentences.",
    "Discuss the rules and uses of punctuation marks in English.",
    "Describe the types and uses of prepositions.",
    "Discuss the concept of gerunds and infinitives in English.",
    "Discuss the concept of conditional sentences in English.",
    "Discuss the uses and rules of articles in English.",
    "Explain the concept of subject-verb agreement in English.",
    "Discuss the difference between countable and uncountable nouns.",
    "What is a tense? Discuss the three basic tenses: past, present, and future.",
    "Explain the concept of reported speech in English.",
    "What are phrasal verbs? Provide examples.",
    "Explain the concept of auxiliary verbs and their functions.",
    "Discuss the concept of comparative and superlative adjectives.",
    "Define and provide examples of the use of determiners.",
    "Discuss the rules of capitalization in English writing.",
    "Explain the concept of synonyms, antonyms, and homonyms.",
    "Discuss the concept of singular and plural nouns and their formation.",
    "Define and provide examples of possessive nouns and pronouns.",
    "Discuss the difference between 'few' and 'a few', 'little' and 'a little'.",
    "Explain the use of quantifiers in English.",
    "Describe the concept of relative clauses and provide examples.",
    "Discuss the proper use and placement of adverbial phrases and clauses.",
    "What is a collocation? Provide examples.",
    "Discuss the concept of subjunctive mood in English.",
    "Define and provide examples of idioms and their usage in sentences.",
    "Discuss the concept of noun clauses in English.",
    "Explain the concept of split infinitives and their acceptance in modern English.",
    "Discuss the difference between 'which' and 'that' in restrictive and nonrestrictive clauses.",
    "What is anaphora? Provide examples.",
    "Explain the concept of ellipsis in English grammar.",
    "What are interjections? Provide examples.",
    "Discuss the concept of tag questions in English.",
    "Define and provide examples of euphemisms in English.",
    "Discuss the concept of compound-complex sentences.",
    "Explain the concept of parallelism in English writing.",
    "What is the Oxford comma and when is it used?",
    "Discuss the use of semi-colons in English grammar.",
    "Describe the rules for using hyphens and dashes.",
    "Explain the concept of pronoun antecedent agreement.",
    "Discuss the different types of adverbs: manner, place, time, frequency, degree, and comment.",
    "Define and provide examples of cleft sentences in English.",
    "Discuss the correct usage of 'who' vs 'whom'.",
    "Explain the concept of reflexive pronouns and their usage in English.",
    "Discuss the difference between 'less' and 'fewer'.",
    "Describe the concept of nominalisation in English.",
    "What is cataphora? Provide examples.",
    "Discuss the proper usage of 'lay' vs 'lie'.",
    "What are cognates? Provide examples.",
    "Explain the concept of double negatives in English.",
    "Discuss the concept and rules of contraction in English.",
    "Define and provide examples of irony in English.",
    "Explain the difference between phatic and referential communication, providing examples of each.",
    "Explain the concept of recursion in English grammar and its significance in constructing sentences.",
    "Discuss the transformational rules in syntax and their role in forming grammatical structures.",
    "Define and provide examples of 'Garden Path Sentences'. How does our brain process such sentences?",
    "Discuss the ambiguity in language, focusing on structural and lexical ambiguity. How does understanding grammar help resolve this?",
    "Explain the concept of 'Global vs Local Parsing' in sentence comprehension.",
    "Discuss the idea of 'Syntactic Priming' and its implications for language production and comprehension.",
    "Explain the role of grammar and syntax in 'Sentence Processing Models' such as the Garden Path Model and the Constraint-Based Model.",
    "Discuss the 'Cooperative Principle' in pragmatics and its implications for grammar and sentence structure.",
    "Define and provide examples of 'Center Embedding' in sentences. How does it challenge our sentence processing?",
    "Discuss the role of grammar in 'Speech Act Theory'. How does it contribute to understanding the intended speech acts?"
]

# Define target audiences
audiences = ["primary school students", "middle school students", "high school students", 
             "undergraduate students", "graduate students", "adult learners",
             "English as a Second Language (ESL) students", "linguistics students", 
             "creative writing students", "professional writers", "journalists", 
             "language arts teachers", "tutors and educators", "speech therapists", 
             "individuals studying for language proficiency tests",
             "people learning English for travel", "translators and interpreters", 
             "professional editors", "proofreaders", "academic researchers", 
              "foreign language teachers", "language course designers"]

# Define vocabulary
diversity_vocab = [
    "statement", "question", "command", "exclamation",
    "subject", "predicate", "phrase", "clause",
    "fragment", "negative", "interrogative", "direct", "indirect",
    "pronoun", "verb", "tense", "active", "passive", 
    "modal", "conjunction", "adjective", "adverb", 
    "punctuation", "preposition", "gerund", "infinitive", "conditional", "auxiliary", "subjunctive", "imperative", "transitive", "intransitive",
    "recursion", "ellipsis", "anaphora", "cataphora", "synonym",
    "antonym", "homonym", "cognate", "compound", "complex", 
    "declarative", "interrogative", "exclamatory", "imperative", 
    "determiner", "quantifier", "prepositional phrase", "restrictive", 
    "nonrestrictive", "modal verb", "phrasal verb", "participle", 
    "irregular verb", "pronoun antecedent", "possessive", 
    "relative clause", "reflexive pronoun", "conjunction", 
    "interjection", "idiom", "collocation", "euphemism", 
    "modal auxiliary", "plural", "singular", "past perfect", 
    "present perfect", "future perfect", "reported speech", 
    "double negative", "contraction", "irony", "split infinitive",
    "countable noun", "uncountable noun", "conditional sentence", 
    "noun clause", "adverbial phrase", "center embedding", 
    "nominalisation", "garden path sentence", "syntactic priming", 
    "speech act", "cooperative principle", "global parsing", 
    "local parsing", "hyphen", "dash", "semi-colon", "Oxford comma", 
    "parallelism", "cleft sentence", "less", "fewer", "lay", "lie"
]

# Read the proxy list from a file
with open('/home/karajan/Downloads/Free_Proxy_List.json', 'r') as f:
    proxy_data = json.load(f)

# Extract the IPs and ports and form the proxy strings
proxies = [f"{proxy['ip']}:{proxy['port']}" for proxy in proxy_data]

def init_chatgpt_client_with_proxy(proxy):
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % proxy)
    chatgpt = ChatGPT_Client("user", "password", options)
    return chatgpt

def interact_with_chatgpt(i, prompts, audiences, diversity_vocab, chatgpt):
    print("Running iteration number:", i)

    prompt = random.choice(prompts)
    audience = random.choice(audiences)
    vocab = random.sample(diversity_vocab, 3)  # choose three random vocabulary terms to inject diversity

    complete_prompt = f"Explain to {audience} about '{prompt}', and try to use these words in your explanation: {', '.join(vocab)}."
    
    print("Sending prompt:", complete_prompt)
    
    answer = chatgpt.interact(complete_prompt)

    print("Received answer from ChatGPT, writing to file")

    with open("dataset.jsonl", "a") as f:
        writer = jsonlines.Writer(f)
        record = {'prompt': complete_prompt, 'response': answer}
        writer.write(record)
        f.flush()

    print("Finished writing to file")

# the main logic of the script
for i in range(int(1e9 // 20)):  # number of iterations to generate 1B+ tokens
    try:
        # reinitialize the client and rotate proxy every 500 iterations
        if i % 500 == 0:
            proxy = proxies[i // 500 % len(proxies)]  # rotate through the proxy list
            chatgpt = init_chatgpt_client_with_proxy(proxy)
            print("ChatGPT client reinitialized with proxy:", proxy)

        interact_with_chatgpt(i, prompts, audiences, diversity_vocab, chatgpt)
    except Exception as e:
        print("Error occurred:", str(e))
        print("Restarting script")
        os.execv(sys.executable, ['python'] + sys.argv)

print("Finished all iterations.")
