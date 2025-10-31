def card_creator() -> str:
    "Manges the card creation query"

    prompt = """
    mutation CreateCard($input: CreateCardInput!) {
          createCard(input: $input) {
            card {
              id
              title
              fields {
                name
                value
              }
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