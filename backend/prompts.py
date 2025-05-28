def build_user_prompt(company):
    return (
        f"You are an expert in company relationships. "
        f"IMPORTANT: Do not include any <think> sections, reasoning, explanations, notes, or any text before or after the JSON. "
        f"Given the company '{company}', return ONLY a JSON array of objects, each with 'name', 'type', and 'logo'. Do not include any notes, explanations, or text outside the JSON array. "
        f"Restrict the number of companies to 10. "
        f"The central company node must have type 'company'. Parent companies must have type 'parent', subsidiaries must have type 'subsidiary'. "
        f"List the parent company (if any), and all direct subsidiaries of {company}, each as a separate object. For subsidiaries, use real-world companies that are or have been subsidiaries of {company}, such as Pratt & Whitney, Collins Aerospace, Raytheon, and others. Do not repeat the same entity for different types unless it is correct in real life. "
        f"For each entity, search Wikimedia Commons for the official logo. Use the direct file URL (ending in .svg or .png) from https://upload.wikimedia.org/wikipedia/commons/. Do not use any URL containing '/thumb/'. If no logo is available, set 'logo' to null. Do not use Wikipedia or any other source. "
        f"Example: [{{\"name\": \"RTX Corporation\", \"type\": \"company\", \"logo\": \"https://upload.wikimedia.org/wikipedia/commons/7/7e/RTX_Corporation_logo.svg\"}}, {{\"name\": \"Pratt & Whitney\", \"type\": \"subsidiary\", \"logo\": \"https://upload.wikimedia.org/wikipedia/commons/2/2d/Pratt_%26_Whitney_logo.svg\"}}, {{\"name\": \"Collins Aerospace\", \"type\": \"subsidiary\", \"logo\": \"https://upload.wikimedia.org/wikipedia/commons/6/6d/Collins_Aerospace_logo.svg\"}}] "
        f"Do not repeat the same name for different types unless it is correct in real life. "
        f"Do not include products such as \"Windows Phone\" or \"Azure\". "
        f"Return ONLY a JSON array of objects as your entire response. Do not include any <think> sections, explanations, or any text before or after the JSON. Your response must be a valid JSON array and nothing else. "
        f"Do not include any characters, markdown, or text outside the JSON array. Do NOT include ```json or ``` in your response. "
    )
