from tally_integration import TallyClient, TallyConnectionError, TallyAPIError


client = TallyClient()

try:
   print(client.get_ledgers_list())
    
except TallyConnectionError as e:
    print(f"Connection Error: {e}")
except TallyAPIError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")