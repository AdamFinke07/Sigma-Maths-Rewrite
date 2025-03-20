from openai import OpenAI

deepseek_api_key = open("env/key.txt", "r").read().strip()

client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")

def get_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    print("Welcome to Deepseek AI Chat!")
    print("Type 'quit' to exit")
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            break
        if user_input:
            print("\nDeepseek AI: ", end="")
            response = get_ai_response(user_input)
            print(response)

if __name__ == "__main__":
    main()

