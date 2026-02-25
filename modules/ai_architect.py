from google import genai
import os

class AIArchitect:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model_id = 'gemini-2.5-flash'

    def generate_solution(self, bounty_title, bounty_description):
        """
        Generates a solution or proposal for a given bounty.
        """
        prompt = f"""
        Act as an expert developer and strategist. 
        I am an autonomous agent working on Superteam Earn.
        Bounty Title: {bounty_title}
        Bounty Description: {bounty_description}
        
        Please provide a detailed architecture, plan, or content for this submission.
        Format it as a technical document.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                return "🚨 **Gemini API Quota Exceeded**: You have reached the limit for the free tier. Please check your usage at https://aistudio.google.com/app/plan_and_billing or try again later."
            elif "404" in err_msg:
                return f"⚠️ **Model Not Found (404)**: The model `{self.model_id}` could not be initialized. Please verify your API key access."
            return f"❌ **AI Error**: {err_msg}"
