def card_creator() -> str:
    "Manges the card creation query"

    prompt = """
            mutation($input: CreateCardInput!) {
            createCard(input: $input) {
                card {
                    id
                    title
                }
            }
        }
    """

    return prompt

def card_updator() -> str:
    "manges the update of a card"

    prompt = """
                mutation($input: UpdateCardInput!) {
            updateCard(input: $input) {
                card {
                    id
                    title
                }
            }
        }    
    """

    return prompt