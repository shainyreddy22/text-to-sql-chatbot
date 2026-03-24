from agent import run_query

def main():
    print("=" * 50)
    print("  Text-to-SQL Bot — Powered by Qwen / Hugging Face")
    print("  Type 'exit' to quit")
    print("=" * 50)

    examples = [
        "How many albums does each artist have?",
        "Show top 5 customers by total spending",
        "Which genre has the most tracks?",
        "List all invoices above $10",
    ]

    print("\nExample questions:")
    for i, q in enumerate(examples, 1):
        print(f"  {i}. {q}")
    print()

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        print("\nBot: Thinking...\n")
        answer = run_query(user_input)
        print(f"Bot: {answer}\n")
        print("-" * 50)


if __name__ == "__main__":
    main()