intents = [
    {
        'patterns': ['hello', 'hi','Hi', 'hey','namaste'],
        'responses': ['👋 Hello! How can I assist you today?', 'Hi there! How can I help?'],
    },
    {
        'patterns': ['complaint', 'issue'],
        'responses': ['😟 I\'m sorry to hear that. Please describe your issue, and I\'ll do my best to assist you.'],
        'context': 'describe_issue'
    },
    {
        'patterns': ['help ', 'support', 'assistance'],
        'responses': ['🤝 Sure, I can help you with that. Please tell me more about your request.'],
        'context': 'provide_details'
    },
    {
        'patterns': ['black', 'display', 'problem','blue'],
        'responses': ['🖥️ Sure, I can help you with that. Can you confirm if your problem is related to the display?'],
        'context': 'display_faq'
    },
    {
        'patterns': ['update', 'updater','windows update', 'window update'],
        'responses': ['🔄 Sure, I can help you with that. Can you confirm if your problem is related to the Windows update?'],
        'context': 'update_faq'
    },
    {
        'patterns': ['internet', 'wifi','network','netslow'],
        'responses': ['🌐 Sure, I can help you with that. Can you confirm if your problem is related to the network?'],
        'context': 'netw_faq'
    },
    {
        'patterns': ['slow', 'hang','overheating','lagging'],
        'responses': ['⚙️ Sure, I can help you with that. Can you confirm if your problem is related to performance?'],
        'context': 'performance_faq'
    },
    {
        'patterns': ['reboot', 'crash','loop','starting','restarting','shutdown'],
        'responses': ['🔄 Sure, I can help you with that. Can you confirm if your problem is related to System Crash, Reboot, or Shut Down?'],
        'context': 'crash_faq'
    },
]
