import csv
import os

data = [
    # Team 16
    {"Grupo": "Team 16 (Bystron)", "Tarea": "2", "LLM": "Gemini", "Tipo": "Spelling/Initial", "Prompt": "“Analyze this website: https://www.manchester.ac.uk/about/our-story/ to identify elements in the webpage that are not Easy to Read compliant, specifically, look for special characters like \, &, <, § or #”"},
    {"Grupo": "Team 16 (Bystron)", "Tarea": "2", "LLM": "Gemini", "Tipo": "Spelling/Punctuation", "Prompt": "“Now analyze the page for parentheses and square brackets”"},
    {"Grupo": "Team 16 (Bystron)", "Tarea": "2", "LLM": "Gemini", "Tipo": "Spelling/Abbr", "Prompt": "“Now analyze the page for abbreviations, acronyms, and initials”"},
    {"Grupo": "Team 16 (Bystron)", "Tarea": "2", "LLM": "Gemini", "Tipo": "Spelling/Symbols", "Prompt": "“Now analyze the page for 'etc.' and suspension points”"},
    {"Grupo": "Team 16 (Bystron)", "Tarea": "2", "LLM": "Gemini", "Tipo": "Spelling/Punctuation", "Prompt": "“Now analyze the page for semi colons”"},
    {"Grupo": "Team 16 (Bystron)", "Tarea": "2", "LLM": "Gemini", "Tipo": "Evaluation", "Prompt": "“Evaluate overall suitability for Easy-to-Read audiences.”"},
    {"Grupo": "Team 16 (Bystron)", "Tarea": "2", "LLM": "Gemini", "Tipo": "Grammar/New Chat", "Prompt": "“Analyze this webpage: https://www.manchester.ac.uk/about/our-story/ for easy-to-read guidelines around grammar. This means analyze for passive language/voice, negative sentences, gerund forms, and starting sentences on new lines”"},
    {"Grupo": "Team 16 (Bystron)", "Tarea": "3", "LLM": "ChatGPT", "Tipo": "Initial", "Prompt": "“Now I need an adaption of this text following the easy-to-read methodology. Can you support me doing that? Let me know if you need any help or you have any questions?“"},
    {"Grupo": "Team 16 (Bystron)", "Tarea": "3", "LLM": "ChatGPT", "Tipo": "Refinement", "Prompt": "“Inclusion Europe is great. I dress people with learning disabilities. We want it very simplified. Every technical term needs an explanation. It should be continuous text. And the entire text adapted please.“"},
    {"Grupo": "Team 16 (Bystron)", "Tarea": "3", "LLM": "ChatGPT", "Tipo": "Headlines", "Prompt": "“Maybe we can add some headlines to the e2r version - what do you think?“"},
    {"Grupo": "Team 16 (Bystron)", "Tarea": "3", "LLM": "Gemini", "Tipo": "Selection", "Prompt": "“Convert 800 words of this document into Easy to Read Text starting from page 4”"},
    {"Grupo": "Team 16 (Bystron)", "Tarea": "3", "LLM": "Gemini", "Tipo": "Correction", "Prompt": "“No, begin on page 4. Take 800 words of the document in order beginning on page 4 and convert only those 800 words into easy to read text”"},
    {"Grupo": "Team 16 (Bystron)", "Tarea": "3", "LLM": "Gemini", "Tipo": "Compliance", "Prompt": "“Must comply with Easy-to-Read requirments”"},
    {"Grupo": "Team 16 (Bystron)", "Tarea": "3", "LLM": "Gemini", "Tipo": "Text Input", "Prompt": "“Convert this text into a text that is fully compliant with all Easy 2 Read guidelines set by Inclusion Europe Guidelines: [text]”"},
    
    # Team 23
    {"Grupo": "Team 23 (Alaa Eddin/Ruth)", "Tarea": "2", "LLM": "Gemini", "Tipo": "Analysis", "Prompt": "Act as an Easy-to-Read (E2R) analysis tool. I will paste a text below. Please scan it for the following errors: Sentences longer than 15 words. Passive voice. Complex words or jargon. Use of acronyms or parentheses. Text: [Pasted Text]. Report your findings in a list format."},
    {"Grupo": "Team 23 (Alaa Eddin/Ruth)", "Tarea": "2", "LLM": "ChatGPT", "Tipo": "Checklist", "Prompt": "Review the provided website's contents according to the easy-to-read (specifically e2r methodology) checklist. For each row in the checklist, write yes/no/unknown(unable to determine), and write details based on the site. If ANY example is found, then that element is present, state this clearly (not “rarely” or “partly”). Negative sentences are not for negative semantics but for negation."},
    {"Grupo": "Team 23 (Alaa Eddin/Ruth)", "Tarea": "3", "LLM": "Gemini/ChatGPT", "Tipo": "Adaptation", "Prompt": "Rewrite the following text to fully comply with Easy-to-Read methodology. Rules: Use simple vocabulary only. One sentence per line where possible. No passive voice. Summarize complex sections into bullet points. Text: [Pasted Text]."},
    
    # Team 21
    {"Grupo": "Team 21 (Zhang/Tao)", "Tarea": "2", "LLM": "GPT/Gemini", "Tipo": "Spelling", "Prompt": "Please analyse the following web page text and identify any spelling-related elements that are not compliant with Easy-to-Read guidelines (e.g., special characters, abbreviations)."},
    {"Grupo": "Team 21 (Zhang/Tao)", "Tarea": "2", "LLM": "GPT/Gemini", "Tipo": "Grammar", "Prompt": "Based on Easy-to-Read guidelines, please identify grammar-related issues (passive voice, negative sentences)."},
    {"Grupo": "Team 21 (Zhang/Tao)", "Tarea": "2", "LLM": "GPT/Gemini", "Tipo": "Vocabulary", "Prompt": "Please identify vocabulary-related elements (abstract terms, synonyms, adverbs ending in -ly)."},
    {"Grupo": "Team 21 (Zhang/Tao)", "Tarea": "2", "LLM": "GPT/Gemini", "Tipo": "Composition", "Prompt": "Please analyse the structure for composition-related issues (long paragraphs, lack of bullet points)."},
    {"Grupo": "Team 21 (Zhang/Tao)", "Tarea": "3", "LLM": "GPT/Gemini", "Tipo": "Adaptation 1", "Prompt": "Please act as an expert in Cognitive Accessibility. Your task is to adapt the following text into Easy-to-Read (E2R) format. Strict guidelines: 1. Use extremely short sentences (one idea per sentence). 2. Use Active Voice only. 3. Use simple, everyday words (A2 level). 4. Summarize main points but keep essential contact info. 5. Do not change proper names of places."},
    {"Grupo": "Team 21 (Zhang/Tao)", "Tarea": "3", "LLM": "GPT/Gemini", "Tipo": "Adaptation 2", "Prompt": "Please act as an expert in Cognitive Accessibility. Adapt the following text into Easy-to-Read format. Strict rules: 1. One idea per sentence. 2. Active Voice only. 3. Simple vocabulary (A2 level). 4. Do not change proper names."},
    
    # Team 1
    {"Grupo": "Team 1 (Sanchez Gimeno)", "Tarea": "2", "LLM": "GPT/Claude/Gemini", "Tipo": "Analysis", "Prompt": "“Verify the following web page to analyze if it follows the Easy to Read guidelines, to do so take into account (wait until the text from the web page is provided): [List: Spelling, Grammar, Vocabulary, Composition]”"},
    {"Grupo": "Team 1 (Sanchez Gimeno)", "Tarea": "3", "LLM": "GPT/Claude/Gemini", "Tipo": "Proposal", "Prompt": "“Given this document, produce a proposal for a new document that follows Easy to Read guidelines, to do so take into account [List: Spelling, Grammar, Vocabulary, Composition]”"},
    
    # Team 3
    {"Grupo": "Team 3 (Rajaonah)", "Tarea": "2", "LLM": "Gemini/ChatGPT", "Tipo": "Assessment", "Prompt": "“I need you to assess point by point each one of the E2R requirements in the photo/excel spreadsheet cells I have uploaded with regards to the article whose link I am pasting. I have also pasted the full article. For each one of the requirements, tell me if its present and list all the occurences you found in the text.”"},
    {"Grupo": "Team 3 (Rajaonah)", "Tarea": "3", "LLM": "Gemini/ChatGPT", "Tipo": "Transformation", "Prompt": "“Given this template I need you to transform into an easy to read (E2R) format this text. For each change you make you must report the original text, the new text, and an explanation for why you changed it like this. Here is the template (image). And here is the text to adapt: [text]”"},
    
    # Team 4
    {"Grupo": "Team 4 (Aller/Van Steijn)", "Tarea": "2", "LLM": "Copilot/ChatGPT", "Tipo": "Evaluation", "Prompt": "“I need to evaluate the following website: X . The evaluation needs to be based on specific easy-to-read elements below: [List]”"},
    {"Grupo": "Team 4 (Aller/Van Steijn)", "Tarea": "2", "LLM": "Copilot/ChatGPT", "Tipo": "Format", "Prompt": "“Please provide the answers in a simple table structure.”"},
    {"Grupo": "Team 4 (Aller/Van Steijn)", "Tarea": "3", "LLM": "Gemini/ChatGPT", "Tipo": "Adaptation", "Prompt": "“I need to adapt the following text into the Easy-to-Read (E2R) methodology. Please follow these strict rules from the IFLA 2010 standards:* One idea per sentence...* New line rule...* Grammar: Use active voice... Vocabulary: Use simple words. If a difficult word is needed, write it in bold and explain it...* Numbers: Write digits...* Lists: Use bullet points...”"},
    
    # Team 5
    {"Grupo": "Team 5 (Osadici)", "Tarea": "2", "LLM": "Gemini", "Tipo": "Analysis", "Prompt": "Act as an Easy-to-Read (E2R) analysis tool. I will paste a text below. Please scan it for the following errors: Sentences longer than 15 words. Passive voice. Complex words or jargon. Use of acronyms or parentheses. Text: [Pasted Text]. Report your findings in a list format."},
    {"Grupo": "Team 5 (Osadici)", "Tarea": "2", "LLM": "ChatGPT", "Tipo": "Checklist", "Prompt": "Review the provided website’s contents according to the easy-to-read (specifically e2r methodology) checklist. For each row in the checklist, write yes/no/unknown(unable to determine), and write details based on the site. If ANY example is found, then that element is present, state this clearly. Negative sentences are not for negative semantics but for negation."},
    {"Grupo": "Team 5 (Osadici)", "Tarea": "3", "LLM": "ChatGPT", "Tipo": "Formatting", "Prompt": "can you format it nice for e2r? maybe some bullet points where necessary, can you make in bold the complicated words? Pay attention to correct formatting following the methodology:"},
    {"Grupo": "Team 5 (Osadici)", "Tarea": "3", "LLM": "ChatGPT", "Tipo": "Refinement", "Prompt": "Please be careful with numbers (remove some if necessary, keep only the most important ones) and structure the text clearly using numbered sections 1., 2., 3."},

    # Team 7
    {"Grupo": "Team 7 (Soleimani/Guillermet)", "Tarea": "2", "LLM": "ChatGPT", "Tipo": "Checklist", "Prompt": "“Based on this website, tell me if it respects those criteria: E2R Guidelines... For each of them, if yes, give an example; if not, also give an example; and if you don’t know, say you don’t know. TEXT.”"},
    {"Grupo": "Team 7 (Soleimani/Guillermet)", "Tarea": "3", "LLM": "ChatGPT", "Tipo": "Initial", "Prompt": "“Could you write this text in Easy-to-Read, please: TEXT.”"},
    {"Grupo": "Team 7 (Soleimani/Guillermet)", "Tarea": "3", "LLM": "ChatGPT", "Tipo": "Methodology", "Prompt": "“Be careful and respect the E2R Methodology. And explain the modifications you made.”"},
    {"Grupo": "Team 7 (Soleimani/Guillermet)", "Tarea": "3", "LLM": "ChatGPT", "Tipo": "Numbers/Structure", "Prompt": "“Please be careful with numbers (remove some if necessary, keep only the most important ones) and structure the text clearly using numbered sections 1., 2., 3.”"},

    # Team 6
    {"Grupo": "Team 6 (Corrado/Anzillotti)", "Tarea": "2", "LLM": "GPT/Gemini", "Tipo": "Description", "Prompt": "Identify non-compliant elements. For each issue: quote the text, explain the problem, and categorise it under E2R sections (spelling, grammar, vocabulary, composition)."},
    {"Grupo": "Team 6 (Corrado/Anzillotti)", "Tarea": "3", "LLM": "GPT/Gemini", "Tipo": "Description", "Prompt": "Create E2R versions of about 800 words while preserving all original information. Conditions: no adding/removing content, consistent terminology, active voice, explain abbreviations, change comma-separated lists to bullet points."},

    # Team 8
    {"Grupo": "Team 8 (Bollen/Friedrichsmeier)", "Tarea": "2", "LLM": "ChatGPT", "Tipo": "Setup", "Prompt": "“For an assignment you are tasked to act as an evaluation tool to evaluate website as Easy to Read, this will be done with the help of the following excel sheet: [PartII-E2R-Analysis-Checklist uploaded]”"},
    {"Grupo": "Team 8 (Bollen/Friedrichsmeier)", "Tarea": "3", "LLM": "ChatGPT/Gemini", "Tipo": "Adaptation", "Prompt": "“PDF uploaded. Adapt it to Easy to Read.”"},

    # Team 10
    {"Grupo": "Team 10 (Kusta/Shkurti)", "Tarea": "2", "LLM": "Claude/ChatGPT", "Tipo": "Comprehensive", "Prompt": "“I need you to analyze this text for Easy-to-Read (E2R) compliance. Please identify the following elements: 1-15... For each element, please: - Count how many instances appear - Provide specific examples from the text - Note if the text is E2R compliant or not.”"},
    {"Grupo": "Team 10 (Kusta/Shkurti)", "Tarea": "3", "LLM": "Claude/ChatGPT", "Tipo": "Adaptation", "Prompt": "Convert the text to Easy to Read format following the 4 main categories (Spelling, Grammar, Vocabulary, Composition)."},

    # Team 9
    {"Grupo": "Team 9 (Lopez/Hernandez)", "Tarea": "2", "LLM": "Gemini", "Tipo": "Description", "Prompt": "Analyze web pages according to the Easy-to-Read Methodology. Resources provided and desired outcome (comments) specified."},
    {"Grupo": "Team 9 (Lopez/Hernandez)", "Tarea": "3", "LLM": "Gemini", "Tipo": "Description", "Prompt": "Propose E2R adaptations for Part III. Provided the resources and desired outcome."},

    # Team 14
    {"Grupo": "Team 14 (Salami/Papapicco)", "Tarea": "2", "LLM": "Gemini/ChatGPT", "Tipo": "Checklist", "Prompt": "”Act as an expert in cognitive accessibility. Analyze the provided text against the E2R Checklist. Identify every instance of: [Spelling, Grammar, Vocabulary, Composition]. Provide the results in a table with columns: ’Elements to be identified’, ’Value’, ’Details’, and ’Comments’.”"},
    {"Grupo": "Team 14 (Salami/Papapicco)", "Tarea": "3", "LLM": "Gemini/ChatGPT/Claude", "Tipo": "Adaptation", "Prompt": "”Act as an expert in cognitive accessibility and the Easy-to-Read (E2R) methodology. Adapt the following text by following these rules: Layout (new line per sentence), Grammar (active voice, no gerunds/negation), Vocabulary (simple words, no metaphors), Composition (bullets), Numbers (digits).”"},

    # Team 11
    {"Grupo": "Team 11 (Momcilovic/Varela)", "Tarea": "2", "LLM": "ChatGPT/Gemini", "Tipo": "Español", "Prompt": "“Elabora un analisis de E2R de la siguiente página web con los siguientes puntos: [List 1-15]”"},
    {"Grupo": "Team 11 (Momcilovic/Varela)", "Tarea": "3", "LLM": "ChatGPT/Gemini", "Tipo": "Rules", "Prompt": "“Rewrite the following text using Easy-to-Read (E2R) guidelines. Rules: short sentences, one idea per line, start each sentence on a new line, avoid passive voice, avoid long words, explain abbreviations, keep meaning, do not summarize.”"},

    # Team 12
    {"Grupo": "Team 12 (Cifrian/Van Lieshout)", "Tarea": "2", "LLM": "Gemini/Claude", "Tipo": "Workflow", "Prompt": "Assistant should thoroughly read the webpage... evaluate against E2R guidelines... organize into 4 categories. Identify non-compliant instances."},
    {"Grupo": "Team 12 (Cifrian/Van Lieshout)", "Tarea": "3", "LLM": "ChatGPT", "Tipo": "Table Format", "Prompt": "Propose a revised version that follows E2R principles. Output: Original | Proposal | Comments. Rules: one idea per line, direct address ('you'), new sentence on new line, sans-serif (Arial 14), explain initials, write numbers as digits."},

    # Team 13
    {"Grupo": "Team 13 (Catalano/Inci)", "Tarea": "2", "LLM": "ChatGPT/Gemini", "Tipo": "Scale 1-4", "Prompt": "Analysis of text found within BBC website... categories: spelling, grammar, vocabulary, composition... Give me a value: 1. Identified by tool, 2. Partially ID, 3. Not ID, 4. Identified by evaluator.”"},
    {"Grupo": "Team 13 (Catalano/Inci)", "Tarea": "3", "LLM": "ChatGPT/Gemini", "Tipo": "A1 Level", "Prompt": "Full translation into E2R version... Guidelines: Lexical Simplification, Syntactic Simplification, Design/Layout. Cognitive level: A1 English."},

    # Team 14 (Dudhiawala duplicates)
    {"Grupo": "Team 14 (Dudhiawala/Papakonstantinou)", "Tarea": "2", "LLM": "ChatGPT/Gemini", "Tipo": "Think Aloud", "Prompt": "Analyze selected web pages through the lens of E2R guidelines... explicitly instructed to 'think aloud' to ensure transparency."},
    {"Grupo": "Team 14 (Dudhiawala/Papakonstantinou)", "Tarea": "3", "LLM": "ChatGPT/Gemini", "Tipo": "Simplification", "Prompt": "Adapt the given texts and propose E2R versions. principles: short sentences, one idea per sentence, starting each sentence on a new line. Think aloud."},

    # Team 15
    {"Grupo": "Team 15 (Alonso/Martin)", "Tarea": "2", "LLM": "ChatGPT/Copilot", "Tipo": "Checklist", "Prompt": "Evaluated texts according to E2R guidelines covering spelling, grammar, vocabulary, and text composition."},
    {"Grupo": "Team 15 (Alonso/Martin)", "Tarea": "3", "LLM": "ChatGPT/Copilot", "Tipo": "Criteria", "Prompt": "“I need you to adapt the text using the Easy to Read methodology and following the list of guidelines. around 800 words. List: [Linguistic, Grammar, Vocabulary, Composition]”"},

    # Team 17/27
    {"Grupo": "Team 17 (Maoro/Cirillo)", "Tarea": "2", "LLM": "ChatGPT/Gemini", "Tipo": "Progressive 1", "Prompt": "This is the text of a web page... determine if it complies with E2R. characters such as \, &, <, §, or #?"},
    {"Grupo": "Team 17 (Maoro/Cirillo)", "Tarea": "2", "LLM": "ChatGPT/Gemini", "Tipo": "Progressive 2", "Prompt": "The text contains parenthesis and square brackets?"},
    {"Grupo": "Team 17 (Maoro/Cirillo)", "Tarea": "2", "LLM": "ChatGPT/Gemini", "Tipo": "Progressive 3", "Prompt": "The text contains Abbreviations, acronyms, and initials?"},
    {"Grupo": "Team 17 (Maoro/Cirillo)", "Tarea": "2", "LLM": "ChatGPT/Gemini", "Tipo": "Progressive 7-8", "Prompt": "The text contains Passive language/voice? Negative sentences? Gerund forms?"},
    {"Grupo": "Team 17 (Maoro/Cirillo)", "Tarea": "3", "LLM": "Gemini / Read Easy.ai", "Tipo": "Rules check", "Prompt": "Check to ensure it follows E2R rules: Keep punctuation simple... Avoid abbreviations... No difficult ideas like metaphors. Now I will send you sentences and tell me if they follow E2R rules."},

    # Team 19
    {"Grupo": "Team 19 (Ollero/Alonso Geesink)", "Tarea": "2", "LLM": "Gemini 3 Pro", "Tipo": "Slides context", "Prompt": "I will ask you a series of questions about the following text... methodology defined in the attached slides. [TEXT]"},
    {"Grupo": "Team 19 (Ollero/Alonso Geesink)", "Tarea": "2", "LLM": "Gemini 3 Pro", "Tipo": "Specific Quest", "Prompt": "Does the text contain special characters? parentheses? abbreviations? passive voice? etc."},
    {"Grupo": "Team 19 (Ollero/Alonso Geesink)", "Tarea": "3", "LLM": "Gemini/GPT", "Tipo": "Iterative", "Prompt": "I will be giving you a text paragraph by paragraph to convert to easy-to-read format. In attached slides there are examples."},
    {"Grupo": "Team 19 (Ollero/Alonso Geesink)", "Tarea": "3", "LLM": "Gemini/GPT", "Tipo": "Refinement", "Prompt": "It's a bit too long, cut out some parts... numbers should be words like few or many."},

    # Team 20
    {"Grupo": "Team 20 (Susano/Hernando)", "Tarea": "2", "LLM": "ChatGPT/Gemini", "Tipo": "Analysis", "Prompt": "Analyzed web pages according to E2R guidelines."},
    {"Grupo": "Team 20 (Susano/Hernando)", "Tarea": "3", "LLM": "Gemini/FACILE", "Tipo": "Multi-aspect", "Prompt": "Detailed instructions on: spelling, grammar, vocabulary, images, typography, composition. Emphasized: short sentences, no abbreviations/percentages, simple images."},

    # Team 25
    {"Grupo": "Team 25 (Verzes/Ma)", "Tarea": "2", "LLM": "Gemini/ChatGPT", "Tipo": "Expert Role", "Prompt": "Role: Act as an expert Editor and Accessibility Auditor specializing in E2R. Task: Analyze Input Text. Identify and extract every non-compliant element grouped by categories. Quote violation."},
    {"Grupo": "Team 25 (Verzes/Ma)", "Tarea": "3", "LLM": "Gemini/ChatGPT", "Tipo": "Expert Role", "Prompt": "Role: Expert in Cognitive Accessibility. Task: Adapt text into E2R format. ~800 words. Do not summarize. Table columns: Original Text, Proposal, Comments."},

    # Team 28
    {"Grupo": "Team 28 (Weerapperuma/Gluck)", "Tarea": "2", "LLM": "ChatGPT/Gemini", "Tipo": "Justification", "Prompt": "Perform E2R analysis according to checklist. Give justification for each row and point to places in text."},
    {"Grupo": "Team 28 (Weerapperuma/Gluck)", "Tarea": "2", "LLM": "ChatGPT/Gemini", "Tipo": "Table results", "Prompt": "Perform E2R analysis according to checklist. Make a table and tell me if you have identified violations and give examples."},
    {"Grupo": "Team 28 (Weerapperuma/Gluck)", "Tarea": "3", "LLM": "ChatGPT/Gemini", "Tipo": "Chunking", "Prompt": "Adapt this text to E2R standard. Divide text into chunks and suggest substitutions. First col chunks, second adaptation. Don't skip content."},
    {"Grupo": "Team 28 (Weerapperuma/Gluck)", "Tarea": "3", "LLM": "ChatGPT/Gemini", "Tipo": "Sentence by sentence", "Prompt": "Convert text to E2R format. Do it sentence by sentence of the original. Big table sentence by sentence."},

    # Team 30
    {"Grupo": "Team 30 (Ciurana/Celie)", "Tarea": "2", "LLM": "Gemini", "Tipo": "Simple", "Prompt": "Dime si ves alguna [infracción] en la página: [Texto]"},
    {"Grupo": "Team 30 (Ciurana/Celie)", "Tarea": "3", "LLM": "Gemini", "Tipo": "Specific correction", "Prompt": "Cómo cambiarías ambos superlativos? 'ultraperiféricas' y 'superiores'. Dame solo el extracto."},

    # Team 31
    {"Grupo": "Team 31 (Gismera/Jordan)", "Tarea": "2", "LLM": "ChatGPT/Gemini", "Tipo": "Detail-oriented", "Prompt": "Analyze text according to E2R guidelines. For EACH element, provide a concise analysis for the 'Details' column. If present, describe and give examples."},
    {"Grupo": "Team 31 (Gismera/Jordan)", "Tarea": "3", "LLM": "ChatGPT/Gemini", "Tipo": "Strict constraints", "Prompt": "Adapt text so it fully complies with E2R methodology. Do not rewrite creatively. Keep meaning. Do NOT summarize or shorten. Follow rules strictly."},

    # Team 2 (Sankar) - Descriptions based on results
    {"Grupo": "Team 2 (Sankar/Abar)", "Tarea": "2", "LLM": "Claude", "Tipo": "Academic", "Prompt": "Analyze following E2R methodology (provided as lecture notes). Output format: 'E2R: [guideline]. [Problem]. [Alternative].'"},
    {"Grupo": "Team 2 (Sankar/Abar)", "Tarea": "3", "LLM": "Claude", "Tipo": "Prescriptive", "Prompt": "Adapt text according to lecture material. Include '[IMAGE: Picture of...]' for suggestions. Rules are rigid (must always)."},
    
    # Salami Ilaria (Papapicco) - Already in Team 14 list but let's separate if needed.
    # I already added Team 14 (Salami/Papapicco).
]

# Write to CSV
output_path = "/home/javi/practices/data/llm_comparison/prompts_analysis.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Grupo", "Tarea", "LLM", "Tipo", "Prompt"])
    writer.writeheader()
    writer.writerows(data)

print(f"Generated {len(data)} prompt entries to {output_path}")
