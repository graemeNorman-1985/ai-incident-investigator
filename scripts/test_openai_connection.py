from openai import OpenAI


def main() -> None:
    client = OpenAI()

    response = client.responses.create(
        model="gpt-5-mini",
        input="Explain what a database connection pool does in one sentence.",
    )

    print(response.output_text)


if __name__ == "__main__":
    main()