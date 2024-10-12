# message_personalization.py
import openai


class MessagePersonalizer:

    def __init__(self, template, api_key):
        self.template = template
        openai.api_key = api_key

    def personalize_message(self, company_name, about_us_content):
        # Using an LLM model to generate personalized messages
        prompt = f"""
        You are an AI assistant tasked with generating a personalized email introduction for a company. 
        The company is called {company_name}. Here's what the company says about itself:
        '{about_us_content}'

        Now, using the following template, personalize it to fit the company:

        Template: {self.template}
        """

        try:
            response = openai.Completion.create(
                engine="gpt-4",
                prompt=prompt,
                max_tokens=300
            )
            personalized_message = response.choices[0].text.strip()
            return personalized_message
        except Exception as e:
            return f"Error generating personalized message: {str(e)}"


# Example usage
if __name__ == "__main__":
    template = """
    Dear [Company Name],

    I hope this message finds you well. We at [Your Company] have developed an AI solution that can help companies like [Company Name] achieve [specific goals]. Based on your company's mission of [Mission or Values], we believe there's a strong fit between our solution and your current goals.

    I'd love to schedule a time to discuss how we can support your objectives.

    Best regards,
    [Your Name]
    """

    personalizer = MessagePersonalizer(template, "your-openai-api-key")
    company_name = "Example Inc."
    about_us_content = "We are dedicated to providing cutting-edge tech solutions for businesses of all sizes."
    print(personalizer.personalize_message(company_name, about_us_content))
