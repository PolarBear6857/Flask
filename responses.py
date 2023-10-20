import random


def get_response(message: str):
    p_message = message.lower()

    if p_message == 'hello':
        return 'hello there'

    if message == 'roll':
        return str(random.randint(1, 6))

    if p_message == 'help':
        return 'nechci ti pomoct XD'

    if message == 'chad':
        return 'https://tenor.com/view/gigachad-chad-gif-20773266'

    if message == 'skill issue':
        return 'https://tenor.com/view/skill-issue-gif-19411985'

    if message == 'nevím':
        return 'https://tenor.com/view/napoleon-there%27s-nothing-we-can-do-napoleon-pyritesian-gif-17490332095914688011'
    if message == 'ni':
        return 'https://tenor.com/view/thanos-banned-gif-24526457'
    if message == 'jirka':
        return 'https://tenor.com/view/carbonatedlean-minecraft-minecraft-skeleton-skeleton-appears-skeleton-army-gif-11355263577746326205'

