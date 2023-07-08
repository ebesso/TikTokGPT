import openai, os, json

def save_story(title, content):
    path = 'content/gpt/AITA/{file_name}.txt'
    with open(path.format(file_name=title), 'w+') as f:
        f.write(content)

openai.api_key = os.environ['OPENAI_SECRET']

nbr_of_stories = 1

total_prompt_tokens = 0
total_completion_tokens = 0

for i in range(nbr_of_stories):
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {
                'role': "system",
                'content': "You are a young adult using reddit"
            },
            {
                'role': 'user',
                'content': 'Write a AITA post. Do not use the word reddit'
            }
        ],
        functions=[
            {
                'name': 'save_story',
                'description': 'saves the generated story and title to a txt file',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'title': {
                            'type': 'string',
                            'description': 'The posts title'
                        },
                        'content': {
                            'type': 'string',
                            'description': 'The posts content'
                        }
                    },
                    'required': ['title', 'content']
                }
            }    
        ],
        function_call={"name": "save_story"}
    )

    arguments = json.loads(resp['choices'][0]['message']['function_call']['arguments'])

    save_story(arguments['title'], arguments['content'])

    total_prompt_tokens += resp['usage']['prompt_tokens']
    total_completion_tokens += resp['usage']['completion_tokens']

usd_to_sek = 10.82

cost_per_input_token = 0.0015 / 10**3 * usd_to_sek
cost_per_output_token = 0.002 / 10**3 * usd_to_sek

print(f'''
Done. \n
Usage:
Prompt_tokens: {total_prompt_tokens}
Completion tokens: {total_completion_tokens}
Total tokens: {total_completion_tokens + total_prompt_tokens}
Total cost: {total_completion_tokens*cost_per_output_token + total_prompt_tokens*cost_per_input_token}kr
''')


