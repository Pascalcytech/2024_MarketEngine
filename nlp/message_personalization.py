import time

import openai


class MessagePersonalizer:

    def __init__(self, template, api_key):
        self.template = template
        openai.api_key = api_key

    def personalize_message(self, company_name, about_us_content):
        prompt = (
            f"Generate a personalized message for {company_name}. Here's their info: '{about_us_content}'"
            f" Using this template: \n{self.template}"
        )

        try:
            response = openai.chat.completions.create(
                model="text-embedding-3-small",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            tokens_used = response['usage']['total_tokens']
            print(f"Tokens used in this request: {tokens_used}")
            personalized_message = response['choices'][0]['message']['content'].strip()
            return personalized_message

        except openai.error.RateLimitError as e:
            print("Rate limit exceeded. Retrying after delay...")
            time.sleep(60)  # Wait for 60 seconds before retrying
            return self.personalize_message(company_name, about_us_content)
        except openai.error.OpenAIError as e:
            return f"Error: {str(e)}"


# Example usage
if __name__ == "__main__":
    template = """
    Dear [Company Name],

    I hope this message finds you well. We at [Your Company] have developed an AI solution that can help companies 
    like [Company Name] achieve [specific goals]. Based on your company's mission of [Mission or Values], we believe 
    there's a strong fit between our solution and your current goals.

    I'd love to schedule a time to discuss how we can support your objectives.

    Best regards,
    [Your Name]
    """

    personalizer = MessagePersonalizer(template, "")
    company_name = "mobileye"
    about_us_content = ("Company Solutions Technology CEO Corner Newsroom THE BEGINNING Mobileye was founded in 1999, "
                        "by Prof. Amnon Shashua, when he evolved his academic research at the Hebrew University of "
                        "Jerusalem into a monocular vision system to detect vehicles using only a camera and software "
                        "algorithms on a processor...")
    print(personalizer.personalize_message(company_name, about_us_content))
