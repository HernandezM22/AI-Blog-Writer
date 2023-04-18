import openai


def string_to_list(string):
    lines = string.strip().split('\n')
    return lines


def generate_prompts_from_word_en(word):
    model_engine = "text-davinci-002"
    prompt = f"Please generate as many NLP prompts in the forms of questions as you can using the key term -{word}- and output them as a list, use - for the list items instead of numbers"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return string_to_list(response.choices[0].text.strip())

def generate_prompt_dict_en(keyterm_list):
    prompt_dict = {}
    for keyterm in keyterm_list:
        prompt_dict[keyterm] = generate_prompts_from_word_en(keyterm)
    return prompt_dict


def write_blogpost_from_prompt_en(prompt):
    text = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a technology blog writer"},
            {"role": "user", "content": f"Write a blogpost of AT LEAST 1000 words about the topic: -{prompt}- be as extense as you can. DO NOT output anything else other than the text."},
        ]
    )

    return text["choices"][0]["message"]["content"]

def generate_prompts_from_word_es(word):
    model_engine = "text-davinci-002"
    prompt = f"Por favor genera prompts de NLP usando la palabra -{word}- y regrésalas como una lista, usa - para los elementos de la lista en lugar de números"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return string_to_list(response.choices[0].text.strip())

def generate_prompt_dict_es(keyterm_list):
    prompt_dict = {}
    for keyterm in keyterm_list:
        prompt_dict[keyterm] = generate_prompts_from_word_es(keyterm)
    return prompt_dict


def write_blogpost_from_prompt_es(prompt):
    text = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "Eres un escritor de blogs de tecnología"},
            {"role": "user", "content": f"Escribe un post de blog de AL MENOS 1000 palabras acerca de: -{prompt}- sé tan extenso como puedas. NO ESCRIBAS NADA MAS QUE EL TEXTO DEL BLOG."},
        ]
    )

    return text["choices"][0]["message"]["content"]