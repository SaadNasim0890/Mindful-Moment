print("Importing ChatPromptTemplate...")
try:
    from langchain_core.prompts import ChatPromptTemplate
    print("ChatPromptTemplate imported.")
except Exception as e:
    print(f"ChatPromptTemplate failed: {e}")

print("Importing JsonOutputParser...")
try:
    from langchain_core.output_parsers import JsonOutputParser
    print("JsonOutputParser imported.")
except Exception as e:
    print(f"JsonOutputParser failed: {e}")

print("Importing ChatOllama...")
try:
    from langchain_community.chat_models import ChatOllama
    print("ChatOllama imported.")
except Exception as e:
    print(f"ChatOllama failed: {e}")
