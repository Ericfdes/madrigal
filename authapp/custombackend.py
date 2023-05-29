from social_core.backends.linkedin import LinkedinOAuth2

class ExtractLinkedinOAuth2(LinkedinOAuth2):
    name = 'extract-linkedin-oauth2'

    KEY_SETTING = 'SOCIAL_AUTH_EXTRACT_LINKEDIN_OAUTH2_KEY'