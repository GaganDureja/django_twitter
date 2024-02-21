from django import template

register = template.Library()

@register.filter(name='short_number')
def short_number(value):
    """
    Convert a large number to a short format like 5K, 1M, etc.
    """
    value = int(value)
    if value >= 1000000:
        return f"{value // 1000000}M"
    elif value >= 1000:
        return f"{value // 1000}K"
    else:
        return str(value)

import re
from user.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string



@register.filter(name='message_links')
def message_links(value):
    
    hashtag_pattern = r'#\w+'
    mention_pattern = r'@\w+'

    hashtags = re.findall(hashtag_pattern, value)
    mentions = re.findall(mention_pattern, value)
    hashtags = [tag[1:] for tag in hashtags]
    mentions = [mention[1:] for mention in mentions]
    
    # Replace hashtags with anchor tags

    for tag in hashtags:
        tweets_message = render_to_string('home/message_links.html', {'hashtag': tag})
        value = re.sub(r'#' + tag, tweets_message, value)
        # value = re.sub(r'#' + tag, '<a href="{% url \'search\' ' + tag + ' %}">#' + tag + '</a>', value)

    for mention in mentions:        
        if User.objects.filter(username=mention).exists():            
            tweets_message = render_to_string('home/message_links.html', {'mention': mention})
            value = re.sub(r'@' + mention, tweets_message, value)
    
    return value

